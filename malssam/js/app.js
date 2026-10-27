// ============================================================
// 🚀 [말쌈 (MALSSAM) 메인 애플리케이션 초기화 모듈]
// ============================================================

// 전역 상태 변수
let currentEra = 'all';
let currentSoulSubcat = 'all';
let currentFilter = 'hot';
window.userVotes = JSON.parse(localStorage.getItem('malssam_votes_v4')) || {};

// 로컬 스토리지 V11 안전 마이그레이션 (318단어 전수 무결점 보장)
window.words = window.DEFAULT_WORDS || [];
try {
  const cached = localStorage.getItem('malssam_words_v11_stable');
  if (cached) {
    const parsed = JSON.parse(cached);
    if (Array.isArray(parsed) && parsed.length >= (window.DEFAULT_WORDS || []).length) {
      window.words = parsed;
    } else {
      window.words = window.DEFAULT_WORDS || [];
      localStorage.setItem('malssam_words_v11_stable', JSON.stringify(window.words));
    }
  } else {
    window.words = window.DEFAULT_WORDS || [];
    localStorage.setItem('malssam_words_v11_stable', JSON.stringify(window.words));
  }
} catch(e) {
  console.warn("Storage init warning:", e);
  window.words = window.DEFAULT_WORDS || [];
}

// 신조어 제보 모달 제어
function openAddModal() {
  const modal = document.getElementById('addModal');
  if (modal) modal.classList.add('active');
}

function closeAddModal() {
  const modal = document.getElementById('addModal');
  if (modal) modal.classList.remove('active');
}

function submitNewWord(e) {
  e.preventDefault();
  const wordVal = document.getElementById('newWord').value.trim();
  const eraVal = document.getElementById('newEra').value;
  const posVal = document.getElementById('newPos').value;
  const defVal = document.getElementById('newDef').value.trim();
  const standardVal = document.getElementById('newStandard').value.trim();
  const exampleVal = document.getElementById('newExample').value.trim();
  const tagsVal = document.getElementById('newTags').value.trim();
  const authorVal = document.getElementById('newAuthor').value.trim() || "언어술사";

  const existing = window.words.find(w => w.word.toLowerCase() === wordVal.toLowerCase());
  if (existing) {
    alert(`'${existing.word}' 은(는) 이미 등록된 신조어입니다!`);
    return;
  }

  const newId = window.words.length + 100;
  const chosungVal = getChosung(wordVal);
  const newObj = {
    id: newId,
    word: wordVal,
    pronunciation: `[${wordVal}]`,
    part_of_speech: posVal,
    chosung: chosungVal,
    era: eraVal,
    era_name: eraVal === 'latte' ? "1. 📟 라떼 추억" : (eraVal === 'smartphone' ? "2. 📱 국민 유행어" : "3. ⚡ 요즘 1020 밈"),
    generation: "사용자 실시간 제보",
    short_def: defVal,
    examples: [exampleVal || `A: 요즘 '${wordVal}' 많이 쓰더라!\nB: 맞아, 완전 유행이야!`],
    tags: tagsVal ? tagsVal.split(',').map(t => t.trim()) : ["실시간신조어"],
    likes: 1,
    dislikes: 0,
    author: authorVal,
    toxicity_level: 1,
    standard_korean_mapping: standardVal || "심사 대기 중",
    trend_status: "HOT"
  };

  window.words.unshift(newObj);
  localStorage.setItem('malssam_words_v11_stable', JSON.stringify(window.words));
  closeAddModal();
  showToast(`🎉 '${wordVal}' 신조어가 성공적으로 제보되었습니다!`);
  updateEraCounts();
  applyFilterAndRender();
}

// DOMContentLoaded 초기화
document.addEventListener('DOMContentLoaded', () => {
  // 1. 배틀 질문 렌더링
  if (typeof renderBattleQuestion === 'function' && typeof getDailyBattleIndex === 'function') {
    renderBattleQuestion(getDailyBattleIndex());
  }

  // 2. 시대별 카운트 & 카드 렌더링
  if (typeof updateEraCounts === 'function') {
    updateEraCounts();
  }
  if (typeof applyFilterAndRender === 'function') {
    applyFilterAndRender();
  }

  // 3. Firebase Firestore 비동기 추가 로드
  if (typeof window.loadFirestoreWords === 'function') {
    window.loadFirestoreWords().then(fbWords => {
      if (fbWords && fbWords.length > 0) {
        fbWords.forEach(fw => {
          if (!window.words.some(w => w.word.toLowerCase() === fw.word.toLowerCase())) {
            window.words.unshift(fw);
          }
        });
        updateEraCounts();
        applyFilterAndRender();
        const badge = document.getElementById('fbStatusBadge');
        if (badge) badge.innerText = `🟢 실시간 DB (${window.words.length})`;
      }
    }).catch(err => console.warn("Firestore load error:", err));
  }
});
