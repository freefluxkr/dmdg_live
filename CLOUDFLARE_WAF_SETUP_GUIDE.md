# 🛡️ DMDG LIVE (dmdg-live.com) Cloudflare 4계층 WAF & 봇 방어 연동 런북

> **목적**: 100% 무료 Cloudflare WAF를 연동하여 소설 서재(`novels.html`) 및 전체 웹앱에 대한 악성 스크래핑 봇, 파이썬 크롤러, DDoS 공격을 서버 진입 전 원천 차단.  
> **예상 소요 시간**: 약 5~10분  
> **비용**: **100% 평생 무료** (Cloudflare Free Plan)

---

## 🚀 3단계 원클릭 연동 절차

### 1단계: Cloudflare 사이트 등록 (2분)
1. [Cloudflare 공식 사이트](https://www.cloudflare.com/ko-kr/) 접속 및 무료 회원가입 (또는 로그인).
2. 대시보드 우측 상단 **[+ 사이트 추가(Add a site)]** 버튼 클릭.
3. 도메인 입력창에 **`dmdg-live.com`** 입력 후 계속 클릭.
4. 요금제 선택 화면에서 맨 아래 **[Free (무료 0원)]** 플랜 선택 후 [계속] 클릭.
5. 기존 DNS 레코드(GitHub Pages IP 4개: `185.199.108.153`, `109.153`, `110.153`, `111.153` 및 CNAME)가 자동으로 스캔됩니다. 그대로 [계속] 클릭.

---

### 2단계: 도메인 구매처(가비아 등)에서 네임서버 변경 (3분)
1. Cloudflare 화면에 할당된 2개의 고유 네임서버 주소가 나타납니다.
   - 예시:
     * `alice.ns.cloudflare.com`
     * `bob.ns.cloudflare.com`
2. **도메인을 구입하신 사이트(가비아, 후이즈, 호스팅KR 등)**에 로그인합니다.
3. [도메인 관리] ➔ `dmdg-live.com` 선택 ➔ **[네임서버(DNS) 변경]** 클릭.
4. 기존 1차/2차 네임서버를 지우고, Cloudflare에서 제공한 주소 2개로 입력 후 저장.
5. Cloudflare 화면으로 돌아와 **[네임서버 확인 완료]** 클릭. (보통 5분~1시간 내 전파 완료)

---

### 3단계: Cloudflare 3대 보안 스위치 켜기 (2분)

네임서버 연결 완료 후, Cloudflare 대시보드 `dmdg-live.com` 관리 페이지에서 아래 3가지만 켜주시면 즉시 무적 방어막이 활성화됩니다:

#### ① Bot Fight Mode (봇 퇴치 모드) 켜기
* **메뉴 이동**: 좌측 메뉴 **[보안(Security)]** ➔ **[봇(Bots)]**
* **설정**: **Bot Fight Mode** 스위치를 `[ON]`으로 켬.
* **효과**: 악성 스크래퍼, 파이썬 requests/urllib, 비인가 크롤러가 사이트에 진입하려 할 때 100% 자동 챌린지 또는 즉각 차단(Block).

#### ② SSL/TLS 암호화 모드 확인
* **메뉴 이동**: 좌측 메뉴 **[SSL/TLS]** ➔ **[개요(Overview)]**
* **설정**: 암호화 모드를 **[전체(Full)]**로 설정.
* **효과**: GitHub Pages와 방문자 간의 트래픽이 2중 SSL로 완벽 암호화되어 중간자 도청 및 스니핑 방지.

#### ③ 소설 서재(`novels.html`) 전용 WAF 규칙 (선택 추천)
* **메뉴 이동**: 좌측 메뉴 **[보안(Security)]** ➔ **[WAF]** ➔ **[사용자 지정 규칙(Custom Rules)]** ➔ [규칙 만들기]
* **규칙 이름**: `Protect Novels E-Reader`
* **조건 설정**:
  - `URI 경로` `포함(contains)` `/novels.html`
  - AND `위협 점수(Threat Score)` `크거나 같음(greater than or equal to)` `10`
* **수행할 작업**: **[관리형 챌린지 (Managed Challenge)]** 선택 후 저장.
* **효과**: 소설 서재에 비정상적인 방법으로 빠르게 접근하는 의심스러운 세션에만 사람 확인 캡차를 자동으로 띄워 스크래핑을 즉시 중단시킴.

---

## 📊 4단계 방어 솔루션 구축 완료 후 방어 현황

| 계층 | 방어 솔루션 | 적용 상태 | 방어 대상 |
| :---: | :--- | :---: | :--- |
| **1계층** | `robots.txt` + `noai` 메타태그 | 🟢 **로컬 적용 및 배포 완료** | GPTBot, ClaudeBot 등 15대 AI 학습 크롤러 전면 차단 |
| **2계층** | `anti-scraping.js` 브라우저 가드 | 🟢 **로컬 적용 및 배포 완료** | 우클릭, 텍스트 드래그, F12, Ctrl+U, 복사 원천 차단 |
| **3계층** | Anti-Headless Webdriver 탐지기 | 🟢 **로컬 적용 및 배포 완료** | Selenium, Puppeteer 등 자동화 크롤링 브라우저 블라인드 |
| **4계층** | Cloudflare WAF & Bot Fight Mode | 🟡 **대표님 네임서버 연동 대기** | 대량 스크래핑 IP 자동 밴, DDoS 방어, 초고속 CDN 캐싱 |
