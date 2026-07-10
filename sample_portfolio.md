# 🚀 백엔드 및 클라우드 아키텍처 주니어 개발자 - 김지민 포트폴리오

안녕하세요! 안정적이고 확장 가능한 백엔드 시스템 구축과 자동화된 인프라 배포에 관심이 많은 주니어 개발자 김지민입니다.

---

## 🛠️ 기술 스택 (Tech Stacks)
* **Backend**: Java / Spring Boot, Python / FastAPI, Node.js
* **Database**: PostgreSQL, MySQL, Redis (Caching)
* **Cloud & DevOps**: AWS (EC2, RDS, S3, VPC), Docker, GitHub Actions (CI/CD)
* **Tools**: Git, Jira, Slack

---

## 💻 주요 프로젝트 (Projects)

### 1. 🛍️ 실시간 트래픽 대응 커머스 플랫폼 "원스톱 샵 (OneStop Shop)"
대규모 할인 이벤트 시 발생하는 트래픽 폭주 문제를 해결하기 위해 캐싱 및 비동기 메시지 큐를 도입하여 안정적인 구매 환경을 구축한 프로젝트입니다.

* **개발 기간**: 2025.10 ~ 2025.12 (3인 협업 프로젝트)
* **담당 역할**: 백엔드 아키텍처 설계, 상품 결제 및 주문 처리 API 개발, 성능 모니터링
* **핵심 성과**:
  * Redis를 캐싱 레이어로 도입하여 인기 상품 조회 API의 응답 속도를 250ms에서 35ms로 **86% 개선**.
  * RabbitMQ를 이용해 주문 생성과 결제 완료 프로세스를 비동기화하여 트래픽 집중 시 데이터베이스 락(Lock) 충돌 현상 방지.
  * AWS CloudWatch와 Prometheus/Grafana를 연동하여 서버 CPU 및 JVM 메모리 사용량 실시간 시각화 대시보드 구축.
* **아쉬운 점 & 보완 계획**:
  * 트래픽 분산을 위해 단일 DB 구조에서 Read/Write 복제(Replication) 구조를 다루지 못해 아쉬움이 남았음. 향후 PostgreSQL Master-Slave 이중화를 시도할 예정.
  * 주문 취소 시 예외 처리가 가끔 모호하게 흘러가 트랜잭션 롤백이 누락되는 엣지 케이스 존재.

---

### 2. 🤖 지능형 회의록 요약 및 할 일 자동화 봇 "Hermes Note"
회의 음성 녹음 파일을 업로드하면 OpenAI Whisper API로 텍스트를 추출하고, LLM을 활용해 주요 안건 요약 및 Jira 이슈를 자동 생성해 주는 협업 툴 연동 봇입니다.

* **개발 기간**: 2026.01 ~ 2026.03 (개인 프로젝트)
* **사용 기술**: Python, FastAPI, OpenAI API, Jira Cloud API, AWS S3
* **핵심 기능**:
  * 음성 파일(mp3, m4a 등)을 AWS S3에 임시 업로드하고 Chunk 단위로 분할 전송하여 Whisper API 요금 최소화 및 제한량 극복.
  * OpenAI GPT-4o-mini 모델을 호출하여 회의록에서 "할 일(Action Item)"을 추출해 Jira API를 활용해 담당자에게 이슈 자동 할당.
  * FastAPI 백엔드에 비동기 Background Tasks를 적용하여 긴 텍스트 분석 중에도 사용자가 다른 화면으로 신속히 이동할 수 있도록 응답성 보장.
* **아쉬운 점 & 보완 계획**:
  * API Key 보안 관리를 `.env` 파일에 단순 기록하는 수준에 그쳐, AWS Secrets Manager나 Vault 같은 전문 자격증명 저장소 연동이 필요함을 느낌.
  * 테스트 코드 작성율(Test Coverage)이 15% 미만으로 매우 낮아, 리팩토링 시 예기치 못한 에러가 다수 발생함. PyTest 기반 단위 테스트 코드 보강 예정.

---

## 🎓 교육 및 활동 (Education & Activities)
* **DMDG 인공지능 및 클라우드 부트캠프 수료** (6개월 과정)
  * Java, Spring Boot 백엔드 아키텍처 및 AWS 클라우드 배포 집중 교육 이수
  * 부트캠프 내 최우수 프로젝트상 수상 (원스톱 샵 팀)
* **컴퓨터공학과 학사 졸업 (2022.03 ~ 2026.02)**
  * 알고리즘 학회 부회장 역임

---

## 🔗 링크 (Links)
* **GitHub**: [github.com/jimin-dev-cloud](https://github.com)
* **Tech Blog**: [jimin-log.tistory.com](https://tistory.com)
