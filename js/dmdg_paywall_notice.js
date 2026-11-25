/**
 * dmdg_paywall_notice.js
 * DMDG 전 서비스 접속 시 2026.12.31 무료 종료 -> 2027.01.01 [구독 + 단건] 하이브리드 유료화 전환 예고 팝업
 * - ~2026.12.31 23:59:59까지 전 서비스 무료 제공
 * - 1. [구독 + 단건] 하이브리드 티어: Free / Single(5,000~29,000원) / Pro(월 9,900~19,900원 · 연 20~30%↓) / Team·B2B
 * - 2. 2026.12 -> 2027.01 전환 전략: 12월 얼리버드 평생 40% 할인 / VIP 초대코드(dmdg_servive) / 유료 원본 소셜 DRM
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

  function getPdfVaultUrl() {
    if (typeof window !== 'undefined' && window.location && window.location.hostname === 'library.dmdg-live.com') {
      return 'https://dmdg-live.com/pdf_vault.html';
    }
    return './pdf_vault.html';
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
        max-width: 720px;
        max-height: 92vh;
        overflow-y: auto;
        background: linear-gradient(155deg, #0f172a 0%, #1e293b 100%);
        border: 1.5px solid rgba(56, 189, 248, 0.42);
        border-radius: 22px;
        box-shadow: 0 28px 60px -12px rgba(0, 0, 0, 0.75);
        color: #f8fafc;
        padding: 26px 24px 20px;
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
        padding-right: 36px;
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
        font-size: 19.5px;
        font-weight: 900;
        margin: 0 0 8px 0;
        line-height: 1.35;
        color: #ffffff;
      }
      .dmdg-pw-lead {
        font-size: 13px;
        color: #cbd5e1;
        line-height: 1.6;
        margin: 0 0 14px 0;
        background: rgba(15, 23, 42, 0.55);
        border-left: 3.5px solid #38bdf8;
        padding: 9px 13px;
        border-radius: 8px;
      }
      .dmdg-pw-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-bottom: 14px;
      }
      @media (max-width: 620px) {
        .dmdg-pw-grid { grid-template-columns: 1fr; }
        .dmdg-pw-modal { padding: 20px 16px 16px; }
      }
      .dmdg-pw-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 14px;
        padding: 11px 12px;
        display: flex;
        flex-direction: column;
        gap: 5px;
      }
      .dmdg-pw-card.featured {
        border-color: rgba(251, 191, 36, 0.55);
        background: rgba(245, 158, 11, 0.08);
      }
      .dmdg-pw-card-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 6px;
        flex-wrap: wrap;
      }
      .dmdg-pw-card-title {
        font-size: 13px;
        font-weight: 800;
        color: #38bdf8;
      }
      .dmdg-pw-card-price {
        font-size: 11.5px;
        font-weight: 800;
        color: #fde68a;
      }
      .dmdg-pw-card-desc {
        font-size: 11.8px;
        color: #cbd5e1;
        line-height: 1.48;
      }
      .dmdg-pw-strategy {
        background: rgba(245, 158, 11, 0.10);
        border: 1px solid rgba(251, 191, 36, 0.36);
        border-radius: 12px;
        padding: 11px 13px;
        margin-bottom: 16px;
        font-size: 12px;
        color: #e2e8f0;
        line-height: 1.55;
      }
      .dmdg-pw-strategy-title {
        font-size: 12.5px;
        font-weight: 800;
        color: #fbbf24;
        margin-bottom: 5px;
      }
      .dmdg-pw-code {
        background: rgba(2, 6, 23, 0.75);
        color: #34d399;
        padding: 1px 6px;
        border-radius: 5px;
        font-family: monospace;
        font-weight: 700;
      }
      .dmdg-pw-footer {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        border-top: 1px solid rgba(148, 163, 184, 0.18);
        padding-top: 13px;
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
      .dmdg-pw-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
      }
      .dmdg-pw-btn-vault {
        background: rgba(56, 189, 248, 0.16);
        border: 1px solid rgba(56, 189, 248, 0.5);
        color: #7dd3fc;
        text-decoration: none;
        padding: 9px 15px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
      }
      .dmdg-pw-btn-vault:hover { background: rgba(56, 189, 248, 0.28); color: #fff; }
      .dmdg-pw-btn-ok {
        background: linear-gradient(135deg, #0284c7, #2563eb);
        color: #ffffff;
        border: none;
        padding: 10px 20px;
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

    const vaultUrl = getPdfVaultUrl();
    const backdrop = document.createElement('div');
    backdrop.id = 'dmdg-paywall-notice-backdrop';
    backdrop.className = 'dmdg-pw-backdrop';
    backdrop.innerHTML = `
      <div class="dmdg-pw-modal" role="dialog" aria-modal="true" aria-labelledby="dmdg-pw-title">
        <button type="button" class="dmdg-pw-close" id="dmdg-pw-close-x" aria-label="닫기">&times;</button>
        <div class="dmdg-pw-badges">
          <span class="dmdg-pw-badge-free">🎁 ~2026. 12. 31 23:59까지 무료 공개</span>
          <span class="dmdg-pw-badge-paid">📅 2027. 01. 01 전면 유료화 전환</span>
        </div>
        <h2 class="dmdg-pw-title" id="dmdg-pw-title">DMDG [구독 + 단건] 하이브리드 유료화 &amp; PDF 보안 전환 안내</h2>
        <p class="dmdg-pw-lead">
          당목담글(<strong>dmdg-live.com</strong>)의 모든 웹앱·시뮬레이터·AI 도서·PDF 자료는 <strong>2026년 12월 31일 자정(23:59)까지 무료</strong>로 제공되며,
          <strong>2027년 1월 1일부터</strong> <strong>[구독 + 단건] 하이브리드 티어</strong>로 전면 유료화됩니다.
        </p>

        <div class="dmdg-pw-grid">
          <div class="dmdg-pw-card">
            <div class="dmdg-pw-card-head">
              <span class="dmdg-pw-card-title">1. Free (무료)</span>
              <span class="dmdg-pw-card-price">0원</span>
            </div>
            <div class="dmdg-pw-card-desc">
              • <strong>~2026.12.31</strong>: 웹 뷰어 전체 열람 + 유효 샘플 다운로드<br>
              • <strong>2027.01.01~</strong>: 각 자료 앞부분(1~3p) 미리보기 + 만료 샘플 안내
            </div>
          </div>
          <div class="dmdg-pw-card">
            <div class="dmdg-pw-card-head">
              <span class="dmdg-pw-card-title">2. Single (단건 소장)</span>
              <span class="dmdg-pw-card-price">건당 5,000 ~ 29,000원</span>
            </div>
            <div class="dmdg-pw-card-desc">
              • 분량·전문성별 차등 책정<br>
              • 해당 자료 <strong>원본 PDF 영구 다운로드</strong> + 웹 뷰어 무제한 열람
            </div>
          </div>
          <div class="dmdg-pw-card featured">
            <div class="dmdg-pw-card-head">
              <span class="dmdg-pw-card-title">3. Pro (월/연 구독)</span>
              <span class="dmdg-pw-card-price">월 9,900 ~ 19,900원 (연 20~30%↓)</span>
            </div>
            <div class="dmdg-pw-card-desc">
              • <strong>전 자료 웹 보안 뷰어 무제한 스트리밍</strong><br>
              • 월 N건(또는 무제한) 원본 PDF 다운로드 + 개정판·신규 자료 우선 열람
            </div>
          </div>
          <div class="dmdg-pw-card">
            <div class="dmdg-pw-card-head">
              <span class="dmdg-pw-card-title">4. Team / B2B</span>
              <span class="dmdg-pw-card-price">별도 문의 (5~10인)</span>
            </div>
            <div class="dmdg-pw-card-desc">
              • 기업·기관·스터디 그룹 다중 계정 웹 뷰어<br>
              • 기관명 각인 원본 PDF 일괄 제공
            </div>
          </div>
        </div>

        <div class="dmdg-pw-strategy">
          <div class="dmdg-pw-strategy-title">🚀 2026.12 → 2027.01 전환 혜택 &amp; 보안 정책</div>
          <div>1) <strong>12월 얼리버드 사전 구독</strong>: <em>"2026.12.31 무료 종료 — 지금 사전 구독 시 2027년 평생 40% 할인"</em></div>
          <div>2) <strong>만료 샘플 초대 코드(Passkey)</strong>: VIP·파트너사 전용 코드 <span class="dmdg-pw-code">dmdg_servive</span> 제공 <em>(유료화 후 월별 로테이션·전용 토큰 분리)</em></div>
          <div>3) <strong>유료 원본 PDF 소셜 DRM</strong>: 본문 가림 없이 하단 여백에 <em>"Licensed to: 이름 (email)"</em> 구매자 각인 워터마크 삽입</div>
        </div>

        <div class="dmdg-pw-footer">
          <label class="dmdg-pw-check-label">
            <input type="checkbox" id="dmdg-paywall-hide-today" />
            <span>오늘 하루 동안 보지 않기</span>
          </label>
          <div class="dmdg-pw-actions">
            <a href="${vaultUrl}" class="dmdg-pw-btn-vault">🔐 PDF 보안 열람실</a>
            <button type="button" class="dmdg-pw-btn-ok" id="dmdg-pw-confirm-btn">무료로 계속 이용하기</button>
          </div>
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
