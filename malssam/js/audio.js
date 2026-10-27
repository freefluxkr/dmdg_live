// ============================================================
// 🔊 [Web Speech API 한국어 TTS 원어민 발음 재생 엔진]
// ============================================================
function speakWord(text, ev) {
  if (ev) ev.stopPropagation();
  if (!('speechSynthesis' in window)) {
    if (typeof showToast === 'function') showToast("이 브라우저는 음성 재생을 지원하지 않습니다.");
    return;
  }
  window.speechSynthesis.cancel();
  const cleanText = text.replace(/\(.*\)/g, '').replace(/[^\w\s가-힣]/g, '').trim();
  const u = new SpeechSynthesisUtterance(cleanText);
  u.lang = 'ko-KR';
  u.rate = 0.92;
  u.pitch = 1.0;
  window.speechSynthesis.speak(u);

  // 시각 효과 피드백
  if (ev && ev.currentTarget) {
    const btn = ev.currentTarget;
    btn.classList.add('speaking');
    u.onend = () => btn.classList.remove('speaking');
    u.onerror = () => btn.classList.remove('speaking');
  }
}
