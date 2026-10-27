// ============================================================
// 🎨 [말쌈 렌더링 & 검색 & 필터링 엔진]
// ============================================================

// 초성 추출 함수
function getChosung(str) {
  if (!str) return "";
  const CHOSUNG = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"];
  let result = "";
  for (let i = 0; i < str.length; i++) {
    const code = str.charCodeAt(i);
    if (code >= 44032 && code <= 55203) {
      result += CHOSUNG[Math.floor((code - 44032) / 588)];
    } else {
      result += str[i];
    }
  }
  return result;
}

// 토스트 메시지 표시
function showToast(msg) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.innerText = msg;
  toast.style.display = 'block';
  setTimeout(() => {
    toast.style.display = 'none';
  }, 3000);
}

// K-Soul 7대 서브카테고리 필터링 (기존 4대 + 신규 의성어, 의태어, 색채어)
function filterSoulSubcat(subcat, ev) {
  currentSoulSubcat = subcat;
  document.querySelectorAll('.soul-subcat-btn').forEach(b => b.classList.remove('active'));
  if (ev && ev.currentTarget) {
    ev.currentTarget.classList.add('active');
  } else if (ev && ev.target) {
    const btn = ev.target.closest('.soul-subcat-btn');
    if (btn) btn.classList.add('active');
  }
  
  // 만약 K-정서 검색창에 검색어가 있다면 해당 카테고리 내에서 재검색
  const soulInput = document.getElementById('soulSearchInput');
  if (soulInput && soulInput.value.trim()) {
    handleSoulSearch();
  } else {
    applyFilterAndRender();
  }
}

// 시대별 & K-정서 서브카테고리 단어 수 카운트 업데이트
function updateEraCounts() {
  if (!window.words) return;
  const latteCount = window.words.filter(w => w.era === 'latte').length;
  const smartCount = window.words.filter(w => w.era === 'smartphone').length;
  const shortsCount = window.words.filter(w => w.era === 'shorts').length;
  const soulCount = window.words.filter(w => w.era === 'soul').length;

  const cAll = document.getElementById('countAll');
  if (cAll) cAll.innerText = `${window.words.length}단어`;
  const cLatte = document.getElementById('countLatte');
  if (cLatte) cLatte.innerText = `1990~2000s (${latteCount})`;
  const cSmart = document.getElementById('countSmartphone');
  if (cSmart) cSmart.innerText = `2010s (${smartCount})`;
  const cShorts = document.getElementById('countShorts');
  if (cShorts) cShorts.innerText = `2020~2026 (${shortsCount})`;
  const cSoul = document.getElementById('countSoul');
  if (cSoul) cSoul.innerText = `K-Soul (${soulCount})`;

  // K-정서 7대 서브카테고리 카운트 갱신
  const countEmotion = window.words.filter(w => w.era === 'soul' && w.sub_category === 'emotion').length;
  const countRel = window.words.filter(w => w.era === 'soul' && w.sub_category === 'relationship').length;
  const countBeh = window.words.filter(w => w.era === 'soul' && w.sub_category === 'behavior').length;
  const countCul = window.words.filter(w => w.era === 'soul' && w.sub_category === 'culture').length;
  const countOno = window.words.filter(w => w.era === 'soul' && w.sub_category === 'onomatopoeia').length;
  const countMim = window.words.filter(w => w.era === 'soul' && w.sub_category === 'mimetic').length;
  const countCol = window.words.filter(w => w.era === 'soul' && w.sub_category === 'color').length;

  const elAll = document.getElementById('soulBtnAll');
  if (elAll) elAll.innerText = `전체보기 (${soulCount})`;
  const elEmo = document.getElementById('soulBtnEmotion');
  if (elEmo) elEmo.innerText = `💭 심리·감정 (${countEmotion})`;
  const elRel = document.getElementById('soulBtnRelationship');
  if (elRel) elRel.innerText = `🤝 관계·유대 (${countRel})`;
  const elBeh = document.getElementById('soulBtnBehavior');
  if (elBeh) elBeh.innerText = `🏃 습관·행동 (${countBeh})`;
  const elCul = document.getElementById('soulBtnCulture');
  if (elCul) elCul.innerText = `🎎 사회·문화 (${countCul})`;
  const elOno = document.getElementById('soulBtnOno');
  if (elOno) elOno.innerText = `🔊 의성어 (${countOno})`;
  const elMim = document.getElementById('soulBtnMim');
  if (elMim) elMim.innerText = `✨ 의태어 (${countMim})`;
  const elCol = document.getElementById('soulBtnCol');
  if (elCol) elCol.innerText = `🎨 색채어 (${countCol})`;

  const statusEl = document.getElementById('soulSearchStatus');
  if (statusEl) statusEl.innerText = `총 ${soulCount}선 K-SOUL 수록`;
}

// 시대 탭 전환 함수
function switchEra(era) {
  const subcatSec = document.getElementById('soulSubcatSection');
  if (subcatSec) {
    subcatSec.style.display = (era === 'soul') ? 'block' : 'none';
  }
  if (era === 'soul') {
    currentSoulSubcat = 'all';
    document.querySelectorAll('.soul-subcat-btn').forEach((b, idx) => {
      if (idx === 0) b.classList.add('active');
      else b.classList.remove('active');
    });
    // K-정서 검색창 초기화
    const soulInput = document.getElementById('soulSearchInput');
    if (soulInput) soulInput.value = '';
    const clearBtn = document.getElementById('soulSearchClearBtn');
    if (clearBtn) clearBtn.style.display = 'none';
  }
  currentEra = era;
  document.querySelectorAll('.era-tab-btn').forEach(b => b.classList.remove('active'));

  const infoBox = document.getElementById('eraInfoContent');

  if (era === 'kakao') {
    const kakaoTab = document.getElementById('tabKakaoBtn');
    if (kakaoTab) kakaoTab.classList.add('active');
    if (infoBox) {
      infoBox.innerHTML = `<span>💬 <strong>4. 실시간 카톡 맥락 판독소 (BEST 10선 & 유저 의뢰)</strong>: '영ㅋㅋ', 'H워얼V', '네.' 마침표 등 헷갈리는 메신저 답장의 속뜻과 뉘앙스를 집단지성으로 실시간 판독합니다.</span><button onclick="openKakaoModal()" class="btn-kakao-request" style="font-size:0.75rem; padding:4px 12px; height:auto; background:linear-gradient(135deg, #eab308, #ca8a04); color:#000; font-weight:800; border-radius:8px; border:none; cursor:pointer; margin-left:8px; white-space:nowrap;">+ 내 카톡 판독 의뢰</button>`;
    }
    renderKakaoFeed();
    return;
  }

  if (era === 'all') {
    const btn = document.getElementById('tabAllBtn');
    if (btn) btn.classList.add('active');
    if (infoBox) infoBox.innerHTML = `<span>✨ <strong>전체 ${window.words.length}선 아카이브</strong>: 1990년대 PC통신부터 2026년 최신 영포티·영ㅋㅋ 밈, K-정서 및 의성·의태·색채어까지 전 시대를 한눈에 탐색합니다.</span><span style='color:var(--accent-yellow); font-weight:700;'>총 ${window.words.length}개 표제어 수록</span>`;
  } else if (era === 'latte') {
    const btn = document.getElementById('tabLatteBtn');
    if (btn) btn.classList.add('active');
    if (infoBox) infoBox.innerHTML = "<span>📟 <strong>1. 라떼 추억 (1990~2000s)</strong>: 삐삐 감성, PC통신(천리안·나우누리), 싸이월드 시절 탄생한 최초의 신조어 세대.</span><span style='color:var(--accent-green); font-weight:700;'>27개 표제어 수록</span>";
  } else if (era === 'smartphone') {
    const btn = document.getElementById('tabSmartBtn');
    if (btn) btn.classList.add('active');
    if (infoBox) infoBox.innerHTML = "<span>📱 <strong>2. 국민 유행어 (2010s)</strong>: 스마트폰 보급, 카카오톡, 커뮤니티(DC·일베·오유 등)를 통해 전국민이 쓰게 된 전성기 유행어.</span><span style='color:var(--accent-cyan); font-weight:700;'>31개 표제어 수록</span>";
  } else if (era === 'shorts') {
    const btn = document.getElementById('tabShortsBtn');
    if (btn) btn.classList.add('active');
    if (infoBox) infoBox.innerHTML = "<span>⚡ <strong>3. 요즘 1020 밈 (2020~2026)</strong>: 틱톡, 릴스, 쇼츠와 버블·위버스 등 실시간 팬덤 소통에서 탄생한 숏폼 세대 밈.</span><span style='color:var(--accent-pink); font-weight:700;'>142개 표제어 수록</span>";
  } else if (era === 'soul') {
    const btn = document.getElementById('tabSoulBtn');
    if (btn) btn.classList.add('active');
    const soulCount = window.words.filter(w => w.era === 'soul').length;
    if (infoBox) infoBox.innerHTML = `<span>💎 <strong>4. K-정서 (번역불가 118선 & 의성·의태·색채어)</strong>: 외국어로 1:1 직역이 불가능한 한국 고유의 감정, 관계, 정서 및 오감 어휘. 전용 검색창과 글로벌 로마자 발음, 영문 맥락 해설을 전수 제공합니다.</span><span style='color:var(--accent-purple); font-weight:700;'>총 ${soulCount}선 K-SOUL 표제어 수록</span>`;
  }

  applyFilterAndRender();
}

// 정렬 필터 전환
function setFilter(type, ev) {
  currentFilter = type;
  document.querySelectorAll('.filter-tab-btn').forEach(b => b.classList.remove('active'));
  if (ev && ev.currentTarget) {
    ev.currentTarget.classList.add('active');
  } else if (ev && ev.target) {
    const btn = ev.target.closest('.filter-tab-btn');
    if (btn) btn.classList.add('active');
  }
  applyFilterAndRender();
}

// 단어 카드 렌더링 엔진 (방어 코드 탑재)
function renderWords(items) {
  try {
    const container = document.getElementById('wordsContainer');
    if (!container) return;
    container.innerHTML = "";

    const badge = document.getElementById('feedCountBadge');
    if (badge) badge.innerText = `${items.length}개`;

    if (!items || items.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 60px 20px; color: #94a3b8;">
          <p style="font-size: 2.5rem; margin-bottom: 10px;">🤔</p>
          <p style="font-size: 1.2rem; font-weight: 700; color: #f1f5f9;">해당 조건의 신조어를 찾을 수 없습니다!</p>
          <p style="margin-top: 6px;">다른 검색어를 입력하시거나 <strong>[+ 신조어 제보하기]</strong>로 등록해 보세요!</p>
        </div>
      `;
      return;
    }

    items.forEach(w => {
      try {
        let badgeClass = 'badge-hot';
        let badgeText = '🔥 HOT';
        if (w.trend_status === 'LEGEND') {
          badgeClass = 'badge-legend';
          badgeText = '👑 레전드';
        } else if (w.trend_status === 'RETRO') {
          badgeClass = 'badge-retro';
          badgeText = '📟 라떼 레트로';
        } else if (w.trend_status === 'STEADY') {
          badgeClass = 'badge-steady';
          badgeText = '✨ 스테디';
        } else if (w.trend_status === 'SOUL') {
          badgeClass = 'badge-soul';
          badgeText = '💎 K-SOUL';
        }

        let eraPillClass = 'era-pill-shorts';
        let eraPillText = '⚡ 요즘 1020 밈';
        if (w.era === 'latte') {
          eraPillClass = 'era-pill-latte';
          eraPillText = '📟 1990s 라떼 추억';
        } else if (w.era === 'smartphone') {
          eraPillClass = 'era-pill-smartphone';
          eraPillText = '📱 2010s 국민 유행어';
        } else if (w.era === 'soul') {
          eraPillClass = 'era-pill-soul';
          eraPillText = '💎 K-정서 (번역불가)';
        }

        let subcatLabel = '';
        if (w.sub_category === 'emotion') subcatLabel = '💭 심리·감정';
        else if (w.sub_category === 'relationship') subcatLabel = '🤝 관계·유대';
        else if (w.sub_category === 'behavior') subcatLabel = '🏃 습관·행동';
        else if (w.sub_category === 'culture') subcatLabel = '🎎 사회·문화';
        else if (w.sub_category === 'onomatopoeia') subcatLabel = '🔊 의성어';
        else if (w.sub_category === 'mimetic') subcatLabel = '✨ 의태어';
        else if (w.sub_category === 'color') subcatLabel = '🎨 색채어';

        const votedState = (window.userVotes || {})[w.id];
        const safeWord = String(w.word || '').replace(/'/g, "\\'");
        const safeShortDef = String(w.short_def || '').replace(/'/g, "\\'");
        const safeEx = (w.examples && w.examples[0]) ? String(w.examples[0]).replace(/\n/g, '<br>') : '';
        const hasRoleplay = (w.has_roleplay || w.id === 202 || w.word === '눈치');

        const card = document.createElement('div');
        card.className = 'word-card';
        card.id = `card-${w.id}`;
        card.innerHTML = `
          <div class="word-header">
            <div class="word-title-group">
              <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                <span class="word-title">${w.word || ''}</span>
                <button class="btn-sound-speak" onclick="speakWord('${safeWord}', event)" title="원어민 발음 듣기 (Listen Pronunciation)">
                  <span>🔊</span>
                </button>
                ${hasRoleplay ? `<button class="btn-card-roleplay" onclick="openRoleplayModal('${w.id}', event)" title="DMDG 3D 숏폼 상황극 보기"><span>🎬 3D 상황극 ↺</span></button>` : ''}
              </div>
              <div class="word-phonetic-badge">
                <span class="phonetic-rr">🗣️ [${w.romanization || w.pronunciation || ''}]</span>
                ${w.phonetic_respelling ? `<span class="phonetic-respell">· ${w.phonetic_respelling}</span>` : ''}
                <span class="word-pos">· ${w.part_of_speech || '어휘'}</span>
              </div>
            </div>
            <div class="word-badges-group">
              <span class="era-pill ${eraPillClass}">${eraPillText}</span>
              <span class="word-badge ${badgeClass}">${badgeText}</span>
              ${w.sub_category ? `<span class="subcat-chip chip-${w.sub_category}">${subcatLabel || w.sub_category}</span>` : ''}
            </div>
          </div>

          <div class="word-definition">${w.short_def || ''}</div>

          ${safeEx ? `<div class="word-example-box">${safeEx}</div>` : ''}

          <div class="word-ai-dna">
            <span>👥 주도 세대: <strong>${w.generation || '전 세대'}</strong></span>
            <span>🚨 위험도: <strong>${w.toxicity_level === 0 ? '🟢 건전 (공식 석상 OK)' : (w.toxicity_level <= 2 ? '🟡 일상 (친구/사내 메신저)' : '🔴 주의 (비속어 주의)')}</strong></span>
            <span>📖 기성 표준어 매칭: <strong>${w.standard_korean_mapping || '대응 단어 없음 (완전 신조어)'}</strong></span>
          </div>
          ${w.en ? `
          <div class="word-en-box" style="margin-top: 10px; padding: 10px 14px; background: rgba(168, 85, 247, 0.08); border-radius: 10px; border: 1px solid rgba(168, 85, 247, 0.25); font-size: 0.82rem; color: #e9d5ff;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <span style="color:#c084fc; font-weight:800; font-size:0.74rem; letter-spacing:0.5px;">🌐 GLOBAL CONTEXTUAL DEF</span>
              <span style="font-size:0.70rem; color:#f472b6; font-weight:700; background:rgba(244,114,182,0.15); padding:1px 6px; border-radius:10px;">Untranslatable K-Culture</span>
            </div>
            <div style="font-weight:700; color:#f8fafc; margin-bottom:3px;">${w.en.slang || ''}</div>
            <div style="color:#d8b4fe; font-size:0.79rem; line-height:1.45;">${w.en.desc || ''}</div>
            ${(w.en.example || w.en.ex) ? `<div style="margin-top:5px; padding-top:5px; border-top:1px dashed rgba(168,85,247,0.2); font-style:italic; color:#cbd5e1; font-size:0.75rem;">${String(w.en.example || w.en.ex).replace(/\n/g, '<br>')}</div>` : ''}
          </div>` : ''}

          <div class="word-footer">
            <div class="vote-group">
              <button class="btn-vote ${votedState === 'up' ? 'voted-up' : ''}" onclick="vote(${w.id}, 'up')">
                <span>👍 공감</span>
                <span id="like-count-${w.id}">${Number(w.likes || 0).toLocaleString()}</span>
              </button>
              <button class="btn-vote ${votedState === 'down' ? 'voted-down' : ''}" onclick="vote(${w.id}, 'down')">
                <span>👎 억지</span>
                <span id="dislike-count-${w.id}">${Number(w.dislikes || 0).toLocaleString()}</span>
              </button>
            </div>

            <div class="word-tags">
              ${(w.tags || []).map(t => `<span class="tag-item">#${t}</span>`).join('')}
            </div>

            <button class="btn-share" onclick="shareWord('${safeWord}', '${safeShortDef}')">
              <span>🔗 공유</span>
            </button>
          </div>
        `;
        container.appendChild(card);
      } catch (cardErr) {
        console.error("Card render error for item:", w, cardErr);
      }
    });
  } catch (err) {
    console.error("renderWords global error:", err);
  }
}

// 다차원 실시간 검색 및 필터링
function applyFilterAndRender() {
  if (!window.words) return;
  let pool = (currentEra === 'all') 
    ? [...window.words] 
    : (currentEra === 'soul' && currentSoulSubcat !== 'all')
      ? window.words.filter(w => w.era === 'soul' && w.sub_category === currentSoulSubcat)
      : window.words.filter(w => w.era === currentEra);

  if (currentFilter === 'hot') {
    pool.sort((a, b) => (b.likes || 0) - (a.likes || 0));
  } else {
    pool.sort((a, b) => b.id - a.id);
  }

  let eraLabel = `전체 신조어 ${window.words.length}선`;
  if (currentEra === 'latte') eraLabel = "1. 📟 라떼 추억 (1990~2000s)";
  if (currentEra === 'smartphone') eraLabel = "2. 📱 국민 유행어 (2010s)";
  if (currentEra === 'shorts') eraLabel = "3. ⚡ 요즘 1020 밈 (2020s~2026)";
  if (currentEra === 'soul') {
    const soulTotal = window.words.filter(w => w.era === 'soul').length;
    eraLabel = `4. 💎 K-정서 (번역불가) & 의성·의태·색채 (${soulTotal}선)`;
  }

  const titleEl = document.getElementById('feedTitleText');
  if (titleEl) titleEl.innerText = eraLabel;
  renderWords(pool);
}

// 💎 K-정서 전용 인라인 실시간 검색 핸들러
function handleSoulSearch() {
  const input = document.getElementById('soulSearchInput');
  if (!input) return;
  const query = input.value.trim().toLowerCase();
  const clearBtn = document.getElementById('soulSearchClearBtn');
  if (clearBtn) clearBtn.style.display = query ? 'flex' : 'none';

  if (!query) {
    applyFilterAndRender();
    return;
  }

  const soulWords = window.words.filter(w => w.era === 'soul');
  const pool = (currentSoulSubcat === 'all') 
    ? soulWords 
    : soulWords.filter(w => w.sub_category === currentSoulSubcat);

  const filtered = pool.filter(w => {
    const wordLower = (w.word || '').toLowerCase();
    const chosung = (w.chosung || '').toLowerCase();
    const defLower = (w.short_def || '').toLowerCase();
    const tagsLower = (w.tags || []).join(' ').toLowerCase();
    const mappingLower = (w.standard_korean_mapping || '').toLowerCase();
    const romLower = (w.romanization || w.pronunciation || '').toLowerCase();
    const respellLower = (w.phonetic_respelling || '').toLowerCase();
    const enSlangLower = (w.en && w.en.slang) ? w.en.slang.toLowerCase() : '';
    const enDescLower = (w.en && w.en.desc) ? w.en.desc.toLowerCase() : '';

    return wordLower.includes(query) ||
           chosung.includes(query) ||
           defLower.includes(query) ||
           tagsLower.includes(query) ||
           mappingLower.includes(query) ||
           romLower.includes(query) ||
           respellLower.includes(query) ||
           enSlangLower.includes(query) ||
           enDescLower.includes(query);
  });

  const statusEl = document.getElementById('soulSearchStatus');
  if (statusEl) {
    statusEl.innerText = `${pool.length}개 중 ${filtered.length}개 검색됨`;
  }

  const titleEl = document.getElementById('feedTitleText');
  if (titleEl) titleEl.innerText = `💎 K-정서 '${query}' 검색 결과 (${filtered.length}건)`;
  renderWords(filtered);
}

function clearSoulSearch() {
  const input = document.getElementById('soulSearchInput');
  if (input) input.value = '';
  const clearBtn = document.getElementById('soulSearchClearBtn');
  if (clearBtn) clearBtn.style.display = 'none';
  const soulWords = window.words.filter(w => w.era === 'soul');
  const statusEl = document.getElementById('soulSearchStatus');
  if (statusEl) statusEl.innerText = `총 ${soulWords.length}선 K-SOUL 수록`;
  applyFilterAndRender();
}

function quickSoulSearch(term) {
  const input = document.getElementById('soulSearchInput');
  if (!input) return;
  input.value = term;
  handleSoulSearch();
}

// 상단 다차원 검색 핸들러 (초성, 단어명, 태그, 시대 매칭)
function handleSearch() {
  const query = document.getElementById('searchInput').value.trim().toLowerCase();
  
  if (currentEra === 'soul') {
    const soulInput = document.getElementById('soulSearchInput');
    if (soulInput) {
      soulInput.value = query;
      handleSoulSearch();
      return;
    }
  }

  if (!query) {
    applyFilterAndRender();
    return;
  }

  let pool = (currentEra === 'all') ? [...window.words] : window.words.filter(w => w.era === currentEra);

  const filtered = pool.filter(w => {
    const wordLower = (w.word || '').toLowerCase();
    const chosung = (w.chosung || '').toLowerCase();
    const defLower = (w.short_def || '').toLowerCase();
    const tagsLower = (w.tags || []).join(' ').toLowerCase();
    const mappingLower = (w.standard_korean_mapping || '').toLowerCase();
    const enSlangLower = (w.en && w.en.slang) ? w.en.slang.toLowerCase() : '';
    const enDescLower = (w.en && w.en.desc) ? w.en.desc.toLowerCase() : '';

    return wordLower.includes(query) ||
           chosung.includes(query) ||
           defLower.includes(query) ||
           tagsLower.includes(query) ||
           mappingLower.includes(query) ||
           enSlangLower.includes(query) ||
           enDescLower.includes(query);
  });

  const titleEl = document.getElementById('feedTitleText');
  if (titleEl) titleEl.innerText = `'${query}' 검색 결과 (${filtered.length}건)`;
  renderWords(filtered);
}

// 투표 처리 함수
function vote(id, type) {
  const target = window.words.find(w => w.id === id);
  if (!target) return;

  if (window.userVotes[id] === type) {
    showToast("이미 투표하셨습니다!");
    return;
  }

  if (type === 'up') {
    target.likes = (target.likes || 0) + 1;
    if (window.userVotes[id] === 'down') target.dislikes = Math.max(0, (target.dislikes || 0) - 1);
  } else {
    target.dislikes = (target.dislikes || 0) + 1;
    if (window.userVotes[id] === 'up') target.likes = Math.max(0, (target.likes || 0) - 1);
  }

  window.userVotes[id] = type;
  localStorage.setItem('malssam_votes_v4', JSON.stringify(window.userVotes));
  localStorage.setItem('malssam_words_v11_stable', JSON.stringify(window.words));

  const likeEl = document.getElementById(`like-count-${id}`);
  const dislikeEl = document.getElementById(`dislike-count-${id}`);
  if (likeEl) likeEl.innerText = target.likes.toLocaleString();
  if (dislikeEl) dislikeEl.innerText = target.dislikes.toLocaleString();
  showToast(type === 'up' ? "👍 공감을 보냈습니다!" : "👎 억지 투표를 반영했습니다.");
}

// 공유하기 함수
function shareWord(word, def) {
  const shareUrl = "https://malssam.com/";
  if (navigator.clipboard) {
    navigator.clipboard.writeText(`[말쌈 (MALSSAM)] '${word}' 뜻: ${def}\n시대별 신조어 & 세대공감 퀴즈 👉 ${shareUrl}`);
    showToast("🔗 단어 정의와 라이브 링크가 클립보드에 복사되었습니다!");
  } else {
    showToast("공유하기를 지원하지 않는 브라우저입니다.");
  }
}
