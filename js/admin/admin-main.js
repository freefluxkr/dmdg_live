/**
 * ==============================================================================
 * DMDG 관리자 콘솔 - 메인 오케스트레이터 모듈
 * 파일명: js/admin/admin-main.js
 * ==============================================================================
 */

import { AdminAuth } from './admin-auth.js';
import { TabOverview } from './tab-overview.js';
import { TabRevenue } from './tab-revenue.js';
import { TabContent } from './tab-content.js';
import { TabAssessment } from './tab-assessment.js';

class AdminApp {
  constructor() {
    this.auth = new AdminAuth();
    this.tabOverview = new TabOverview();
    this.tabRevenue = new TabRevenue();
    this.tabContent = new TabContent();
    this.tabAssessment = new TabAssessment();
    
    this.currentTab = 'overview';
  }

  init() {
    this.auth.init();

    // 전역 스코프 바인딩 (인라인 이벤트 호환용)
    window.handleAdminLogin = (e) => {
      const id = document.getElementById('loginAdminId')?.value.trim();
      const pw = document.getElementById('loginAdminPw')?.value.trim();
      if (this.auth.login(id, pw)) {
        this.initActiveTab();
      }
    };

    window.revealDashboard = () => {
      this.auth.quickAccess();
      this.initActiveTab();
    };

    window.handleAdminLogout = () => {
      this.auth.logout();
    };

    window.switchStudioTab = (tabName) => {
      this.switchTab(tabName);
    };

    this.bindTabButtons();

    // 초기 탭 활성화
    if (this.auth.isAuthenticated()) {
      this.initActiveTab();
    }

    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      window.lucide.createIcons();
    }
  }

  bindTabButtons() {
    const tabs = ['overview', 'revenue', 'content', 'assessment'];
    tabs.forEach(t => {
      const btn = document.getElementById(`tab-btn-${t}`);
      if (btn) {
        btn.addEventListener('click', () => this.switchTab(t));
      }
    });
  }

  switchTab(tabName) {
    this.currentTab = tabName;

    // 1. 탭 버튼 스타일 갱신
    const tabs = ['overview', 'revenue', 'content', 'assessment'];
    tabs.forEach(t => {
      const btn = document.getElementById(`tab-btn-${t}`);
      const panel = document.getElementById(`panel-${t}`);

      if (btn) {
        if (t === tabName) {
          btn.classList.add('active', 'text-amber-400', 'border-amber-500');
          btn.classList.remove('text-slate-400', 'border-transparent');
        } else {
          btn.classList.remove('active', 'text-amber-400', 'border-amber-500');
          btn.classList.add('text-slate-400', 'border-transparent');
        }
      }

      if (panel) {
        if (t === tabName) {
          panel.classList.add('active');
        } else {
          panel.classList.remove('active');
        }
      }
    });

    this.initActiveTab();

    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      window.lucide.createIcons();
    }
  }

  initActiveTab() {
    if (this.currentTab === 'overview') {
      this.tabOverview.init();
    } else if (this.currentTab === 'revenue') {
      this.tabRevenue.init();
    } else if (this.currentTab === 'content') {
      this.tabContent.init();
    } else if (this.currentTab === 'assessment') {
      this.tabAssessment.init();
    }
  }
}

// 부트스트랩
document.addEventListener('DOMContentLoaded', () => {
  const app = new AdminApp();
  app.init();
});
