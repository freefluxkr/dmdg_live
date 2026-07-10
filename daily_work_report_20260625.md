# 📝 작업 이력 보고서 - 2026-06-25 (PDF 도서 자동 빌더 구축)

금일 요청사항에 따라 진행한 웹 사이트 도서 콘텐츠 크롤링 및 챕터/파트별 고품질 PDF 전자책 자동 빌더 구축 작업의 요약 문서입니다.

---

## 📅 실시간 작업 이력 요약

금일 총 5권의 온라인 IT 도서에 대한 전용 PDF 크롤러 및 생성기 파이썬 스크립트 5개를 구축 완료했습니다.

### 1. 🐍 Let's Get IT 파이썬 프로그래밍 PDF 빌더
* **파일명**: [build_pdf_book.py](file:///c:/Users/user/Downloads/DMDG_LIVE/build_pdf_book.py)
* **대상 사이트**: `thebook.io/080251` (총 860페이지 분량)
* **저장 위치**: `pdf_chapters/` (15개 장 + 해설 노트, 총 16개 PDF 파일 생성)
* **특징**: 책 고유의 CSS 스타일을 분석해 병합 뼈대에 연동했으며, 대용량 처리를 위해 로컬 캐싱 기능과 크롬/엣지 헤드리스 프로필 잠금 방지 장치가 탑재되었습니다.

### 2. 🧠 인공지능·생성형 AI 개발 입문 PDF 빌더
* **파일명**: [build_ai_pdf_book.py](file:///c:/Users/user/Downloads/DMDG_LIVE/build_ai_pdf_book.py)
* **대상 사이트**: `wikidocs.net` (338385 ~ 338419 페이지)
* **저장 위치**: `PDF_인공지능생성형 AI 개발 입문/` (9개 Part별로 총 9개 PDF 파일 생성)
* **특징**: 구글 애드센스 광고 요소를 원천 제거하는 필터링 엔진과 WikiDocs의 글 제목(`h1.page-subject`)을 상단에 자동 복원해 주는 타이틀 인젝션 기능이 추가되었습니다.

### 3. 🤖 Hermes Agent: 성장하는 AI 에이전트 실전 가이드 PDF 빌더
* **파일명**: [build_hermes_pdf_book.py](file:///c:/Users/user/Downloads/DMDG_LIVE/build_hermes_pdf_book.py)
* **대상 사이트**: `wikidocs.net` (334919 ~ 335007 페이지)
* **저장 위치**: `PDF_3wnck Hermes Agent - 성장하는 AI 에이전트 실전 가이드/` (총 15개 PDF 파일 생성)
* **특징**: 개별 서브챕터들의 페이지 ID가 비연속적으로 존재(수정/추가 페이지 반영)하는 문제를 해결하기 위해 정확한 페이지 매핑 목록을 내장했습니다. 또한 Windows 운영체제 파일명 금지 문자(콜론 `:` 등)를 우회하여 폴더명을 안전하게 생성하도록 설계했습니다.

### 4. 💼 에르메스 에이전트(Hermes Agent) 업무 자동화 PDF 빌더
* **파일명**: [build_hermes_auto_pdf_book.py](file:///c:/Users/user/Downloads/DMDG_LIVE/build_hermes_auto_pdf_book.py)
* **대상 사이트**: `wikidocs.net` (346135 ~ 346956 페이지)
* **저장 위치**: `에르메스 에이전트(Hermes Agent) 업무  자동화/` (총 13개 PDF 파일 생성)
* **특징**: 90여 개가 넘는 비연속적 WikiDocs 페이지 ID 목록을 목차(TOC) 분석 결과에 따라 완벽하게 구조화하여 매핑했습니다.

### 5. 🤫 사장님 몰래 하는 파이썬 업무자동화 PDF 빌더
* **파일명**: [build_boss_pdf_book.py](file:///c:/Users/user/Downloads/DMDG_LIVE/build_boss_pdf_book.py)
* **대상 사이트**: `wikidocs.net` (135792 ~ 153818 페이지)
* **저장 위치**: `사장님 몰래 하는 파이썬 업무자동화/` (Ch0 ~ Ch4 별로 총 5개 PDF 파일 생성)
* **특징**: 방대한 Ch3 패키지 가이드(61개 페이지) 및 프로젝트 실전 챕터인 Ch4의 세부 구조를 완벽하게 분류해 매핑 및 병합 빌더를 완성했습니다.

---

## 💡 크롤러 및 생성기 공통 설계 특징

1. **로컬 캐싱 시스템**: 수집 중 차단(Rate limit)되거나 끊겨도 다시 실행하면 **이전에 다운로드한 HTML은 캐시 폴더(`html_cache_*`)에서 바로 읽어오므로 중단 시점부터 이어 받기가 지원**됩니다.
2. **헤드리스 브라우저 인쇄 엔진**: 시스템에 설치된 Chrome 또는 Edge 브라우저를 파이썬 백그라운드(`--headless=new`)로 구동해 HTML을 PDF로 인쇄하므로 웹 렌더링 품질이 100% 보존됩니다.
3. **독립 프로필 격리**: 사용자가 이미 크롬 브라우저를 띄워두고 있어도 충돌(Locking)되지 않도록 임시 브라우저 프로필 디렉토리를 생성하여 안정성을 대폭 향상시켰습니다.
4. **광고 차단 및 제목 복원**: 구글 애드센스(`adsbygoogle`, `ins`, `iframe`) 등 도서 레이아웃을 해치는 요소를 완벽하게 걸러내어, 원본 대제목(`page-subject`)과 구분선만 상단에 정갈하게 배치한 책 레이아웃을 제공합니다.
5. **실행 옵션**:
   - `python build_xxx.py test`: 1장 첫페이지만 시범 빌드하여 PDF 품질을 확인하는 모드입니다.
   - `python build_xxx.py`: 대기 없이 처음부터 끝까지 논스톱으로 자동 일괄 생성합니다.
   - `python build_xxx.py pause`: 장/파트별 생성이 끝날 때마다 일시 정지하여 PDF를 직접 눈으로 검수하고 엔터 키를 입력받아 진행하는 모드입니다.

---

## 🔀 Git 작업 마무리 및 로컬 파일 보관

* **Git 충돌 안전 상태 보장**: 현재 새로 작성한 파이썬 스크립트(`build_*.py`)와 캐시 폴더들은 깃에 등록되지 않은 **추적되지 않는 파일(Untracked files)** 상태입니다. 따라서 다른 컴퓨터에서 Git 작업을 수행하셨더라도, `git pull`이나 브랜치 전환 시 **파일이 꼬이거나 충돌(Conflict)을 유발하지 않으므로 전혀 걱정하지 않으셔도 됩니다.**
* 모든 파이썬 스크립트 원본 및 데이터 수집 결과물은 사용자분의 로컬 PC workspace (`c:\Users\user\Downloads\DMDG_LIVE`)에 안전하게 저장되어 보존되어 있습니다.
