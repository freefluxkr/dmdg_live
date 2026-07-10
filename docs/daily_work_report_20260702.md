# 📝 당목담글 2026-07-02 작업 이력 보고서

금일 모바일 기기에서의 화면 렌더링 마비 현상 분석을 기점으로 진행한 오프라인 예외 처리(Fail-safe), Firestore 보안 규칙 연장, UI 부드러움 전환 튜닝 및 깃허브 배포 동기화 내역을 정리한 작업 이력 보고서입니다.

---

## 📅 실시간 작업 이력 요약

### 1. 📱 모바일/오프라인 구동 강건성 패치 및 SyntaxError 해결
* **원인**: 이전 깃허브 원격 병합 시 충돌 마커가 섞여 들어가 자바스크립트 파싱 오류가 발생했고, [js/app.js](file:///c:/Users/user/Downloads/DMDG_LIVE/js/app.js) 내부에서 `emotions` 변수가 이중으로 중복 선언되어 브라우저 기동이 완전히 마비되었습니다.
* **조치**: 
  * `index.html`을 충돌 전 깨끗한 원본 커밋(`1b80588`)으로 롤백한 후, 인라인 `<script>` 태그의 중복을 걷어내고 순수 HTML 마크업으로 정돈했습니다.
  * [js/app.js](file:///c:/Users/user/Downloads/DMDG_LIVE/js/app.js) 내의 `emotions` 변수 중복 선언을 삭제하여 구문 에러를 해소했습니다.
  * `loadPrimersFromDB` 함수 시작부에서 `firestore` 객체의 존재 유무(`typeof firestore !== 'undefined' && firestore !== null`)를 철저히 검사하게 하여, 파이어베이스 로드에 이상이 생겨도 타입 에러 없이 안전하게 로컬 오프라인 데이터베이스(IndexedDB) 우선 모드로 분기되도록 리팩토링했습니다.

### 2. 🛡️ Firebase Firestore 보안 규칙 만료 대응
* **원인**: 테스트 모드 생성으로 인해 1일 후 클라이언트 접속 권한이 만료되어 데이터 로딩 및 동기화가 중단될 예정이었습니다.
* **조치**: 
  * Firebase 콘솔의 Firestore 보안 규칙에서 데이터베이스 접근 허용 만료일을 **2027년 12월 31일**로 넉넉히 연장했습니다.
  * 마중물 편지(`primers`) 컬렉션의 누구나 읽고 쓸 수 있는 규칙 설정을 원격 게시 완료하여 데이터베이스 만료 위험을 완전히 해결했습니다.

### 3. 🎨 국가 테마 전환 시의 화면 떨림/깜빡임 버그 픽스
* **원인**: 언어를 바꿀 때마다 [js/app.js](file:///c:/Users/user/Downloads/DMDG_LIVE/js/app.js)에서 브라우저 전면의 `backgroundImage` (방사형 그래디언트)를 강제로 재생성하여 화면 전체에 급격한 레이아웃 리페인트와 깜빡임(Flashing)이 생겼습니다.
* **조치**: 
  * 런타임에 동적으로 그래디언트 이미지를 재생성하던 비효율적인 연산을 제거했습니다.
  * [index.html](file:///c:/Users/user/Downloads/DMDG_LIVE/index.html) 배경 블러 서클에 세팅된 CSS color transition에 맞추어 `backgroundColor` 값만 전환되도록 단순화하여, 테마 교체 시 0.5초 동안 파스텔톤 배경이 부드럽고 잔잔하게 페이드 전환되도록 연출을 보강했습니다.

### 🌌 4. 대시보드 은하수 별빛 캔버스 드로잉 영역 매핑 오류 해결
* **원인**: 글로벌 온기 분석 대시보드 내부의 `milkyway-canvas` 드로잉 내부 해상도가 윈도우 크기 전체(`window.innerWidth`, `window.innerHeight`)로 설정되어 있어, 실제 144px 크기인 로고 컨테이너 내부에서는 별들이 모두 원 밖 영역에 그려져 아예 안 보였던 버그가 있었습니다.
* **조치**: 
  * 캔버스 드로잉 크기를 원형 로고 컨테이너 픽셀 크기에 딱 맞추어 가로/세로 **`144`**로 정밀 교정했습니다.
  * 150개의 모든 별 파티클이 원형 로고 내부 공간에서만 은하수처럼 반짝이며 부드럽게 흘러내리는 시각 효과를 온전히 복원했습니다.

### 🔄 5. sw.js 서비스 워커 캐시 업데이트 및 최종 배포
* **파일명**: [sw.js](file:///c:/Users/user/Downloads/DMDG_LIVE/sw.js)
* **조치**: 
  * 폰에서 캐시가 굳어 있어 변경된 코드가 즉시 반영되지 않던 현상을 해결하기 위해 서비스 워커 캐시 네임을 `dangmok-cache-v15`에서 **`dangmok-cache-v16`**으로 갱신했습니다.
  * 이 변경 사항을 포함하여 모든 수정 사항을 깃허브 `main` 브랜치에 안전하게 커밋 및 푸시하여, 모바일 폰에서도 최신 버전의 코드가 즉각 갱신되어 배포되도록 조치했습니다.

---

## 🔗 주요 링크 정보
* **당목담글 모바일 라이브 서비스 주소**: [https://freefluxkr.github.io/dmdg_live/](https://freefluxkr.github.io/dmdg_live/)
* **GitHub 원격 소스코드 저장소**: [https://github.com/freefluxkr/dmdg_live](https://github.com/freefluxkr/dmdg_live)
* **Firebase Console (DMDG-PWA)**: [https://console.firebase.google.com/u/0/project/dmdg-live/overview](https://console.firebase.google.com/u/0/project/dmdg-live/overview)

---

## 🧡 최종 배포 완료 상태
모든 롤백, 버그 픽스 및 캐시 갱신 파일이 깃허브 `main` 저장소에 최종 반영되었습니다. 폰과 브라우저 양쪽에서 테마 변경, 마중물 교체, 대시보드 별빛 애니메이션 등 모든 기능이 온전히 작동함을 상시 확인 가능한 무결점 상태로 전환해 두었습니다.
