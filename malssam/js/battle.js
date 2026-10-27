// ============================================================
// 🔥 [실시간 말투 밸런스 배틀 엔진]
// ============================================================
let CURRENT_BATTLE_INDEX = 0;

// 날짜 기반 고유 시드 계산 (매일 자정마다 자동 변경)
function getDailyBattleIndex() {
  const list = window.MALSSAM_BATTLE_QUESTIONS || [];
  if (list.length === 0) return 0;
  const todayStr = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
  let hash = 0;
  for (let i = 0; i < todayStr.length; i++) {
    hash = (hash * 31 + todayStr.charCodeAt(i)) & 0xFFFFFFFF;
  }
  return Math.abs(hash) % list.length;
}

// 특정 인덱스의 배틀 질문 화면에 렌더링
function renderBattleQuestion(idx) {
  const list = window.MALSSAM_BATTLE_QUESTIONS || [];
  if (list.length === 0) return;
  if (idx < 0 || idx >= list.length) idx = 0;
  CURRENT_BATTLE_INDEX = idx;
  const q = list[idx];

  const tagEl = document.getElementById('liveBattleTag');
  const qEl = document.getElementById('liveBattleQ');
  const descEl = document.getElementById('liveBattleDesc');
  const titleA = document.getElementById('liveTitleA');
  const titleB = document.getElementById('liveTitleB');
  const labelA = document.getElementById('liveLabelA');
  const labelB = document.getElementById('liveLabelB');
  const pctA = document.getElementById('livePctA');
  const pctB = document.getElementById('livePctB');
  const gaugeA = document.getElementById('liveGaugeA');
  const gaugeB = document.getElementById('liveGaugeB');
  const btnA = document.getElementById('liveBtnA');
  const btnB = document.getElementById('liveBtnB');
  const msgEl = document.getElementById('liveVoteResultMsg');

  if (tagEl) tagEl.textContent = `🔥 LIVE BATTLE #${q.num} · 실시간 말투 밸런스 게임`;
  if (qEl) qEl.innerHTML = q.question;
  if (descEl) descEl.textContent = q.desc;
  if (titleA) titleA.textContent = q.optA;
  if (titleB) titleB.textContent = q.optB;
  if (labelA) labelA.textContent = q.labelA;
  if (labelB) labelB.textContent = q.labelB;

  // 이전 투표 내역 확인
  const votedChoice = localStorage.getItem('malssam_battle_' + q.id);
  if (btnA) btnA.classList.remove('voted');
  if (btnB) btnB.classList.remove('voted');

  let curPctA = q.pctA;
  let curPctB = q.pctB;

  if (votedChoice === 'A') {
    if (btnA) btnA.classList.add('voted');
    curPctA = Math.min(99, q.pctA + 1);
    curPctB = Math.max(1, 100 - curPctA);
    if (pctA) pctA.innerText = `${curPctA}% (내 선택)`;
    if (pctB) pctB.innerText = `${curPctB}%`;
    if (msgEl) msgEl.style.display = 'block';
  } else if (votedChoice === 'B') {
    if (btnB) btnB.classList.add('voted');
    curPctB = Math.min(99, q.pctB + 1);
    curPctA = Math.max(1, 100 - curPctB);
    if (pctA) pctA.innerText = `${curPctA}%`;
    if (pctB) pctB.innerText = `${curPctB}% (내 선택)`;
    if (msgEl) msgEl.style.display = 'block';
  } else {
    if (pctA) pctA.innerText = `${curPctA}% 투표`;
    if (pctB) pctB.innerText = `${curPctB}% 투표`;
    if (msgEl) msgEl.style.display = 'none';
  }

  if (gaugeA) gaugeA.style.width = `${curPctA}%`;
  if (gaugeB) gaugeB.style.width = `${curPctB}%`;

  if (msgEl) {
    msgEl.innerHTML = `✨ 집단지성 투표 반영 완료! (현재 참여자: ${q.participants}) — 동료들과 링크를 공유해 의견을 나눠보세요!`;
  }
}

// 다음 랜덤 질문 보기
function nextRandomBattle() {
  const list = window.MALSSAM_BATTLE_QUESTIONS || [];
  if (list.length === 0) return;
  let nextIdx = (CURRENT_BATTLE_INDEX + 1) % list.length;
  renderBattleQuestion(nextIdx);
  if (typeof showToast === 'function') {
    showToast(`새로운 밸런스 배틀 #${list[nextIdx].num} 로드 완료!`);
  }
}

// 투표 처리 함수
function voteLiveBattle(choice) {
  const list = window.MALSSAM_BATTLE_QUESTIONS || [];
  if (list.length === 0) return;
  const q = list[CURRENT_BATTLE_INDEX];
  const btnA = document.getElementById('liveBtnA');
  const btnB = document.getElementById('liveBtnB');
  const elMsg = document.getElementById('liveVoteResultMsg');

  if (btnA) btnA.classList.remove('voted');
  if (btnB) btnB.classList.remove('voted');

  let newPctA = q.pctA;
  let newPctB = q.pctB;

  if (choice === 'A') {
    if (btnA) btnA.classList.add('voted');
    newPctA = Math.min(99, q.pctA + 1);
    newPctB = Math.max(1, 100 - newPctA);
    const pA = document.getElementById('livePctA');
    if (pA) pA.innerText = `${newPctA}% (내 선택)`;
    const pB = document.getElementById('livePctB');
    if (pB) pB.innerText = `${newPctB}%`;
    if (typeof showToast === 'function') {
      showToast(q.toastA);
    }
  } else {
    if (btnB) btnB.classList.add('voted');
    newPctB = Math.min(99, q.pctB + 1);
    newPctA = Math.max(1, 100 - newPctB);
    const pA = document.getElementById('livePctA');
    if (pA) pA.innerText = `${newPctA}%`;
    const pB = document.getElementById('livePctB');
    if (pB) pB.innerText = `${newPctB}% (내 선택)`;
    if (typeof showToast === 'function') {
      showToast(q.toastB);
    }
  }

  const gA = document.getElementById('liveGaugeA');
  if (gA) gA.style.width = `${newPctA}%`;
  const gB = document.getElementById('liveGaugeB');
  if (gB) gB.style.width = `${newPctB}%`;
  if (elMsg) elMsg.style.display = 'block';

  localStorage.setItem('malssam_battle_' + q.id, choice);
}
