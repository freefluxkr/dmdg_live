# 🔑 DMDG 프로젝트 인증 정보 및 API KEY 위치 가이드

프로젝트 내외에 분산되어 있는 각 서비스의 API Key, 토큰, 계정 자격증명 파일들의 위치를 한눈에 정리한 보안 레퍼런스 문서입니다.

---

### 📂 1. 주요 API KEY 및 인증 파일 위치 맵

| 서비스 / 플랫폼 | 인증 정보 유형 | 파일 위치 | 설명 및 용도 |
| :--- | :--- | :--- | :--- |
| **위키독스 (WikiDocs)** | API Token | [DMDG_LIV_작업_README.md](file:///c:/Users/tuesv/Downloads/DMDG_LIVE_CODE/DMDG_LIV_작업_README.md#L84-L85) | 위키독스 전자책/페이지 생성 및 수정을 위한 Bearer/Token 인증키 (`a85dcdacf...`) |
| **Firebase Firestore** | Admin SDK 비공개 키 | [serviceAccountKey.json](file:///c:/Users/tuesv/Downloads/DMDG_LIVE_CODE/serviceAccountKey.json) | Python 크롤러(`happy_scrapper.py`) 및 관리자 Firestore 쓰기 권한 (`dmdg-live`) |
| **Firebase API Key** | 서비스 계정 키 백업 | [firebase-adminsdk-api_key.json](file:///c:/Users/tuesv/Downloads/DMDG_LIVE_CODE/firebase-adminsdk-api_key.json) | Firebase 서비스 계정 키 동일 사본 |
| **PayPal Sandbox** | Access Token & 대시보드 | [PayPal 가입계정.txt](file:///c:/Users/tuesv/Downloads/DMDG_LIVE_CODE/PayPal%20%EA%B0%80%EC%9E%85%EA%B3%84%EC%A0%95.txt) <br> [mcp_config.json](file:///c:/Users/tuesv/.gemini/config/mcp_config.json) | 페이팔 개발자 앱 접속 URL 및 글로벌 MCP 서버 Access Token (`A21AALL2r...`) |
| **GitHub** | Personal Access Token | [mcp_config.json](file:///c:/Users/tuesv/.gemini/config/mcp_config.json#L38) | GitHub MCP 서버 연동용 개인 액세스 토큰 (`ghp_mPxfj...`) |
| **Telegram Bot** | Bot Token & Chat ID | [.agents/telegram/send_complete.py](file:///c:/Users/tuesv/Downloads/DMDG_LIVE_CODE/.agents/telegram/send_complete.py#L4-L5) | 스마트폰 비서 텔레그램 알림 발송용 봇 토큰 (`8837085399:...`) 및 챗 ID |

---

### ⚠️ 보안 주의사항
* 위 키 파일들 중 특히 `serviceAccountKey.json`과 `mcp_config.json`의 토큰들은 관리자 권한을 가지므로 외부 공개 저장소에 커밋되지 않도록 `.gitignore`에 등록되어 있습니다.
* 외부 협업 시에는 해당 키 값들을 절대 노출하지 마시고, 환경 변수(`.env`) 또는 GitHub Secrets를 활용해 관리해 주세요.
