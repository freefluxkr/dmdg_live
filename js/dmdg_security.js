/**
 * dmdg_security.js
 * DMDG 전 서비스 콘텐츠 무단 복사·유출 방지 보안 아키텍처 엔진
 * 1) 기간 한정(OTT형) 전용: HMAC-SHA256 기반 Signed URL & 만료 토큰(exp) 발급·검증
 * 2) 완전 소유 / 정기 구독 / 기간 한정 공통:
 *    - Unicode Zero-Width Steganography(\u200B, \u200C, \u200D) 비가시 워터마킹 인코더/디코더
 *    - 클립보드 복사 이벤트 자동 비가시 워터마킹
 *    - 다운로드 파일(TXT/JSON/PDF/ZIP) 구매자·열람자 식별 해시 각인
 */
(function (global) {
  'use strict';

  const SECRET_PEPPER = 'DMDG-2026-SEC-HMAC-PEPPER-V1';
  const ZW_ZERO = '\u200B';  // bit 0
  const ZW_ONE = '\u200C';   // bit 1
  const ZW_MARK = '\u200D';  // start / end delimiter

  // ---------------------------------------------------------------------------
  // 1. Pure-JS Synchronous SHA-256 & HMAC-SHA256 (file:// & http:// 100% 호환)
  // ---------------------------------------------------------------------------
  function sha256Bytes(bytes) {
    const K = [
      0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
      0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
      0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
      0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
      0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
      0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
      0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
      0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ];
    const H = [
      0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
      0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ];

    const l = bytes.length;
    const bitLenHi = Math.floor((l * 8) / 0x100000000);
    const bitLenLo = (l * 8) >>> 0;
    const paddedLen = Math.ceil((l + 9) / 64) * 64;
    const padded = new Uint8Array(paddedLen);
    padded.set(bytes);
    padded[l] = 0x80;
    const view = new DataView(padded.buffer);
    view.setUint32(paddedLen - 8, bitLenHi, false);
    view.setUint32(paddedLen - 4, bitLenLo, false);

    const w = new Uint32Array(64);
    for (let offset = 0; offset < paddedLen; offset += 64) {
      for (let i = 0; i < 16; i++) {
        w[i] = view.getUint32(offset + i * 4, false);
      }
      for (let i = 16; i < 64; i++) {
        const s0 = ((w[i - 15] >>> 7) | (w[i - 15] << 25)) ^ ((w[i - 15] >>> 18) | (w[i - 15] << 14)) ^ (w[i - 15] >>> 3);
        const s1 = ((w[i - 2] >>> 17) | (w[i - 2] << 15)) ^ ((w[i - 2] >>> 19) | (w[i - 2] << 13)) ^ (w[i - 2] >>> 10);
        w[i] = (w[i - 16] + s0 + w[i - 7] + s1) >>> 0;
      }

      let [a, b, c, d, e, f, g, h] = H;
      for (let i = 0; i < 64; i++) {
        const S1 = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7));
        const ch = (e & f) ^ (~e & g);
        const temp1 = (h + S1 + ch + K[i] + w[i]) >>> 0;
        const S0 = ((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10));
        const maj = (a & b) ^ (a & c) ^ (b & c);
        const temp2 = (S0 + maj) >>> 0;

        h = g; g = f; f = e; e = (d + temp1) >>> 0;
        d = c; c = b; b = a; a = (temp1 + temp2) >>> 0;
      }
      H[0] = (H[0] + a) >>> 0; H[1] = (H[1] + b) >>> 0;
      H[2] = (H[2] + c) >>> 0; H[3] = (H[3] + d) >>> 0;
      H[4] = (H[4] + e) >>> 0; H[5] = (H[5] + f) >>> 0;
      H[6] = (H[6] + g) >>> 0; H[7] = (H[7] + h) >>> 0;
    }

    const out = new Uint8Array(32);
    const outView = new DataView(out.buffer);
    for (let i = 0; i < 8; i++) outView.setUint32(i * 4, H[i], false);
    return out;
  }

  function hmacSha256Hex(keyStr, msgStr) {
    const enc = new TextEncoder();
    let keyBytes = enc.encode(keyStr);
    if (keyBytes.length > 64) keyBytes = sha256Bytes(keyBytes);
    const kPad = new Uint8Array(64);
    kPad.set(keyBytes);

    const oKey = new Uint8Array(64);
    const iKey = new Uint8Array(64);
    for (let i = 0; i < 64; i++) {
      oKey[i] = kPad[i] ^ 0x5c;
      iKey[i] = kPad[i] ^ 0x36;
    }

    const msgBytes = enc.encode(msgStr);
    const innerInput = new Uint8Array(64 + msgBytes.length);
    innerInput.set(iKey);
    innerInput.set(msgBytes, 64);
    const innerHash = sha256Bytes(innerInput);

    const outerInput = new Uint8Array(64 + 32);
    outerInput.set(oKey);
    outerInput.set(innerHash, 64);
    const finalHash = sha256Bytes(outerInput);

    return Array.from(finalHash).map(b => b.toString(16).padStart(2, '0')).join('');
  }

  // ---------------------------------------------------------------------------
  // 2. Viewer Identity & Audit Log
  // ---------------------------------------------------------------------------
  function getViewerId() {
    let uid = localStorage.getItem('dmdg_viewer_id');
    if (!uid) {
      const rand = Math.random().toString(36).substring(2, 8).toUpperCase();
      uid = `DMDG-${rand}`;
      localStorage.setItem('dmdg_viewer_id', uid);
    }
    return uid;
  }

  function recordSecurityEvent(eventObj) {
    try {
      const logs = JSON.parse(localStorage.getItem('dmdg_security_audit_logs') || '[]');
      logs.unshift({
        ...eventObj,
        timestamp: new Date().toISOString()
      });
      if (logs.length > 50) logs.length = 50;
      localStorage.setItem('dmdg_security_audit_logs', JSON.stringify(logs));
    } catch (e) {}
  }

  // ---------------------------------------------------------------------------
  // 3. Expiring Token & Signed URL (기간 한정 OTT형 전용)
  // ---------------------------------------------------------------------------
  function createSignedUrl(resourcePath, ttlSeconds = 1800, customUid = null, mode = 'limited') {
    const uid = customUid || getViewerId();
    const exp = Date.now() + Number(ttlSeconds) * 1000;
    const nonce = Math.random().toString(36).substring(2, 10);
    const cleanPath = resourcePath.split('?')[0];
    const canonical = `${cleanPath}|${uid}|${exp}|${nonce}|${mode}`;
    const sig = hmacSha256Hex(SECRET_PEPPER, canonical).slice(0, 32);

    const qs = new URLSearchParams({
      uid,
      exp: String(exp),
      nonce,
      mode,
      sig
    });

    recordSecurityEvent({
      type: 'SIGNED_URL_ISSUED',
      resource: cleanPath,
      uid,
      mode,
      exp
    });

    return `${cleanPath}?${qs.toString()}`;
  }

  function verifySignedUrl(urlString, nowMs = Date.now()) {
    try {
      const parsed = new URL(urlString, global.location ? global.location.origin : 'https://dmdg-live.com');
      const cleanPath = parsed.pathname.replace(/^\//, '');
      const rawPath = urlString.split('?')[0];
      const uid = parsed.searchParams.get('uid');
      const expStr = parsed.searchParams.get('exp');
      const nonce = parsed.searchParams.get('nonce');
      const mode = parsed.searchParams.get('mode') || 'limited';
      const sig = parsed.searchParams.get('sig');

      if (!uid || !expStr || !nonce || !sig) {
        return { valid: false, reason: 'MISSING_PARAMS', message: '서명 토큰 파라미터가 누락되었습니다. (403 Forbidden)' };
      }

      const exp = Number(expStr);
      // 경로 매칭은 rawPath 또는 pathname 둘 다 허용
      const sigA = hmacSha256Hex(SECRET_PEPPER, `${rawPath}|${uid}|${exp}|${nonce}|${mode}`).slice(0, 32);
      const sigB = hmacSha256Hex(SECRET_PEPPER, `${cleanPath}|${uid}|${exp}|${nonce}|${mode}`).slice(0, 32);

      if (sig !== sigA && sig !== sigB) {
        return { valid: false, reason: 'INVALID_SIGNATURE', message: '위변조된 Signed URL 서명입니다. (403 Invalid Signature)' };
      }

      if (Number.isNaN(exp) || nowMs > exp) {
        return {
          valid: false,
          reason: 'EXPIRED',
          uid,
          exp,
          message: '만료된 토큰입니다. 열람 가능 시간이 종료되어 접근이 차단되었습니다. (403 Expired Token)'
        };
      }

      return {
        valid: true,
        reason: 'OK',
        uid,
        mode,
        exp,
        remainingSeconds: Math.max(0, Math.floor((exp - nowMs) / 1000)),
        message: '유효한 Signed URL 토큰이 검증되었습니다.'
      };
    } catch (e) {
      return { valid: false, reason: 'PARSE_ERROR', message: '잘못된 URL 형식입니다.' };
    }
  }

  // ---------------------------------------------------------------------------
  // 4. Invisible Watermarking (Unicode Zero-Width Steganography)
  // ---------------------------------------------------------------------------
  function encodeZeroWidth(payloadStr) {
    const bytes = new TextEncoder().encode(payloadStr);
    let bits = '';
    for (let i = 0; i < bytes.length; i++) {
      bits += bytes[i].toString(2).padStart(8, '0');
    }
    const encoded = bits.split('').map(b => (b === '0' ? ZW_ZERO : ZW_ONE)).join('');
    return `${ZW_MARK}${encoded}${ZW_MARK}`;
  }

  function decodeZeroWidth(text) {
    if (!text || typeof text !== 'string') return { found: false };
    const regex = new RegExp(`${ZW_MARK}([${ZW_ZERO}${ZW_ONE}]+)${ZW_MARK}`);
    const match = text.match(regex);
    if (!match || !match[1]) return { found: false };

    const bitStr = match[1].split('').map(ch => (ch === ZW_ZERO ? '0' : '1')).join('');
    if (bitStr.length < 8) return { found: false };

    const byteArr = [];
    for (let i = 0; i + 8 <= bitStr.length; i += 8) {
      byteArr.push(parseInt(bitStr.slice(i, i + 8), 2));
    }
    try {
      const payload = new TextDecoder().decode(new Uint8Array(byteArr));
      return { found: true, payload, bitLength: bitStr.length };
    } catch (e) {
      return { found: false };
    }
  }

  function embedTextWatermark(text, meta = {}) {
    const uid = meta.uid || getViewerId();
    const mode = meta.mode || 'owned';
    const ts = meta.ts || Math.floor(Date.now() / 1000);
    const resource = meta.resource || 'DMDG';
    const payload = `DMDG|UID:${uid}|MODE:${mode}|RES:${resource}|TS:${ts}`;
    const zw = encodeZeroWidth(payload);

    if (!text) return zw;
    const spaceIdx = text.indexOf(' ');
    if (spaceIdx > 0 && spaceIdx < 40) {
      return text.slice(0, spaceIdx) + zw + text.slice(spaceIdx);
    }
    return text + zw;
  }

  function extractTextWatermark(text) {
    const res = decodeZeroWidth(text);
    if (!res.found) return res;
    const parsed = {};
    res.payload.split('|').forEach(part => {
      const idx = part.indexOf(':');
      if (idx > 0) {
        parsed[part.slice(0, idx)] = part.slice(idx + 1);
      }
    });
    return {
      found: true,
      payload: res.payload,
      parsed,
      bitLength: res.bitLength
    };
  }

  function attachCopyWatermark(targetSelector = 'body', meta = {}) {
    const el = typeof targetSelector === 'string'
      ? document.querySelector(targetSelector)
      : targetSelector;
    if (!el || el.dataset.dmdgCopyWmAttached === '1') return;
    el.dataset.dmdgCopyWmAttached = '1';

    el.addEventListener('copy', (e) => {
      try {
        const sel = global.getSelection ? global.getSelection().toString() : '';
        if (!sel || sel.trim().length < 4) return;
        const watermarked = embedTextWatermark(sel, {
          uid: meta.uid || getViewerId(),
          mode: meta.mode || 'subscription',
          resource: meta.resource || (global.location ? global.location.pathname : 'page')
        });
        if (e.clipboardData) {
          e.clipboardData.setData('text/plain', watermarked);
          e.preventDefault();
          recordSecurityEvent({
            type: 'COPY_WATERMARK_EMBEDDED',
            resource: meta.resource || (global.location ? global.location.pathname : 'page'),
            length: sel.length
          });
        }
      } catch (err) {}
    });
  }

  // ---------------------------------------------------------------------------
  // 5. File / Blob / PDF Download Watermarking Helper
  // ---------------------------------------------------------------------------
  function buildWatermarkedTextBlob(rawText, meta = {}) {
    const uid = meta.uid || getViewerId();
    const mode = meta.mode || 'owned';
    const ts = new Date().toISOString();
    const sig = hmacSha256Hex(SECRET_PEPPER, `${uid}|${mode}|${ts}`).slice(0, 16).toUpperCase();
    const watermarkedBody = embedTextWatermark(rawText, { uid, mode, resource: meta.resource || 'file' });
    const invisibleFooter = encodeZeroWidth(`DMDG_FILE|UID:${uid}|MODE:${mode}|SIG:${sig}|TS:${ts}`);
    const content = `${watermarkedBody}\n${invisibleFooter}`;
    return {
      blob: new Blob([content], { type: meta.mimeType || 'text/plain;charset=utf-8' }),
      uid,
      sig,
      ts
    };
  }

  function injectPdfWatermarkBanner(containerEl, meta = {}) {
    if (!containerEl) return;
    const uid = meta.uid || getViewerId();
    const mode = meta.mode || 'owned';
    const ts = new Date().toISOString();
    const sig = hmacSha256Hex(SECRET_PEPPER, `${uid}|${mode}|${ts}`).slice(0, 12).toUpperCase();
    let stamp = containerEl.querySelector('.dmdg-invisible-pdf-wm');
    if (!stamp) {
      stamp = document.createElement('div');
      stamp.className = 'dmdg-invisible-pdf-wm';
      stamp.style.cssText = 'font-size:1px;line-height:1px;color:rgba(128,128,128,0.015);user-select:none;pointer-events:none;height:1px;overflow:hidden;';
      containerEl.appendChild(stamp);
    }
    stamp.textContent = embedTextWatermark(`DMDG-LICENSE:${uid}:${mode}:${sig}:${ts}`, { uid, mode, resource: 'pdf' });
  }

  function checkCurrentPageTokenGate() {
    if (!global.location || !global.location.search) return { valid: true };
    const params = new URLSearchParams(global.location.search);
    if (!params.has('sig') && !params.has('exp')) return { valid: true };

    const res = verifySignedUrl(global.location.href);
    if (!res.valid) {
      const overlay = document.createElement('div');
      overlay.id = 'dmdg-token-blocked-overlay';
      overlay.style.cssText = 'position:fixed;inset:0;z-index:999999;background:rgba(15,23,42,0.97);color:#f8fafc;display:flex;align-items:center;justify-content:center;padding:24px;font-family:sans-serif;text-align:center;';
      overlay.innerHTML = `
        <div style="max-width:460px;background:#1e293b;border:1.5px solid #ef4444;border-radius:18px;padding:32px;box-shadow:0 25px 50px rgba(0,0,0,0.6);">
          <div style="font-size:40px;margin-bottom:12px;">⛔</div>
          <h2 style="margin:0 0 10px 0;font-size:20px;font-weight:800;color:#f87171;">접근 차단 (${res.reason})</h2>
          <p style="margin:0 0 20px 0;font-size:14px;color:#cbd5e1;line-height:1.6;">${res.message}</p>
          <a href="./index.html" style="display:inline-block;padding:10px 22px;background:#0284c7;color:#fff;border-radius:10px;text-decoration:none;font-weight:700;font-size:13px;">DMDG 홈으로 이동</a>
        </div>
      `;
      if (document.body) {
        document.body.appendChild(overlay);
      } else {
        document.addEventListener('DOMContentLoaded', () => document.body.appendChild(overlay));
      }
    }
    return res;
  }

  const api = {
    getViewerId,
    hmacSha256Hex,
    createSignedUrl,
    verifySignedUrl,
    encodeZeroWidth,
    decodeZeroWidth,
    embedTextWatermark,
    extractTextWatermark,
    attachCopyWatermark,
    buildWatermarkedTextBlob,
    injectPdfWatermarkBanner,
    checkCurrentPageTokenGate,
    getAuditLogs: () => JSON.parse(localStorage.getItem('dmdg_security_audit_logs') || '[]')
  };

  global.DMDG_Security = api;

  if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
      checkCurrentPageTokenGate();
      attachCopyWatermark('body', { mode: 'subscription' });
    });
  }
})(typeof window !== 'undefined' ? window : globalThis);

