/**
 * ==============================================================================
 * DMDG 관리자 콘솔 - 인증 모듈
 * 파일명: js/admin/admin-auth.js
 * ==============================================================================
 */

export class AdminAuth {
  constructor() {
    this.tokenKey = 'dmdg_admin_auth_token';
    this.dom = {
      authOverlay: document.getElementById('auth-overlay'),
      dashboardContainer: document.getElementById('dashboard-container'),
      loginIdInput: document.getElementById('loginAdminId'),
      loginPwInput: document.getElementById('loginAdminPw'),
      loginErrorMsg: document.getElementById('loginErrorMsg'),
      loginErrorText: document.getElementById('loginErrorText')
    };
  }

  init() {
    // 세션 유지 여부 확인
    if (this.isAuthenticated()) {
      this.showDashboard();
    } else {
      this.showLogin();
    }
  }

  isAuthenticated() {
    try {
      return sessionStorage.getItem(this.tokenKey) === 'authenticated_dmdg_master';
    } catch (e) {
      return false;
    }
  }

  login(id, pw) {
    const validId = 'DMDG-LIVE';
    const validPw = 'qusejrwoddl';

    if (id === validId && pw === validPw) {
      try {
        sessionStorage.setItem(this.tokenKey, 'authenticated_dmdg_master');
      } catch (e) {}
      this.hideError();
      this.showDashboard();
      return true;
    } else {
      this.showError('아이디 또는 비밀번호가 일치하지 않습니다.');
      return false;
    }
  }

  quickAccess() {
    try {
      sessionStorage.setItem(this.tokenKey, 'authenticated_dmdg_master');
    } catch (e) {}
    this.hideError();
    this.showDashboard();
  }

  logout() {
    try {
      sessionStorage.removeItem(this.tokenKey);
    } catch (e) {}
    this.showLogin();
  }

  showDashboard() {
    if (this.dom.authOverlay) {
      this.dom.authOverlay.classList.add('hidden');
    }
    if (this.dom.dashboardContainer) {
      this.dom.dashboardContainer.classList.remove('hidden');
      setTimeout(() => {
        this.dom.dashboardContainer.classList.remove('opacity-0');
      }, 50);
    }
  }

  showLogin() {
    if (this.dom.dashboardContainer) {
      this.dom.dashboardContainer.classList.add('opacity-0');
      this.dom.dashboardContainer.classList.add('hidden');
    }
    if (this.dom.authOverlay) {
      this.dom.authOverlay.classList.remove('hidden');
    }
  }

  showError(msg) {
    if (this.dom.loginErrorMsg && this.dom.loginErrorText) {
      this.dom.loginErrorText.textContent = msg;
      this.dom.loginErrorMsg.classList.remove('hidden');
    }
  }

  hideError() {
    if (this.dom.loginErrorMsg) {
      this.dom.loginErrorMsg.classList.add('hidden');
    }
  }
}
