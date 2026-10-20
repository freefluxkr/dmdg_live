/**
 * DMDG LIVE - Official Master Portal Hub Client Logic
 * Layout: Mockup 1 Backdrop + Mockup 3 Dashboard
 * Features: Live Real-time Card Search, Keyboard Shortcuts ('/' to search, 'Esc' to clear)
 */

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('liveSearchInput');
  const allCards = document.querySelectorAll('.app-item-card, .sim-item-card, .book-card-item');

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.trim().toLowerCase();
      allCards.forEach(card => {
        const keyword = (card.dataset.keyword || '').toLowerCase();
        const text = card.textContent.toLowerCase();
        if (!q || keyword.includes(q) || text.includes(q)) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });

    window.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== searchInput) {
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
      }
      if (e.key === 'Escape' && document.activeElement === searchInput) {
        searchInput.value = '';
        searchInput.dispatchEvent(new Event('input'));
        searchInput.blur();
      }
    });
  }
});
