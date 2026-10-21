# 🏛️ DMDG LIVE (당목담글 공식 대표 포털)

> **공식 서비스 URL**: [https://dmdg-live.com/](https://dmdg-live.com/)  
> **GitHub Pages URL**: [https://freefluxkr.github.io/dmdg_potal/](https://freefluxkr.github.io/dmdg_potal/)  
> **소스코드 리포지토리**: [`freefluxkr/dmdg_potal`](https://github.com/freefluxkr/dmdg_potal) (Main) & [`freefluxkr/dmdg_live`](https://github.com/freefluxkr/dmdg_live) (Live Deploy)  
> **총괄 기획**: 당목담글(DMDG) 스튜디오 자율 에이전트 엔지니어링 본부

---

## 🌟 1. 플랫폼 개요 및 핵심 아키텍처

DMDG LIVE(`dmdg-live.com`)는 사람과 마음을 연결하는 이어읽기 플랫폼이자, **Google Antigravity 자율 에이전트 생태계, REA 역공학 도구, 위키북스 출판 라인업, 인터랙티브 AI 시뮬레이터 28종**을 통합 서비스하는 DMDG의 공식 대표 포털입니다.

### 🎨 디자인 시스템 (Mockup 1 & 3 하이브리드)
1. **헤더 & 백드롭 (Design Mockup 1 시그니처)**:
   - 상단 3중 유기적 레이어드 페이퍼컷 웨이브 (Deep Navy, Turquoise, Warm Amber).
   - 좌우 측면 유기적 곡선 웨이브 프레임.
   - 중앙 상단 원형 대형 엠블럼 (`assets/dmdg_emblem_hq.png`).
   - 볼드 슬로건: *"사람과 마음을 연결하는 세상에서 가장 따뜻한 이어읽기 플랫폼"*.
2. **대시보드 패널 (Design Mockup 3 시그니처: 3열 균형 구조)**:
   - **3열 카드 5개 제한 규칙**: 각 컬럼당 카드 노출을 5개로 정렬하여 수직 1:1:1 완벽한 시각 균형 확립.
   - **총 컨텐츠 개수 배지 보존**:
     - `Column 1 (LIVE WEB APPS)`: `6 Services`
     - `Column 2 (INTERACTIVE SIMULATORS)`: `28 Total ➔` (28종 마스터 허브 직결)
     - `Column 3 (WIKIBOOKS)`: `11 Books (전체 ➔)` (위키독스 전체 도서 직결)
   - **지능형 실시간 검색**: 상단 검색창에 검색어 입력 시, 숨겨진 6번째 이후 카드도 키워드 일치 시 즉시 노출.

---

## 🎓 2. Antigravity IDE × REA 부트캠프 교육 시스템

취업 준비생 및 주니어 개발자를 위한 **8주 완성 모던 역공학 & 클린룸 재구현 부트캠프** 시스템이 포털에 완벽히 연동되어 있습니다.

1. **상세 커리큘럼 페이지 (`curriculum.html`)**:
   - 우상단 네비게이션 `[🎓 Antigravity × REA 과정 상세 안내]` 클릭 시 직결.
   - 8주차 상세 강의계획서, 공식 교재 매핑, 3대 취업 무기 전문 수록.
   - **오프라인 강의장 위치 안내**:
     > **강의장 위치 : 신청자들의 공통 위치로 선정하여 추후 공지 (현재는 성남시 태평역 부근 예정)**  
     > *(20명 모집 확정 시 신청자 거주지 분포를 종합 분석하여 최적 접근성의 교육장 최종 배정)*
2. **수강 신청 온보딩 팝업 & 데이터베이스 연동**:
   - 포털 접속 시 모달 팝업 자동 안내 (오늘 하루 보지 않기 쿠키 지원).
   - 목표 20명 달성 프로그레스 바 실시간 연동 (20명 이상 신청 시 정식 개강).
   - 신청 데이터 이중 보관: **Firebase Firestore (`rea_course_applications`) + LocalStorage fallback**.
3. **관리자 콘솔 (`admin.html`)**:
   - URL: `https://dmdg-live.com/admin.html`
   - 인증: ID `DMDG` / PW `ekdahrekarmf`
   - 실시간 신청자 명단 조회, 20명 개강 여부 배지, **UTF-8 BOM 지원 엑셀 CSV 원클릭 다운로드**.

---

## 📂 3. 포털 주요 파일 구성

```text
dmdg_potal/
├── index.html              # DMDG LIVE 대표 포털 메인 대시보드
├── curriculum.html         # Antigravity × REA 8주 마스터 상세 커리큘럼 전문
├── admin.html              # 수강 신청자 관리자 콘솔 대시보드
├── novels.html             # DMDG 서재 (Hamilton.Kang 팩션 소설 & 미래 3부작 E-Reader)
├── scm_dashboard.html      # AI 에이전트 & SCM MLOps 공급망 관제 대시보드
├── sim_mcp_explorer.html   # REA × MCP JSON-RPC 2.0 프로토콜 인스펙터
├── sim_master_hub.html     # 28종 전체 수학·AI 시뮬레이터 마스터 허브
├── style.css               # 통합 디자인 시스템 (네온 다크, 웨이브, 반응형)
├── CHANGELOG.md            # dmdg-live.com 전체 수정 및 배포 상세 이력
├── js/
│   ├── firebase-config.js  # Firebase Firestore 실시간 DB 설정
│   └── admin.js            # 관리자 콘솔 인증 및 CSV 내보내기 로직
└── assets/                 # 당목담글 공식 로고, 엠블럼, 백드롭 에셋
```

---

## 🔄 4. 수정 및 배포 동기화 절차

1. `temp_dmdg_live` (GitHub Pages `freefluxkr/dmdg_live` 배포 리포지토리)에서 작업 및 검증.
2. `dmdg_potal` (`freefluxkr/dmdg_potal` 마스터 리포지토리)로 변경 파일 전체 복사 및 동기화:
   ```powershell
   Copy-Item -Path "c:\DMDG_Jobs\temp_dmdg_live\*" -Destination "c:\DMDG_Jobs\dmdg_potal\" -Recurse -Force
   ```
3. 양대 리포지토리 git commit & push:
   ```bash
   git add .
   git commit -m "feat: update portal"
   git push origin main
   ```
4. 실서버 확인: `https://dmdg-live.com/` (Fastly CDN 캐시 무효화 확인)

---

## 🏛️ 하단 정보
당목담글(DMDG) 스튜디오 자율 에이전트 엔지니어링 본부  
대표도메인: `dmdg-live.com` & `malssam.com`
