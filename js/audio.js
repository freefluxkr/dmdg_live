// Audio Engine
    class AudioPlayerEngine {
      constructor() {
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        this.analyser = this.audioContext.createAnalyser();
        this.analyser.fftSize = 64;
        this.analyser.connect(this.audioContext.destination);
        this.playbackRate = 1.0;
        this.activeSource = null;
        
        // 안드로이드 WebM 재생 실패 대비용 Fallback Audio
        this.fallbackAudio = new Audio();
        // 주의: Blob URL을 사용하므로 crossOrigin="anonymous"를 설정하면 오디오가 음소거됨. 설정 금지.
        this.fallbackSource = this.audioContext.createMediaElementSource(this.fallbackAudio);
        this.fallbackSource.connect(this.analyser);
      }

      setSpeed(rate) {
        this.playbackRate = rate;
      }

      stop() {
        if (this.activeSource) {
          try {
            if (this.activeSource.stop) this.activeSource.stop();
          } catch (e) {
            console.log("Audio source stop error:", e);
          }
          this.activeSource = null;
        }
        if (!this.fallbackAudio.paused) {
           this.fallbackAudio.pause();
        }
      }

      playChunk(arrayBuffer, onEndedCallback) {
        return new Promise(async (resolve) => {
          if (this.audioContext.state === 'suspended') {
            await this.audioContext.resume();
          }
          this.stop();
          
          try {
            // 원본 데이터가 손상되지 않게 복사본 사용
            const bufferCopy = arrayBuffer.slice(0);
            const audioBuffer = await this.audioContext.decodeAudioData(bufferCopy);
            const source = this.audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.playbackRate.value = this.playbackRate;
            source.connect(this.analyser);
            
            this.activeSource = source;
            source.onended = () => {
              if (this.activeSource === source) this.activeSource = null;
              if (onEndedCallback) setTimeout(onEndedCallback, 100);
              resolve();
            };
            source.start(0);
          } catch (error) {
            console.warn("decodeAudioData 실패 (안드로이드 WebM 버그 추정). HTML5 Audio로 우회합니다.", error);
            
            const blob = new Blob([arrayBuffer]);
            const url = URL.createObjectURL(blob);
            this.fallbackAudio.src = url;
            this.fallbackAudio.playbackRate = this.playbackRate;
            
            this.activeSource = {
               stop: () => {
                   this.fallbackAudio.pause();
                   URL.revokeObjectURL(url);
               }
            };
            
            this.fallbackAudio.onended = () => {
                URL.revokeObjectURL(url);
                if (onEndedCallback) setTimeout(onEndedCallback, 100);
                resolve();
            };
            
            this.fallbackAudio.play().catch(e => {
                console.error("Fallback 오디오 재생 실패:", e);
                resolve();
            });
          }
        });
      }
    }