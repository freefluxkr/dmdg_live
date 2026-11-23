/**
 * dmdg_firebase_backend.js
 * DMDG 공식 Firebase 통합 동적 백엔드 클라이언트 SDK (dmdg-live)
 * - Firestore (users, exam_results, voice_relays)
 * - Storage (voice_relays 오디오, reports PDF 성적표)
 * - Cloud Functions v2 (us-central1: lookupExamResultsByEmail, issueSecureReportUrl, verifyPortOnePayment)
 */
(function (global) {
  'use strict';

  const DEFAULT_FIREBASE_CONFIG = {
    apiKey: 'AIzaSyBcS8aS5yHk2KFNYPImXslsFkSyoBwYrKI',
    authDomain: 'dmdg-live.firebaseapp.com',
    projectId: 'dmdg-live',
    storageBucket: 'dmdg-live.firebasestorage.app',
    messagingSenderId: '357433220336',
    appId: '1:357433220336:web:1a8914811da09123a0f635',
    measurementId: 'G-RRYE7JKKWX'
  };

  const FUNCTIONS_REGION = 'us-central1';

  function _normalizeName(name) {
    return String(name || '').replace(/\s+/g, '').toLowerCase();
  }

  function _normalizeEmail(email) {
    return String(email || '').trim().toLowerCase();
  }

  function _inferAudioExtension(mimeType) {
    const m = String(mimeType || '').toLowerCase();
    if (m.includes('wav')) return 'wav';
    if (m.includes('mpeg') || m.includes('mp3')) return 'mp3';
    if (m.includes('ogg')) return 'ogg';
    if (m.includes('mp4') || m.includes('m4a')) return 'm4a';
    return 'webm';
  }

  function ensureInitialized() {
    if (typeof global.firebase === 'undefined') {
      throw new Error('Firebase SDK가 로드되지 않았습니다.');
    }
    const cfg = global.firebaseConfig || DEFAULT_FIREBASE_CONFIG;
    if (!global.firebaseConfig) {
      global.firebaseConfig = cfg;
    }
    if (!global.firebase.apps || !global.firebase.apps.length) {
      global.firebase.initializeApp(cfg);
    }

    const app = global.firebase.app();
    const db = typeof global.firebase.firestore === 'function' ? global.firebase.firestore() : null;
    const storage = typeof global.firebase.storage === 'function' ? global.firebase.storage() : null;
    const auth = typeof global.firebase.auth === 'function' ? global.firebase.auth() : null;
    const functions = typeof app.functions === 'function'
      ? app.functions(FUNCTIONS_REGION)
      : (typeof global.firebase.functions === 'function' ? global.firebase.functions() : null);

    if (db && !global.firestore) {
      global.firestore = db;
    }

    return { app, db, storage, auth, functions };
  }

  async function syncUserProfile({ uid, email, displayName } = {}) {
    const { db, auth } = ensureInitialized();
    if (!db) throw new Error('Firestore를 사용할 수 없습니다.');

    const currentUser = auth && auth.currentUser ? auth.currentUser : null;
    const targetUid = uid || (currentUser ? currentUser.uid : null);
    if (!targetUid) {
      throw new Error('사용자 UID가 필요합니다.');
    }

    const userRef = db.collection('users').doc(targetUid);
    const snap = await userRef.get();
    const serverTs = global.firebase.firestore.FieldValue.serverTimestamp();

    const payload = {
      uid: targetUid,
      email: _normalizeEmail(email || (currentUser ? currentUser.email : '')),
      displayName: String(displayName || (currentUser ? currentUser.displayName : '') || '사용자').trim(),
      lastLoginAt: serverTs
    };

    if (!snap.exists) {
      payload.createdAt = serverTs;
    }

    await userRef.set(payload, { merge: true });
    return { ok: true, uid: targetUid };
  }

  async function saveExamResult({ email, studentName, examId, score100, acesScores, metadata } = {}) {
    const { db, auth } = ensureInitialized();
    if (!db) throw new Error('Firestore를 사용할 수 없습니다.');

    const cleanName = String(studentName || '').trim();
    const numericScore = Math.round(Number(score100) * 10) / 10;
    if (!cleanName || !examId || !Number.isFinite(numericScore) || numericScore < 0 || numericScore > 100) {
      throw new Error('유효한 studentName, examId, score100(0~100)이 필요합니다.');
    }

    const currentUser = auth && auth.currentUser ? auth.currentUser : null;
    const cleanEmail = _normalizeEmail(email || (currentUser ? currentUser.email : ''));

    const docData = {
      uid: currentUser ? currentUser.uid : null,
      email: cleanEmail || null,
      studentName: cleanName,
      studentNameNormalized: _normalizeName(cleanName),
      examId: String(examId),
      score100: numericScore,
      acesScores: acesScores && typeof acesScores === 'object' ? acesScores : null,
      metadata: metadata && typeof metadata === 'object' ? metadata : null,
      submittedAt: new Date().toISOString(),
      createdAt: global.firebase.firestore.FieldValue.serverTimestamp()
    };

    const ref = await db.collection('exam_results').add(docData);
    return { id: ref.id, examId: docData.examId, score100: numericScore };
  }

  async function _lookupExamResultsDirect(db, { email, studentName }) {
    const cleanEmail = _normalizeEmail(email);
    const normName = _normalizeName(studentName);
    const colMap = {
      sql: 'sql_exam_submissions',
      math: 'ai_math_exam_submissions',
      data: 'ai_data_exam_submissions',
      python: 'python_ai_exam_submissions'
    };

    const scores = {};
    for (const examId of Object.keys(colMap)) {
      const snap = await db.collection(colMap[examId]).limit(300).get();
      snap.forEach(function (doc) {
        const d = doc.data();
        if (!d) return;
        const matchEmail = cleanEmail && _normalizeEmail(d.email) === cleanEmail;
        const matchName = normName && _normalizeName(d.studentName) === normName;
        if (!matchEmail && !matchName) return;
        const sc = Number(d.score100);
        if (Number.isFinite(sc) && (scores[examId] === undefined || sc > scores[examId])) {
          scores[examId] = Math.round(sc * 10) / 10;
        }
      });
    }

    const advSnap = await db.collection('dmdg_advanced_exam_submissions').limit(300).get();
    advSnap.forEach(function (doc) {
      const d = doc.data();
      if (!d || !d.examId) return;
      const matchEmail = cleanEmail && _normalizeEmail(d.email) === cleanEmail;
      const matchName = normName && _normalizeName(d.studentName) === normName;
      if (!matchEmail && !matchName) return;
      const sc = Number(d.score100);
      if (Number.isFinite(sc) && (scores[d.examId] === undefined || sc > scores[d.examId])) {
        scores[d.examId] = Math.round(sc * 10) / 10;
      }
    });

    return {
      matchedCount: Object.keys(scores).length,
      scores: scores,
      fallback: true
    };
  }

  async function lookupExamResults({ email, studentName, syncToUnified = false } = {}) {
    const { db, functions } = ensureInitialized();
    const cleanEmail = _normalizeEmail(email);
    const cleanName = String(studentName || '').trim();
    if (!cleanEmail && !cleanName) {
      throw new Error('이메일 또는 성명을 입력해 주세요.');
    }

    if (functions) {
      try {
        const fn = functions.httpsCallable('lookupExamResultsByEmail');
        const res = await fn({
          email: cleanEmail || null,
          studentName: cleanName || null,
          syncToUnified: Boolean(syncToUnified)
        });
        return res.data;
      } catch (err) {
        console.warn('lookupExamResultsByEmail 호출 실패 — Firestore 직접 조회 폴백 사용:', err);
      }
    }

    if (!db) throw new Error('Firestore를 사용할 수 없습니다.');
    return _lookupExamResultsDirect(db, { email: cleanEmail, studentName: cleanName });
  }

  async function uploadVoiceRelay(audioBlob, { text, category = 'malssam', emotion = '온화', prevRelayId = null, authorName = '익명', userId = null } = {}) {
    const { db, storage, auth } = ensureInitialized();
    if (!db || !storage) {
      throw new Error('Firestore 또는 Firebase Storage가 초기화되지 않았습니다.');
    }
    if (!audioBlob || typeof audioBlob.size !== 'number' || audioBlob.size <= 0) {
      throw new Error('유효한 음성 오디오 파일(Blob)이 필요합니다.');
    }
    const cleanText = String(text || '').trim();
    if (!cleanText || cleanText.length > 2000) {
      throw new Error('문장 텍스트는 1~2000자여야 합니다.');
    }

    const currentUser = auth && auth.currentUser ? auth.currentUser : null;
    const ownerId = userId || (currentUser ? currentUser.uid : 'guest');
    const ext = _inferAudioExtension(audioBlob.type);
    const fileName = `${Date.now()}_${Math.random().toString(36).slice(2, 8)}.${ext}`;
    const storagePath = `voice_relays/${ownerId}/${fileName}`;

    const storageRef = storage.ref().child(storagePath);
    const uploadSnap = await storageRef.put(audioBlob, {
      contentType: audioBlob.type || 'audio/webm'
    });
    const audioUrl = await uploadSnap.ref.getDownloadURL();

    const docPayload = {
      userId: ownerId,
      authorName: String(authorName || '익명').trim(),
      category: String(category || 'malssam'),
      emotion: String(emotion || '온화'),
      text: cleanText,
      prevRelayId: prevRelayId || null,
      nextRelayId: null,
      audioPath: storagePath,
      audioUrl: audioUrl,
      createdAt: global.firebase.firestore.FieldValue.serverTimestamp()
    };

    const docRef = await db.collection('voice_relays').add(docPayload);
    return {
      id: docRef.id,
      audioPath: storagePath,
      audioUrl: audioUrl
    };
  }

  async function listVoiceRelays({ category = null, limitCount = 20 } = {}) {
    const { db } = ensureInitialized();
    if (!db) throw new Error('Firestore를 사용할 수 없습니다.');

    let q = db.collection('voice_relays');
    if (category) {
      q = q.where('category', '==', String(category));
    }
    q = q.orderBy('createdAt', 'desc').limit(Number(limitCount) || 20);

    const snap = await q.get();
    const list = [];
    snap.forEach(function (doc) {
      list.push(Object.assign({ id: doc.id }, doc.data()));
    });
    return list;
  }

  async function uploadAcesPdfReport(pdfBlob, { userId = null, reportName = null } = {}) {
    const { storage, auth } = ensureInitialized();
    if (!storage) throw new Error('Firebase Storage를 사용할 수 없습니다.');

    const currentUser = auth && auth.currentUser ? auth.currentUser : null;
    const targetUid = userId || (currentUser ? currentUser.uid : null);
    if (!targetUid) {
      throw new Error('PDF 성적표 업로드에는 로그인된 사용자 UID가 필요합니다.');
    }
    if (!pdfBlob || typeof pdfBlob.size !== 'number' || pdfBlob.size <= 0) {
      throw new Error('유효한 PDF 파일(Blob)이 필요합니다.');
    }

    const safeName = String(reportName || `aces_report_${Date.now()}`).replace(/[^a-zA-Z0-9_-]/g, '_');
    const storagePath = `reports/${targetUid}/${safeName}.pdf`;
    const storageRef = storage.ref().child(storagePath);

    await storageRef.put(pdfBlob, { contentType: 'application/pdf' });
    return {
      storagePath: storagePath,
      userId: targetUid
    };
  }

  async function getSecureDownloadUrl({ storagePath, type = 'report', bookId = null } = {}) {
    const { functions } = ensureInitialized();
    if (!functions) throw new Error('Firebase Functions를 사용할 수 없습니다.');
    if (!storagePath) throw new Error('storagePath가 필요합니다.');

    const fn = functions.httpsCallable('issueSecureReportUrl');
    const res = await fn({
      storagePath: storagePath,
      type: type,
      bookId: bookId
    });
    return res.data;
  }

  async function verifyPayment({ paymentId, expectedAmount, bookId = null, option = null } = {}) {
    const { functions } = ensureInitialized();
    if (!functions) throw new Error('Firebase Functions를 사용할 수 없습니다.');
    if (!paymentId) throw new Error('paymentId가 필요합니다.');

    const fn = functions.httpsCallable('verifyPortOnePayment');
    const res = await fn({
      paymentId: paymentId,
      expectedAmount: expectedAmount,
      bookId: bookId,
      option: option
    });
    return res.data;
  }

  global.DMDGFirebaseBackend = Object.freeze({
    ensureInitialized: ensureInitialized,
    syncUserProfile: syncUserProfile,
    saveExamResult: saveExamResult,
    lookupExamResults: lookupExamResults,
    uploadVoiceRelay: uploadVoiceRelay,
    listVoiceRelays: listVoiceRelays,
    uploadAcesPdfReport: uploadAcesPdfReport,
    getSecureDownloadUrl: getSecureDownloadUrl,
    verifyPayment: verifyPayment
  });
})(window);
