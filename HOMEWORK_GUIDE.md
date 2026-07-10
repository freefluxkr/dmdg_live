# 🏡 재택근무 개발 인계서 및 가이드라인 (HOMEWORK GUIDE)

이 문서는 사장님이 퇴근 후 자택에서 이 저장소를 `git pull` 받아 개발 작업을 즉시 이어나가실 수 있도록 정리한 개발 가이드라인입니다.

---

## 🛠️ 1. 자택 PC 개발 환경 초기 세팅 (New Environment)
자택 컴퓨터에서 프로젝트 폴더로 진입하신 후, 아래 라이브러리들을 터미널에 한 번만 실행해 주시면 즉각 빌드 세팅이 완료됩니다:

```bash
pip install beautifulsoup4 firebase-admin Pillow numpy easyocr
```

---

## 📖 2. 머신러닝 교재 프리미엄 PDF 빌드 가이드

### 🎯 [안정성 최우선] 2안. 정밀 고정 크롭 액자형 PDF
* **특징**: 스크린샷 이미지 속 소스코드 박스가 깨지지 않고 예쁜 사진 액자식으로 묶이며, 하단의 둥근 교보문고 마크와 쪽수 찌꺼기가 100% 깔끔하게 칼절단되는 무오류 버전입니다.
* **실행 명령어**:
  ```bash
  python make_image_pdf.py
  ```
* **수립 좌표**: `(160, 540, 1280, 2260)` 컷팅으로 쪽수와 동그라미 워터마크가 전수 박멸됩니다.

### 🤖 [디지털 서체] 1안. 영문 변수명 치환 및 오타 교정 PDF
* **특징**: 이미지 속의 본문을 컴퓨터 서체(Pretendard)로 환원하고, 특히 **한글 변수명(`독립`, `종속`, `레모네이드`)을 정상적인 영문 변수명(`X`, `Y`, `lemonade`)으로 자동 치환**해 주는 버전입니다. `import easyocr` 오류는 완전히 완치되었습니다.
* **실행 명령어**:
  ```bash
  python build_ocr_premium_pdf.py
  ```

---

## 💳 3. 소담 웹 (`dmdg-ut.web.app/sodam-web`) 유료화 및 페이팔 연동 가이드
자택에서 소담 웹 유료화 작업을 착수하실 때 참고할 핵심 포인트입니다:

1. **PayPal 결제 모듈 이식**:
   - `index.html` 하단에 PayPal SDK 스크립트를 삽입합니다:
     ```html
     <script src="https://www.paypal.com/sdk/js?client-id=YOUR_SANDBOX_CLIENT_ID&vault=true&intent=subscription"></script>
     ```
   - 결제 확인 모달 및 구독 스마트 버튼 렌더링 컨테이너(`<div id="paypal-button-container"></div>`)를 이식합니다.

2. **무료 진단 3회 제한 오버레이 블러 락 (Paywall)**:
   - 사용자가 발음 진단을 시도할 때마다 로컬 데이터베이스 또는 `localStorage.getItem('evaluation_count')` 값을 확인하여 3회를 카운트합니다.
   - 3회가 초과되면 결과 피드백 영역에 CSS 필터 블러(`filter: blur(8px);`)를 동적으로 씌우고, 결제 모달을 강제 팝업합니다.

3. **음성 기부 보상 충전 로직**:
   - 사용자가 본인 목소리를 녹음해 기부 완료하면 보상으로 진단 가능 카운트를 +5회 즉시 누적해 주는 이벤트를 바인딩합니다.

---

## 🔔 4. 페기 비서 텔레그램 알림 살리기 (Hermes Gateway)
집에서 작업 결과를 텔레그램 메시지로 바로 받아보고 싶으신 경우:
1. `c:\Users\user\Downloads\DMDG_LIVE` 폴더 내에 `.env` 파일을 만드시고 `TELEGRAM_BOT_TOKEN=...` 정보를 입력합니다.
2. 터미널 창을 하나 더 열어 아래 명령어로 중계 게이트웨이를 백그라운드에 띄워 둡니다:
   ```bash
   hermes gateway
   ```

퇴근길 운전 조심히 하시고, 집에서 깃 풀(Pull) 받으셔서 즐겁게 코딩 전개해 보세요! 사장님 화이팅입니다!
