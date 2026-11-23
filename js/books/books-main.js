/**
 * ==============================================================================
 * DMDG 스튜디오 도서관 (Books) 메인 컨트롤러 모듈
 * 파일명: js/books/books-main.js
 * ==============================================================================
 */

class BooksApp {
  constructor() {
    this.books = [];
    this.currentCategory = 'all';
    this.searchQuery = '';
    this.selectedBook = null;
    this.activeViewerTab = 'overview';

    this.dom = {
      grid: document.getElementById('books-grid'),
      searchInput: document.getElementById('books-search-input'),
      chips: document.querySelectorAll('.books-chip'),
      totalCountBadge: document.getElementById('books-total-count'),

      // Dedicated Viewer Modal Frame
      modalBackdrop: document.getElementById('book-viewer-modal'),
      btnCloseModal: document.getElementById('viewer-btn-close'),
      headerNumBadge: document.getElementById('viewer-book-num'),
      headerTitle: document.getElementById('viewer-book-title'),
      headerSubtitle: document.getElementById('viewer-book-subtitle'),
      tabBtns: document.querySelectorAll('.viewer-tab-btn'),
      tabPanels: document.querySelectorAll('.viewer-tab-panel'),
      
      // Panel Elements
      panelOverview: document.getElementById('viewer-panel-overview'),
      panelChapters: document.getElementById('viewer-panel-chapters'),
      panelSim: document.getElementById('viewer-panel-sim'),
      panelIframe: document.getElementById('viewer-panel-iframe'),
      iframeEl: document.getElementById('viewer-inapp-iframe'),
      externalLinkBtn: document.getElementById('viewer-btn-external')
    };
  }

  async init() {
    try {
      const res = await fetch('js/data/books.json');
      if (res.ok) {
        this.books = await res.json();
      } else {
        console.warn('books.json 로드 실패');
      }
    } catch (e) {
      console.error('도서 데이터 로드 중 예외:', e);
    }

    this.bindEvents();
    this.render();
  }

  bindEvents() {
    // 실시간 검색
    if (this.dom.searchInput) {
      this.dom.searchInput.addEventListener('input', (e) => {
        this.searchQuery = e.target.value.trim().toLowerCase();
        this.render();
      });
    }

    // 카테고리 필터 칩
    this.dom.chips.forEach(chip => {
      chip.addEventListener('click', () => {
        this.dom.chips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        this.currentCategory = chip.dataset.category || 'all';
        this.render();
      });
    });

    // 뷰어 모달 닫기
    if (this.dom.btnCloseModal) {
      this.dom.btnCloseModal.addEventListener('click', () => this.closeViewerModal());
    }
    if (this.dom.modalBackdrop) {
      this.dom.modalBackdrop.addEventListener('click', (e) => {
        if (e.target === this.dom.modalBackdrop) this.closeViewerModal();
      });
    }

    // 뷰어 탭 전환
    this.dom.tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        this.switchViewerTab(tab);
      });
    });

    // ESC 키로 뷰어 닫기
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.dom.modalBackdrop?.classList.contains('open')) {
        this.closeViewerModal();
      }
    });
  }

  getFilteredBooks() {
    return this.books.filter(b => {
      const matchCat = this.currentCategory === 'all' || b.category === this.currentCategory;
      if (!matchCat) return false;

      if (!this.searchQuery) return true;
      const titleMatch = b.title?.toLowerCase().includes(this.searchQuery);
      const subMatch = b.subtitle?.toLowerCase().includes(this.searchQuery);
      const descMatch = b.desc?.toLowerCase().includes(this.searchQuery);
      const idMatch = b.bookNumber?.toLowerCase().includes(this.searchQuery);

      return titleMatch || subMatch || descMatch || idMatch;
    });
  }

  render() {
    if (!this.dom.grid) return;
    this.dom.grid.innerHTML = '';

    const filtered = this.getFilteredBooks();

    if (this.dom.totalCountBadge) {
      this.dom.totalCountBadge.textContent = `총 ${filtered.length}종 수록`;
    }

    if (filtered.length === 0) {
      this.dom.grid.innerHTML = `
        <div class="books-empty-state">
          <div style="font-size:2.5rem; margin-bottom:0.75rem;">🔍</div>
          <h3>검색 조건에 맞는 위키북스 기술서적이 없습니다.</h3>
          <p style="margin-top:0.35rem; font-size:0.9rem;">도서 번호(예: 21911) 또는 키워드로 다시 검색해보세요.</p>
        </div>
      `;
      return;
    }

    filtered.forEach(b => {
      const card = document.createElement('article');
      card.className = `book-tech-card ${b.isLatest ? 'latest-border' : ''}`;
      
      const topicsHtml = (b.topics || []).map(t => `<span class="book-topic-tag">#${t}</span>`).join('');

      card.innerHTML = `
        <div>
          <div class="book-card-top">
            <span class="book-badge-num">${b.bookNumber}</span>
            ${b.isLatest ? '<span class="book-badge-latest">✨ 최신간</span>' : ''}
          </div>
          <h3 class="book-card-title">${b.title}</h3>
          <div class="book-card-subtitle">${b.subtitle}</div>
          <p class="book-card-desc">${b.desc}</p>
          <div class="book-topics-row">${topicsHtml}</div>
        </div>

        <div class="book-card-actions">
          <button class="btn-book-action secondary btn-open-viewer" data-id="${b.id}">
            <span>📘</span> <span>전용관 열람 (목차/원문)</span>
          </button>
          <a href="${b.simUrl}" class="btn-book-action primary" onclick="event.stopPropagation();">
            <span>${b.simLabel}</span>
          </a>
        </div>
      `;

      // 카드 클릭 시 DMDG 전용관 틀 오픈
      card.addEventListener('click', () => this.openViewerModal(b));
      card.querySelector('.btn-open-viewer')?.addEventListener('click', (e) => {
        e.stopPropagation();
        this.openViewerModal(b);
      });

      this.dom.grid.appendChild(card);
    });
  }

  openViewerModal(book) {
    this.selectedBook = book;
    if (!this.dom.modalBackdrop) return;

    if (this.dom.headerNumBadge) this.dom.headerNumBadge.textContent = book.bookNumber;
    if (this.dom.headerTitle) this.dom.headerTitle.textContent = book.title;
    if (this.dom.headerSubtitle) this.dom.headerSubtitle.textContent = book.subtitle;

    // 외부 링크 버튼 갱신
    if (this.dom.externalLinkBtn) {
      this.dom.externalLinkBtn.href = book.wikidocsUrl;
    }

    // 1. 도서 개요 렌더링
    if (this.dom.panelOverview) {
      this.dom.panelOverview.innerHTML = `
        <div style="background:linear-gradient(135deg, rgba(0,168,150,0.08), rgba(11,27,61,0.04)); padding:1.5rem; border-radius:14px; border:1px solid rgba(0,168,150,0.2); margin-bottom:1.5rem;">
          <h4 style="font-size:1.1rem; font-weight:800; color:#0B1B3D; margin-bottom:0.5rem;">${book.title}</h4>
          <p style="font-size:0.95rem; color:#475569; line-height:1.7;">${book.desc}</p>
          <div style="margin-top:1rem; display:flex; gap:0.5rem; flex-wrap:wrap;">
            ${(book.topics || []).map(t => `<span style="font-size:0.8rem; background:#FFFFFF; color:#00A896; border:1px solid rgba(0,168,150,0.3); padding:3px 10px; border-radius:6px; font-weight:700;"># ${t}</span>`).join('')}
          </div>
        </div>

        <h4 style="font-size:1rem; font-weight:800; color:#0B1B3D; margin-bottom:0.75rem;">📑 수록 파트(PART) 및 핵심 로드맵</h4>
        <div class="viewer-chapter-list">
          ${(book.parts || book.chapters || []).map(ch => `
            <div class="viewer-chapter-item">
              <div class="viewer-chapter-header">
                <span class="viewer-chapter-num">${ch.num}</span>
                <span class="viewer-chapter-title">${ch.title}</span>
              </div>
              <p class="viewer-chapter-desc">${ch.desc}</p>
            </div>
          `).join('')}
        </div>
      `;
    }

    // 2. 시뮬레이터 연동 탭 렌더링
    if (this.dom.panelSim) {
      this.dom.panelSim.innerHTML = `
        <div style="text-align:center; padding:2rem 1rem;">
          <div style="font-size:3rem; margin-bottom:1rem;">🧪</div>
          <h3 style="font-size:1.3rem; font-weight:800; color:#0B1B3D; margin-bottom:0.5rem;">${book.title} 전용 인터랙티브 실습</h3>
          <p style="font-size:0.95rem; color:#64748B; max-width:540px; margin:0 auto 1.5rem;">
            이론으로 배운 내용을 브라우저에서 직접 파라미터를 조작하며 실시간 수렴 곡선과 그래프를 눈으로 확인하세요.
          </p>
          <a href="${book.simUrl}" class="btn-book-action primary" style="max-width:280px; margin:0 auto; padding:0.85rem 1.5rem; font-size:0.95rem;">
            <span>${book.simLabel} 즉시 실행 🚀</span>
          </a>
        </div>
      `;
    }

    // 3. 인앱 원문 뷰어 (iframe) 갱신
    if (this.dom.iframeEl) {
      this.dom.iframeEl.src = book.wikidocsUrl;
    }

    this.switchViewerTab('overview');
    this.dom.modalBackdrop.classList.add('open');
  }

  closeViewerModal() {
    if (!this.dom.modalBackdrop) return;
    this.dom.modalBackdrop.classList.remove('open');
    if (this.dom.iframeEl) {
      this.dom.iframeEl.src = 'about:blank'; // 메모리 정리
    }
  }

  switchViewerTab(tabName) {
    this.activeViewerTab = tabName;

    this.dom.tabBtns.forEach(btn => {
      if (btn.dataset.tab === tabName) btn.classList.add('active');
      else btn.classList.remove('active');
    });

    this.dom.tabPanels.forEach(panel => {
      if (panel.id === `viewer-panel-${tabName}`) panel.classList.add('active');
      else panel.classList.remove('active');
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const app = new BooksApp();
  app.init();
});
