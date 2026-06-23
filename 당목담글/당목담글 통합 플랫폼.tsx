import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Save, Heart, Sun, Coffee, Play, Trash2 } from 'lucide-react';
import Dexie from 'dexie';
import { useObservable } from 'dexie-react-hooks';
import { liveQuery } from 'dexie';

// 1. Database Setup
const db = new Dexie('DangmokdamgeulDB');
db.version(1).stores({
  relays: '++id, emotion, content, timestamp, audioData'
});

// 2. Audio Processing Engine (Queueing System)
class AudioPlayerEngine {
  constructor() {
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    this.nextStartTime = 0;
  }

  async playChunk(arrayBuffer) {
    // 끊김 방지: 오디오 버퍼를 디코딩하고 재생 시간을 정밀하게 스케줄링
    const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
    const source = this.audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(this.audioContext.destination);

    const currentTime = this.audioContext.currentTime;
    if (this.nextStartTime < currentTime) {
      this.nextStartTime = currentTime;
    }
    
    source.start(this.nextStartTime);
    this.nextStartTime += audioBuffer.duration;
  }
}

export default function App() {
  const [status, setStatus] = useState('IDLE');
  const [emotionFilter, setEmotionFilter] = useState('전체');
  const [isRecording, setIsRecording] = useState(false);
  
  // Dexie liveQuery로 UI 자동 동기화
  const relays = useObservable(
    liveQuery(() => {
      if (emotionFilter === '전체') return db.relays.orderBy('timestamp').reverse().toArray();
      return db.relays.where('emotion').equals(emotionFilter).reverse().toArray();
    })
  );

  const engine = useRef(new AudioPlayerEngine());
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);

  const startRecording = async () => {
    setStatus('LISTENING');
    setIsRecording(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder.current = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=opus' });

    mediaRecorder.current.ondataavailable = (e) => {
      if (e.data.size > 0) audioChunks.current.push(e.data);
    };

    mediaRecorder.current.start(100);
  };

  const stopRecording = async () => {
    setStatus('SAVING');
    setIsRecording(false);
    mediaRecorder.current.stop();

    // 릴레이 저장 (실제 서비스에서는 API 응답 데이터 활용)
    const finalBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
    await db.relays.add({
      emotion: emotionFilter === '전체' ? '위로' : emotionFilter,
      content: "오늘 하루, 당신의 목소리가 참 따뜻하네요.",
      timestamp: Date.now(),
      audioData: finalBlob
    });

    audioChunks.current = [];
    setStatus('IDLE');
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-orange-50 min-h-screen font-sans">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-orange-900">당목담글</h1>
        <p className="text-orange-600 text-sm">마음을 이어주는 목소리 릴레이</p>
      </header>

      {/* 감정 필터 UI */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {['전체', '위로', '설렘', '평온'].map(e => (
          <button 
            key={e}
            onClick={() => setEmotionFilter(e)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              emotionFilter === e ? 'bg-orange-500 text-white shadow-lg' : 'bg-white text-orange-800'
            }`}
          >
            {e}
          </button>
        ))}
      </div>

      {/* 메인 레코딩 버튼 */}
      <div className="flex justify-center mb-10">
        <button
          onClick={isRecording ? stopRecording : startRecording}
          className={`p-8 rounded-full shadow-xl transition-all ${
            isRecording ? 'bg-red-500 animate-pulse' : 'bg-orange-500 hover:scale-105'
          }`}
        >
          {isRecording ? <Square color="white" size={40} /> : <Mic color="white" size={40} />}
        </button>
      </div>

      {/* 릴레이 리스트 */}
      <div className="space-y-4">
        {relays?.map((relay) => (
          <div key={relay.id} className="bg-white p-4 rounded-2xl shadow-sm border border-orange-100 flex items-center justify-between">
            <div>
              <p className="font-medium text-orange-900">{relay.content}</p>
              <p className="text-xs text-orange-400">{new Date(relay.timestamp).toLocaleTimeString()}</p>
            </div>
            <button className="p-2 bg-orange-100 rounded-full text-orange-600">
              <Play size={20} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}