# 🛡️ DMDG 2대 대표 사이트 Cloudflare 4계층 WAF & 안티-스크래핑 방어 런북

> **목적**: 100% 무료 Cloudflare WAF를 연동하여 소설 서재(`novels.html`), 신조어 사전 DB(`words_db.json`) 및 웹앱 전체에 대한 악성 스크래핑 봇, AI 크롤러, DDoS 공격을 원천 차단.  
> **비용**: **100% 평생 무료** (Cloudflare Free Plan)  
> **최종 갱신**: 2026-10-23 (dmdg-live.com 4계층 풀가동 완결 & malssam.com 1~3계층 가동 완결)

---

## 🌐 1. 보호 대상 2대 공식 라이브 사이트 명세

| 사이트 명칭 | 공식 접속 URL | 핵심 서비스 및 탑재 콘텐츠 설명 | 보안 방어 상태 |
| :--- | :--- | :--- | :---: |
| **DMDG LIVE<br>(공식 대표 포털)** | [https://dmdg-live.com](https://dmdg-live.com) | • **DMDG 공식 대표 통합 포털 대시보드**<br>• **DMDG 서재 (`novels.html`)**: 미래 3부작 & 2027 팩션 소설 48개 전 챕터 원문 낭독 E-Reader<br>• **Antigravity × REA 커리큘럼 (`curriculum.html`)**: 8주 과정 실시간 수강신청 관제<br>• **28종 인터랙티브 AI·수학 시뮬레이터 허브** 및 비노출 관리자 콘솔 (`admin.html`) | 🟢 **1~4계층 100% 풀가동**<br>(Cloudflare WAF + Bot Fight Mode) |
| **말쌈 (MALSSAM)<br>(한글 어반 딕셔너리)** | [https://malssam.com](https://malssam.com) | • **대한민국 세대 공감 현대 한국어 신조어 사전 PWA**<br>• 1990s PC통신부터 2026 최신 숏폼 밈까지 8대 세대별 어휘 DB (`words_db.json`)<br>• 초성 검색, 실시간 인정/억지 배틀 투표, AI 단어 DNA 지표<br>• 5개 국어(영·일·스페인·베트남·인도네시아어) 글로벌 허브 (`global/`) | 🟢 **1~3계층 100% 가동 중**<br>(robots.txt + anti-scraping.js + Headless차단) |

---

## 🚀 2. `dmdg-live.com` Cloudflare 4계층 실서버 연동 내역 (완결)

### 1단계: Cloudflare 사이트 등록 (완료)
* 도메인: `dmdg-live.com` (Cloudflare Free 요금제)
* 기존 DNS 레코드(GitHub Pages IP 4개: `185.199.108.153` ~ `111.153` 및 `www` CNAME) 100% 자동 스캔 바인딩.

---

### 2단계: 호스팅케이알(hosting.kr) 네임서버 변경 (완료)
* 도메인 등록처: **호스팅케이알 (https://www.hosting.kr)**
* 할당 및 변경 완료된 네임서버 2개:
  * **1차 네임서버**: `serena.ns.cloudflare.com`
  * **2차 네임서버**: `vin.ns.cloudflare.com`
* 전 세계 DNS 전파 100% 완료 (`nslookup` 조회 검증 완료).

---

### 3단계: Cloudflare 3대 핵심 보안 방패 가동 (완료)
* 🟢 **Bot Fight Mode**: `ON (활성화)` ➔ 악성 스크래퍼 및 파이썬 자동화 봇 진입 즉각 차단.
* 🟢 **Hotlink Protection**: `ON (활성화)` ➔ 도서 표지, 엠블럼 등 이미지 무단 링크/도용 원천 차단.
* 🟢 **Browser Integrity Check**: `ON (활성화)` ➔ 비정상 HTTP 헤더 조작 탐지 및 차단.

---

## 📊 3. 4단계 방어 솔루션 최종 현황

| 계층 | 방어 솔루션 | 적용 기술 및 파일 | 방어 대상 및 효과 |
| :---: | :--- | :--- | :--- |
| **1계층** | `robots.txt` + `noai` 메타태그 | [robots.txt](file:///c:/DMDG_JOBs/DMDG_PRJ/dmdg_live_dot_com/robots.txt) | GPTBot, ClaudeBot 등 15대 상용 AI 학습 봇 접근 거부 |
| **2계층** | `anti-scraping.js` 브라우저 가드 | [anti-scraping.js](file:///c:/DMDG_JOBs/DMDG_PRJ/dmdg_live_dot_com/js/anti-scraping.js) | 마우스 우클릭, 텍스트 드래그, F12, Ctrl+U, 복사 원천 차단 |
| **3계층** | Anti-Headless Webdriver 탐지기 | [anti-scraping.js](file:///c:/DMDG_JOBs/DMDG_PRJ/dmdg_live_dot_com/js/anti-scraping.js) | Selenium, Puppeteer 등 자동화 크롤러 브라우저 블라인드 |
| **4계층** | Cloudflare WAF & Bot Fight Mode | Cloudflare Network Edge | 대량 스크래핑 IP 자동 밴, DDoS 방어, 초고속 전 세계 CDN 캐싱 |
