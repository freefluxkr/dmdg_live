/**
 * ==============================================================================
 * DMDG 스튜디오 E-Book & 오디오북 - 다국어 음성 낭독 (Web Speech API TTS)
 * 파일명: js/reader/reader-tts.js
 * 지원 언어: 🇰🇷 ko-KR | 🇺🇸 en-US | 🇯🇵 ja-JP | 🇫🇷 fr-FR | 🇮🇩 id-ID | 🇪🇸 es-ES
 * ==============================================================================
 */

export class ReaderTTS {
  constructor(options = {}) {
    this.synth = window.speechSynthesis || null;
    this.voices = [];
    this.currentVoice = null;
    this.currentLang = options.defaultLang || 'ko-KR';
    
    this.isPlaying = false;
    this.isPaused = false;
    
    this.currentParagraphIdx = 0;
    this.paragraphs = [];
    this.speedRates = [0.8, 1.0, 1.2, 1.5, 2.0];
    this.speedIndex = 1; // 1.0x default
    this.pitch = 1.0;
    
    this.onStateChange = options.onStateChange || (() => {});
    this.onParagraphHighlight = options.onParagraphHighlight || (() => {});
    
    this.initVoices();
  }

  initVoices() {
    if (!this.synth) {
      console.warn('이 브라우저는 Web Speech API TTS를 지원하지 않습니다.');
      return;
    }

    const load = () => {
      this.voices = this.synth.getVoices();
      this.updateVoiceForCurrentLang();
    };

    load();
    if (this.synth.onvoiceschanged !== undefined) {
      this.synth.onvoiceschanged = load;
    }
  }

  setLanguage(langCode) {
    this.currentLang = langCode;
    this.updateVoiceForCurrentLang();
    if (this.isPlaying) {
      // 언어 변경 시 현재 단락부터 재시작
      this.speakCurrentParagraph();
    }
  }

  updateVoiceForCurrentLang() {
    if (!this.voices || this.voices.length === 0) return;

    // 언어 코드 매칭 (prefix 일치 기준)
    const targetPrefix = this.currentLang.split('-')[0].toLowerCase();
    
    // 1. 정확한 locale 일치 확인
    let match = this.voices.find(v => v.lang.toLowerCase() === this.currentLang.toLowerCase());
    
    // 2. prefix 일치 확인 (예: 'ko', 'en', 'ja', 'fr', 'id', 'es')
    if (!match) {
      match = this.voices.find(v => v.lang.toLowerCase().startsWith(targetPrefix));
    }
    
    // 3. 없으면 기본 첫 번째 음성
    this.currentVoice = match || this.voices[0];
  }

  setParagraphs(pElements) {
    this.paragraphs = Array.from(pElements);
    this.currentParagraphIdx = 0;
  }

  togglePlay() {
    if (!this.synth) return;

    if (this.isPlaying) {
      if (this.isPaused) {
        this.resume();
      } else {
        this.pause();
      }
    } else {
      this.play();
    }
  }

  play(startIdx = null) {
    if (!this.synth || this.paragraphs.length === 0) return;

    if (startIdx !== null && startIdx >= 0 && startIdx < this.paragraphs.length) {
      this.currentParagraphIdx = startIdx;
    }

    this.isPlaying = true;
    this.isPaused = false;
    this.speakCurrentParagraph();
    this.notifyState();
  }

  pause() {
    if (!this.synth) return;
    this.synth.pause();
    this.isPaused = true;
    this.notifyState();
  }

  resume() {
    if (!this.synth) return;
    this.synth.resume();
    this.isPaused = false;
    this.notifyState();
  }

  stop() {
    if (!this.synth) return;
    this.synth.cancel();
    this.isPlaying = false;
    this.isPaused = false;
    this.onParagraphHighlight(null);
    this.notifyState();
  }

  cycleSpeed() {
    this.speedIndex = (this.speedIndex + 1) % this.speedRates.length;
    const newRate = this.speedRates[this.speedIndex];
    if (this.isPlaying) {
      this.speakCurrentParagraph();
    }
    this.notifyState();
    return newRate;
  }

  getSpeedRate() {
    return this.speedRates[this.speedIndex];
  }

  speakCurrentParagraph() {
    if (!this.synth) return;
    this.synth.cancel();

    if (this.currentParagraphIdx >= this.paragraphs.length) {
      this.stop();
      return;
    }

    const pEl = this.paragraphs[this.currentParagraphIdx];
    const text = pEl.textContent.trim();

    if (!text) {
      // 빈 문단이면 다음으로 자동 이동
      this.currentParagraphIdx++;
      this.speakCurrentParagraph();
      return;
    }

    // UI 하이라이트 및 자동 스크롤
    this.onParagraphHighlight(pEl);
    pEl.scrollIntoView({ behavior: 'smooth', block: 'center' });

    const utterance = new SpeechSynthesisUtterance(text);
    if (this.currentVoice) {
      utterance.voice = this.currentVoice;
    }
    utterance.lang = this.currentLang;
    utterance.rate = this.getSpeedRate();
    utterance.pitch = this.pitch;

    utterance.onend = () => {
      if (this.isPlaying && !this.isPaused) {
        this.currentParagraphIdx++;
        this.speakCurrentParagraph();
      }
    };

    utterance.onerror = (e) => {
      console.warn('TTS 재생 중 오류 발생:', e);
      if (this.isPlaying) {
        this.currentParagraphIdx++;
        this.speakCurrentParagraph();
      }
    };

    this.synth.speak(utterance);
  }

  nextParagraph() {
    if (this.currentParagraphIdx < this.paragraphs.length - 1) {
      this.currentParagraphIdx++;
      if (this.isPlaying) this.speakCurrentParagraph();
    }
  }

  prevParagraph() {
    if (this.currentParagraphIdx > 0) {
      this.currentParagraphIdx--;
      if (this.isPlaying) this.speakCurrentParagraph();
    }
  }

  notifyState() {
    this.onStateChange({
      isPlaying: this.isPlaying,
      isPaused: this.isPaused,
      currentSpeed: this.getSpeedRate(),
      currentLang: this.currentLang,
      paragraphIdx: this.currentParagraphIdx,
      totalParagraphs: this.paragraphs.length
    });
  }
}
