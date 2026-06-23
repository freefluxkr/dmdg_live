import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Play, Coffee, Heart, Sun, Settings2, RotateCcw } from 'lucide-react';
import Dexie from 'dexie';
import { useObservable } from 'dexie-react-hooks';
import { liveQuery } from 'dexie';

// Database setup
const db = new Dexie('DangmokdamgeulDB');
db.version(1).stores({
  relays: '++id, emotion, content, timestamp, audioData'
});

class AudioPlayerEngine {
  constructor() {
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    this.analyser = this.audioContext.createAnalyser();
    this.analyser.fftSize = 256;
    this.analyser.connect(this.audioContext.destination);
    this.playbackRate = 1.0;
    this.nextStartTime = 0;
  }

  setSpeed(rate) {
    this.playbackRate = rate;
  }

  async playChunk(arrayBuffer) {
    if (this.audioContext.state === 'suspended') await this.audioContext.resume();
    
    const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
    const source = this.audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.playbackRate.value = this.playbackRate;
    
    // Connect to analyser for visualization
    source.connect(this.analyser);
    source.connect(this.audioContext.destination);

    const currentTime = this.audioContext.currentTime;
    if (this.nextStartTime < currentTime) this.nextStartTime = currentTime;
    
    source.start(this.nextStartTime);
    this.nextStartTime += audioBuffer.duration / this.playbackRate;
  }
}

export default function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [speed, setSpeed] = useState(1.0);
  const [emotionFilter, setEmotionFilter] = useState('전체');
  const engine = useRef(new AudioPlayerEngine());
  const canvasRef = useRef(null);

  const relays = useObservable(
    liveQuery(() => emotionFilter === '전체' 
      ? db.relays.orderBy('timestamp').reverse().toArray()
      : db.relays.where('emotion').equals(emotionFilter).reverse().toArray()
    )
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const bufferLength = engine.current.analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    function draw() {
      requestAnimationFrame(draw);
      engine.current.analyser.getByteFrequencyData(dataArray);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const barWidth = (canvas.width / bufferLength) * 2.5;
      let x = 0;
      
      for(let i = 0; i < bufferLength; i++) {
        const barHeight = (dataArray[i] / 255) * canvas.height;
        ctx.fillStyle = `rgb(251, 146, 60)`;
        ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
        x += barWidth + 1;
      }
    }
    draw();
  }, []);

  return (
    <div className="max-w-md mx-auto p-6 bg-orange-50 min-h-screen font-sans">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-orange-900">당목담글</h1>
        <p className="text-orange-600 text-sm">목소리로 이어지는 따뜻한 릴레이</p>
      </header>

      {/* Control Panel */}
      <div className="bg-white p-4 rounded-2xl mb-6 shadow-sm border border-orange-100 flex items-center justify-between">
        <div className="flex gap-2">
          {['전체', '위로', '설렘', '평온'].map(e => (
            <button key={e} onClick={() => setEmotionFilter(e)} className={`px-3 py-1 rounded-full text-xs ${emotionFilter === e ? 'bg-orange-500 text-white' : 'bg-orange-100'}`}>
              {e}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-2 text-orange-600">
          <Settings2 size={16} />
          <select value={speed} onChange={(e) => { 
            const val = parseFloat(e.target.value); 
            setSpeed(val); 
            engine.current.setSpeed(val); 
          }} className="bg-transparent text-xs font-bold">
            <option value="0.5">0.5x</option>
            <option value="1.0">1.0x</option>
            <option value="1.5">1.5x</option>
          </select>
        </div>
      </div>

      {/* Visualizer */}
      <canvas ref={canvasRef} className="w-full h-24 bg-white rounded-2xl mb-6 border border-orange-100" />

      {/* Main Recording Button */}
      <div className="flex justify-center mb-10">
        <button onClick={() => setIsRecording(!isRecording)} className={`p-8 rounded-full shadow-xl transition-all ${isRecording ? 'bg-red-500' : 'bg-orange-500'}`}>
          {isRecording ? <Square color="white" size={40} /> : <Mic color="white" size={40} />}
        </button>
      </div>

      {/* Relay List */}
      <div className="space-y-4">
        {relays?.map((relay) => (
          <div key={relay.id} className="bg-white p-4 rounded-2xl shadow-sm flex items-center justify-between">
            <p className="text-sm text-orange-900">{relay.content}</p>
            <button className="p-2 bg-orange-100 rounded-full text-orange-600"><Play size={20} /></button>
          </div>
        ))}
      </div>
    </div>
  );
}