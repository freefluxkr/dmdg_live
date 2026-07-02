# 🍊 당목담글 - 마음을 이어주는 따스한 목소리 릴레이 PWA

> **AI 에이전트를 위한 당목담글 프로젝트의 기술 명세 및 온보딩 가이드입니다. 코딩 또는 기능 개선 작업을 시작하기 전에 아래의 구조와 표준을 반드시 숙지하고 준수해 주세요.**

---

## 1. ⚙️ 프로젝트 개요
당목담글은 사용자가 '행복한가'의 따뜻한 글귀(마중물 편지)를 감상하고, 본인의 마이크로 직접 목소리를 녹음해 마음을 이어나가는 **오프라인 우선(Offline-First) 무료 PWA 웹 애플리케이션**입니다. 
사용자 음성 재생에 이어, 다정하고 귀여운 일본어 구어체 공감 멘트가 Web Speech API(TTS) 엔진을 통해 동시에/순차적으로 낭독되는 감성 오디오북 기능을 지원합니다.

---

## 2. 🛠 기술 스택 (Tech Stack)
* **Frontend**: Pure HTML5, Tailwind CSS (CDN), Lucide Icons, Google Fonts
* **Local Database**: [Dexie.js](https://dexie.org/) (IndexedDB wrapper) - 버전 3 스키마 구성
* **Backend Database**: Firebase Firestore v10.8.0 (Compat SDK)
* **Scraper**: Python 3.10+ (BeautifulSoup4, Firebase Admin SDK)
* **Deployment**: GitHub Pages (웹 앱), GitHub Actions (주간 자동 크롤러 스케줄러)

---

## 3. 📂 핵심 폴더 및 파일 구조
* **[index.html](file:///c:/Users/tuesv/Downloads/DMDG_LIVE_CODE/index.html)**: 싱글 페이지 웹 앱(SPA)의 모든 UI 마크업, CSS 스타일, 로컬 상태 관리 및 오디오 재생/녹음 등 핵심 자바스크립트 로직이 통합되어 있습니다.
* **[happy_scrapper.py](file:///c:/Users/tuesv/Downloads/DMDG_LIVE_CODE/happy_scrapper.py)**: '행복한가' 웹사이트에서 일상스토리 및 문화생활정보 카테고리의 글귀를 수집해 Firestore에 업로드하는 증분 적재 크롤러 스크립트입니다.
* **[sw.js](file:///c:/Users/tuesv/Downloads/DMDG_LIVE_CODE/sw.js)**: 오프라인 모드 구동을 위한 캐시 생명주기 및 네트워크 패치 처리를 담당하는 서비스 워커입니다.
* **[manifest.json](file:///c:/Users/tuesv/Downloads/DMDG_LIVE_CODE/manifest.json)**: PWA를 스마트폰 및 데스크톱 홈 화면에 독립 앱으로 설치하기 위한 명세서입니다.
* **[serviceAccountKey.json](file:///c:/Users/tuesv/Downloads/DMDG_LIVE_CODE/serviceAccountKey.json)**: Python 크롤러가 `dmdg-live` Firestore 데이터베이스에 쓰기 작업을 수행하기 위한 Firebase Admin SDK의 비공개 자격증명 키 파일입니다.

---

## 4. 📐 핵심 구현 지침 및 코딩 표준 (Strict Rules)

### 📱 A. iOS Safari(아이폰) TTS 잠금해제 필수 (`unlockTts`)
* **제약**: iOS Safari는 반드시 **사용자가 화면을 직접 탭하는 순간(동기적 이벤트 핸들러)**에만 TTS(`speechSynthesis.speak`) 활성화를 허용합니다. 비동기 작업(예: 오디오 디코딩 완료 후 실행되는 비동기 체인) 내부에서 TTS를 호출하면 소리가 차단됩니다.
* **해결 표준**: 사용자가 [오디오북 재생], [이전/일시정지/다음], [릴레이 리스트 카드]를 클릭하는 즉시 **`unlockTts()`**를 호출하여 무음 문자(`" "`)를 1회 발화하도록 하여 오디오 세션 잠금을 우선 해제해야 합니다.

### 🎧 B. 오디오 겹침 방지 및 순차 재생 (Promise 기반)
* **제약**: 한국어 녹음 목소리 재생과 일본어 TTS 낭독이 서로 겹치거나 꼬여서 흘러나오지 않아야 합니다.
* **해결 표준**: `audioEngine.playChunk` 함수는 반드시 `Promise`를 반환해야 하며, 한국어 원본 재생이 완료된 시점에 `resolve()`가 호출되도록 합니다. 이를 호출할 때에는 `await audioEngine.playChunk(arrayBuffer)`와 같이 **재생 종료를 대기**한 후 TTS 낭독 단계로 진입하도록 설계해야 합니다.

### 💾 C. IndexedDB 로컬 데이터베이스 (Dexie.js) 스키마
로컬 영구 캐시 저장을 위한 테이블 표준입니다:
* `personas`: 각 감정 큐레이터 정보 (`id`, `name`, `style`, `tone`, `preferredWritingStyle`)
* `primers`: Firebase Firestore로부터 로드하여 동기화한 마중물 편지 본문 (`id`, `content`, `timestamp`, `emotion`, `type` 등)
* `relays`: 사용자가 직접 녹음한 음성 레코드 및 매칭된 공감 멘트 본문 (`id`, `emotion`, `content`, `audioBlob` [바이너리 데이터], `timestamp`)

### 🕷️ D. 크롤러 증분 적재 및 일괄 처리
* **중복 제거**: 수집한 에세이 글귀는 공백을 제거한 **MD5 해시값**을 기존 Firestore 데이터들과 대조하여 오직 신규 추가된 건만 증분 업데이트합니다.
* **배치 적재**: 네트워크 트래픽 및 오버헤드 최소화를 위해 수집된 데이터는 크롤링이 100% 완료된 시점에 **`batch.commit()`**을 사용하여 일괄 적재합니다.

---

## 5. 🚀 로컬 테스트 및 구동 가이드
1. **수동 크롤러 가동**:
   ```powershell
   $env:PYTHONIOENCODING="utf-8"
   python happy_scrapper.py
   ```
2. **원격 크롤러 자동화 스케줄러**:
   * `.github/workflows/weekly_scraper.yml`을 통해 **매주 일요일 오전 5시(한국시각)**에 자동으로 GitHub Actions 환경에서 `happy_scrapper.py`가 작동됩니다.

---

## 🔑 6. Firebase 키 발급 및 GitHub Actions 연동 설정

### 🔓 A. Firebase Admin SDK 비공개 키 발급
GitHub Actions 클라우드 서버가 Firebase `dmdg-live` 프로젝트에 쓰기 작업을 수행하기 위해서는 관리자 권한 파일이 필요합니다.
1. **Firebase 콘솔 서비스 계정 페이지**에 접속합니다.
   * [Firebase Console - Service Accounts](https://console.firebase.google.com/u/0/project/dmdg-live/settings/serviceaccounts/adminsdk)
2. 화면 하단에 있는 파란색 **[새 비공개 키 생성]** 버튼을 클릭합니다.
3. 안내 팝업창에서 **[키 생성]** 버튼을 누릅니다.
4. 컴퓨터에 다운로드된 `dmdg-live-firebase-adminsdk-xxxx.json` 파일을 보관합니다.
   * *주의: 이 키 파일은 외부로 유출되면 데이터베이스 권한을 뺏기므로 깃허브 코드에는 올리지 말고 절대 보안을 유지해 주세요.*

### 🔒 B. GitHub Secrets (비밀 키) 등록
보안 유지를 위해 위에서 다운로드한 키의 텍스트 내용을 GitHub 클라우드 저장소 비밀 데이터 공간에 저장합니다.
1. 내 프로젝트 깃허브 저장소 주소에 접속합니다.
   * [dmdg_live GitHub Repository](https://github.com/freefluxkr/dmdg_live)
2. 상단 메뉴 탭 중에서 **[Settings]**를 클릭합니다.
3. 왼쪽 사이드바 메뉴에서 **[Secrets and variables]** ➔ **[Actions]**를 클릭합니다.
4. **Repository secrets** 영역의 초록색 **[New repository secret]** 버튼을 클릭합니다.
5. 아래와 같이 값을 채워 넣고 **[Add secret]**을 누릅니다:
   * **Name**: `FIREBASE_SERVICE_ACCOUNT_KEY`
   * **Secret**: (다운로드했던 `.json` 키 파일을 메모장으로 연 후, 내부의 `{ ... }` 괄호를 포함한 전체 텍스트를 그대로 복사해서 붙여넣습니다.)

### 🚀 C. 로컬 노트북 개발 환경 세팅 방법 (New Laptop)
다른 노트북이나 개발 환경을 새로 세팅할 때 수동 크롤러를 구동하는 방법입니다.
1. **Git 저장소 복제 (Clone)**:
   ```bash
   git clone https://github.com/freefluxkr/dmdg_live.git
   cd dmdg_live
   ```
2. **필요 파이썬 라이브러리 설치**:
   ```bash
   pip install beautifulsoup4 firebase-admin
   ```
3. **로컬 실행용 키 파일 복사**:
   * 다운로드했던 `.json` 파일의 이름을 **`serviceAccountKey.json`**으로 변경합니다.
   * 이 파일을 복제한 프로젝트 폴더의 최상위 경로(`happy_scrapper.py`가 있는 폴더)에 넣어둡니다.
   * *(.gitignore에 등록되어 있으므로 원격 깃허브에 키 파일이 올라가지 않습니다.)*
4. **수동 크롤러 동작 테스트**:
   ```bash
   $env:PYTHONIOENCODING="utf-8"
   python happy_scrapper.py
   ```

---

## 💳 7. PayPal MCP 연동 설정 가이드

IDE 내에서 PayPal 관련 API 도구들을 활용하기 위한 설정 가이드입니다.

### 🔓 A. PayPal Developer 샌드박스 인증 정보 준비
1. [PayPal Developer Dashboard](https://developer.paypal.com/)에 로그인합니다.
2. **Apps & Credentials** 페이지에서 Sandbox용 **Client ID**와 **Secret**을 발급받거나 확인합니다.
3. 테스트용 **Sandbox Access Token**을 미리 메모해 둡니다.

### ⚙️ B. IDE 글로벌 MCP 설정 반영
글로벌 MCP 설정 파일인 **[mcp_config.json](file:///c:/Users/tuesv/.gemini/config/mcp_config.json)**에 페이팔 서버 정보를 추가합니다.

> [!IMPORTANT]
> PayPal MCP 서버 구동 시, 활성화할 API 기능을 지정하는 `"--tools=all"` 인자(args)가 반드시 포함되어야 합니다. 그렇지 않으면 `initialize` 단계에서 에러가 발생합니다.

* **설정 파일 위치**: `C:\Users\tuesv\.gemini\config\mcp_config.json`
* **설정 예시**:
```json
{
  "mcpServers": {
    "paypal-mcp-server": {
      "$typeName": "exa.cascade_plugins_pb.CascadePluginCommandTemplate",
      "command": "npx",
      "args": [
        "-y",
        "@paypal/mcp",
        "--tools=all"
      ],
      "env": {
        "PAYPAL_ACCESS_TOKEN": "YOUR_PAYPAL_ACCESS_TOKEN",
        "PAYPAL_ENVIRONMENT": "SANDBOX"
      }
    }
  }
}
```
* **적용 방법**: 설정 저장 후 IDE를 재시작하거나 MCP 서버를 다시 로드합니다.

