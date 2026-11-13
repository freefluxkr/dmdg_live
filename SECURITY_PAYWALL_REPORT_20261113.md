# DMDG 유료화 전환 공지 및 콘텐츠 보안 엔진 구현 보고서

- **작업 일시**: 2026-11-13 23:00 ~ 23:07 KST
- **대상 저장소**: `c:\DMDG_Jobs\DMDG_PRJ\dmdg_live_dot_com` (`origin/main`)

## 1. 구현 내역

### (1) 2027.1.1 유료화 전환 공지 팝업 (`js/dmdg_paywall_notice.js`)
- **공지 문구**: `2026년 12월 31일까지 전 서비스 100% 무료 제공`, `2027년 1월 1일부터 전면 유료화 전환`.
- **OTT형 3대 이용 모델 및 보안 태그 안내**:
  1. **기간 한정 (OTT형)**: 단기 열람/스트리밍 (`만료 토큰 + Signed URL + 눈에 안 보이는 워터마킹`)
  2. **완전 소유 (영구 소장)**: PDF/실습 코드/오디오북 다운로드 (`눈에 안 보이는 워터마킹`)
  3. **정기 구독 (멤버십)**: 월간/연간 전 서비스 이용 (`눈에 안 보이는 워터마킹`)
- **오늘 하루 동안 보지 않기**: 체크박스 선택 후 닫기 시 `localStorage` (`dmdg_paywall_notice_hide_until`)에 당일 `23:59:59.999` 타임스탬프 저장.
- **적용 페이지**: `index.html`, `novels.html`, `store.html`, `scm_dashboard.html`, `career_aces.html`, `security_verifier.html`

### (2) 콘텐츠 보안 엔진 (`js/dmdg_security.js`) 및 연동
- **만료 토큰 & HMAC-SHA256 Signed URL**: `createSignedUrl()`, `verifySignedUrl()`, `checkCurrentPageTokenGate()` (만료/변조 시 403 차단).
- **비가시성 워터마킹 (Zero-Width Steganography)**: `\u200B`/`\u200C`/`\u200D` 기반 `embedTextWatermark()`, `extractTextWatermark()`, `attachCopyWatermark()`, `buildWatermarkedTextBlob()`, `injectPdfWatermarkBanner()`.
- **페이지/모듈 연동**:
  - `js/dmdg_payment.js`: `triggerPdfDownload()`에 인쇄용 워터마크 배너 주입, `triggerAudioDownload()`에 Signed URL + 비가시성 워터마크 텍스트 블롭 적용.
  - `scm_dashboard.html`: `total_prj.zip` 다운로드 시 Signed URL 생성·검증 함수(`dmdgDownloadScmZip`) 연동.
  - `career_aces.html`: `downloadReportPDF()` 호출 시 PDF 출력 영역에 워터마크 배너 주입.
  - `security_verifier.html`: Signed URL 발급/만료(403) 시뮬레이션, 워터마크 인코딩/디코딩, 유료화 공지 팝업 재오픈 QA 콘솔 신설.

## 2. 검증 결과
- **JS 구문 검사 (`node -c`)**: `js/dmdg_security.js`, `js/dmdg_paywall_notice.js`, `js/dmdg_payment.js` 모두 Exit Code 0 통과.
- **Node.js 기능 단위 검증**:
  - `DMDG_Security.createSignedUrl` → `verifySignedUrl` 정상 `valid: true`, 만료 시각 검증 시 `valid: false` (`reason: "EXPIRED"`).
  - `embedTextWatermark` → `extractTextWatermark` 역추적 복원 확인 (`UID`, `MODE: "owned"`, `RES: "career_aces_pdf"`).
  - `DMDG_PaywallNotice.open` 및 `shouldShow()` 정상 동작 확인.
- **로컬 HTTP 서빙 검증 (`http://localhost:8766`)**: 대상 HTML 6종 및 JS 3종 모두 HTTP 200 응답 확인.
- **실시간 Chrome DevTools 브라우저 QA**: Chrome 원격 디버깅 승인 다이얼로그(`Allow remote debugging?`) 응답 대기 60초 타임아웃으로 미완료 (야간 예약 실행 환경).
