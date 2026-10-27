/**
 * ==============================================================================
 * MALSSAM (https://malssam.com) Anti-Scraping & IP Shield Engine
 * Author: DMDG Great AI Engineering Team
 * Features:
 *   1. Anti-Headless (Selenium, Puppeteer, Playwright Bot Detection)
 *   2. Anti-Copy, Anti-Drag, Anti-RightClick Contextmenu Guard
 *   3. Anti-DevTools & Source Inspection Keyboard Shortcuts (F12, Ctrl+U, etc.)
 *   4. Dynamic Security Toast Notification
 * ==============================================================================
 */

(function () {
  'use strict';

  // ── 1. Anti-Headless & Automated Scraping Bot Detection ─────────────────────
  function detectHeadlessBrowser() {
    // 로컬 개발 환경(file:, localhost, 127.0.0.1) 또는 관리자 페이지는 패스
    if (window.location && (
      window.location.protocol === 'file:' || 
      window.location.hostname === 'localhost' || 
      window.location.hostname === '127.0.0.1' ||
      (window.location.pathname && window.location.pathname.includes('admin'))
    )) {
      return;
    }

    // 모바일 기기(Android, iOS, Samsung Internet 등)는 플러그인이 없는 모바일 표준 브라우저이므로 차단 면제
    const isMobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile|SamsungBrowser/i.test(navigator.userAgent || '');
    if (isMobileDevice) {
      return;
    }

    // 명시적인 Selenium / Puppeteer / PhantomJS 자동화 환경만 안전하게 식별
    const isHeadless = !!(
      navigator.webdriver === true ||
      window.__webdriver_evaluate ||
      window.__selenium_evaluate ||
      window.__webdriver_script_fn ||
      document.__selenium_unwrapped ||
      document.__webdriver_evaluate ||
      window.callPhantom ||
      window._phantom
    );

    if (isHeadless) {
      console.warn('[MALSSAM Shield] Automated scraping environment detected.');
      const blockUI = function () {
        document.body.innerHTML = `
          <div style="position:fixed;inset:0;background:#0b0f17;color:#f1f5f9;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:-apple-system,BlinkMacSystemFont,Pretendard,sans-serif;text-align:center;padding:24px;z-index:999999;">
            <div style="font-size:48px;margin-bottom:16px;">🛡️</div>
            <h1 style="font-size:24px;font-weight:800;color:#f59e0b;margin-bottom:8px;">비정상 자동화 접근 차단</h1>
            <p style="font-size:14px;color:#94a3b8;max-width:420px;line-height:1.6;margin-bottom:24px;">
              말쌈(MALSSAM) 저작권 보호 시스템에 의해 자동화 스크래퍼(Selenium, Puppeteer 등) 환경의 접근이 제한되었습니다.<br>
              일반 웹 브라우저(Chrome, Safari, Edge 등)를 통해 직접 접속해 주세요.
            </p>
            <a href="https://malssam.com" style="background:#f59e0b;color:#0b0f17;font-weight:700;padding:10px 20px;border-radius:10px;text-decoration:none;font-size:14px;">메인 화면으로 이동</a>
          </div>
        `;
      };
      if (document.body) {
        blockUI();
      } else {
        document.addEventListener('DOMContentLoaded', blockUI);
      }
      throw new Error('[MALSSAM Shield] Scraper access revoked.');
    }
  }

  try {
    detectHeadlessBrowser();
  } catch (err) {
    return;
  }

  // ── 2. Toast UI Notification for Security Warnings ─────────────────────────
  let toastTimeout = null;
  function showSecurityToast(msg) {
    let toast = document.getElementById('malssam-security-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'malssam-security-toast';
      toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%) translateY(20px);
        background: rgba(15, 23, 42, 0.95);
        color: #f1f5f9;
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 999px;
        padding: 10px 22px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: -0.01em;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(245, 158, 11, 0.2);
        z-index: 9999999;
        display: flex;
        align-items: center;
        gap: 8px;
        opacity: 0;
        pointer-events: none;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        font-family: -apple-system, BlinkMacSystemFont, Pretendard, sans-serif;
      `;
      document.body.appendChild(toast);
    }

    toast.innerHTML = `<span>🔒</span> <span>${msg}</span>`;
    toast.style.opacity = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';

    if (toastTimeout) clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(-50%) translateY(20px)';
    }, 2200);
  }

  // ── 3. Right Click (Context Menu) Guard ─────────────────────────────────────
  document.addEventListener('contextmenu', function (e) {
    const targetTag = (e.target && e.target.tagName ? e.target.tagName.toLowerCase() : '');
    if (targetTag === 'input' || targetTag === 'textarea') return;

    e.preventDefault();
    showSecurityToast('말쌈 신조어 사전 저작권 보호를 위해 우클릭이 제한되어 있습니다.');
    return false;
  }, true);

  // ── 4. Copy & Cut Guard ───────────────────────────────────────────────────
  document.addEventListener('copy', function (e) {
    const targetTag = (e.target && e.target.tagName ? e.target.tagName.toLowerCase() : '');
    if (targetTag === 'input' || targetTag === 'textarea') return;

    e.preventDefault();
    showSecurityToast('말쌈 신조어 DB의 무단 대량 복제 및 스크래핑은 금지되어 있습니다.');
    return false;
  }, true);

  document.addEventListener('cut', function (e) {
    const targetTag = (e.target && e.target.tagName ? e.target.tagName.toLowerCase() : '');
    if (targetTag === 'input' || targetTag === 'textarea') return;
    e.preventDefault();
    return false;
  }, true);

  // ── 5. Drag & Selection Guard ──────────────────────────────────────────────
  document.addEventListener('selectstart', function (e) {
    const targetTag = (e.target && e.target.tagName ? e.target.tagName.toLowerCase() : '');
    if (targetTag === 'input' || targetTag === 'textarea') return;
    
    // 사전 본문/정의 카드 영역 선택 차단
    if (e.target && typeof e.target.closest === 'function' && (e.target.closest('.word-card') || e.target.closest('.dict-detail') || e.target.closest('#dictionary-view'))) {
      e.preventDefault();
      return false;
    }
  }, true);

  document.addEventListener('dragstart', function (e) {
    const targetTag = (e.target && e.target.tagName ? e.target.tagName.toLowerCase() : '');
    if (targetTag === 'input' || targetTag === 'textarea') return;
    e.preventDefault();
    return false;
  }, true);

  // ── 6. DevTools & Inspection Shortcut Blocker ─────────────────────────────
  document.addEventListener('keydown', function (e) {
    const key = e.key || '';
    const keyCode = e.keyCode || e.which;
    const isCtrl = e.ctrlKey || e.metaKey;

    if (key === 'F12' || keyCode === 123) {
      e.preventDefault();
      e.stopPropagation();
      showSecurityToast('개발자 도구 진입이 제한되어 있습니다.');
      return false;
    }

    if (isCtrl && e.shiftKey && (key === 'I' || key === 'i' || key === 'J' || key === 'j' || key === 'C' || key === 'c' || keyCode === 73 || keyCode === 74 || keyCode === 67)) {
      e.preventDefault();
      e.stopPropagation();
      showSecurityToast('개발자 도구 진입이 제한되어 있습니다.');
      return false;
    }

    if (isCtrl && (key === 'u' || key === 'U' || keyCode === 85)) {
      e.preventDefault();
      e.stopPropagation();
      showSecurityToast('페이지 소스 보기가 제한되어 있습니다.');
      return false;
    }

    if (isCtrl && (key === 's' || key === 'S' || keyCode === 83)) {
      e.preventDefault();
      e.stopPropagation();
      showSecurityToast('페이지 무단 저장이 제한되어 있습니다.');
      return false;
    }

    if (isCtrl && (key === 'p' || key === 'P' || keyCode === 80)) {
      e.preventDefault();
      e.stopPropagation();
      showSecurityToast('무단 인쇄 및 저장이 제한되어 있습니다.');
      return false;
    }
  }, true);

  // ── 7. Global CSS User-Select Protection Injection ────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    const styleEl = document.createElement('style');
    styleEl.textContent = `
      .word-card, .dict-detail, #dictionary-view, .meaning-box, .etymology-box {
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
        user-select: none !important;
      }
      ::selection {
        background: transparent !important;
        color: inherit !important;
      }
    `;
    document.head.appendChild(styleEl);
  });

})();
