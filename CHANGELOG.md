# 📋 DMDG LIVE (dmdg-live.com) 전체 수정 및 변경 이력 (CHANGELOG)

> **공식 도메인**: [https://dmdg-live.com/](https://dmdg-live.com/)  
> **미러 저장소**: [`freefluxkr/dmdg_potal`](https://github.com/freefluxkr/dmdg_potal)  
> **배포 저장소**: [`freefluxkr/dmdg_live`](https://github.com/freefluxkr/dmdg_live)  
> **기록 책임자**: Peggy (Secretariat Lead) & Craig (Lead Systems Engineer)

---

## 📅 [2026-10-21] 세션 작업 내역 (최신 업데이트)

### 1. 우상단 [🎓 Antigravity × REA 과정 상세 안내] 링크 및 상세 커리큘럼 페이지(`curriculum.html`) 신설
* **우상단 네비게이션 버튼 갱신**:
  - 기존 팝업 모달 호출 버튼 ➔ `[🎓 Antigravity × REA 과정 상세 안내]` 링크로 승격 및 `./curriculum.html`로 직결.
* **`curriculum.html` 상세 커리큘럼 단독 웹페이지 제작 및 배포**:
  - `projects/CURRICULUM/커리큘럼 마크다운 원본 소스.md`의 전체 내용(1~5장)을 정밀 반영.
  - **오프라인 강의장 위치 안내 공식 명시 (하단 배너)**:
    - **`강의장 위치 : 신청자들의 공통 위치로 선정하여 추후 공지 (현재는 성남시 태평역 부근 예정)`**
    - 20명 모집 확정 시 신청자 거주 지역 분포를 종합 분석하여 최적의 접근성을 갖춘 강의장을 최종 확정·공지하도록 안내.
  - **직결 수강 신청 연동**:
    - `curriculum.html` 내 `[📝 과정 신청하기 (20명 달성 시 개강) ➔]` 클릭 시 `index.html?openApply=true`로 이동하여 수강 신청서가 즉시 자동 팝업되도록 UX 연계.
  - **1주차~8주차 상세 강의계획서 전수 수록**:
    - 오전 이론 해체 쇼, 오후 Hands-on 실습 랩, 포트폴리오 깃허브 빌드, 면접 대비 고난도 Q&A 24선 카드 배치.

### 2. 일일 타임테이블 신규 표준 개편 (커리큘럼 마크다운 및 연계 문서 전수 동기화)
* **신규 일일 타임테이블 확립**:
  - 🌅 **오전 세션 [09:00 ~ 12:50]**: 핵심 이론 & 라이브 해체 쇼 (4시간, 1~4교시)
  - 🍱 **점심 및 네트워킹 [12:50 ~ 13:50]**: 1시간
  - 🌇 **오후 세션 [13:50 ~ 17:40]**: Hands-on 실습 & 포트폴리오화 (4시간, 5~8교시)
  - ⚠️ **금요일 조기 종료 규칙 명시**: **매주 금요일은 7교시(16:40)에 수업 종료**
* **동기화 파일 목록**:
  - `projects/CURRICULUM/커리큘럼 마크다운 원본 소스.md`
  - `projects/CURRICULUM/반응형 웹 인쇄용 HTML.html`
  - `projects/CURRICULUM/웹 뷰어 및 랜딩페이지 삽입용 HTML.html`
  - `projects/CURRICULUM/모집공고 마크다운 원본 소스.md`
  - `projects/12. REA/CURRICULUM_ANTIGRAVITY_MCP_REA_20261207.md`
  - `projects/12. REA/COURSE_RECRUITMENT_NOTICE.md`
  - `curriculum.html`

### 3. 3대 대시보드 컬럼 5개 카드 제한 및 우측 상단 총 컨텐츠 개수 배지 균형 최적화
* **1:1:1 수직 시각 균형 달성 (각 컬럼당 상위 5개 카드만 노출)**:
  - **Column 1 (`LIVE WEB APPS`)**:
    - 노출 (5개): 말쌈, 당목담글 공식 블로그, DMDG 서재, 소담 라이브, 당목담글 보이스
    - 숨김 (1개): 방법 라이브 (`dmdg-hidden-card` 클래스 적용)
    - 우측 배지: `<span class="panel-count-badge">6 Services</span>` 유지
  - **Column 2 (`INTERACTIVE SIMULATORS`)**:
    - 노출 (5개): AI 에이전트 & SCM MLOps, REA × MCP Protocol Inspector, 크롬 공룡 랩, 윈도우 계산기 랩, 클린룸 TDD 검증기
    - 숨김 (3개): K-오피스 생존 연구소, 0원 SaaS 빌더 랩, 수학 시뮬레이터 마스터 허브 (`dmdg-hidden-card` 클래스 적용)
    - 우측 배지: `<a href=".../sim_master_hub.html" class="panel-count-badge">28 Total ➔</a>` (28종 전체 시뮬레이터 마스터 허브 직결)
  - **Column 3 (`WIKIBOOKS`)**:
    - 노출 (5개): Book 21781 REA 완벽 마스터 가이드, Book 21777 Antigravity IDE 완벽 가이드, Book 21755 모던 REA (클린룸), Book 21754 리버스 실전 바이블, Book 21753 남의 앱 뜯어보기
    - 숨김 (6권): Book 21748, Book 21747, Book 21746, Book 21733, Book 21701, Book 21658 (`dmdg-hidden-card` 클래스 적용)
    - 우측 배지: `<a href="https://dmdg.wikidocs.net/book/" class="panel-count-badge">11 Books (전체 ➔)</a>` (위키독스 전체 도서 목록 직결)
* **지능형 실시간 검색 연동 (Live Search)**:
  - 상단 검색창에 검색어 입력 시, 숨겨진 카드라도 검색 키워드에 매칭되면 즉시 노출.
  - 검색어 삭제 시 원래의 기본 5개 노출 상태로 부드럽게 복원.

### 4. 수강생 모집 온보딩 팝업 & Firebase Firestore 실시간 DB & 관리자 콘솔(`admin.html`)
* **온보딩 팝업 모달 (`rea-course-modal-backdrop`)**:
  - 포털 접속 시 《Antigravity IDE × REA 모던 역공학 & 클린룸 재구현 과정》 소개 자동 팝업 (오늘 하루 보지 않기 쿠키 지원).
  - 4대 교육 기둥, 20명 달성 시 개강 안내, 실시간 목표 게이지 바 연동.
  - 하단 오프라인 강의장 안내 명시: `강의장 위치 : 신청자들의 공통 위치로 선정하여 추후 공지 (현재는 성남시 태평역 부근 예정)`.
* **수강 신청 Form 및 데이터베이스 저장**:
  - 수집 필드: 이름, 연락처(010-XXXX-XXXX 자동 하이픈 포맷), 지역(17개 시도), 내일배움카드 소지 여부.
  - Firebase Firestore (`rea_course_applications` 컬렉션) 및 LocalStorage dual-write 회복 탄력성 저장 구조.
* **관리자 전용 대시보드 (`admin.html`)**:
  - 인증: ID `DMDG` / PW `ekdahrekarmf`.
  - 실시간 신청자 집계, 20명 달성 여부 게이지, 전체 명단 테이블, UTF-8 BOM 엑셀 CSV 원클릭 내보내기 지원.

### 5. DMDG 서재(E-Reader) 미래 3부작 연동 및 위키독스 정비
* **우상단 네비게이션**: `🎙️ 발음 교정` ➔ `📖 DMDG 서재 (E-Reader)` (`novels.html`) 교체.
* **`novels.html` 카테고리 승격**:
  - 2027 팩션 스릴러에 더해 **미래 베스트셀러 3부작** ([Book 21746](https://wikidocs.net/book/21746), [Book 21747](https://wikidocs.net/book/21747), [Book 21748](https://wikidocs.net/book/21748)) 총 48개 세부 챕터 원문 텍스트 탑재 및 TTS 음성 낭독 지원.
* **위키북스 정규 링크**: WIKIBOOKS 전체 보기 링크를 `https://dmdg.wikidocs.net/book/` 공식 도서관 주소로 확정.

---

## 📅 [2026-10-20] 세션 작업 내역

### 1. 도메인 분리 및 대표 포털 론칭
* **`malssam.com` 독립 분리**: 말쌈 우리말 사전 & 퀴즈 PWA 서비스 전용 도메인으로 분리 운영.
* **`dmdg-live.com` 대표 포털 구축**:
  - Mockup 1 (3중 유기적 페이퍼컷 웨이브 백드롭, 대형 엠블럼, 볼드 슬로건)과 Mockup 3 (3열 대시보드 구조) 융합 디자인 채택.
  - 사장님 3대 지침 엄수:
    1. Official Channels & GitHub 메뉴 제외
    2. Movie Scenarios 대신 위키북스(WIKIBOOKS) 정규 라인업 탑재
    3. 푸터에 `"대표도메인 : dmdg-live.com & malssam.com"` 명시

### 2. 서비스 복원 및 링크 무결성 검증
* **소담 라이브(Sodam Web)**: Firebase 호스팅 주소(`dmdg-ut.web.app/sodam-web/`) 정상 연결 복원.
* **당목담글 공식 블로그**: 위키독스 공식 기술 블로그(`dmdg.wikidocs.net/blog/`) 라이브 링크 연동.
* **SSL 인증서**: Naver 밴드 등 모바일 `www.` 접두어 호출에 대응하는 Multi-SAN SSL 인증서 적용.

---

## 🏛️ 포털 구성 요소 및 라우팅 맵

| 경로 / URL | 역할 및 기능 | 주요 특징 |
| :--- | :--- | :--- |
| `/index.html` (`/`) | DMDG LIVE 메인 대시보드 | 3열 5개 카드 제한, 실시간 검색, 과정 신청 모달 탑재 |
| `/curriculum.html` | Antigravity × REA 상세 커리큘럼 | 8주차 강의계획서 전문, 시간표, 강의장 위치 안내, 신청 링크 |
| `/admin.html` | 수강 신청자 관리자 콘솔 | 로그인 인증(DMDG/ekdahrekarmf), 실시간 DB 통계, CSV 다운로드 |
| `/novels.html` | DMDG 서재 (E-Reader) | 팩션 소설 및 미래 3부작 48개 챕터 낭독기 + TTS |
| `/sim_mcp_explorer.html`| REA × MCP Protocol Inspector | JSON-RPC 2.0 패킷 트레이서, 3대 AI 스위처, 시뮬레이터 |
| `/sim_master_hub.html` | 28종 수학·AI 시뮬레이터 허브 | 20종 수학 알고리즘 및 8대 프로덕션 시뮬레이터 통합 관제 |
| `/scm_dashboard.html` | SCM MLOps 공급망 관제 대시보드 | LLM Brain 지식 그래프 연계 실시간 리스크 추론 관제 |

---

## 🔐 보안 및 인증 정보 요약
* **관리자 로그인**:
  - URL: `https://dmdg-live.com/admin.html`
  - ID: `DMDG`
  - PW: `ekdahrekarmf`
* **데이터베이스**:
  - Firebase Firestore: `rea_course_applications` 컬렉션
  - LocalStorage 백업: `dmdg_rea_applications` 키로 이중 안전 보관
