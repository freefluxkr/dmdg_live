const { onCall, HttpsError } = require("firebase-functions/v2/https");
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

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new HttpsError("failed-precondition", "서버 API 키가 구성되지 않았습니다.");
  }

  const langMap = {
    'ko': 'Korean',
    'ja': 'Japanese',
    'en': 'English'
  };
  const targetLangName = langMap[targetLang] || 'English';

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;
  const prompt = `Translate the following literary/poetic sentence into ${targetLangName} naturally while maintaining its warm, comforting, and emotional tone. Respond ONLY with the translated text without any explanation, markdown, prefix, or quotation marks:\n\n"${text}"`;

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
  const { originalText, recognizedText } = request.data || {};
  if (!originalText || !recognizedText) {
    throw new HttpsError("invalid-argument", "평가에 필요한 정보가 누락되었습니다.");
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new HttpsError("failed-precondition", "서버 API 키가 구성되지 않았습니다.");
  }

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
  
  const prompt = `당신은 한국어 발음 교육 및 코칭 전문가입니다.
사용자가 낭독해야 할 '원래 목표 문장'과, 사용자의 음성을 Web Speech API로 인식한 '음성 인식 결과' 텍스트가 제공됩니다.
음성 인식 결과에서 발생한 오타나 누락을 분석하여, 사용자가 어느 발음(특히 어느 단어의 자음/모음/받침)이 부정확했는지 유추해 정밀하고 날카롭게 평가해 주세요.

원래 목표 문장: "${originalText}"
음성 인식 결과: "${recognizedText}"

다음 형식의 JSON 데이터로만 응답해 주세요. 마크다운 기호나 추가 텍스트 없이 순수한 JSON만 반환해야 합니다.
{
  "score": <0~100 사이의 정수 (발음 정확도 유추 점수)>,
  "good": "<사용자 발음의 장점과 칭찬 포인트 (다정하고 온화한 격려 톤)>",
  "improve": "<사용자가 발음을 개선할 수 있는 구체적인 피드백 (음성 인식 오류를 바탕으로 유추한 교정 팁)>"
}`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        contents: [{
          parts: [{ text: prompt }]
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
      improve: result.improve || "자음과 모음을 한 글자씩 차분하고 또박또박 발음해 보세요."
    };
  } catch (err) {
    console.error("발음 평가 에러 발생:", err);
    throw new HttpsError("internal", err.message || "발음 평가 중 서버 오류가 발생했습니다.");
  }
});
