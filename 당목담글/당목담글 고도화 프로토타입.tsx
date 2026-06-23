import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Play, Settings2, Coffee, Heart, Sun } from 'lucide-react';
import Dexie from 'dexie';
import { useObservable } from 'dexie-react-hooks';
import { liveQuery } from 'dexie';

// PWA Meta data (실제 앱에서는 index.html에 포함 필요)
/*
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#fff7ed">
*/

const db = new Dexie('DangmokdamgeulDB');
db.version(1).stores({
  relays: '++id, emotion, content, timestamp, audioData'
});

class AudioPlayerEngine {
  constructor() {
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    this.analyser = this.audioContext.createAnalyser();
    this.analyser.fftSize = 64;
    this.analyser.connect(this.audioContext.destination);
    this.playbackRate = 1.0;
  }

  async playChunk(arrayBuffer) {
    if (this.audioContext.state === 'suspended') await this.audioContext.resume();
    const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
    const source = this.audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.playbackRate.value = this.playbackRate;
    source.connect(this.analyser);
    source.connect(this.audioContext.destination);
    source.start(0);
  }
}

export default function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [emotionFilter, setEmotionFilter] = useState('전체');
  const engine = useRef(new AudioPlayerEngine());
  const canvasRef = useRef(null);
  const animationRef = useRef(null);

  const relays = useObservable(
    liveQuery(() => emotionFilter === '전체' 
      ? db.relays.toArray()
      : db.relays.where('emotion').equals(emotionFilter).toArray()
    )
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const bufferLength = engine.current.analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    
    let time = 0;

    function draw() {
      animationRef.current = requestAnimationFrame(draw);
      engine.current.analyser.getByteFrequencyData(dataArray);
      
      // Calculate average volume
      let sum = 0;
      for(let i = 0; i < bufferLength; i++) sum += dataArray[i];
      const avg = sum / bufferLength;

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const baseRadius = 60 + avg * 0.5;
      
      // Draw smooth blob
      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, baseRadius * 1.5);
      gradient.addColorStop(0, 'rgba(251, 146, 60, 0.6)');
      gradient.addColorStop(1, 'rgba(255, 237, 213, 0)');
      
      ctx.beginPath();
      ctx.arc(centerX, centerY, baseRadius, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();
      
      // Inner core
      ctx.beginPath();
      ctx.arc(centerX, centerY, baseRadius * 0.5 + Math.sin(time) * 5, 0, Math.PI * 2);
      ctx.fillStyle = '#fb923c';
      ctx.fill();
      
      time += 0.05;
    }
    draw();
    return () => cancelAnimationFrame(animationRef.current);
  }, []);

  return (
    <div className="max-w-md mx-auto p-4 bg-orange-50 min-h-screen font-sans touch-manipulation">
      <header className="py-6 text-center">
        <h1 className="text-2xl font-bold text-orange-900">당목담글</h1>
        <p className="text-orange-600 text-sm opacity-80">마음을 잇는 따뜻한 소리</p>
      </header>

      {/* Visualizer Container */}
      <canvas ref={canvasRef} width={300} height={300} className="w-full h-64 mb-6" />

      {/* Control Section */}
      <div className="bg-white p-6 rounded-3xl shadow-sm mb-8">
        <div className="flex justify-center gap-4 mb-8">
          {['위로', '설렘', '평온'].map(e => (
            <button key={e} onClick={() => setEmotionFilter(e)} className={`flex items-center gap-2 p-4 rounded-2xl transition-all ${emotionFilter === e ? 'bg-orange-500 text-white' : 'bg-orange-100 text-orange-600'}`}>
              {e === '위로' && <Heart size={20} />}
              {e === '설렘' && <Sun size={20} />}
              {e === '평온' && <Coffee size={20} />}
            </button>
          ))}
        </div>

        <button 
          onClick={() => setIsRecording(!isRecording)} 
          className={`w-full h-16 rounded-2xl flex items-center justify-center gap-3 text-white font-bold transition-all ${isRecording ? 'bg-red-500' : 'bg-orange-600'}`}
        >
          {isRecording ? <><Square size={24} /> 녹음 멈추기</> : <><Mic size={24} /> 목소리 담기</>}
        </button>
      </div>

      {/* Relay List */}
      <div className="space-y-4 pb-10">
        {relays?.map((relay) => (
          <div key={relay.id} className="bg-white p-5 rounded-2xl shadow-sm flex items-center justify-between active:scale-95 transition-transform">
            <span className="text-orange-900 font-medium truncate">{relay.content || "따뜻한 릴레이..."}</span>
            <button className="p-3 bg-orange-100 rounded-full text-orange-600"><Play size={20} /></button>
          </div>
        ))}
      </div>
    </div>
  );
}