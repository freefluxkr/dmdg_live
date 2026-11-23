/**
 * DMDG LIVE - Core Modules & Search & Notification Controller
 * Modular Component Architecture
 */

document.addEventListener('DOMContentLoaded', () => {
  initNotifications();
  initCoreApps();
  initSimClusters();
  initLiveSearch();
});

// ── 1. Notification Hub Module ──
let notificationsData = [];

async function initNotifications() {
  const bellBtn = document.getElementById('notifBellBtn');
  const modal = document.getElementById('notifModal');
  const closeBtn = document.getElementById('closeNotifBtn');
  const listContainer = document.getElementById('notifItemsList');
  const badgePill = document.getElementById('notifBadgePill');

  if (!bellBtn || !modal) return;

  try {
    const res = await fetch('./js/data/notifications.json');
    notificationsData = await res.json();
    
    // 뱃지 숫자 갱신
    if (badgePill) {
      badgePill.textContent = notificationsData.length;
    }

    // 아이템 렌더링
    if (listContainer) {
      listContainer.innerHTML = notificationsData.map(item => `
        <a href="${item.url}" target="${item.target || '_blank'}" class="notif-item">
          <div class="notif-item-top">
            <span class="notif-tag" style="background: ${item.badgeColor || '#00A896'};">${item.badge}</span>
            <span class="notif-date">${item.date}</span>
          </div>
          <div class="notif-item-title">${item.title}</div>
          <div class="notif-item-desc">${item.desc}</div>
        </a>
      `).join('');
    }
  } catch (err) {
    console.warn('Notifications load fallback:', err);
  }

  // 모달 토글
  bellBtn.addEventListener('click', () => {
    modal.classList.add('active');
  });

  closeBtn?.addEventListener('click', () => {
    modal.classList.remove('active');
  });

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.remove('active');
    }
  });
}

// ── 2. 5 Core Apps Horizontal Suite Module ──
let coreAppsData = [];

async function initCoreApps() {
  const grid = document.getElementById('coreAppsGrid');
  if (!grid) return;

  try {
    const res = await fetch('./js/data/core_apps.json');
    coreAppsData = await res.json();

    grid.innerHTML = coreAppsData.map(app => {
      const subLinksHtml = app.subLinks && app.subLinks.length > 0 
        ? `<div class="core-card-sublinks">
             ${app.subLinks.map(link => `
               <a href="${link.url}" target="${link.target || '_blank'}" class="sublink-item">
                 <span>${link.icon || '🔗'}</span>
                 <span>${link.text || link.name || ""}</span>
               </a>
             `).join('')}
           </div>`
        : '';

      const metaIconsHtml = app.metaIcons && app.metaIcons.length > 0
        ? `<div class="core-meta-icons">
             ${app.metaIcons.map(icon => `<span>${icon}</span>`).join('')}
           </div>`
        : '';

      return `
        <article class="core-card" id="${app.id}" data-keywords="${app.keywords || ''}">
          <div>
            <div class="core-card-head">
              <div class="core-card-brand">
                <span class="core-card-avatar" style="color: ${app.iconColor || '#00A896'};">${app.icon}</span>
                <div class="core-card-titles">
                  <h3>${app.name}</h3>
                  <span>${app.subtitle}</span>
                </div>
              </div>
              <span class="core-badge ${app.badgeType || 'live'}">${app.badge}</span>
            </div>

            <p class="core-card-desc">${app.desc}</p>

            <div class="core-card-visitor">
              <span>👥</span> 누적 접속자 <strong>${app.visitorCount}</strong>명
            </div>

            ${subLinksHtml}
          </div>

          <div class="core-card-footer">
            <a href="${app.primaryBtn.url}" target="${app.primaryBtn.target || '_self'}" class="btn-core-action ${app.primaryBtn.style || 'teal'}">
              <span>${app.primaryBtn.text}</span>
            </a>
            ${metaIconsHtml}
          </div>
        </article>
      `;
    }).join('');

  } catch (err) {
    console.warn('Core apps load fallback:', err);
  }
}

// ── 3. Simulator Clusters (4 Tracks) Module ──
let simTracksData = [];

async function initSimClusters() {
  const tabsContainer = document.getElementById('simTrackTabs');
  const cardsContainer = document.getElementById('simCardsGrid');
  if (!tabsContainer || !cardsContainer) return;

  try {
    const res = await fetch('./js/data/simulators.json');
    simTracksData = await res.json();

    // 탭 렌더링
    tabsContainer.innerHTML = simTracksData.map((track, idx) => `
      <button class="btn-track-tab ${idx === 0 ? 'active' : ''}" data-track-id="${track.id}">
        <span>${track.icon}</span>
        <span>${track.name}</span>
      </button>
    `).join('');

    // 첫 번째 트랙 렌더링
    renderTrackCards(simTracksData[0].id);

    // 탭 클릭 이벤트
    tabsContainer.addEventListener('click', (e) => {
      const btn = e.target.closest('.btn-track-tab');
      if (!btn) return;

      tabsContainer.querySelectorAll('.btn-track-tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      renderTrackCards(btn.dataset.trackId);
    });

  } catch (err) {
    console.warn('Simulators load fallback:', err);
  }
}

function renderTrackCards(trackId) {
  const cardsContainer = document.getElementById('simCardsGrid');
  if (!cardsContainer) return;

  const track = simTracksData.find(t => t.id === trackId);
  if (!track) return;

  cardsContainer.innerHTML = track.simulators.map(sim => `
    <div class="sim-item-card" data-keywords="${sim.title} ${sim.book} ${sim.desc}">
      <div>
        <div class="sim-item-head">
          <span class="sim-item-book">${sim.book}</span>
          <span style="font-size: 20px;">${sim.icon}</span>
        </div>
        <h4 class="sim-item-title">${sim.title}</h4>
        <p class="sim-item-desc">${sim.desc}</p>
      </div>
      <a href="${sim.url}" class="btn-run-sim" target="_blank">
        <span>실습 런처 열기</span> <span>➔</span>
      </a>
    </div>
  `).join('');
}

// ── 4. Smart Instant Search (Live Filter) Module ──
function initLiveSearch() {
  const searchInput = document.getElementById('liveSearchInput');
  if (!searchInput) return;

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim().toLowerCase();

    // 5대 코어 카드 필터링
    const coreCards = document.querySelectorAll('.core-card');
    coreCards.forEach(card => {
      const keywords = card.getAttribute('data-keywords') || '';
      const text = card.innerText.toLowerCase();
      if (!query || keywords.toLowerCase().includes(query) || text.includes(query)) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });

    // 시뮬레이터 카드 필터링
    const simCards = document.querySelectorAll('.sim-item-card');
    simCards.forEach(card => {
      const keywords = card.getAttribute('data-keywords') || '';
      const text = card.innerText.toLowerCase();
      if (!query || keywords.toLowerCase().includes(query) || text.includes(query)) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  });
}
