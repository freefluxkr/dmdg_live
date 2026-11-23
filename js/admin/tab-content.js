/**
 * ==============================================================================
 * DMDG 관리자 콘솔 - 탭 3: 콘텐츠 지표 & 실시간 알림 관리 (Content) 모듈
 * 파일명: js/admin/tab-content.js
 * ==============================================================================
 */

export class TabContent {
  constructor() {
    this.storageKey = 'dmdg_notifications';
    this.notifications = [];
  }

  init() {
    this.loadNotifications();
    this.renderNotificationList();
    this.bindEvents();
  }

  loadNotifications() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      if (stored) {
        this.notifications = JSON.parse(stored);
      } else {
        // 기본 샘플 알림 목록
        this.notifications = [
          {
            id: 'notif-1',
            type: 'book',
            tag: '✨ 신간 출시',
            title: '《지식 그래프 & Graph RAG 파이프라인》 완간',
            date: '2026-10-28',
            desc: 'Neo4j와 S-P-O 트리플 추출, LangGraph 멀티홉 추론을 다룬 신간이 등록되었습니다.',
            link: './books.html'
          },
          {
            id: 'notif-2',
            type: 'youtube',
            tag: '📺 영상 등록',
            title: '당목담글 공식 채널 신규 영상 공개',
            date: '2026-10-26',
            desc: '조선의 마지막 숨결, 덕수궁 석조전 미공개 다큐멘터리가 업로드되었습니다.',
            link: 'https://www.youtube.com/@dmdg-free'
          },
          {
            id: 'notif-3',
            type: 'feature',
            tag: '🚀 기능 업데이트',
            title: '말쌈 신조어 사전 718개 단어 6개 국어 지원',
            date: '2026-10-25',
            desc: '한국어뿐만 아니라 영어, 일본어, 프랑스어, 인도네시아어, 스페인어 음성 낭독이 지원됩니다.',
            link: '../malssam_app/index.html'
          }
        ];
        localStorage.setItem(this.storageKey, JSON.stringify(this.notifications));
      }
    } catch (e) {
      console.warn('알림 로드 오류:', e);
    }
  }

  saveNotifications() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.notifications));
    } catch (e) {}
  }

  bindEvents() {
    const addBtn = document.getElementById('btn-add-notification');
    if (addBtn) {
      addBtn.addEventListener('click', () => this.handleAddNewNotification());
    }
  }

  handleAddNewNotification() {
    const titleInput = document.getElementById('notif-input-title');
    const tagInput = document.getElementById('notif-input-tag');
    const descInput = document.getElementById('notif-input-desc');
    const linkInput = document.getElementById('notif-input-link');

    if (!titleInput || !descInput) return;

    const title = titleInput.value.trim();
    const tag = tagInput ? tagInput.value.trim() : '📢 공지사항';
    const desc = descInput.value.trim();
    const link = linkInput ? linkInput.value.trim() : './';

    if (!title || !desc) {
      alert('알림 제목과 내용을 모두 입력해주세요.');
      return;
    }

    const todayStr = new Date().toISOString().split('T')[0];
    const newNotif = {
      id: `notif-${Date.now()}`,
      type: 'feature',
      tag: tag || '📢 알림',
      title: title,
      date: todayStr,
      desc: desc,
      link: link || './'
    };

    this.notifications.unshift(newNotif);
    this.saveNotifications();
    this.renderNotificationList();

    // 입력창 초기화
    titleInput.value = '';
    descInput.value = '';
    if (linkInput) linkInput.value = '';
    alert('새 알림이 성공적으로 등록되었습니다. 포털 사용자에게 즉시 노출됩니다.');
  }

  deleteNotification(id) {
    if (!confirm('정말 이 알림을 삭제하시겠습니까?')) return;
    this.notifications = this.notifications.filter(n => n.id !== id);
    this.saveNotifications();
    this.renderNotificationList();
  }

  renderNotificationList() {
    const listEl = document.getElementById('admin-notif-list-container');
    if (!listEl) return;

    listEl.innerHTML = '';

    if (this.notifications.length === 0) {
      listEl.innerHTML = '<div class="text-xs text-slate-500 py-4 text-center">등록된 알림이 없습니다.</div>';
      return;
    }

    this.notifications.forEach(n => {
      const item = document.createElement('div');
      item.className = 'p-3.5 bg-slate-900/80 border border-slate-800 rounded-xl flex items-start justify-between gap-3';
      
      item.innerHTML = `
        <div class="flex-1">
          <div class="flex items-center gap-2 mb-1">
            <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/15 text-amber-400 border border-amber-500/30">${n.tag}</span>
            <span class="text-[11px] text-slate-500 font-mono">${n.date}</span>
          </div>
          <h4 class="text-xs font-bold text-white mb-0.5">${n.title}</h4>
          <p class="text-[11px] text-slate-400 line-clamp-2">${n.desc}</p>
        </div>
        <button class="btn-del-notif text-xs text-rose-400 hover:text-rose-300 p-1.5 hover:bg-rose-500/10 rounded-lg transition-colors cursor-pointer" data-id="${n.id}" title="알림 삭제">
          ✕
        </button>
      `;

      item.querySelector('.btn-del-notif').addEventListener('click', () => {
        this.deleteNotification(n.id);
      });

      listEl.appendChild(item);
    });
  }
}
