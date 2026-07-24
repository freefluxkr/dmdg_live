# 📂 DMDG_LIVE 프로젝트 작업 폴더 구조 가이드

![DMDG_LIVE 폴더 구조 시각화](file:///C:/Users/user/.gemini/antigravity-ide/brain/5eba6871-ff28-40dd-92cd-69a008cfeae0/folder_structure_visual_1784163431825.png)

이 문서는 `clean_workspace.py` 실행을 통해 루트 경로가 깔끔하게 정리정돈된 후의 최신 작업 폴더 및 주요 파일 구조를 설명합니다.

---

## 🏗️ 1. 폴더 트리 구조 (Directory Tree)

```text
c:\Users\user\Downloads\DMDG_LIVE\
│
├── 📂 00_Textbook_Builders/       # [정리완료] 교재 빌드용 파이썬 스크립트 및 윈도우 배치 파일 (.bat) 모음
├── 📂 00_HTML_Caches/             # [정리완료] 크롤링 시 수집된 임시 HTML 캐시 및 장별 조각 폴더 모음
├── 📂 00_Textbooks/               # [정리완료] 최종 컴파일 완료된 PDF 결과물 및 교재 폴더 모음
├── 📂 01_Assets/                  # [정리완료] 이미지 파일 등 디자인 에셋 모음 (.png, .jpg 등)
├── 📂 02_Documents/               # [정리완료] PDF, PPTX, CSV, TXT 등 문서 및 데이터 파일 모음
├── 📂 03_Scripts/                 # [정리완료] 기타 테스트 및 유틸리티 파이썬 스크립트 모음
│
├── 📂 csv_test/                   # 판다스 데이터 실습 및 실시간 박스오피스 대시보드 공간
│   ├── bc_card_out2020_03.txt     # BC카드 소비 패턴 원본 데이터 (UTF-8)
│   ├── crawler_naver.py           # 네이버 박스오피스 영화 크롤러
│   ├── crawler_daum.py            # 다음 박스오피스 영화 크롤러
│   └── dashboard.py               # 스트림릿 기반 실시간 통합 영화 대시보드
│
├── 📂 js/                         # 당목담글 PWA 프론트엔드 자바스크립트 소스코드
│   ├── app.js                     # 렌더링, 국가별 테마, 페이팔 결제(Paywall), 번역 핵심 로직
│   ├── audio.js                   # Web Audio API 녹음/TTS 제어 엔진
│   ├── db.js                      # Dexie.js 기반 로컬 데이터베이스(IndexedDB) 연동
│   └── firebase-config.js         # 파이어베이스 초기화 설정
│
├── 📂 css/                        # PWA 공통 스타일시트 (style.css)
│
├── 📂 .agent/                     # 양방향 AI 비서 봇 소스 및 텔레그램 연동부
│   └── 📂 telegram/               # 텔레그램 봇 API 스크립트 (bot.py, send_complete.py 등)
├── 📂 agent/                      # 텔레그램 봇을 통해 파일이 드롭되는 인박스 (inbox/peggy/ 등)
│
├── 📂 .github/                    # GitHub Actions 자동 크롤러 워크플로 스케줄러
├── 📂 .venv/                      # 파이썬 3.12 가상환경 폴더 (Git 추적 대상 제외)
├── 📂 functions/                  # Firebase Cloud Functions 백엔드 소스코드
├── 📂 scratch/                    # 테스트용 임시 스크래치 스크립트 공간 (test_run.js 등)
└── 📂 당목담글/ / Subway/ / docs/  # 서비스 에셋 및 기타 문서/서브 프로젝트 리소스
```

---

## 📄 2. 루트 경로 주요 파일 설명

### 🌐 웹 애플리케이션 핵심 파일 (PWA)
* **[index.html](file:///c:/Users/user/Downloads/DMDG_LIVE/index.html)**: 싱글 페이지 웹 앱(SPA) 마크업 및 Tailwind CSS UI 구조 정의 파일.
* **[admin.html](file:///c:/Users/user/Downloads/DMDG_LIVE/admin.html)**: 크롤링 관리 및 IndexedDB 데이터 수동 동기화를 위한 관리자 대시보드.
* **[sw.js](file:///c:/Users/user/Downloads/DMDG_LIVE/sw.js)**: 오프라인 우선(Offline-First) 구동을 지원하는 PWA 서비스 워커.
* **[manifest.json](file:///c:/Users/user/Downloads/DMDG_LIVE/manifest.json)**: 스마트폰 홈 화면에 바로가기 앱으로 설치하기 위한 명세서.

### 🐍 파이썬 크롤러 및 유틸리티
* **[happy_scrapper.py](file:///c:/Users/user/Downloads/DMDG_LIVE/happy_scrapper.py)**: '행복한가' 웹사이트에서 따뜻한 글귀를 수집해 Firestore에 증분 적재하는 크롤러.
* **[clean_workspace.py](file:///c:/Users/user/Downloads/DMDG_LIVE/clean_workspace.py)**: 최상위 루트 경로를 눈부시게 청소 및 분류해 주는 정돈 스크립트 (본 구조를 만든 주역).

### ⚙️ 환경 변수 및 설정 파일
* **[.env](file:///c:/Users/user/Downloads/DMDG_LIVE/.env)**: `TELEGRAM_BOT_TOKEN` 및 `CHAT_ID`를 안전하게 로드하기 위한 로컬 환경변수 설정 파일 (복구 완료).
* **[.gitignore](file:///c:/Users/user/Downloads/DMDG_LIVE/.gitignore)**: 가상환경(`.venv`) 등 불필요한 대용량 파일이 Git에 추적되어 과부하 걸리는 것을 차단하는 무시 리스트 설정 (가상환경 예외 규칙 반영 완료).
* **[firebase.json](file:///c:/Users/user/Downloads/DMDG_LIVE/firebase.json)**: Firebase 호스팅 및 배포 구성 파일.

### 📖 업무 지침서 및 가이드라인
* **[HOMEWORK_GUIDE.md](file:///c:/Users/user/Downloads/DMDG_LIVE/HOMEWORK_GUIDE.md)**: 퇴근 후 자택 PC 환경 초기 세팅 및 소담 웹 페이팔 연동 세부 지침서.
* **[WEEKEND_TODO.md](file:///c:/Users/user/Downloads/DMDG_LIVE/WEEKEND_TODO.md)**: 주말 예정된 텔레그램 연동 복구 및 주요 작업 캘린더.
* **[GEMINI.md](file:///c:/Users/user/Downloads/DMDG_LIVE/GEMINI.md)**: AI 에이전트 전용 온보딩 규칙 및 페이팔 연동 수동 가이드라인.
* **[README.md](file:///c:/Users/user/Downloads/DMDG_LIVE/README.md)**: 당목담글 프로젝트의 전체 서비스 소개서.
