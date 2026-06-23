import React, { useState, useEffect, useRef } from 'react';
import { Mic, Square, Play, Sparkles } from 'lucide-react';

const LiveAudioEngine = () => {
  const [status, setStatus] = useState('IDLE'); // IDLE, LISTENING, RELAYING
  const audioContext = useRef(null);
  const mediaRecorder = useRef(null);
  const socket = useRef(null); // 실제 구현 시 Gemini WebSocket 또는 SDK 세션

  const startRecording = async () => {
    setStatus('LISTENING');
    // 브라우저 마이크 권한 획득
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    
    // MediaRecorder로 오디오 데이터 청크 생성
    mediaRecorder.current = new MediaRecorder(stream, { mimeType: 'audio/webm' });
    mediaRecorder.current.ondataavailable = (event) => {
      if (event.data.size > 0 && socket.current) {
        // 여기에 마이크 데이터를 Gemini 세션으로 전송하는 로직
        // socket.current.send(event.data); 
      }
    };
    mediaRecorder.current.start(100); // 100ms 단위로 청크 전송
  };

  const stopRecording = () => {
    setStatus('RELAYING');
    mediaRecorder.current.stop();
    // 릴레이 생성 시점: 서버로부터 최종 텍스트 수신 완료 후
    // saveToRelayDb(finalText, finalAudio);
  };

  return { status, startRecording, stopRecording };
};

export default function App() {
  const { status, startRecording, stopRecording } = LiveAudioEngine();
  const [relays, setRelays] = useState([]);

  return (
    <div className="max-w-md mx-auto p-6 bg-orange-50 min-h-screen flex flex-col font-sans">
      <header className="mb-8">
        <h1 className="text-2xl font-bold text-orange-900">당목담글</h1>
        <p className="text-sm text-orange-600">당신의 상황에 맞춘 따뜻한 이어읽기</p>
      </header>

      {/* 실시간 릴레이 상태 표시 */}
      <div className="flex-1 space-y-4">
        {relays.map((r, i) => (
          <div key={i} className="bg-white p-4 rounded-xl shadow-sm text-sm text-orange-800">
            {r.content}
          </div>
        ))}
        {status === 'RELAYING' && (
          <div className="flex items-center gap-2 text-orange-500 animate-pulse">
            <Sparkles size={16} /> 마음을 담은 릴레이를 생성 중이에요...
          </div>
        )}
      </div>

      {/* 조작 버튼 영역 */}
      <div className="mt-auto pt-6 flex justify-center">
        <button
          onClick={status === 'IDLE' ? startRecording : stopRecording}
          className={`p-6 rounded-full shadow-lg transition-all ${
            status === 'LISTENING' ? 'bg-red-500 hover:bg-red-600' : 'bg-orange-500 hover:bg-orange-600'
          }`}
        >
          {status === 'LISTENING' ? <Square color="white" size={32} /> : <Mic color="white" size={32} />}
        </button>
      </div>
    </div>
  );
}