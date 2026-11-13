/**
 * dmdg_paywall_notice.js
 * DMDG 전 서비스 접속 시 2027.01.01 전면 유료화 전환 예고 & OTT형 3대 정책 안내 팝업
 * - 2026.12.31까지 전 서비스 100% 무료 제공
 * - 유료화 3대 정책: 기간 한정(만료토큰+Signed URL+워터마킹) / 완전 소유(워터마킹) / 정기 구독(워터마킹)
 * - "오늘 하루 동안 보지 않기" 체크박스 (당일 23:59:59까지 localStorage 억제)
 */
(function (global) {
  'use strict';

  const STORAGE_KEY = 'dmdg_paywall_notice_hide_until';

  function getEndOfTodayMs() {
    const now = new Date();
    const end = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59, 999);
    return end.getTime();
  }

  function shouldShowNotice() {
    try {
      const hideUntil = Number(localStorage.getItem(STORAGE_KEY) || '0');
      return Date.now() > hideUntil;
    } catch (e) {
      return true;
    }
  }

  function injectStyles() {
    if (document.getElementById('dmdg-paywall-notice-style')) return;
    const style = document.createElement('style');
    style.id = 'dmdg-paywall-notice-style';
    style.textContent = `
      .dmdg-pw-backdrop {
        position: fixed;
        inset: 0;
        z-index: 99990;
        background: rgba(2, 6, 23, 0.78);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        display: none;
        align-items: center;
        justify-content: center;
        padding: 16px;
        font-family: 'Pretendard', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
      }
      .dmdg-pw-backdrop.active {
        display: flex;
        animation: dmdgPwFadeIn 0.25s ease-out;
      }
      @keyframes dmdgPwFadeIn {
        from { opacity: 0; transform: scale(0.97); }
        to { opacity: 1; transform: scale(1); }
      }
      .dmdg-pw-modal {
        width: 100%;
        max-width: 640px;
        max-height: 90vh;
        overflow-y: auto;
        background: linear-gradient(155deg, #0f172a 0%, #1e293b 100%);
        border: 1.5px solid rgba(56, 189, 248, 0.42);
        border-radius: 22px;
        box-shadow: 0 28px 60px -12px rgba(0, 0, 0, 0.75);
        color: #f8fafc;
        padding: 28px 26px 22px;
        position: relative;
      }
      .dmdg-pw-close {
        position: absolute;
        top: 16px;
        right: 18px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.14);
        color: #cbd5e1;
        width: 34px;
        height: 34px;
        border-radius: 999px;
        font-size: 18px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .dmdg-pw-close:hover { background: rgba(255, 255, 255, 0.18); color: #fff; }
      .dmdg-pw-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 12px;
      }
      .dmdg-pw-badge-free {
        background: rgba(16, 185, 129, 0.18);
        border: 1px solid rgba(16, 185, 129, 0.5);
        color: #34d399;
        font-size: 11.5px;
        font-weight: 800;
        padding: 4px 11px;
        border-radius: 999px;
      }
      .dmdg-pw-badge-paid {
        background: rgba(245, 158, 11, 0.18);
        border: 1px solid rgba(245, 158, 11, 0.5);
        color: #fbbf24;
        font-size: 11.5px;
        font-weight: 800;
        padding: 4px 11px;
        border-radius: 999px;
      }
      .dmdg-pw-title {
        font-size: 20px;
        font-weight: 900;
        margin: 0 0 8px 0;
        line-height: 1.35;
        color: #ffffff;
      }
      .dmdg-pw-lead {
        font-size: 13.5px;
        color: #cbd5e1;
        line-height: 1.65;
        margin: 0 0 18px 0;
        background: rgba(15, 23, 42, 0.55);
        border-left: 3.5px solid #38bdf8;
        padding: 10px 14px;
        border-radius: 8px;
      }
      .dmdg-pw-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-bottom: 18px;
      }
      @media (max-width: 600px) {
        .dmdg-pw-grid { grid-template-columns: 1fr; }
        .dmdg-pw-modal { padding: 22px 18px 18px; }
      }
      .dmdg-pw-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 14px;
        padding: 13px 12px;
        display: flex;
        flex-direction: column;
        gap: 6px;
      }
      .dmdg-pw-card-title {
        font-size: 13px;
        font-weight: 800;
        color: #38bdf8;
      }
      .dmdg-pw-card-desc {
        font-size: 12px;
        color: #cbd5e1;
        line-height: 1.5;
      }
      .dmdg-pw-sec-tag {
        margin-top: auto;
        font-size: 11px;
        font-weight: 700;
        color: #fbbf24;
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid rgba(245, 158, 11, 0.28);
        padding: 5px 8px;
        border-radius: 8px;
        line-height: 1.4;
      }
      .dmdg-pw-footer {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        border-top: 1px solid rgba(148, 163, 184, 0.18);
        padding-top: 14px;
      }
      .dmdg-pw-check-label {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: #e2e8f0;
        cursor: pointer;
        user-select: none;
      }
      .dmdg-pw-check-label input[type="checkbox"] {
        width: 17px;
        height: 17px;
        accent-color: #38bdf8;
        cursor: pointer;
      }
      .dmdg-pw-btn-ok {
        background: linear-gradient(135deg, #0284c7, #2563eb);
        color: #ffffff;
        border: none;
        padding: 10px 22px;
        border-radius: 10px;
        font-size: 13.5px;
        font-weight: 800;
        cursor: pointer;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);
      }
      .dmdg-pw-btn-ok:hover { filter: brightness(1.1); }
    `;
    document.head.appendChild(style);
  }

  function buildModal() {
    if (document.getElementById('dmdg-paywall-notice-backdrop')) return;
    injectStyles();

    const backdrop = document.createElement('div');
    backdrop.id = 'dmdg-paywall-notice-backdrop';
    backdrop.className = 'dmdg-pw-backdrop';
    backdrop.innerHTML = `
      <div class="dmdg-pw-modal" role="dialog" aria-modal="true" aria-labelledby="dmdg-pw-title">
        <button type="button" class="dmdg-pw-close" id="dmdg-pw-close-x" aria-label="닫기">&times;</button>
        <div class="dmdg-pw-badges">
          <span class="dmdg-pw-badge-free">🎁 ~2026. 12. 31까지 전 서비스 100% 무료 제공</span>
          <span class="dmdg-pw-badge-paid">📅 2027. 01. 01 전면 유료화 전환</span>
        </div>
        <h2 class="dmdg-pw-title" id="dmdg-pw-title">DMDG 서비스 정책 개편 및 2027 유료화 전환 안내</h2>
        <p class="dmdg-pw-lead">
          당목담글(DMDG)의 모든 웹앱·시뮬레이터·AI 도서·팩션 서재 콘텐츠는 <strong>2026년 12월 31일까지 무료</strong>로 제공되며,
          <strong>2027년 1월 1일부터</strong> OTT형 3대 이용 정책과 콘텐츠 보안 아키텍처를 적용한 전면 유료 서비스로 전환됩니다.
        </p>
        <div class="dmdg-pw-grid">
          <div class="dmdg-pw-card">
            <div class="dmdg-pw-card-title">1️⃣ 기간 한정 (OTT형)</div>
            <div class="dmdg-pw-card-desc">단기 열람권·스트리밍 전용 이용 모델 (24시간/7일/30일)</div>
            <div class="dmdg-pw-sec-tag">🛡️ 만료 토큰 + Signed URL + 눈에 안 보이는 워터마킹</div>
          </div>
          <div class="dmdg-pw-card">
            <div class="dmdg-pw-card-title">2️⃣ 완전 소유 (영구 소장)</div>
            <div class="dmdg-pw-card-desc">PDF 단행본·실습 코드·오디오북 영구 소장 다운로드</div>
            <div class="dmdg-pw-sec-tag">🛡️ 눈에 안 보이는 워터마킹 (구매자 식별 각인)</div>
          </div>
          <div class="dmdg-pw-card">
            <div class="dmdg-pw-card-title">3️⃣ 정기 구독 (멤버십)</div>
            <div class="dmdg-pw-card-desc">월간·연간 구독으로 전 서비스 무제한 열람 및 이용</div>
            <div class="dmdg-pw-sec-tag">🛡️ 눈에 안 보이는 워터마킹 (구독자 세션 각인)</div>
          </div>
        </div>
        <div class="dmdg-pw-footer">
          <label class="dmdg-pw-check-label">
            <input type="checkbox" id="dmdg-paywall-hide-today" />
            <span>오늘 하루 동안 보지 않기</span>
          </label>
          <button type="button" class="dmdg-pw-btn-ok" id="dmdg-pw-confirm-btn">무료로 계속 이용하기</button>
        </div>
      </div>
    `;
    document.body.appendChild(backdrop);

    const closeHandler = () => closeNotice();
    document.getElementById('dmdg-pw-close-x').addEventListener('click', closeHandler);
    document.getElementById('dmdg-pw-confirm-btn').addEventListener('click', closeHandler);
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) closeHandler();
    });
  }

  function openNotice(force = false) {
    if (!force && !shouldShowNotice()) return;
    buildModal();
    const backdrop = document.getElementById('dmdg-paywall-notice-backdrop');
    if (backdrop) backdrop.classList.add('active');
  }

  function closeNotice() {
    const chk = document.getElementById('dmdg-paywall-hide-today');
    if (chk && chk.checked) {
      try {
        localStorage.setItem(STORAGE_KEY, String(getEndOfTodayMs()));
      } catch (e) {}
    }
    const backdrop = document.getElementById('dmdg-paywall-notice-backdrop');
    if (backdrop) backdrop.classList.remove('active');
  }

  global.DMDG_PaywallNotice = {
    open: openNotice,
    close: closeNotice,
    shouldShow: shouldShowNotice,
    reset: () => localStorage.removeItem(STORAGE_KEY)
  };

  if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(() => openNotice(false), 350);
    });
  }
})(typeof window !== 'undefined' ? window : globalThis);

