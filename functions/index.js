const crypto = require("crypto");
const { onCall, onRequest, HttpsError } = require("firebase-functions/v2/https");
const { onDocumentCreated } = require("firebase-functions/v2/firestore");
const { setGlobalOptions } = require("firebase-functions/v2");
const admin = require("firebase-admin");

admin.initializeApp();

// 글로벌 설정 적용: 2세대 함수 배포 지역 및 오류가 있는 기본 compute 계정 우회를 위한 서비스 계정 지정
setGlobalOptions({
  region: "us-central1",
  serviceAccount: "dmdg-live@appspot.gserviceaccount.com"
});

const BASIC_EXAM_COLLECTIONS = {
  sql: "sql_exam_submissions",
  math: "ai_math_exam_submissions",
  data: "ai_data_exam_submissions",
  python: "python_ai_exam_submissions"
};

const ADVANCED_EXAM_IDS = [
  "smartcar_lakehouse",
  "graphrag_mcp",
  "continual_memory"
];

/**
 * 음성 릴레이/기부 시 월 최대 3회까지 무료 평가 횟수(+5회) 지급 공통 트랜잭션
 */
async function grantMonthlyVoiceReward(uid) {
  if (!uid) return;
  const now = new Date();
  const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;
  const maxRewardsPerMonth = 3;
  const userRef = admin.firestore().collection("users").doc(uid);

  await admin.firestore().runTransaction(async (transaction) => {
    const userDoc = await transaction.get(userRef);
    if (!userDoc.exists) {
      transaction.set(userRef, {
        free_evals: 8,
        reward_month: currentMonth,
        monthly_reward_count: 1
      }, { merge: true });
      return;
    }

    const userData = userDoc.data();
    let currentRewardMonth = userData.reward_month || "";
    let monthlyCount = userData.monthly_reward_count || 0;

    if (currentRewardMonth !== currentMonth) {
      currentRewardMonth = currentMonth;
      monthlyCount = 0;
    }

    if (monthlyCount < maxRewardsPerMonth) {
      transaction.set(userRef, {
        free_evals: admin.firestore.FieldValue.increment(5),
        reward_month: currentRewardMonth,
        monthly_reward_count: monthlyCount + 1
      }, { merge: true });
    }
  });
}

function normalizeName(name) {
  return String(name || "").replace(/\s+/g, "").toLowerCase();
}

function normalizeEmail(email) {
  return String(email || "").trim().toLowerCase();
}

function parseTimestampMs(rawTs, fallback) {
  if (!rawTs) return fallback;
  if (typeof rawTs.toMillis === "function") return rawTs.toMillis();
  const ms = new Date(rawTs).getTime();
  return Number.isFinite(ms) ? ms : fallback;
}

function normalizeScoreValue(rawScore) {
  const n = Number(rawScore);
  if (!Number.isFinite(n) || n < 0 || n > 100) return null;
  return Math.round(n * 10) / 10;
}

// 1. 텍스트 번역 프록시 함수 (Gemini 2.5 Flash 이용 - v2)
exports.translateText = onCall({
  secrets: ["GEMINI_API_KEY"],
  timeoutSeconds: 60,
  memory: "256MiB"
}, async (request) => {
  const { text, targetLang } = request.data || {};
  if (!text || !targetLang) {
    throw new HttpsError("invalid-argument", "필수 파라미터가 누락되었습니다.");
  }

  const apiKey = process.env.GEMINI_API_KEY || request.data.apiKey;
  if (!apiKey) {
    throw new HttpsError("failed-precondition", "서버 API 키가 구성되지 않았습니다.");
  }

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;
  const prompt = `Translate the following literary/poetic sentence into the language with ISO 639-1 code "${targetLang}" naturally while maintaining its warm, comforting, and emotional tone. Respond ONLY with the translated text without any explanation, markdown, prefix, or quotation marks:\n\n"${text}"`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        contents: [{
          parts: [{ text: prompt }]
        }]
      })
    });

    if (!response.ok) {
      const errJson = await response.json();
      console.error("Gemini Translation API Error:", errJson);
      throw new HttpsError("internal", errJson.error?.message || "Gemini 번역 API 호출 실패");
    }

    const resData = await response.json();
    const translatedText = resData.candidates?.[0]?.content?.parts?.[0]?.text || "";

    return {
      translatedText: translatedText.trim()
    };
  } catch (err) {
    console.error("번역 에러 발생:", err);
    throw new HttpsError("internal", err.message || "번역 처리 중 문제가 발생했습니다.");
  }
});

// 2. 음성 발음 평가 프록시 함수 (Gemini 1.5 Flash 텍스트 분석 이용 - v2)
exports.evaluatePronunciation = onCall({
  secrets: ["GEMINI_API_KEY"],
  timeoutSeconds: 60,
  memory: "256MiB"
}, async (request) => {
  const { originalText, audioBase64, mimeType } = request.data || {};
  if (!originalText || !audioBase64) {
    throw new HttpsError("invalid-argument", "평가에 필요한 정보(오디오 데이터 등)가 누락되었습니다.");
  }

  let isPremium = false;
  let hasFreeCount = false;
  const uid = request.auth ? request.auth.uid : null;

  if (uid) {
    const userDoc = await admin.firestore().collection("users").doc(uid).get();
    if (userDoc.exists) {
      const data = userDoc.data();
      if (data.premium === true) {
        isPremium = true;
      }
      if (typeof data.free_evals === "number" && data.free_evals > 0) {
        hasFreeCount = true;
      }
    } else {
      hasFreeCount = true;
      await admin.firestore().collection("users").doc(uid).set({ free_evals: 3 }, { merge: true });
    }
  }

  const apiKey = process.env.GEMINI_API_KEY || request.data.apiKey;
  if (!apiKey) {
    throw new HttpsError("failed-precondition", "서버 API 키가 구성되지 않았습니다.");
  }

  if (!request.data.apiKey && !isPremium && !hasFreeCount) {
    throw new HttpsError("permission-denied", "무료 평가 횟수가 소진되었습니다. 프리미엄 결제 또는 API 키 등록이 필요합니다.");
  }

  if (!request.data.apiKey && !isPremium && hasFreeCount && uid) {
    await admin.firestore().collection("users").doc(uid).set({
      free_evals: admin.firestore.FieldValue.increment(-1)
    }, { merge: true });
  }

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;

  const prompt = `당신은 최고 수준의 아나운서 발음 코칭을 담당하는 한국어 음성학 전문가입니다.
사용자가 낭독해야 할 '원래 목표 문장'과, 사용자가 직접 녹음한 음성 파일이 제공됩니다.
제공된 음성을 직접 듣고 STT(Speech-to-Text)를 수행한 후, '원래 목표 문장'과 비교하여 발음, 억양, 속도 등을 엄밀하게 분석해 주세요.
절대 대충 평가하지 말고, 유료 프리미엄 과외를 받는 고객이 납득할 수 있는 수준의 날카롭고 전문적인 피드백을 제공해야 합니다.
만약 오디오에서 아무 소리도 들리지 않는다면 빈 소음이라고 명확히 지적해주세요.

원래 목표 문장: "${originalText}"

다음 형식의 JSON 데이터로만 응답해 주세요. 마크다운 기호나 추가 텍스트 없이 순수한 JSON만 반환해야 합니다.
{
  "score": <0~100 사이의 정수 (발음 정확도 점수)>,
  "good": "<사용자 발음의 장점과 칭찬 포인트 (다정하고 온화한 격려 톤)>",
  "improve": "<사용자가 발음을 개선할 수 있는 구체적인 피드백>",
  "bad_words": [
    {
      "word": "<원래 목표 문장에서 잘못 발음되거나 누락된 단어 (특수기호 제외)>",
      "meaning": "<이 한국어 단어의 사전적 의미나 뜻을 간결하게 설명 (한국어로 작성)>"
    }
  ]
}`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        contents: [{
          parts: [
            { text: prompt },
            {
              inlineData: {
                mimeType: mimeType || "audio/webm",
                data: audioBase64
              }
            }
          ]
        }],
        generationConfig: {
          responseMimeType: "application/json"
        }
      })
    });

    if (!response.ok) {
      const errJson = await response.json();
      console.error("Gemini Evaluation API Error:", errJson);
      throw new HttpsError("internal", errJson.error?.message || "Gemini 평가 API 호출 실패");
    }

    const resData = await response.json();
    let rawJsonString = resData.candidates?.[0]?.content?.parts?.[0]?.text || "{}";
    rawJsonString = rawJsonString.replace(/```json/g, "").replace(/```/g, "").trim();

    let result;
    try {
      result = JSON.parse(rawJsonString);
    } catch (parseErr) {
      console.error("JSON 파싱 에러:", rawJsonString);
      throw new HttpsError("internal", "AI 피드백 데이터를 분석하는 데 실패했습니다.");
    }

    return {
      score: result.score || 0,
      good: result.good || "목소리 기부 감사합니다! 따뜻한 음성이 돋보입니다.",
      improve: result.improve || "자음과 모음을 한 글자씩 차분하고 또박또박 발음해 보세요.",
      bad_words: result.bad_words || []
    };
  } catch (err) {
    throw new HttpsError("internal", err.message || "발음 평가 중 서버 오류가 발생했습니다.");
  }
});

// 3. 기존 relays 컬렉션 음성 기부 시 무료 평가 횟수 월간 보상 트리거
exports.onVoiceDonated = onDocumentCreated("relays/{docId}", async (event) => {
  const data = event.data ? event.data.data() : null;
  if (!data || !data.userId) return;
  await grantMonthlyVoiceReward(data.userId);
});

// 4. 신규 voice_relays 컬렉션 음성 이어읽기 등록 시 무료 평가 횟수 월간 보상 트리거
exports.onVoiceRelayCreated = onDocumentCreated("voice_relays/{docId}", async (event) => {
  const data = event.data ? event.data.data() : null;
  if (!data || !data.userId) return;
  await grantMonthlyVoiceReward(data.userId);
});

// 5. 포트원(PortOne v2) 실전 결제 사후 위변조 검증 & 원장 기록 (onCall)
// PORTONE_API_SECRET 미등록 상태에서도 배포 가능하도록 런타임 process.env 체크 적용
exports.verifyPortOnePayment = onCall({
  timeoutSeconds: 30,
  memory: "256MiB"
}, async (request) => {
  const { paymentId, expectedAmount, bookId, option } = request.data || {};
  if (!paymentId) {
    throw new HttpsError("invalid-argument", "paymentId가 누락되었습니다.");
  }

  const apiSecret = process.env.PORTONE_API_SECRET;
  if (!apiSecret) {
    throw new HttpsError("failed-precondition", "서버 PORTONE_API_SECRET 환경변수가 구성되지 않았습니다.");
  }

  try {
    const response = await fetch(`https://api.portone.io/payments/${encodeURIComponent(paymentId)}`, {
      method: "GET",
      headers: {
        "Authorization": `PortOne ${apiSecret}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("포트원 결제 조회 실패:", response.status, errText);
      throw new HttpsError("internal", "포트원 결제 조회에 실패했습니다.");
    }

    const payment = await response.json();
    const actualAmount = payment.amount?.total;
    const status = payment.status;

    if (status !== "PAID") {
      throw new HttpsError("failed-precondition", `결제 미완료 상태입니다: ${status}`);
    }

    if (expectedAmount && Number(actualAmount) !== Number(expectedAmount)) {
      throw new HttpsError("permission-denied", `결제 금액 불일치(위변조 의심): 결제금액(${actualAmount}) != 요청금액(${expectedAmount})`);
    }

    const uid = request.auth ? request.auth.uid : null;
    const paidAt = payment.paidAt || new Date().toISOString();
    const db = admin.firestore();

    await db.collection("payments").doc(String(paymentId)).set({
      paymentId: String(paymentId),
      uid: uid,
      bookId: bookId || null,
      option: option || null,
      paidAmount: Number(actualAmount) || 0,
      status: "PAID",
      paidAt: paidAt,
      verifiedAt: admin.firestore.FieldValue.serverTimestamp(),
      source: "verifyPortOnePayment"
    }, { merge: true });

    if (uid && bookId) {
      await db.collection("users").doc(uid).set({
        purchasedBooks: admin.firestore.FieldValue.arrayUnion(String(bookId)),
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      }, { merge: true });
    }

    return {
      success: true,
      paymentId: paymentId,
      paidAmount: actualAmount,
      status: status,
      paidAt: paidAt
    };
  } catch (err) {
    if (err instanceof HttpsError) throw err;
    console.error("포트원 결제 검증 중 에러:", err);
    throw new HttpsError("internal", err.message || "결제 검증 처리 중 오류가 발생했습니다.");
  }
});

// 6. 포트원(PortOne v2) 비동기 결제 웹훅 수신기 (onRequest)
exports.portOneWebhook = onRequest({
  cors: true,
  timeoutSeconds: 30,
  memory: "256MiB"
}, async (req, res) => {
  if (req.method !== "POST") {
    res.status(405).json({ ok: false, error: "Method Not Allowed" });
    return;
  }

  const body = req.body || {};
  const paymentId = body.data?.paymentId || body.payment_id || body.paymentId;
  if (!paymentId) {
    res.status(400).json({ ok: false, error: "Missing paymentId in webhook payload" });
    return;
  }

  const apiSecret = process.env.PORTONE_API_SECRET;
  if (!apiSecret) {
    res.status(503).json({ ok: false, error: "PORTONE_API_SECRET is not configured" });
    return;
  }

  try {
    const response = await fetch(`https://api.portone.io/payments/${encodeURIComponent(paymentId)}`, {
      method: "GET",
      headers: {
        "Authorization": `PortOne ${apiSecret}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("포트원 웹훅 재조회 실패:", response.status, errText);
      res.status(502).json({ ok: false, error: "Failed to query PortOne payment status" });
      return;
    }

    const payment = await response.json();
    const status = payment.status || "UNKNOWN";
    const paidAmount = payment.amount?.total || 0;
    const paidAt = payment.paidAt || new Date().toISOString();

    await admin.firestore().collection("payments").doc(String(paymentId)).set({
      paymentId: String(paymentId),
      status: status,
      paidAmount: Number(paidAmount) || 0,
      paidAt: paidAt,
      webhookType: body.type || null,
      webhookReceivedAt: admin.firestore.FieldValue.serverTimestamp(),
      source: "portOneWebhook"
    }, { merge: true });

    res.status(200).json({
      ok: true,
      paymentId: String(paymentId),
      status: status
    });
  } catch (err) {
    console.error("포트원 웹훅 처리 에러:", err);
    res.status(500).json({ ok: false, error: err.message || "Webhook processing failed" });
  }
});

// 7. 이메일 / 성명 기반 7대 시험 성적 일괄 조회 및 통합 exam_results 동기화 (onCall)
exports.lookupExamResultsByEmail = onCall({
  timeoutSeconds: 30,
  memory: "256MiB"
}, async (request) => {
  const { email, studentName, syncToUnified } = request.data || {};
  const cleanEmail = normalizeEmail(email);
  const cleanName = String(studentName || "").trim();
  const normName = normalizeName(cleanName);

  if (!cleanEmail && !normName) {
    throw new HttpsError("invalid-argument", "email 또는 studentName 중 하나 이상을 입력해야 합니다.");
  }

  const db = admin.firestore();
  const bestByExam = {};

  function considerRecord(examId, score, ts, sourceCol) {
    const validScore = normalizeScoreValue(score);
    if (validScore === null) return;
    const prev = bestByExam[examId];
    if (!prev || validScore > prev.score || (validScore === prev.score && ts > prev.ts)) {
      bestByExam[examId] = {
        examId: examId,
        score: validScore,
        ts: ts,
        sourceCollection: sourceCol
      };
    }
  }

  function matchesTarget(docData) {
    if (!docData) return false;
    const docEmail = normalizeEmail(docData.email);
    const docName = normalizeName(docData.studentName);
    if (cleanEmail && docEmail && docEmail === cleanEmail) return true;
    if (normName && docName && docName === normName) return true;
    return false;
  }

  // 7-1. 기초 4대 시험 컬렉션 조회
  for (const [examId, colName] of Object.entries(BASIC_EXAM_COLLECTIONS)) {
    let docs = [];
    if (cleanEmail) {
      try {
        const emailSnap = await db.collection(colName).where("email", "==", cleanEmail).limit(50).get();
        docs = docs.concat(emailSnap.docs);
      } catch (_) {}
    }
    if (normName) {
      try {
        const recentSnap = await db.collection(colName).orderBy("submittedAt", "desc").limit(300).get();
        docs = docs.concat(recentSnap.docs);
      } catch (_) {
        const fallbackSnap = await db.collection(colName).limit(300).get();
        docs = docs.concat(fallbackSnap.docs);
      }
    }
    for (const d of docs) {
      const data = d.data();
      if (!matchesTarget(data)) continue;
      considerRecord(examId, data.score100, parseTimestampMs(data.submittedAt, Date.now()), colName);
    }
  }

  // 7-2. 심화 3대 시험 컬렉션 조회
  {
    let advDocs = [];
    if (cleanEmail) {
      try {
        const emailSnap = await db.collection("dmdg_advanced_exam_submissions").where("email", "==", cleanEmail).limit(100).get();
        advDocs = advDocs.concat(emailSnap.docs);
      } catch (_) {}
    }
    if (normName) {
      try {
        const recentSnap = await db.collection("dmdg_advanced_exam_submissions").orderBy("submittedAt", "desc").limit(300).get();
        advDocs = advDocs.concat(recentSnap.docs);
      } catch (_) {
        const fallbackSnap = await db.collection("dmdg_advanced_exam_submissions").limit(300).get();
        advDocs = advDocs.concat(fallbackSnap.docs);
      }
    }
    for (const d of advDocs) {
      const data = d.data();
      if (!data || !ADVANCED_EXAM_IDS.includes(data.examId)) continue;
      if (!matchesTarget(data)) continue;
      considerRecord(data.examId, data.score100, parseTimestampMs(data.submittedAt || data.ts, Date.now()), "dmdg_advanced_exam_submissions");
    }
  }

  // 7-3. 통합 exam_results 컬렉션 조회
  {
    let unifiedDocs = [];
    if (cleanEmail) {
      try {
        const emailSnap = await db.collection("exam_results").where("email", "==", cleanEmail).limit(100).get();
        unifiedDocs = unifiedDocs.concat(emailSnap.docs);
      } catch (_) {}
    }
    if (normName) {
      try {
        const nameSnap = await db.collection("exam_results").where("studentNameNormalized", "==", normName).limit(100).get();
        unifiedDocs = unifiedDocs.concat(nameSnap.docs);
      } catch (_) {}
    }
    for (const d of unifiedDocs) {
      const data = d.data();
      if (!data || !data.examId || data.isSummary === true) continue;
      if (!matchesTarget(data)) continue;
      considerRecord(data.examId, data.score100, parseTimestampMs(data.submittedAt, Date.now()), "exam_results");
    }
  }

  const scores = {};
  for (const [examId, info] of Object.entries(bestByExam)) {
    scores[examId] = info.score;
  }

  let syncedSummaryId = null;
  if (syncToUnified === true && Object.keys(bestByExam).length > 0) {
    const hashSeed = cleanEmail || normName;
    const summaryId = "summary_" + crypto.createHash("sha256").update(hashSeed).digest("hex").slice(0, 24);
    await db.collection("exam_results").doc(summaryId).set({
      isSummary: true,
      email: cleanEmail || null,
      studentName: cleanName || null,
      studentNameNormalized: normName || null,
      scores: scores,
      details: bestByExam,
      matchedCount: Object.keys(bestByExam).length,
      syncedAt: admin.firestore.FieldValue.serverTimestamp()
    }, { merge: true });
    syncedSummaryId = summaryId;
  }

  return {
    matchedCount: Object.keys(bestByExam).length,
    scores: scores,
    details: bestByExam,
    syncedSummaryId: syncedSummaryId
  };
});

// 8. A.C.E.S PDF 성적표 및 유료 전자책 15분 만료 보안 다운로드 URL 발급 (onCall)
exports.issueSecureReportUrl = onCall({
  timeoutSeconds: 30,
  memory: "256MiB"
}, async (request) => {
  if (!request.auth || !request.auth.uid) {
    throw new HttpsError("unauthenticated", "보안 다운로드 링크 발급을 위해 로그인이 필요합니다.");
  }

  const uid = request.auth.uid;
  const { storagePath, type, bookId } = request.data || {};
  if (!storagePath || typeof storagePath !== "string") {
    throw new HttpsError("invalid-argument", "storagePath가 누락되었습니다.");
  }

  const cleanPath = storagePath.replace(/^\/+/, "");
  if (cleanPath.includes("..") || cleanPath.includes("\\")) {
    throw new HttpsError("invalid-argument", "허용되지 않은 파일 경로입니다.");
  }

  const db = admin.firestore();

  if (type === "report") {
    if (!cleanPath.startsWith(`reports/${uid}/`)) {
      throw new HttpsError("permission-denied", "본인의 A.C.E.S 성적표 리포트만 다운로드할 수 있습니다.");
    }
  } else if (type === "ebook") {
    if (!bookId || typeof bookId !== "string") {
      throw new HttpsError("invalid-argument", "전자책/오디오북 조회에는 bookId가 필요합니다.");
    }
    if (!cleanPath.startsWith(`ebooks/${bookId}/`)) {
      throw new HttpsError("permission-denied", "요청한 도서 경로와 bookId가 일치하지 않습니다.");
    }

    let hasPurchased = false;
    const userSnap = await db.collection("users").doc(uid).get();
    if (userSnap.exists) {
      const purchasedBooks = userSnap.data().purchasedBooks;
      if (Array.isArray(purchasedBooks) && purchasedBooks.includes(bookId)) {
        hasPurchased = true;
      }
    }

    if (!hasPurchased) {
      const paySnap = await db.collection("payments")
        .where("uid", "==", uid)
        .where("bookId", "==", bookId)
        .where("status", "==", "PAID")
        .limit(1)
        .get();
      if (!paySnap.empty) {
        hasPurchased = true;
      }
    }

    if (!hasPurchased) {
      throw new HttpsError("permission-denied", "결제 완료 내역이 확인되지 않아 다운로드 링크를 발급할 수 없습니다.");
    }
  } else {
    throw new HttpsError("invalid-argument", "지원하지 않는 type 입니다. ('report' 또는 'ebook')");
  }

  const expiresMs = Date.now() + 15 * 60 * 1000;
  try {
    const file = admin.storage().bucket().file(cleanPath);
    const [signedUrl] = await file.getSignedUrl({
      action: "read",
      expires: expiresMs
    });
    return {
      url: signedUrl,
      storagePath: cleanPath,
      expiresAt: new Date(expiresMs).toISOString()
    };
  } catch (err) {
    console.error("Signed URL 발급 오류:", err);
    throw new HttpsError("internal", err.message || "보안 다운로드 링크 생성에 실패했습니다.");
  }
});
