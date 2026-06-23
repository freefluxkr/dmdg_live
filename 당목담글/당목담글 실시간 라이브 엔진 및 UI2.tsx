import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Save } from 'lucide-react';
import Dexie from 'dexie';

// 데이터베이스 초기화
const db = new Dexie('DangmokdamgeulDB');
db.version(1).stores({ relays: '++id, content, audioBlob' });

export default function App() {
  const [status, setStatus] = useState('IDLE');
  const [audioChunks, setAudioChunks] = useState([]); // 서버에서 받은 응답 데이터 임시 저장
  const mediaRecorder = useRef(null);

  const startRecording = async () => {
    setStatus('LISTENING');
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    
    // Opus 코덱 설정으로 음질 손실 최소화 및 낮은 지연 시간 확보
    mediaRecorder.current = new MediaRecorder(stream, { 
      mimeType: 'audio/webm;codecs=opus' 
    });

    mediaRecorder.current.ondataavailable = (event) => {
      if (event.data.size > 0) {
        // 실제 구현 시: socket.send(event.data); 
        console.log("Sending chunk to Gemini...");
      }
    };
    
    // 100ms 단위로 청크 전송 (지연 시간 최적화)
    mediaRecorder.current.start(100);
  };

  const stopRecording = async () => {
    setStatus('SAVING');
    mediaRecorder.current.stop();

    // 1. 임시 데이터 결합 (Blob 생성)
    const finalBlob = new Blob(audioChunks, { type: 'audio/webm' });
    
    // 2. Dexie DB에 저장
    await db.relays.add({
      content: "사용자의 마음을 담은 이어읽기",
      audioBlob: finalBlob,
      timestamp: Date.now()
    });
    
    setStatus('IDLE');
    setAudioChunks([]); // 버퍼 초기화
    console.log("Relay saved successfully!");
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-orange-50 min-h-screen flex flex-col items-center justify-center">
      <h1 className="text-2xl font-bold text-orange-900 mb-8">당목담글 엔진</h1>
      
      <button
        onClick={status === 'IDLE' ? startRecording : stopRecording}
        className={`p-8 rounded-full shadow-xl transition-all ${
          status === 'LISTENING' ? 'bg-red-500 hover:bg-red-600' : 'bg-orange-500 hover:bg-orange-600'
        }`}
      >
        {status === 'LISTENING' ? <Square color="white" size={40} /> : <Mic color="white" size={40} />}
      </button>

      <div className="mt-8 text-sm text-orange-700">
        Status: {status}
      </div>
    </div>
  );
}