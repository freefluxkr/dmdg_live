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

// 2. 음성 발음 평가 프록시 함수 (Gemini 2.5 Flash 오디오 분석 이용 - v2)
exports.evaluatePronunciation = onCall({
  secrets: ["GEMINI_API_KEY"],
  timeoutSeconds: 120, // 음성 분석 시간 확보
  memory: "512MiB"
}, async (request) => {
  // v2에서는 파라미터가 request.data에 들어있습니다.
  const { originalText, audioBase64, mimeType } = request.data || {};
  if (!originalText || !audioBase64) {
    throw new HttpsError("invalid-argument", "평가에 필요한 정보가 누락되었습니다.");
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new HttpsError("failed-precondition", "서버 API 키가 구성되지 않았습니다.");
  }

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;
  
  const systemPrompt = `당신은 한국어 발음 교육 및 코칭 전문가입니다.
사용자가 낭독한 오디오 파일과 원래 목표 문장(originalText)이 제공됩니다.
사용자의 발음 음성을 직접 자세히 듣고, 원래 문장과 비교하여 정밀하게 평가해 주세요.

다음 형식의 JSON 데이터로만 응답해 주세요. 마크다운 기호(예: \`\`\`json)나 추가 텍스트 없이 순수한 JSON만 반환해야 합니다:
{
  "score": 0~100 사이의 정수 (원래 문장과 발음 일치도 점수),
  "good": "사용자 발음의 장점과 칭찬 포인트 (다정하고 온화한 격려 톤)",
  "improve": "사용자가 발음을 개선할 수 있는 구체적인 피드백 (어느 단어나 자모 발음이 흐릿했는지, 연음이 잘 되었는지, 템포 조절 팁 등)"
}

목표 문장: "${originalText}"`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        contents: [{
          parts: [
            {
              inlineData: {
                mimeType: mimeType || "audio/webm",
                data: audioBase64
              }
            },
            {
              text: systemPrompt
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
    const rawJsonString = resData.candidates?.[0]?.content?.parts?.[0]?.text || "{}";
    
    let result;
    try {
      result = JSON.parse(rawJsonString.trim());
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
