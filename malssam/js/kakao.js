// ============================================================
// 💬 [실시간 카톡 맥락 판독소 모듈]
// ============================================================

function openKakaoModal() {
  const m = document.getElementById('kakaoModal');
  if (m) m.classList.add('active');
}

function closeKakaoModal() {
  const m = document.getElementById('kakaoModal');
  if (m) m.classList.remove('active');
}

function submitKakaoRequest(e) {
  e.preventDefault();
  const cat = document.getElementById('kakaoCat').value;
  const title = document.getElementById('kakaoTitle').value.trim();
  let text = document.getElementById('kakaoText').value.trim();
  const optA = document.getElementById('kakaoOptA').value.trim();
  const optB = document.getElementById('kakaoOptB').value.trim();

  // 전화번호 마스킹 가드레일
  text = text.replace(/010[- ]?\d{4}[- ]?\d{4}/g, '010-****-****');

  const customCard = {
    id: 'custom_' + Date.now(),
    cat: cat,
    title: title,
    sender: '상대방',
    senderBubble: '최근 대화 상황',
    myBubble: text,
    optA: optA,
    optB: optB,
    pctA: 50, pctB: 50, votes: 1,
    traffic: 'green', trafficLabel: '신규등록 🟢'
  };

  let customList = JSON.parse(localStorage.getItem('malssam_kakao_user_cards') || '[]');
  customList.unshift(customCard);
  localStorage.setItem('malssam_kakao_user_cards', JSON.stringify(customList));

  const form = document.getElementById('kakaoRequestForm');
  if (form) form.reset();

  closeKakaoModal();
  showToast('🎉 카톡 판독 의뢰가 등록되었습니다! 판독소 탭에서 확인하세요.');
  switchEra('kakao');

  const el = document.getElementById('feedTitleText');
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// 카톡 판독소 카드 렌더링
function renderKakaoFeed() {
  const container = document.getElementById('wordsContainer');
  if (!container) return;
  const userCards = JSON.parse(localStorage.getItem('malssam_kakao_user_cards') || '[]');
  const seedCards = window.KAKAO_SEED_CARDS || [];
  let allKakao = [...userCards, ...seedCards];

  if (currentFilter === 'hot') {
    allKakao.sort((a, b) => (b.votes || 0) - (a.votes || 0));
  }

  const titleEl = document.getElementById('feedTitleText');
  if (titleEl) titleEl.innerText = '💬 실시간 카톡 맥락 판독소 BEST 10선';
  const badgeEl = document.getElementById('feedCountBadge');
  if (badgeEl) badgeEl.innerText = allKakao.length + '개 안건';

  let html = '';
  allKakao.forEach(item => {
    const key = 'voted_' + item.id;
    const myVote = localStorage.getItem(key);
    let pctTextA = item.pctA + '%';
    let pctTextB = item.pctB + '%';
    if (myVote === 'A') pctTextA += ' (내 선택)';
    if (myVote === 'B') pctTextB += ' (내 선택)';

    html += `
      <div class="kakao-card" id="card_${item.id}">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span class="word-badge badge-hot">${item.cat}</span>
            <span class="traffic-pill traffic-${item.traffic}">${item.trafficLabel}</span>
          </div>
          <span style="font-size:0.75rem; color:#94a3b8;">참여: ${item.votes}명</span>
        </div>
        
        <h3 style="font-size:1.15rem; font-weight:800; color:#f8fafc; margin-bottom:10px;">${item.title}</h3>

        <!-- Kakao Mockup Bubble -->
        <div class="kakao-chat-room">
          <div class="bubble-row-other">
            <div class="avatar-circle" style="background:#64748b;">상대</div>
            <div class="bubble-other">${item.senderBubble}</div>
          </div>
          <div class="bubble-row-me">
            <div class="bubble-me">${item.myBubble}</div>
          </div>
        </div>

        <!-- Vote Poll Options -->
        <div style="display:flex; flex-direction:column; gap:8px; margin-top:14px;">
          <button class="live-vote-btn" onclick="voteKakao('${item.id}', 'A')">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:0.88rem; font-weight:700; color:#fff;">🅰️ ${item.optA}</span>
              <span id="pctA_${item.id}" style="color:#f43f5e; font-weight:800;">${pctTextA}</span>
            </div>
            <div class="live-vote-gauge-wrap">
              <div class="live-vote-gauge gauge-a" id="barA_${item.id}" style="width:${item.pctA}%;"></div>
            </div>
          </button>

          <button class="live-vote-btn" onclick="voteKakao('${item.id}', 'B')">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:0.88rem; font-weight:700; color:#fff;">🅱️ ${item.optB}</span>
              <span id="pctB_${item.id}" style="color:#38bdf8; font-weight:800;">${pctTextB}</span>
            </div>
            <div class="live-vote-gauge-wrap">
              <div class="live-vote-gauge gauge-b" id="barB_${item.id}" style="width:${item.pctB}%;"></div>
            </div>
          </button>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

// 카톡 카드 투표 로직
function voteKakao(cardId, choice) {
  const key = 'voted_' + cardId;
  if (localStorage.getItem(key)) {
    showToast('이미 투표에 참여하셨습니다!');
    return;
  }
  localStorage.setItem(key, choice);
  showToast(`✨ 판독 투표 완료! 집단지성에 기여하셨습니다.`);
  
  const elPctA = document.getElementById('pctA_' + cardId);
  const elPctB = document.getElementById('pctB_' + cardId);
  const elBarA = document.getElementById('barA_' + cardId);
  const elBarB = document.getElementById('barB_' + cardId);
  
  if (choice === 'A' && elPctA && elBarA) {
    let curVal = parseInt(elPctA.innerText) || 50;
    let newVal = Math.min(99, curVal + 1);
    elPctA.innerText = newVal + '% (내 선택)';
    elBarA.style.width = newVal + '%';
    if (elPctB && elBarB) {
      let bVal = Math.max(1, 100 - newVal);
      elPctB.innerText = bVal + '%';
      elBarB.style.width = bVal + '%';
    }
  } else if (choice === 'B' && elPctB && elBarB) {
    let curVal = parseInt(elPctB.innerText) || 50;
    let newVal = Math.min(99, curVal + 1);
    elPctB.innerText = newVal + '% (내 선택)';
    elBarB.style.width = newVal + '%';
    if (elPctA && elBarA) {
      let aVal = Math.max(1, 100 - newVal);
      elPctA.innerText = aVal + '%';
      elBarA.style.width = aVal + '%';
    }
  }
}
