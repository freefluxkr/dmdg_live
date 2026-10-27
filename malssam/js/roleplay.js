// ============================================================
// 🎬 [말쌈 3D 숏폼 상황극 엔진 v3: js/roleplay.js]
// - 프랑스어(fr) 포함 6개국어(KR, EN, JA, ES, FR, ID) 완벽 지원
// - 문장 청크 큐잉(Sentence Queue) 시스템으로 대화 짤림 100% 원천 박멸
// - 캐릭터별 자연어 Voice 매핑 & 구어체 전처리 (~, 5G, AWS, UI/UX)
// - 사람 대화 호흡 1.4초 보장 (Natural Turn-taking Pause)
// - 인스타그램 숏폼 릴스 스타일 실시간 동기화 프로그레스 게이지
// - Web Audio API 부드러운 씬 트랜지션 사운드 효과
// ============================================================

(function () {
  'use strict';

  let currentLang = 'ko';
  let currentScene = 0;
  let isPlaying = false;
  let isMuted = false;
  let fallbackTimer = null;
  let keepAliveInterval = null;
  let activeSceneToken = 0;
  let cachedVoices = [];
  let audioCtx = null;

  // 🔊 Web Audio API 기반 소프트 트랜지션 사운드
  function playSoftChime() {
    if (isMuted) return;
    try {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) return;
      if (!audioCtx) audioCtx = new AudioContextClass();
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      const now = audioCtx.currentTime;

      osc.type = 'sine';
      osc.frequency.setValueAtTime(523.25, now); // C5
      osc.frequency.exponentialRampToValueAtTime(783.99, now + 0.08); // G5

      gain.gain.setValueAtTime(0.04, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

      osc.connect(gain);
      gain.connect(audioCtx.destination);

      osc.start(now);
      osc.stop(now + 0.12);
    } catch (e) {
      // AudioContext 방어
    }
  }

  // 🎙️ 브라우저 사용 가능 음성 로드 & 캐싱
  function loadVoices() {
    if ('speechSynthesis' in window) {
      cachedVoices = window.speechSynthesis.getVoices();
    }
  }

  if ('speechSynthesis' in window) {
    loadVoices();
    if (window.speechSynthesis.onvoiceschanged !== undefined) {
      window.speechSynthesis.onvoiceschanged = loadVoices;
    }
  }

  // 🎭 캐릭터 & 언어별 최적 Voice 탐색
  function selectBestVoice(lang, actorName) {
    if (!cachedVoices || cachedVoices.length === 0) {
      loadVoices();
    }
    const voices = cachedVoices || [];
    const targetLangPrefix = lang.toLowerCase();

    // 언어 일치 음성 필터링
    const langVoices = voices.filter(v => v.lang && v.lang.toLowerCase().startsWith(targetLangPrefix));
    if (langVoices.length === 0) {
      return null;
    }

    const isFemale = (actorName && (actorName.includes('제니퍼') || actorName.includes('Jennifer')));

    // 1) 한국어
    if (targetLangPrefix === 'ko') {
      const googleKo = langVoices.find(v => v.name.includes('Google') || v.name.includes('한국의'));
      if (googleKo) return googleKo;
      return langVoices[0];
    }

    // 2) 영어
    if (targetLangPrefix === 'en') {
      if (isFemale) {
        const femaleVoice = langVoices.find(v => v.name.includes('Zira') || v.name.includes('Female') || v.name.includes('Samantha') || v.name.includes('Jenny'));
        if (femaleVoice) return femaleVoice;
      } else {
        const maleVoice = langVoices.find(v => v.name.includes('David') || v.name.includes('Mark') || v.name.includes('Guy') || v.name.includes('Male'));
        if (maleVoice) return maleVoice;
      }
      const googleEn = langVoices.find(v => v.name.includes('Google'));
      if (googleEn) return googleEn;
      return langVoices[0];
    }

    // 3) 일본어
    if (targetLangPrefix === 'ja') {
      const googleJa = langVoices.find(v => v.name.includes('Google') || v.name.includes('日本語') || v.name.includes('Ayumi') || v.name.includes('Haruka'));
      return googleJa || langVoices[0];
    }

    // 4) 스페인어
    if (targetLangPrefix === 'es') {
      const googleEs = langVoices.find(v => v.name.includes('Google') || v.name.includes('Helena') || v.name.includes('Laura'));
      return googleEs || langVoices[0];
    }

    // 5) 프랑스어 (베트남 대체)
    if (targetLangPrefix === 'fr') {
      if (isFemale) {
        const femaleFr = langVoices.find(v => v.name.includes('Hortense') || v.name.includes('Julie') || v.name.includes('Female') || v.name.includes('Google'));
        if (femaleFr) return femaleFr;
      }
      const googleFr = langVoices.find(v => v.name.includes('Google') || v.name.includes('Français') || v.name.includes('Paul'));
      return googleFr || langVoices[0];
    }

    // 6) 인도네시아어
    if (targetLangPrefix === 'id') {
      const googleId = langVoices.find(v => v.name.includes('Google') || v.name.includes('Gadis') || v.name.includes('Andika'));
      return googleId || langVoices[0];
    }

    return langVoices[0];
  }

  // 📝 구어체 발음 전처리 (특수기호, 외래어, 약어 음성 다듬기)
  function sanitizeSpeechText(text, lang) {
    if (!text) return '';
    let cleaned = String(text);

    if (lang === 'ko') {
      cleaned = cleaned
        .replace(/~/g, ', ')                      // 물결표는 여유로운 쉼표로 발음
        .replace(/5G/gi, '파이브지')              // 5G -> 파이브지
        .replace(/AWS/gi, '에이더블유에스')       // AWS -> 에이더블유에스
        .replace(/UI\/UX/gi, '유아이 유엑스')     // UI/UX -> 유아이 유엑스
        .replace(/UX/gi, '유엑스')                // UX -> 유엑스
        .replace(/UI/gi, '유아이')                // UI -> 유아이
        .replace(/[!]{2,}/g, '!')                 // 연속 느낌표 정돈
        .replace(/[?]{2,}/g, '?')                 // 연속 물음표 정돈
        .replace(/\.\.\./g, '... ');              // 말줄임표 여운
    } else if (lang === 'en') {
      cleaned = cleaned
        .replace(/~/g, ', ')
        .replace(/5G/gi, 'five G')
        .replace(/AWS/gi, 'A W S')
        .replace(/UI\/UX/gi, 'U I and U X');
    } else if (lang === 'fr') {
      cleaned = cleaned
        .replace(/~/g, ', ')
        .replace(/5G/gi, 'cinq G')
        .replace(/AWS/gi, 'A W S')
        .replace(/UI\/UX/gi, 'U I et U X');
    } else {
      cleaned = cleaned.replace(/~/g, ', ');
    }

    return cleaned.trim();
  }

  // ✂️ 긴 문장을 자연스러운 호흡 단위(구문)로 분할 (크롬 15초 버그 & 대화 짤림 100% 원천 방어)
  function splitIntoSentenceChunks(text) {
    if (!text) return [];
    // 마침표, 느낌표, 물음표, 쉼표 기준 자연스러운 문장 분할
    const parts = text.match(/[^.!?]+[.!?]+|[^.!?]+$/g);
    if (!parts || parts.length === 0) return [text];
    return parts.map(p => p.trim()).filter(p => p.length > 0);
  }

  // ⏱️ 대사 전체 예상 소요 시간 계산
  function calculateTotalExpectedDuration(text, rate, lang) {
    const safeRate = rate || 1.0;
    const len = (text || '').length;
    let charMs = 175; // 한국어 글자당 평균 약 175ms

    if (lang === 'en' || lang === 'es' || lang === 'fr') charMs = 85;
    else if (lang === 'ja') charMs = 155;
    else if (lang === 'id') charMs = 110;

    const computed = (len * charMs) / safeRate;
    return Math.max(5000, Math.round(computed));
  }

  // 🎴 모달 열기 / 닫기
  window.openRoleplayModal = function (wordId, ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    const modal = document.getElementById('roleplayModal');
    if (!modal) return;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';

    // 기본 언어 한국어 설정 및 씬 초기화
    setRoleplayLanguage('ko');
    flipToFront();
    currentScene = 0;
    renderScene(0);
  };

  window.closeRoleplayModal = function () {
    const modal = document.getElementById('roleplayModal');
    if (!modal) return;

    stopAudio();
    isPlaying = false;
    modal.classList.remove('active');
    document.body.style.overflow = '';
    flipToFront();
  };

  // 🌐 6개국어 전환 (베트남 -> 프랑스어 교체 적용)
  window.setRoleplayLanguage = function (lang) {
    const metaMap = window.LANG_METADATA || {};
    const meta = metaMap[lang] || metaMap['ko'] || {};

    currentLang = lang;

    // 언어 버튼 활성화 UI
    document.querySelectorAll('.rp-lang-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });

    // 앞면 메타데이터 갱신
    const badgeEl = document.getElementById('rpFrontBadge');
    if (badgeEl) badgeEl.innerText = meta.badge || '💎 K-SOUL #01 · 번역불가 한국어';

    const titleEl = document.getElementById('rpFrontTitle');
    if (titleEl) titleEl.innerText = meta.word || '눈치';

    const pronEl = document.getElementById('rpFrontPron');
    if (pronEl) pronEl.innerText = meta.altPron ? `🗣️ ${meta.altPron}` : '🗣️ [nun-chi · NOON-chee]';

    const descEl = document.getElementById('rpFrontDesc');
    if (descEl) descEl.innerText = meta.def || '상대방의 기분, 분위기, 눈빛을 0.1초 만에 파악해 알아서 처신하는 한국 고유의 생존 본능.';

    const punchEl = document.getElementById('rpFrontPunch');
    if (punchEl) punchEl.innerText = meta.punchText ? `💡 ${meta.punchText}` : '💡 “말하지 않아도 공기를 읽는 K-직장인 생존술”';

    // 출연진 명칭 갱신
    const castDemisEl = document.getElementById('rpCastNameDemis');
    if (castDemisEl && meta.castDemis) castDemisEl.innerText = meta.castDemis;

    const castCraigEl = document.getElementById('rpCastNameCraig');
    if (castCraigEl && meta.castCraig) castCraigEl.innerText = meta.castCraig;

    const castJenniferEl = document.getElementById('rpCastNameJennifer');
    if (castJenniferEl && meta.castJennifer) castJenniferEl.innerText = meta.castJennifer;

    // 뒷면 언어 오디오 Pill
    const backLangEl = document.getElementById('rpCurrentLangPill');
    if (backLangEl) backLangEl.innerText = meta.pill || '🇰🇷 KO AUDIO';

    stopAudio();
    renderScene(currentScene);
    if (isPlaying) {
      playCurrentSceneAudio();
    }
  };

  // 🎴 3D FLIP 회전 제어
  window.flipToBackAndPlay = function () {
    const card = document.getElementById('rpFlipCardInner');
    if (card) card.classList.add('flipped');
    playShow();
  };

  window.flipToFront = function () {
    const card = document.getElementById('rpFlipCardInner');
    if (card) card.classList.remove('flipped');
    pauseShow();
  };

  // 앞면 퀵 발음 듣기
  window.speakQuickWord = function (word) {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(word || '눈치');
      u.lang = 'ko-KR';
      const voice = selectBestVoice('ko', '');
      if (voice) u.voice = voice;
      u.rate = 0.9;
      window.speechSynthesis.speak(u);
    }
  };

  // 씬 렌더링
  function renderScene(idx) {
    const scripts = (window.DRAMA_SCRIPTS && window.DRAMA_SCRIPTS[currentLang]) ? window.DRAMA_SCRIPTS[currentLang] : (window.DRAMA_SCRIPTS ? window.DRAMA_SCRIPTS['ko'] : []);
    if (!scripts || !scripts[idx]) return;

    const s = scripts[idx];
    const counterEl = document.getElementById('rpSceneCounter');
    if (counterEl) counterEl.innerText = `SCENE ${idx + 1} / ${scripts.length}`;

    // 액터 아바타 & 뱃지
    const avatarImg = document.getElementById('rpActorAvatar');
    if (avatarImg) avatarImg.src = s.avatar;

    const nameEl = document.getElementById('rpActorName');
    if (nameEl) nameEl.innerText = s.actor;

    const titleEl = document.getElementById('rpActorTitle');
    if (titleEl) {
      titleEl.innerText = s.title;
      titleEl.style.color = s.color || '#38bdf8';
    }

    const iconEl = document.getElementById('rpActorRoleIcon');
    if (iconEl) iconEl.innerText = s.roleIcon || '👤';

    const stickerEl = document.getElementById('rpReactionSticker');
    if (stickerEl) stickerEl.innerText = s.sticker || '✨';

    const hintEl = document.getElementById('rpActingHint');
    if (hintEl) hintEl.innerText = s.acting || '';

    const subEl = document.getElementById('rpMainSubtitle');
    if (subEl) subEl.innerText = s.dialogue || '';

    const transEl = document.getElementById('rpSubtitlesTrans');
    if (transEl) transEl.innerText = s.trans || '';

    // 애니메이션 & 시각 효과
    const stage = document.getElementById('rpCharacterStage');
    if (stage) stage.style.transform = `scale(${s.zoom || 1})`;

    const speedLines = document.getElementById('rpSpeedLines');
    if (speedLines) {
      if (s.speedLines) speedLines.classList.add('active');
      else speedLines.classList.remove('active');
    }

    const wrapper = document.getElementById('rpAvatarWrapper');
    if (wrapper) {
      wrapper.style.boxShadow = `0 0 35px ${s.color || '#ff007f'}88`;
      wrapper.style.background = `linear-gradient(135deg, ${s.color || '#ff007f'}, #ff007f)`;
    }

    const ambient = document.getElementById('rpAmbientLight');
    if (ambient) {
      ambient.style.background = `radial-gradient(circle, ${s.color || '#ff007f'}77 0%, transparent 70%)`;
    }

    const player = document.getElementById('rpCardBack');
    if (player) {
      if (s.shake) player.classList.add('rp-screen-shake');
      else player.classList.remove('rp-screen-shake');
    }

    // 프로그레스 바 초기화 (현재 씬 이전은 100%, 이후는 0%)
    for (let i = 0; i < scripts.length; i++) {
      const fill = document.getElementById(`rpFill-${i}`);
      if (fill) {
        fill.style.transition = 'none';
        if (i < idx) fill.style.width = '100%';
        else fill.style.width = '0%';
      }
    }
  }

  function stopAudio() {
    activeSceneToken++; // 이전 모든 발화 큐 무효화
    if (fallbackTimer) {
      clearTimeout(fallbackTimer);
      fallbackTimer = null;
    }
    if (keepAliveInterval) {
      clearInterval(keepAliveInterval);
      keepAliveInterval = null;
    }
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    window._activeUtterance = null;
    const sub = document.getElementById('rpMainSubtitle');
    if (sub) {
      sub.style.border = 'none';
      sub.style.boxShadow = 'none';
    }
  }

  // 🎬 핵심: 문장 큐잉 순차 발화 & 대화 짤림 100% 방지 엔진
  function playCurrentSceneAudio() {
    stopAudio();
    const thisToken = ++activeSceneToken;

    const scripts = (window.DRAMA_SCRIPTS && window.DRAMA_SCRIPTS[currentLang]) ? window.DRAMA_SCRIPTS[currentLang] : (window.DRAMA_SCRIPTS ? window.DRAMA_SCRIPTS['ko'] : []);
    if (!scripts || !scripts[currentScene]) return;

    const s = scripts[currentScene];
    const metaMap = window.LANG_METADATA || {};
    const meta = metaMap[currentLang] || metaMap['ko'];
    const targetTtsLang = meta ? meta.ttsLang : 'ko-KR';

    // 씬 전환 시 가벼운 트랜지션 사운드
    playSoftChime();

    // 자막 하이라이트 펄스 연출
    const sub = document.getElementById('rpMainSubtitle');
    if (sub) {
      sub.style.border = `1.5px solid ${s.color || '#ff007f'}`;
      sub.style.borderRadius = '10px';
      sub.style.padding = '8px 12px';
      sub.style.background = 'rgba(0,0,0,0.65)';
      sub.style.boxShadow = `0 0 20px ${s.color || '#ff007f'}55`;
    }

    // 발화 텍스트 정밀 전처리 & 문장 단위 안전 분할
    const rawText = s.speechText || s.dialogue || '';
    const fullTextToSpeak = sanitizeSpeechText(rawText, currentLang);
    const sentenceChunks = splitIntoSentenceChunks(fullTextToSpeak);
    const voiceRate = s.voiceRate || 0.95;

    // 예상 발화 시간 & 사람 간 자연스러운 대화 호흡(1.4초)
    const expectedDuration = calculateTotalExpectedDuration(fullTextToSpeak, voiceRate, currentLang);
    const naturalTurnPause = 1400; // 대화 턴테이킹 호흡 간격
    const totalSceneDuration = expectedDuration + naturalTurnPause;

    // 📱 인스타그램 스토리 릴스 스타일 실시간 프로그레스 바 채우기
    const curFill = document.getElementById(`rpFill-${currentScene}`);
    if (curFill) {
      curFill.style.transition = 'none';
      curFill.style.width = '0%';
      requestAnimationFrame(() => {
        curFill.style.transition = `width ${totalSceneDuration}ms linear`;
        curFill.style.width = '100%';
      });
    }

    if (!isMuted && ('speechSynthesis' in window)) {
      const bestVoice = selectBestVoice(currentLang, s.actor);

      // 크롬 백그라운드 침묵 방지 keep-alive 핑
      keepAliveInterval = setInterval(() => {
        if (window.speechSynthesis.speaking) {
          window.speechSynthesis.pause();
          window.speechSynthesis.resume();
        } else {
          clearInterval(keepAliveInterval);
        }
      }, 6000);

      let chunkIndex = 0;

      function speakNextChunk() {
        if (!isPlaying || activeSceneToken !== thisToken) return;

        if (chunkIndex >= sentenceChunks.length) {
          // 모든 문장 발화 완료! 실제 오디오가 끝날 때까지 250ms 단위 안전 검증
          const verifyInterval = setInterval(() => {
            if (activeSceneToken !== thisToken) {
              clearInterval(verifyInterval);
              return;
            }
            if (!window.speechSynthesis.speaking) {
              clearInterval(verifyInterval);
              clearInterval(keepAliveInterval);
              // 대화 끝난 후 1.4초 여운 호흡 후 다음 씬으로 부드럽게 전환!
              fallbackTimer = setTimeout(() => {
                if (isPlaying && activeSceneToken === thisToken) {
                  advanceNext();
                }
              }, naturalTurnPause);
            }
          }, 250);

          // 비정상 정지 방지용 세이프가드
          setTimeout(() => {
            clearInterval(verifyInterval);
            if (isPlaying && activeSceneToken === thisToken) {
              advanceNext();
            }
          }, naturalTurnPause + 2000);
          return;
        }

        const chunk = sentenceChunks[chunkIndex++];
        const u = new SpeechSynthesisUtterance(chunk);
        u.lang = targetTtsLang;
        u.rate = voiceRate;
        u.pitch = s.pitch || 1.0;
        if (bestVoice) u.voice = bestVoice;

        window._activeUtterance = u;

        u.onend = () => {
          if (activeSceneToken !== thisToken) return;
          // 문장과 문장 사이 180ms 자연스러운 쉼표 숨고르기
          setTimeout(() => {
            speakNextChunk();
          }, 180);
        };

        u.onerror = (e) => {
          if (activeSceneToken !== thisToken) return;
          console.warn("Speech chunk error:", e);
          setTimeout(() => {
            speakNextChunk();
          }, 200);
        };

        window.speechSynthesis.speak(u);
      }

      speakNextChunk();

    } else {
      // 음소거 상태: 자막을 편안히 읽을 수 있는 넉넉한 시간 제공
      fallbackTimer = setTimeout(() => {
        if (isPlaying && activeSceneToken === thisToken) {
          advanceNext();
        }
      }, totalSceneDuration);
    }
  }

  function advanceNext() {
    if (!isPlaying) return;
    const scripts = (window.DRAMA_SCRIPTS && window.DRAMA_SCRIPTS[currentLang]) ? window.DRAMA_SCRIPTS[currentLang] : (window.DRAMA_SCRIPTS ? window.DRAMA_SCRIPTS['ko'] : []);
    if (!scripts) return;

    currentScene++;
    if (currentScene < scripts.length) {
      renderScene(currentScene);
      playCurrentSceneAudio();
    } else {
      stopAudio();
      isPlaying = false;
      const playBtn = document.getElementById('rpBtnPlayPause');
      if (playBtn) playBtn.innerHTML = `<span>↺ 다시보기</span>`;
      currentScene = 0;
    }
  }

  window.prevRoleplayScene = function () {
    stopAudio();
    currentScene = Math.max(0, currentScene - 1);
    renderScene(currentScene);
    if (isPlaying) playCurrentSceneAudio();
  };

  window.nextRoleplayScene = function () {
    stopAudio();
    const scripts = (window.DRAMA_SCRIPTS && window.DRAMA_SCRIPTS[currentLang]) ? window.DRAMA_SCRIPTS[currentLang] : (window.DRAMA_SCRIPTS ? window.DRAMA_SCRIPTS['ko'] : []);
    if (!scripts) return;
    currentScene = (currentScene + 1) % scripts.length;
    renderScene(currentScene);
    if (isPlaying) playCurrentSceneAudio();
  };

  window.toggleRoleplayPlayPause = function () {
    if (isPlaying) {
      pauseShow();
    } else {
      playShow();
    }
  };

  function playShow() {
    isPlaying = true;
    const playBtn = document.getElementById('rpBtnPlayPause');
    if (playBtn) playBtn.innerHTML = `<span>⏸️ 일시정지</span>`;
    renderScene(currentScene);
    playCurrentSceneAudio();
  }

  function pauseShow() {
    isPlaying = false;
    stopAudio();
    const playBtn = document.getElementById('rpBtnPlayPause');
    if (playBtn) playBtn.innerHTML = `<span>▶️ 이어보기</span>`;
  }

  window.toggleRoleplayMute = function () {
    isMuted = !isMuted;
    const muteBtn = document.getElementById('rpBtnSoundToggle');
    if (muteBtn) muteBtn.innerText = isMuted ? '🔇' : '🔊';
    if (isMuted) stopAudio();
    else if (isPlaying) playCurrentSceneAudio();
  };

  window.jumpToRoleplayScene = function (idx) {
    stopAudio();
    currentScene = idx;
    renderScene(currentScene);
    if (isPlaying) playCurrentSceneAudio();
  };

})();
