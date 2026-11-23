/**
 * ==============================================================================
 * DMDG 스튜디오 E-Book & 오디오북 - 코어 리더기 모듈
 * 파일명: js/reader/reader-core.js
 * ==============================================================================
 */

export class ReaderCore {
  constructor(options = {}) {
    this.novels = [];
    this.currentNovel = null;
    this.currentChapterIdx = 0;
    
    // 테마 설정
    this.themes = ['theme-dark', 'theme-sepia', 'theme-light', 'theme-oled'];
    this.themeNames = ['다크', '세피아', '라이트', 'OLED'];
    this.themeIcons = ['🌙', '📜', '☀️', '⚫'];
    this.themeIndex = 0;
    
    // 폰트 크기
    this.fontSize = 18; // px
    
    // 콜백 함수들
    this.onChapterChange = options.onChapterChange || (() => {});
    this.onViewChange = options.onViewChange || (() => {});
    
    this.initStorage();
  }

  initStorage() {
    try {
      const savedTheme = localStorage.getItem('dmdg_novel_theme');
      if (savedTheme) {
        const idx = this.themes.indexOf(savedTheme);
        if (idx !== -1) {
          this.themeIndex = idx;
          this.applyTheme(this.themes[idx]);
        }
      }

      const savedFontSize = localStorage.getItem('dmdg_novel_fontsize');
      if (savedFontSize) {
        this.fontSize = parseInt(savedFontSize, 10);
        document.documentElement.style.setProperty('--reader-font-size', `${this.fontSize}px`);
      }
    } catch (e) {
      console.warn('LocalStorage access restricted:', e);
    }
  }

  setNovels(novelsList) {
    this.novels = novelsList;
  }

  toggleTheme() {
    this.themeIndex = (this.themeIndex + 1) % this.themes.length;
    const themeClass = this.themes[this.themeIndex];
    this.applyTheme(themeClass);
    try {
      localStorage.setItem('dmdg_novel_theme', themeClass);
    } catch (e) {}
    return {
      name: this.themeNames[this.themeIndex],
      icon: this.themeIcons[this.themeIndex],
      theme: themeClass
    };
  }

  applyTheme(themeClass) {
    document.body.classList.remove('theme-dark', 'theme-sepia', 'theme-light', 'theme-oled');
    if (themeClass !== 'theme-dark') {
      document.body.classList.add(themeClass);
    }
  }

  changeFontSize(delta) {
    this.fontSize = Math.min(28, Math.max(14, this.fontSize + delta));
    document.documentElement.style.setProperty('--reader-font-size', `${this.fontSize}px`);
    try {
      localStorage.setItem('dmdg_novel_fontsize', this.fontSize);
    } catch (e) {}
    return this.fontSize;
  }

  openNovel(novelId, chapterIdx = 0) {
    const novel = this.novels.find(n => n.id === novelId);
    if (!novel) return null;

    this.currentNovel = novel;
    
    // 마지막 읽던 위치 복원 시도
    if (chapterIdx === null || chapterIdx === undefined) {
      try {
        const lastIdx = localStorage.getItem(`dmdg_novel_last_${novelId}`);
        chapterIdx = lastIdx ? parseInt(lastIdx, 10) : 0;
      } catch (e) {
        chapterIdx = 0;
      }
    }

    this.loadChapter(chapterIdx);
    return this.currentNovel;
  }

  loadChapter(chapterIdx) {
    if (!this.currentNovel || !this.currentNovel.chapters) return null;
    
    if (chapterIdx < 0) chapterIdx = 0;
    if (chapterIdx >= this.currentNovel.chapters.length) {
      chapterIdx = this.currentNovel.chapters.length - 1;
    }

    this.currentChapterIdx = chapterIdx;
    const chapter = this.currentNovel.chapters[chapterIdx];

    // 읽던 위치 저장
    try {
      localStorage.setItem(`dmdg_novel_last_${this.currentNovel.id}`, chapterIdx);
    } catch (e) {}

    const parsedHtml = this.parseMarkdownToHtml(chapter.content);

    this.onChapterChange({
      novel: this.currentNovel,
      chapter: chapter,
      chapterIdx: chapterIdx,
      totalChapters: this.currentNovel.chapters.length,
      htmlContent: parsedHtml
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });
    return chapter;
  }

  parseMarkdownToHtml(md) {
    if (!md) return '';

    let html = md.replace(/\r\n/g, '\n');

    // Code blocks
    html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');

    // Horizontal Rule
    html = html.replace(/^---$/gm, '<hr>');

    // Headers
    html = html.replace(/^### (.*$)/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gm, '<h1>$1</h1>');

    // Blockquotes
    html = html.replace(/^> (.*$)/gm, '<blockquote>$1</blockquote>');

    // Bold & Italic
    html = html.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Dialogue styling (따옴표로 시작하는 대사)
    html = html.replace(/^("[^"]+")/gm, '<p class="novel-dialogue">$1</p>');

    // Paragraphs
    const blocks = html.split(/\n{2,}/);
    html = blocks.map(b => {
      b = b.trim();
      if (!b) return '';
      if (b.startsWith('<h') || b.startsWith('<pre') || b.startsWith('<hr') || b.startsWith('<blockquote') || b.startsWith('<p')) {
        return b;
      }
      return `<p>${b.replace(/\n/g, '<br>')}</p>`;
    }).join('\n');

    return html;
  }
}
