const { onCall, HttpsError } = require("firebase-functions/v2/https");
const { onDocumentCreated } = require("firebase-functions/v2/firestore");
const { setGlobalOptions } = require("firebase-functions/v2");
const admin = require("firebase-admin");

admin.initializeApp();

// 글로벌 설정 적용: 2세대 함수 배포 지역 및 오류가 있는 기본 compute 계정 우회를 위한 서비스 계정 지정
setGlobalOptions({
  region: "us-central1",
  serviceAccount: "dmdg-live@appspot.gserviceaccount.com"
});

// 1. 텍스트 번역 프록시 함수 (Gemini 2.5 Flash 이용 - v2)
exports.translateText = onCall({
  secrets: ["GEMINI_API_KEY"],
  timeoutSeconds: 60,
  memory: "256MiB"
}, async (request) => {
  // v2에서는 파라미터가 request.data에 들어있습니다.
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
  let uid = request.auth ? request.auth.uid : null;

  if (uid) {
    const userDoc = await admin.firestore().collection("users").doc(uid).get();
    if (userDoc.exists) {
      const data = userDoc.data();
      if (data.premium === true) {
        isPremium = true;
      }
      if (typeof data.free_evals === 'number' && data.free_evals > 0) {
        hasFreeCount = true;
      }
    } else {
      // 최초 사용자일 경우 기본 무료 횟수 3회 부여 (DB 생성)
      hasFreeCount = true;
      await admin.firestore().collection("users").doc(uid).set({ free_evals: 3 }, { merge: true });
    }
  }

  const apiKey = process.env.GEMINI_API_KEY || request.data.apiKey;
  if (!apiKey) {
    throw new HttpsError("failed-precondition", "서버 API 키가 구성되지 않았습니다.");
  }

  // 권한 검증: 사용자가 개별 API 키를 보내지 않았는데, 프리미엄도 아니고 무료 횟수도 없으면 차단
  if (!request.data.apiKey && !isPremium && !hasFreeCount) {
    throw new HttpsError("permission-denied", "무료 평가 횟수가 소진되었습니다. 프리미엄 결제 또는 API 키 등록이 필요합니다.");
  }

  // 서버 API 키를 사용하면서 프리미엄이 아닌 경우 무료 횟수 차감
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
    rawJsonString = rawJsonString.replace(/```json/g, '').replace(/```/g, '').trim();
    
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

// 3. 기부 시 무료 평가 횟수 월간 제한 트리거 (월 최대 3회 제한)
exports.onVoiceDonated = onDocumentCreated("relays/{docId}", async (event) => {
  const data = event.data.data();
  if (!data || !data.userId) return;

  const uid = data.userId;
  const now = new Date();
  // YYYY-MM 형식의 현재 달 문자열 생성
  const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
  const maxRewardsPerMonth = 3;

  const userRef = admin.firestore().collection("users").doc(uid);
  
  await admin.firestore().runTransaction(async (transaction) => {
    const userDoc = await transaction.get(userRef);
    if (!userDoc.exists) {
      // 최초 기부인 경우 기본값 3회 + 보상 5회 = 8회
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
    
    // 달이 바뀌었으면 카운트 초기화
    if (currentRewardMonth !== currentMonth) {
      currentRewardMonth = currentMonth;
      monthlyCount = 0;
    }

    // 한도(3회) 미만이면 보상 지급
    if (monthlyCount < maxRewardsPerMonth) {
      transaction.set(userRef, {
        free_evals: admin.firestore.FieldValue.increment(5),
        reward_month: currentRewardMonth,
        monthly_reward_count: monthlyCount + 1
      }, { merge: true });
    }
    // 3회 도달 또는 초과 시 보상 없이 트랜잭션 종료
  });
});
