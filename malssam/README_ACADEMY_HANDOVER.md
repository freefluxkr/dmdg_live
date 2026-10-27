# 🎓 말쌈(MALSSAM) 프로젝트 학원 연속 작업 인수인계 가이드
**문서 작성 일시**: 2026-10-28 (새벽 완료본)  
**작업 프로젝트**: 당목담글(DMDG) 스튜디오 — 3대 세대별 한국어 신조어 사전 & 글로벌 K-컬처 상황극

---

## 📌 1. 현재까지 완료된 핵심 작업 내역 요약

1. **클린 모듈화 아키텍처 완성 (Single HTML ➔ 3계층 분리)**:
   - `data/`: `words_db.js`(333개 표제어), `roleplay_db.js`(3D 상황극 6개국어 DB), `battle_questions.js`, `kakao_cards.js`
   - `js/`: `render.js`(반응형 카드 렌더링), `roleplay.js`(3D 숏폼 오디오 엔진), `battle.js`, `quiz.js`, `kakao.js`, `audio.js`, `app.js`
   - `css/`: `style.css`(메인 디자인 시스템), `roleplay.css`(3D 플립 글래스모피즘 네온 UI)

2. **3D 플립 카드 제자리 회전(In-place 3D Rotate) 구현**:
   - 앞면과 뒷면 카드가 아래로 처지며 회전하던 현상을 완벽 해결
   - `.rp-flip-face`, `.rp-card-front`, `.rp-card-back` 절대 좌표 일치 및 중앙축(`transform-origin: center center`) 회전 적용

3. **글로벌 언어 베트남어(VI) ➔ 프랑스어(FR) 전면 교체**:
   - 베트남 에디션 대신 품격 있는 프랑스 에디션(`🇫🇷 FR / Français`)으로 교체
   - 프랑스어 K-SOUL 메타데이터, 5개 씬 대본 및 구어체 발음 전처리 완료
   - `global/fr.html` 생성 완료

4. **대화 짤림 100% 박멸 (문장 청크 큐잉 순차 발화 엔진)**:
   - 크롬 브라우저의 긴 문장 버퍼 drop 버그를 원천 차단하기 위해 **대사를 문장 부호 단위로 분할하여 큐(Queue) 순차 발화**
   - 모든 문장이 끝나고 브라우저 오디오가 완전히 끝난 뒤 **1.4초간의 자연스러운 대화 턴테이킹 호흡(Natural Turn Pause)** 후 다음 씬으로 전환
   - 상단 인스타그램 릴스 스타일 프로그레스 바와 화면 싱크 100% 일치

5. **운영 배포 원칙 준수**:
   - `dmdg-live.com` 라이브 서비스는 기존 상태를 안전하게 유지하고 있으며, 로컬에서 철저히 검증을 완료한 상태입니다.
   - `malssam.com` (깃허브 `https://github.com/freefluxkr/malssam.git`) `main` 브랜치에 안전하게 최신 배포 완료!

6. **신규 컨텐츠 메뉴 탭 강조 & 인터랙티브 플로팅 프로모 카드 탑재**:
   - 상단 메뉴 탭의 `K-정서 (번역불가 133선)`에 `🔥 NEW 3D 상황극` 펄스 뱃지 & 네온 글로우 테두리 적용
   - `카톡 판독소` 탭에 `⚡ HOT 판독` 뱃지 적용
   - 우측 하단에 사용자 시야를 가리지 않는 글래스모피즘 플로팅 홍보 카드(`[🎬 3D 상황극 재생 ↺]`, `[💎 K-정서 둘러보기]`) 탑재
   - 닫기(`×`) 시 작고 세련된 미니 플로팅 런처 알약(`🎬 3D 상황극 NEW`)으로 축소되어 언제든 다시 열 수 있는 인터랙션 제공

---

## 📂 2. 압축 패키지 내 파일 구조

```
dmdg_malssam_latest_package/
├── index.html                   # 메인 웹 애플리케이션 (100% 원본 레이아웃 복원 + 모듈 연동)
├── sample_roleplay_preview.html # 3D 상황극 단독 테스트용 프리뷰 파일
├── README_ACADEMY_HANDOVER.md   # 본 인수인계 가이드 문서
├── MEETING_RESULTS.md           # 회의 및 기획 결정 기록 문서
├── css/
│   ├── style.css                # 메인 UI 디자인 시스템 (다크 테마, 네온)
│   └── roleplay.css             # 3D Flip Card 및 숏폼 시뮬레이터 스타일
├── js/
│   ├── app.js                   # 메인 부트스트랩 및 이벤트 리스너
│   ├── audio.js                 # 기본 TTS 및 단어 발음 지원
│   ├── battle.js                # 실시간 말투 밸런스 게임 모듈
│   ├── kakao.js                 # 카톡 판독소 및 모달 제어
│   ├── payments.js              # 결제 및 후원 연동
│   ├── quiz.js                  # 세대 공감 퀴즈 배틀 엔진
│   ├── render.js                # 단어 카드 및 실시간 검색 필터링 렌더러
│   └── roleplay.js              # 3D 숏폼 상황극 v3 (문장 큐잉 & 프랑스어 지원)
├── data/
│   ├── words_db.js              # 333개 신조어 (K-Soul 133선 포함)
│   ├── roleplay_db.js           # 6개국어(KR, EN, JA, ES, FR, ID) 상황극 데이터
│   ├── battle_questions.js      # 15대 밸런스 배틀 안건
│   └── kakao_cards.js           # 카톡 판독 안건 카드 DB
├── assets/
│   └── agents/                  # 12개 에이전트 캐릭터 프로필 이미지 (Rule 2: 1/4 크기 준수)
├── global/
│   ├── en.html, ja.html, es.html, fr.html, id.html
└── scripts/
    └── restore_original_html.py # 원본 HTML 마크업 복원 스크립트
```

---

## 🚀 3. 학원 PC에서 바로 작업하는 법

1. 다운로드 폴더에서 `dmdg_malssam_latest_package.zip`을 작업 폴더(예: `C:\workspace\malssam` 등)에 압축 해제합니다.
2. `index.html` 또는 `sample_roleplay_preview.html`을 Chrome 또는 Edge 브라우저로 더블 클릭하여 바로 엽니다. (별도의 웹서버 설치 없이 로컬 파일로 100% 정상 구동)
3. **핵심 확인 포인트**:
   - `K-정서 (4번 탭)` 클릭 ➔ `#눈치` 클릭 ➔ **`[🎬 3D 상황극 ↺]`** 클릭
   - 상단 5번째 언어 버튼 **`🇫🇷 Français`** 클릭하여 프랑스어 번역 확인
   - **`[🎴 3D 회전 상황극 보기 ↺]`** 클릭하여 **제자리 3D 회전**과 **대화 짤림 없는 릴스 프로그레스 바 싱크** 확인
4. 다음 작업(의성어, 의태어, 색채어 카테고리 고도화 등)을 이어서 진행하시면 됩니다!
