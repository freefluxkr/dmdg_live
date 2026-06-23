# 🍊 당목담글 - Firebase 신규 이전 및 GitHub Actions 연동 가이드

나중에 다른 노트북이나 개발 환경을 새로 세팅할 때 보고 따라 할 수 있는 연동 매뉴얼입니다.

---

## 🔑 1. Firebase Admin SDK 비공개 키 발급 방법

GitHub Actions 클라우드 서버가 내 Firebase `dmdg-live` 프로젝트에 쓰기 작업을 수행하려면 관리자 권한 파일이 필요합니다.

1. **Firebase 콘솔 서비스 계정 페이지**에 접속합니다.
   * [Firebase Console - Service Accounts](https://console.firebase.google.com/u/0/project/dmdg-live/settings/serviceaccounts/adminsdk)
2. 화면 하단에 있는 파란색 **[새 비공개 키 생성]** 버튼을 클릭합니다.
3. 안내 팝업창에서 **[키 생성]** 버튼을 누릅니다.
4. 컴퓨터에 다운로드된 `dmdg-live-firebase-adminsdk-xxxx.json` 파일을 보관합니다.
   * *주의: 이 키 파일은 외부로 유출되면 데이터베이스 권한을 뺏기므로 깃허브 코드에는 올리지 말고 절대 보안을 유지해 주세요.*

---

## 🔒 2. GitHub Secrets (비밀 키) 등록 방법

보안 유지를 위해 위에서 다운로드한 키의 텍스트 내용을 GitHub 클라우드 저장소 비밀 데이터 공간에 저장합니다.

1. 내 프로젝트 깃허브 저장소 주소에 접속합니다.
   * [dmdg_live GitHub Repository](https://github.com/freefluxkr/dmdg_live)
2. 상단 메뉴 탭 중에서 **[Settings]**를 클릭합니다.
3. 왼쪽 사이드바 메뉴에서 **[Secrets and variables]** ➔ **[Actions]**를 클릭합니다.
4. **Repository secrets** 영역의 초록색 **[New repository secret]** 버튼을 클릭합니다.
5. 아래와 같이 값을 채워 넣고 **[Add secret]**을 누릅니다:
   * **Name**: `FIREBASE_SERVICE_ACCOUNT_KEY`
   * **Secret**: (다운로드했던 `.json` 키 파일을 메모장으로 연 후, 내부의 `{ ... }` 괄호를 포함한 전체 텍스트를 그대로 복사해서 붙여넣습니다.)

---

## 🚀 3. 로컬 노트북 개발 환경 세팅 방법 (New Laptop)

나중에 다른 노트북에서 이 프로젝트 소스코드를 다운로드하고 수동 크롤러를 구동하고 싶을 때 순서입니다.

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
   * **1단계**에서 다운로드했던 `.json` 파일의 이름을 **`serviceAccountKey.json`**으로 변경하거나 복사(Copy) 명령어를 사용합니다:
     ```powershell
     # Windows PowerShell/CMD 기준 파일명 맞추기
     copy firebase-adminsdk-api_key.json serviceAccountKey.json
     ```
   * 이 파일을 복제한 `dmdg_live` 프로젝트 폴더의 **최상위 경로(happy_scrapper.py가 있는 폴더)**에 넣어둡니다.
   * *(.gitignore에 등록되어 있으므로 원격 깃허브에 키 파일이 올라가지 않습니다.)*
4. **수동 크롤러 동작 테스트**:
   * 만약 실행 시 `ModuleNotFoundError: No module named 'bs4'` 에러가 난다면, 반드시 라이브러리를 먼저 설치해 줍니다:
     ```bash
     pip install beautifulsoup4 firebase-admin
     ```
   * 설치 후 아래 명령어로 수동 구동하여 데이터베이스를 실시간 강제 업데이트합니다:
     ```bash
     python happy_scrapper.py
     ```
     *(성공적으로 크롤링 완료 로그가 출력되며 즉시 Firestore에 동기화됩니다.)*
