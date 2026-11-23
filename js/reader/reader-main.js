/**
 * ==============================================================================
 * DMDG 스튜디오 E-Book & 오디오북 - 메인 컨트롤러 모듈
 * 파일명: js/reader/reader-main.js
 * ==============================================================================
 */

import { ReaderTTS } from './reader-tts.js';
import { ReaderCore } from './reader-core.js';

class NovelsApp {
  constructor() {
    this.novels = [];
    this.core = null;
    this.tts = null;
    this.currentFilter = 'all';

    this.dom = {
      bookshelfView: document.getElementById('bookshelf-view'),
      readerView: document.getElementById('reader-view'),
      booksGrid: document.getElementById('books-grid-container'),
      progressBar: document.getElementById('reader-progress'),
      
      // Header
      btnHome: document.getElementById('btn-home'),
      btnThemeToggle: document.getElementById('btn-theme-toggle'),
      themeIcon: document.getElementById('theme-icon'),
      themeLabel: document.getElementById('theme-label'),
      langSelect: document.getElementById('reader-lang-select'),
      btnFullscreen: document.getElementById('btn-fullscreen'),
      
      // Filter Chips
      filterChips: document.querySelectorAll('.filter-chip'),

      // Reader Elements
      btnBackToShelf: document.getElementById('btn-back-to-shelf'),
      btnToggleToc: document.getElementById('btn-toggle-toc'),
      readerBookTitle: document.getElementById('reader-book-title'),
      readerChapterTitle: document.getElementById('reader-chapter-title'),
      readerContent: document.getElementById('reader-content'),
      
      // Reader Controls
      btnFontDec: document.getElementById('btn-font-dec'),
      btnFontInc: document.getElementById('btn-font-inc'),
      btnTtsPlay: document.getElementById('btn-tts-play'),
      ttsIcon: document.getElementById('tts-icon'),
      ttsText: document.getElementById('tts-text'),
      btnTtsSpeed: document.getElementById('btn-tts-speed'),
      ttsPulse: document.getElementById('tts-pulse'),
      ttsStatusDesc: document.getElementById('tts-status-desc'),

      // Bottom Navigation
      btnPrevChapter: document.getElementById('btn-prev-chapter'),
      btnScrollTop: document.getElementById('btn-scroll-top'),
      btnNextChapter: document.getElementById('btn-next-chapter'),

      // Table of Contents Drawer
      tocDrawer: document.getElementById('toc-drawer'),
      drawerBackdrop: document.getElementById('drawer-backdrop'),
      btnCloseToc: document.getElementById('btn-close-toc'),
      tocBookTitle: document.getElementById('toc-drawer-book-title'),
      tocList: document.getElementById('toc-items-list')
    };
  }

  async init() {
    try {
      // 1. 순수 문학 소설 JSON 비동기 로드
      const res = await fetch('js/data/novels.json');
      if (res.ok) {
        this.novels = await res.json();
      } else {
        console.warn('novels.json 로드 실패, window.NOVELS_DATA 폴백 확인');
        this.novels = (window.NOVELS_DATA || []).filter(n => !n.wikidocsUrl);
      }
    } catch (e) {
      console.warn('데이터 로드 예외 발생:', e);
      this.novels = (window.NOVELS_DATA || []).filter(n => !n.wikidocsUrl);
    }

    // 2. 코어 및 TTS 모듈 인스턴스화
    this.core = new ReaderCore({
      onChapterChange: (data) => this.handleChapterRender(data)
    });
    this.core.setNovels(this.novels);

    this.tts = new ReaderTTS({
      defaultLang: this.dom.langSelect ? this.dom.langSelect.value : 'ko-KR',
      onStateChange: (state) => this.handleTtsState(state),
      onParagraphHighlight: (pEl) => this.handleParagraphHighlight(pEl)
    });

    // 3. UI 및 이벤트 바인딩
    this.bindEvents();
    this.renderBookshelf('all');
  }

  bindEvents() {
    // 테마 토글
    if (this.dom.btnThemeToggle) {
      this.dom.btnThemeToggle.addEventListener('click', () => {
        const info = this.core.toggleTheme();
        if (this.dom.themeIcon) this.dom.themeIcon.textContent = info.icon;
        if (this.dom.themeLabel) this.dom.themeLabel.textContent = info.name;
      });
    }

    // 언어 선택 (6개 국어)
    if (this.dom.langSelect) {
      this.dom.langSelect.addEventListener('change', (e) => {
        this.tts.setLanguage(e.target.value);
      });
    }

    // 전체화면 토글
    if (this.dom.btnFullscreen) {
      this.dom.btnFullscreen.addEventListener('click', () => {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(() => {});
        } else {
          document.exitFullscreen().catch(() => {});
        }
      });
    }

    // 필터 칩
    this.dom.filterChips.forEach(chip => {
      chip.addEventListener('click', () => {
        this.dom.filterChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        this.currentFilter = chip.dataset.filter || 'all';
        this.renderBookshelf(this.currentFilter);
      });
    });

    // 책장으로 돌아가기
    if (this.dom.btnBackToShelf) {
      this.dom.btnBackToShelf.addEventListener('click', () => this.closeReader());
    }
    if (this.dom.btnHome) {
      this.dom.btnHome.addEventListener('click', () => this.closeReader());
    }

    // 목차 열기/닫기
    if (this.dom.btnToggleToc) {
      this.dom.btnToggleToc.addEventListener('click', () => this.openToc());
    }
    if (this.dom.btnCloseToc) {
      this.dom.btnCloseToc.addEventListener('click', () => this.closeToc());
    }
    if (this.dom.drawerBackdrop) {
      this.dom.drawerBackdrop.addEventListener('click', () => this.closeToc());
    }

    // 글자 크기
    if (this.dom.btnFontDec) {
      this.dom.btnFontDec.addEventListener('click', () => this.core.changeFontSize(-2));
    }
    if (this.dom.btnFontInc) {
      this.dom.btnFontInc.addEventListener('click', () => this.core.changeFontSize(2));
    }

    // TTS 컨트롤
    if (this.dom.btnTtsPlay) {
      this.dom.btnTtsPlay.addEventListener('click', () => this.tts.togglePlay());
    }
    if (this.dom.btnTtsSpeed) {
      this.dom.btnTtsSpeed.addEventListener('click', () => {
        const speed = this.tts.cycleSpeed();
        this.dom.btnTtsSpeed.textContent = `${speed.toFixed(1)}x`;
      });
    }

    // 이전/다음 챕터
    if (this.dom.btnPrevChapter) {
      this.dom.btnPrevChapter.addEventListener('click', () => {
        this.tts.stop();
        this.core.loadChapter(this.core.currentChapterIdx - 1);
      });
    }
    if (this.dom.btnNextChapter) {
      this.dom.btnNextChapter.addEventListener('click', () => {
        this.tts.stop();
        this.core.loadChapter(this.core.currentChapterIdx + 1);
      });
    }
    if (this.dom.btnScrollTop) {
      this.dom.btnScrollTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    // 스크롤 프로그레스
    window.addEventListener('scroll', () => this.updateProgressBar(), { passive: true });

    // 단축키
    window.addEventListener('keydown', (e) => {
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) return;
      if (e.key === 'Escape') {
        if (this.dom.tocDrawer.classList.contains('open')) this.closeToc();
        else if (this.dom.readerView.classList.contains('active')) this.closeReader();
      } else if (e.key === ' ' && this.dom.readerView.classList.contains('active')) {
        // 스페이스바로 TTS 재생/정지
        e.preventDefault();
        this.tts.togglePlay();
      }
    });
  }

  renderBookshelf(filter = 'all') {
    if (!this.dom.booksGrid) return;
    this.dom.booksGrid.innerHTML = '';

    const filtered = this.novels.filter(n => {
      if (filter === 'all') return true;
      if (filter === 'cypher') return n.author?.includes('Cypher') || n.persona?.includes('Cypher') || n.genre?.includes('암호학');
      if (filter === 'kmin') return n.author?.includes('K.Min') || n.persona?.includes('K.Min') || n.genre?.includes('지정학');
      if (filter === 'scifi') return n.genre?.includes('사이버') || n.category?.includes('scifi');
      return true;
    });

    filtered.forEach(novel => {
      const card = document.createElement('article');
      card.className = 'book-card';
      const c = novel.color || { from: '#1e293b', to: '#0f172a', accent: '#f59e0b', glow: 'rgba(245,158,11,0.2)' };
      card.style.setProperty('--cover-from', c.from);
      card.style.setProperty('--cover-to', c.to);
      card.style.setProperty('--card-accent', c.accent);
      card.style.setProperty('--card-glow', c.glow);

      const coverIcon = novel.id.includes('2027') ? '🔐' :
                        (novel.id.includes('sun') || novel.id.includes('태양') ? '☀️' :
                        (novel.id.includes('wolf') || novel.id.includes('늑대') ? '🐺' : '🛡️'));

      card.innerHTML = `
        <div class="book-cover">
          <div class="cover-badge-row">
            <span class="cover-badge">${novel.badge || '✨ 명작 팩션'}</span>
            <span class="cover-icon">${coverIcon}</span>
          </div>
          <div class="cover-main">
            <h3 class="cover-title">${novel.title}</h3>
            <div class="cover-author">${novel.author} (${novel.persona || 'DMDG 작가진'})</div>
          </div>
        </div>

        <div class="book-body">
          <div>
            <div class="book-subtitle">${novel.subtitle || ''}</div>
            <p class="book-synopsis">${novel.synopsis || ''}</p>
          </div>

          <div>
            <div class="book-meta">
              <span>⏱️ ${novel.readingTime || '약 60분'}</span>
              <span>📑 ${novel.chapterCount || (novel.chapters ? novel.chapters.length : 0)}개 챕터</span>
              <span>🔤 ${(novel.charCount || 40000).toLocaleString()}자</span>
            </div>
            <button class="btn-read" data-id="${novel.id}">
              <span>📖</span> <span>지금 읽기 & 낭독 듣기</span>
            </button>
          </div>
        </div>
      `;

      card.addEventListener('click', () => this.openNovel(novel.id));
      this.dom.booksGrid.appendChild(card);
    });
  }

  openNovel(novelId) {
    this.tts.stop();
    const novel = this.core.openNovel(novelId);
    if (!novel) return;

    this.dom.bookshelfView.style.display = 'none';
    this.dom.readerView.classList.add('active');
    this.renderTocList();
  }

  closeReader() {
    this.tts.stop();
    this.closeToc();
    this.dom.readerView.classList.remove('active');
    this.dom.bookshelfView.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  handleChapterRender({ novel, chapter, chapterIdx, totalChapters, htmlContent }) {
    if (this.dom.readerBookTitle) this.dom.readerBookTitle.textContent = novel.title;
    if (this.dom.readerChapterTitle) this.dom.readerChapterTitle.textContent = chapter.title || `${chapterIdx + 1}장`;
    if (this.dom.readerContent) {
      this.dom.readerContent.innerHTML = htmlContent;
      // TTS 대상 단락 등록
      const pElements = this.dom.readerContent.querySelectorAll('p');
      this.tts.setParagraphs(pElements);
    }

    if (this.dom.btnPrevChapter) {
      this.dom.btnPrevChapter.disabled = chapterIdx <= 0;
      this.dom.btnPrevChapter.style.opacity = chapterIdx <= 0 ? '0.4' : '1';
    }
    if (this.dom.btnNextChapter) {
      this.dom.btnNextChapter.disabled = chapterIdx >= totalChapters - 1;
      this.dom.btnNextChapter.style.opacity = chapterIdx >= totalChapters - 1 ? '0.4' : '1';
    }

    this.updateActiveToc(chapterIdx);
    this.updateProgressBar();
  }

  handleTtsState(state) {
    if (this.dom.ttsIcon && this.dom.ttsText) {
      if (state.isPlaying && !state.isPaused) {
        this.dom.ttsIcon.textContent = '⏸️';
        this.dom.ttsText.textContent = '일시정지';
        if (this.dom.ttsPulse) this.dom.ttsPulse.classList.add('playing');
        if (this.dom.ttsStatusDesc) {
          this.dom.ttsStatusDesc.textContent = `음성 낭독 중 (${state.paragraphIdx + 1}/${state.totalParagraphs} 문단)`;
        }
      } else {
        this.dom.ttsIcon.textContent = '▶️';
        this.dom.ttsText.textContent = state.isPaused ? '이어듣기' : 'AI 낭독';
        if (this.dom.ttsPulse) this.dom.ttsPulse.classList.remove('playing');
        if (this.dom.ttsStatusDesc) {
          this.dom.ttsStatusDesc.textContent = state.isPaused ? '일시 정지됨' : '6개 국어 음성 준비됨';
        }
      }
    }
  }

  handleParagraphHighlight(pEl) {
    // 기존 하이라이트 제거
    const actives = this.dom.readerContent.querySelectorAll('.tts-active-highlight');
    actives.forEach(el => el.classList.remove('tts-active-highlight'));

    if (pEl) {
      pEl.classList.add('tts-active-highlight');
    }
  }

  openToc() {
    this.dom.tocDrawer.classList.add('open');
    this.dom.drawerBackdrop.classList.add('open');
  }

  closeToc() {
    this.dom.tocDrawer.classList.remove('open');
    this.dom.drawerBackdrop.classList.remove('open');
  }

  renderTocList() {
    if (!this.core.currentNovel || !this.dom.tocList) return;
    this.dom.tocBookTitle.textContent = this.core.currentNovel.title;
    this.dom.tocList.innerHTML = '';

    this.core.currentNovel.chapters.forEach((ch, idx) => {
      const li = document.createElement('li');
      li.className = 'toc-item';
      li.dataset.idx = idx;
      li.innerHTML = `
        <span>${ch.title}</span>
        <span style="font-size:0.75rem; color:var(--text-muted);">${idx + 1}</span>
      `;
      li.addEventListener('click', () => {
        this.tts.stop();
        this.core.loadChapter(idx);
        this.closeToc();
      });
      this.dom.tocList.appendChild(li);
    });

    this.updateActiveToc(this.core.currentChapterIdx);
  }

  updateActiveToc(activeIdx) {
    if (!this.dom.tocList) return;
    const items = this.dom.tocList.querySelectorAll('.toc-item');
    items.forEach((item, idx) => {
      if (idx === activeIdx) item.classList.add('active');
      else item.classList.remove('active');
    });
  }

  updateProgressBar() {
    if (!this.dom.progressBar) return;
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = scrollHeight > 0 ? Math.min(100, Math.max(0, (scrollTop / scrollHeight) * 100)) : 0;
    this.dom.progressBar.style.width = `${pct}%`;
  }
}

// 애플리케이션 시작
document.addEventListener('DOMContentLoaded', () => {
  const app = new NovelsApp();
  app.init();
});
