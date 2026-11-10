/**
 * DMDG A.C.E.S 공인 시험 성적 무결성 검증 & 임의 수정 차단 모듈
 * - 7대 시험 점수의 임의 입력, URL 파라미터 조작(?score=100), DevTools DOM 변조 방지
 * - 심화 3대 시험: 시험 완료 시 무결성 서명 토큰 발급 (데모 샘플은 연동 차단)
 * - 기초 4대 시험: Firebase Firestore(dmdg-live) 실명 기반 공인 응시 기록 조회 연동
 */
(function (global) {
  'use strict';

  const STORAGE_KEY = 'dmdg_aces_verified_scores_v1';
  const SIG_SALT = 'DMDG::ACES::LOCK::2026::INTEGRITY';

  const EXAM_CONFIG = {
    sql: {
      inputId: 'exam_sql',
      badgeId: 'badge_exam_sql',
      collection: 'sql_exam_submissions',
      label: 'SQL 실무 평가'
    },
    math: {
      inputId: 'exam_math',
      badgeId: 'badge_exam_math',
      collection: 'ai_math_exam_submissions',
      label: 'AI·LLM 사전수학'
    },
    data: {
      inputId: 'exam_data',
      badgeId: 'badge_exam_data',
      collection: 'ai_data_exam_submissions',
      label: 'AI 데이터 분석'
    },
    python: {
      inputId: 'exam_python',
      badgeId: 'badge_exam_python',
      collection: 'python_ai_exam_submissions',
      label: '파이썬 & ML/DL'
    },
    smartcar_lakehouse: {
      inputId: 'exam_smartcar',
      badgeId: 'badge_exam_smartcar',
      collection: null,
      label: '[심화 1] 자율주행 레이크하우스'
    },
    graphrag_mcp: {
      inputId: 'exam_graphrag',
      badgeId: 'badge_exam_graphrag',
      collection: null,
      label: '[심화 2] FastMCP·GraphRAG'
    },
    continual_memory: {
      inputId: 'exam_memory',
      badgeId: 'badge_exam_memory',
      collection: null,
      label: '[심화 3] 지속 메모리·모델정렬'
    }
  };

  const FIREBASE_CFG = {
    apiKey: 'AIzaSyBcS8aS5yHk2KFNYPImXslsFkSyoBwYrKI',
    authDomain: 'dmdg-live.firebaseapp.com',
    projectId: 'dmdg-live',
    storageBucket: 'dmdg-live.firebasestorage.app',
    messagingSenderId: '357433220336',
    appId: '1:357433220336:web:1a8914811da09123a0f635'
  };

  // Closure-protected verified state (not directly exposed as mutable plain object)
  const _verifiedState = Object.create(null);

  function _normalizeScore(val) {
    const n = Number(val);
    if (!Number.isFinite(n)) return null;
    const rounded = Math.round(n * 10) / 10;
    if (rounded < 0 || rounded > 100) return null;
    return rounded;
  }

  function _hash32(str, seed) {
    let h = (0x811c9dc5 ^ (seed >>> 0)) >>> 0;
    for (let i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = Math.imul(h, 0x01000193) >>> 0;
    }
    h ^= h >>> 16;
    h = Math.imul(h, 0x85ebca6b) >>> 0;
    h ^= h >>> 13;
    h = Math.imul(h, 0xc2b2ae35) >>> 0;
    h ^= h >>> 16;
    return (h >>> 0).toString(16).padStart(8, '0');
  }

  function computeExamSig(examId, score, ts, studentName, source) {
    const payload = [
      SIG_SALT,
      String(examId || ''),
      String(score),
      String(ts || 0),
      String(studentName || '').trim(),
      String(source || 'exam')
    ].join('|');
    const p1 = _hash32(payload, 0x13579bdf);
    const p2 = _hash32(payload.split('').reverse().join(''), 0x2468ace0);
    return p1 + p2;
  }

  function _isValidRecord(examId, rec) {
    if (!rec || !EXAM_CONFIG[examId]) return false;
    const score = _normalizeScore(rec.score);
    if (score === null) return false;
    const ts = Number(rec.ts);
    if (!Number.isFinite(ts) || ts <= 0) return false;
    const expected = computeExamSig(examId, score, ts, rec.studentName || '', rec.source || 'exam');
    return rec.sig === expected;
  }

  function _readRawStorage() {
    try {
      const raw = global.localStorage.getItem(STORAGE_KEY);
      if (!raw) return {};
      const parsed = JSON.parse(raw);
      return parsed && typeof parsed === 'object' ? parsed : {};
    } catch (_) {
      return {};
    }
  }

  function _writeVerifiedStorage() {
    try {
      const out = {};
      Object.keys(_verifiedState).forEach(function (examId) {
        out[examId] = Object.assign({}, _verifiedState[examId]);
      });
      global.localStorage.setItem(STORAGE_KEY, JSON.stringify(out));
    } catch (_) {}
  }

  function _setVerifiedRecord(examId, score, ts, studentName, source) {
    const normScore = _normalizeScore(score);
    if (normScore === null || !EXAM_CONFIG[examId]) return null;
    const cleanName = String(studentName || '응시자').trim();
    const cleanSource = String(source || 'exam');
    const sig = computeExamSig(examId, normScore, ts, cleanName, cleanSource);
    const rec = Object.freeze({
      examId: examId,
      score: normScore,
      ts: Number(ts),
      studentName: cleanName,
      source: cleanSource,
      sig: sig
    });
    _verifiedState[examId] = rec;
    _writeVerifiedStorage();
    return rec;
  }

  function hydrateFromStorage() {
    const stored = _readRawStorage();
    Object.keys(EXAM_CONFIG).forEach(function (examId) {
      delete _verifiedState[examId];
      const rec = stored[examId];
      if (_isValidRecord(examId, rec)) {
        _verifiedState[examId] = Object.freeze({
          examId: examId,
          score: _normalizeScore(rec.score),
          ts: Number(rec.ts),
          studentName: String(rec.studentName || ''),
          source: String(rec.source || 'exam'),
          sig: rec.sig
        });
      }
    });
  }

  /**
   * 심화 시험 완료 시 호출 (실제 응시 완료만 허용, 샘플 데모는 호출 금지)
   */
  function recordOfficialExamScore(examId, score100, studentName) {
    hydrateFromStorage();
    const ts = Date.now();
    const cleanName = String(studentName || '응시자').trim() || '응시자';
    const rec = _setVerifiedRecord(examId, score100, ts, cleanName, 'official_exam');
    if (!rec) return '';
    const params = new URLSearchParams();
    params.set('exam', rec.examId);
    params.set('score', String(rec.score));
    params.set('ts', String(rec.ts));
    params.set('name', rec.studentName);
    params.set('sig', rec.sig);
    return params.toString();
  }

  /**
   * URL 서명 파라미터 및 로컬 저장소 무결성 동시 검증
   */
  function verifyPortalState(searchStr) {
    hydrateFromStorage();
    const params = new URLSearchParams(searchStr || global.location.search || '');
    const examId = params.get('exam');
    const scoreRaw = params.get('score');
    const tsRaw = params.get('ts');
    const nameRaw = params.get('name') || '';
    const sigRaw = params.get('sig') || '';

    let urlResult = { hasUrlExam: false, urlTampered: false, examId: null, score: null };

    if (examId || scoreRaw !== null) {
      urlResult.hasUrlExam = true;
      urlResult.examId = examId;
      const normScore = _normalizeScore(scoreRaw);
      const tsNum = Number(tsRaw);
      if (EXAM_CONFIG[examId] && normScore !== null && Number.isFinite(tsNum) && tsNum > 0 && sigRaw) {
        const expected = computeExamSig(examId, normScore, tsNum, nameRaw, 'official_exam');
        if (sigRaw === expected) {
          _setVerifiedRecord(examId, normScore, tsNum, nameRaw, 'official_exam');
          urlResult.score = normScore;
        } else {
          urlResult.urlTampered = true;
        }
      } else {
        urlResult.urlTampered = true;
      }
    }

    return {
      urlResult: urlResult,
      scores: getAllVerifiedScores()
    };
  }

  function _getFirestore() {
    if (typeof global.firebase === 'undefined' || typeof global.firebase.firestore !== 'function') {
      return null;
    }
    try {
      if (!global.firebase.apps || !global.firebase.apps.length) {
        global.firebase.initializeApp(FIREBASE_CFG);
      }
      return global.firebase.firestore();
    } catch (_) {
      return null;
    }
  }

  /**
   * Firebase Firestore에서 응시자 실명으로 4대 기초 공인 시험 성적 조회 및 서명 잠금
   */
  async function lookupFirestoreScoresByName(studentName) {
    const cleanName = String(studentName || '').trim();
    if (!cleanName) {
      throw new Error('응시자 성명을 입력해 주세요.');
    }

    const db = _getFirestore();
    if (!db) {
      throw new Error('Firebase Firestore 연결을 초기화할 수 없습니다. 인터넷 연결을 확인해 주세요.');
    }

    const basicIds = ['sql', 'math', 'data', 'python'];
    const matchedDetails = [];

    for (let i = 0; i < basicIds.length; i++) {
      const examId = basicIds[i];
      const cfg = EXAM_CONFIG[examId];
      let snap = null;
      try {
        snap = await db.collection(cfg.collection).orderBy('submittedAt', 'desc').limit(300).get();
      } catch (_) {
        snap = await db.collection(cfg.collection).limit(300).get();
      }

      if (!snap || snap.empty) continue;

      let bestRecord = null;
      const normQueryName = cleanName.replace(/\s+/g, '').toLowerCase();
      snap.docs.forEach(function (doc) {
        const d = doc.data();
        if (!d) return;
        const recName = String(d.studentName || '').trim();
        if (recName.replace(/\s+/g, '').toLowerCase() !== normQueryName) return;
        const sc = _normalizeScore(d.score100);
        if (sc === null) return;
        const recTs = d.submittedAt ? new Date(d.submittedAt).getTime() : Date.now();
        if (!bestRecord || recTs > bestRecord.ts) {
          bestRecord = { score: sc, ts: Number.isFinite(recTs) ? recTs : Date.now() };
        }
      });

      if (bestRecord) {
        _setVerifiedRecord(examId, bestRecord.score, bestRecord.ts, cleanName, 'firestore');
        matchedDetails.push({ examId: examId, label: cfg.label, score: bestRecord.score });
      }
    }

    return {
      matchedCount: matchedDetails.length,
      matchedDetails: matchedDetails,
      scores: getAllVerifiedScores()
    };
  }

  function getVerifiedRecord(examId) {
    const rec = _verifiedState[examId];
    return rec ? Object.assign({}, rec) : null;
  }

  function getAllVerifiedScores() {
    const out = {};
    Object.keys(EXAM_CONFIG).forEach(function (examId) {
      const rec = _verifiedState[examId];
      out[examId] = rec ? rec.score : 0;
    });
    return out;
  }

  function getVerifiedCount() {
    return Object.keys(_verifiedState).length;
  }

  function clearVerifiedScores() {
    Object.keys(_verifiedState).forEach(function (k) {
      delete _verifiedState[k];
    });
    try {
      global.localStorage.removeItem(STORAGE_KEY);
    } catch (_) {}
  }

  global.DMDGScoreLock = Object.freeze({
    EXAM_CONFIG: EXAM_CONFIG,
    computeExamSig: computeExamSig,
    recordOfficialExamScore: recordOfficialExamScore,
    verifyPortalState: verifyPortalState,
    lookupFirestoreScoresByName: lookupFirestoreScoresByName,
    getVerifiedRecord: getVerifiedRecord,
    getAllVerifiedScores: getAllVerifiedScores,
    getVerifiedCount: getVerifiedCount,
    clearVerifiedScores: clearVerifiedScores
  });
})(window);

