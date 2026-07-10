import os
import sys
import re
import subprocess

# =====================================================================
# 📚 1. 4명 학생의 5대 기업 에이전트별 가감 없는 피드백 데이터 내장
# =====================================================================
FEEDBACK_DATA = {
    "어창선": {
        "title_desc": "시계열·AI 엔지니어 지망 (비전공자)",
        "summary": "비전공자임에도 시계열 미래 정보 누수를 차단하기 위해 Walk-forward CV와 Embargo gap을 도입하고 Diebold-Mariano 검정으로 모델 성능의 통계적 유의성을 검증하는 등 이론적 엄격성을 집요하게 챙긴 점이 우수합니다. 또한 네트워크 장비 방화벽 UFW 문제를 docker0 라우팅 및 autossh 터널링으로 직접 트러블슈팅해 원격 GPU 환경을 다룬 해결 이력이 매우 훌륭합니다. 다만, 비전공 전공자로서 코딩 테스트 및 대용량 DB 아키텍처 다중화(Replication) 설계 지식이 얕아 보완이 시급하며, 팀원(한정현)과 프로젝트가 완전히 일치하여 개별 기여도를 명확히 쪼개는 포지셔닝이 필요합니다. 또한 이력서에 'ADsP [준비 중]' 문구를 지우지 않고 방치한 사소한 마무리의 아쉬움이 존재합니다.",
        "agents": {
            "samsung_sds": {
                "rating": "B+", "fit_score": 78,
                "summary": "시계열 예측 검증 설계에 대한 학술적 접근은 신입 지원자로서 보기 드문 강점이나, 대용량 트랜잭션 및 분산 처리에 대한 경험이 부족하여 대형 SI 시스템 설계에 필요한 CS 기본기 검증이 추가로 요구됩니다.",
                "strengths": [
                    {"title": "시계열 검증 설계의 수학적 엄격성", "content": "미래 정보 누수(Leakage)를 방지하기 위해 Walk-forward CV and Embargo gap을 코드에 적용하고 Diebold-Mariano 검정으로 우연에 의한 성능 개선을 걸러내려 한 시도는 데이터 신뢰성을 극도로 중시하는 엔지니어링 표준에 부합함."},
                    {"title": "구체적인 네트워크 트러블슈팅", "content": "로컬 사설망과 클라우드 서버 간의 SSH 터널 및 autossh 영속화, UFW 방화벽 차단을 해결하기 위한 bridge 네트워크 분석 흐름이 매우 논리적임."}
                ],
                "weaknesses": [
                    {"title": "CS 기본 지식 및 알고리즘 깊이 부족", "content": "아동복지학 출신 비전공자로서 백엔드 분산 아키텍처와 DB 이중화(Replication) 설계 등의 시스템 핵심 영역에 대한 설명이 다소 얕게 서술되어 코딩 테스트 및 면접 시 기초 CS 지식 장벽에 부딪힐 우려가 큼."},
                    {"title": "팀원과의 차별화 부족", "content": "동일 팀원과 3대 프로젝트(ADA, My Mini Co-di, Churn 예측)가 완전히 겹치는데, 본인만의 독자적 소스 코드 기여분이 명확히 드러나지 않음."}
                ],
                "advice": ["자료구조(그래프, 트리, 해시 테이블 등)와 운영체제 프로세스/메모리 관리 등 코딩 테스트용 알고리즘 이론 학습 필수.", "데이터베이스 Master-Slave 복제 및 분산 환경의 데이터 정합성 보장 기법 추가 공부 추천."]
            },
            "lg_cns": {
                "rating": "A-", "fit_score": 85,
                "summary": "네트워크 방화벽 및 autossh 포트 포워딩 등 시스템 배포 과정에서 겪은 에러를 끈질기게 추적해 뚫어낸 디버깅/인프라 역량이 매우 훌륭합니다. 신기술을 시도하려는 의지도 돋보입니다.",
                "strengths": [
                    {"title": "끈질긴 디버깅(삽질) 기록", "content": "방화벽 차단 문제를 docker0 인터페이스 허용 및 bridge 네트워크 설정 튜닝으로 트러블슈팅해 나간 해결 과정이 실무에 즉시 투입 가능한 수준임."},
                    {"title": "오케스트레이션 및 파라미터 최적화", "content": "AutoML 플랫폼 구축 시 26종 모델의 성능을 비교하기 위해 Optuna를 통합 적용하여 튜닝 과정을 자동화한 엔지니어링 시도가 우수함."}
                ],
                "weaknesses": [
                    {"title": "AWS 클라우드 아키텍처 활용 제한", "content": "단순 EC2/VPS 기반의 호스팅에 머물러 있어, 실제 상용 DX 아키텍처에서 요구되는 매니지드 서비스(ECS, EKS, Serverless 등) 설계 역량이 아쉬움."}
                ],
                "advice": ["Docker Compose 수준을 넘어 Kubernetes(K8s) 오케스트레이션 기초 구조와 배포 프로세스 학습 권장.", "AWS CloudFront, API Gateway 등을 활용한 아키텍처 고도화 시도 추천."]
            },
            "shinsegae_inc": {
                "rating": "B", "fit_score": 72,
                "summary": "백엔드 인프라와 정형 데이터 예측 성능 개선 이력은 탄탄하나, 실제 리테일 비즈니스 관점에서 서비스가 어떻게 가치를 창출하고 최종 사용자에게 편리함을 주는지에 대한 고민이 보완되어야 합니다.",
                "strengths": [
                    {"title": "비즈니스 지표 활용 시도", "content": "고객 이탈 예측을 단순히 모델링에 그치지 않고, 이탈 고위험 고객 타깃 마케팅을 위한 Target List 추출로 연계하여 실용적인 가치로 바꾼 시도가 긍정적임."}
                ],
                "weaknesses": [
                    {"title": "리테일테크 분야와의 접점 부족", "content": "구축한 시스템들이 순수 데이터 분석이나 인프라 영역에 집중되어 있어, e-Commerce 결제, 장바구니 동시성 제어 등 리테일 도메인에서 발생할 수 있는 대용량 트랜잭션 처리에 대한 역량 어필이 부족함."}
                ],
                "advice": ["결제 모듈 연동 및 대규모 트래픽 분산 처리를 위한 Redis 캐시 무력화(Invalidation) 전략 등 상용 결제 도메인 공부 권장."]
            },
            "lotte_innovate": {
                "rating": "B-", "fit_score": 68,
                "summary": "예외 처리 및 확률 보정을 통한 데이터 무결성 추구 태도는 바람직하나, 포트폴리오 문서의 오타 방치 및 미완성 항목 누출은 신뢰성과 꼼꼼함 기준에서 큰 감점 요소입니다.",
                "strengths": [
                    {"title": "신중한 모델 튜닝 및 계량 검증", "content": "Brier Score 확률 보정 및 F2 Score 기준 임계값 조정을 통해 오탐을 최소화하고 의사결정 신뢰도를 높이려 한 꼼꼼한 세부 튜닝 접근법을 칭찬함."}
                ],
                "weaknesses": [
                    {"title": "치명적인 문서 오점 방치", "content": "자격증 목록에 'ADsP [준비 중 / 취득 시 날짜 입력]'이라는 템플릿 괄호 텍스트를 지우지 않은 상태로 제출함. 이는 문서 검수 및 꼼꼼함 결여로 비춰질 수 있음."},
                    {"title": "단위 테스트 이력 부재", "content": "인프라와 백엔드 코드가 많은 것에 비해 PyTest 등 개발 품질을 증명할 단위 테스트나 TDD 작성 흔적이 없어 코드의 안정성을 신뢰하기 어려움."}
                ],
                "advice": ["자격증란의 미완성 문구를 즉시 정정하고 문서의 사소한 마무리를 정밀 재검수할 것.", "코드의 안정성을 증명하기 위해 테스트 커버리지 및 TDD 개발 프로세스 적용 경험을 추가할 것."]
            },
            "cj_olivenetworks": {
                "rating": "B+", "fit_score": 80,
                "summary": "인프라가 갖춰지지 않은 부트캠프 환경에서 원격 GPU 학습 서버를 주도적으로 구축해 낸 성장 열망('하고잡이' 정신)을 높이 삽니다. 다만 프로젝트의 주제들이 다소 전형적이어서 차별성이 필요합니다.",
                "strengths": [
                    {"title": "주도적인 한계 극복 스토리", "content": "비전공자라는 백그라운드 한계를 뛰어넘기 위해 원격 학습 인프라 구축을 도맡고, Docker 환경 표준화를 주도하며 팀에 기여한 성장의 역동성이 잘 전달됨."}
                ],
                "weaknesses": [
                    {"title": "전형적인 포트폴리오 구성", "content": "이탈 예측 및 AutoML 플랫폼 등은 전형적인 부트캠프 프로젝트로, 지원자만의 ONLYONE 독창성과 차별화 포인트가 부족해 보임."}
                ],
                "advice": ["개인 블로그 운영이나 오픈소스 기여 등 남들이 하지 않은 주도적이고 개성 있는 기술 시도를 프로젝트 전반에 가미해 보십시오."]
            }
        }
    },
    "송지현": {
        "title_desc": "CRM 데이터 분석가 및 MarTech AI 엔지니어 지망 (경력 전환자)",
        "summary": "오랜 고객센터(CS) 직무 경력을 살려 고객 중심의 기획과 비즈니스 가치 창출 관점을 훌륭히 어필하고 있습니다. 맛집 개인화 추천 엔진이나 정서 케어 AI 챗봇의 비동기 세션 연결 등 CRM 비즈니스에 밀접한 기능을 구현한 점이 뛰어납니다. 다만, 기술 스택에 나열한 LangGraph, Kafka, Docker 등에 비해 포트폴리오 상의 기여도가 '발표, 기획'에 편중되어 있습니다. 실제로 본인이 백엔드 API나 정량 데이터 분석(RFM, Churn) 로직을 직접 구현했는지 증명되지 않아 코딩 깊이가 약점으로 지적됩니다. 또한 3개 프로젝트의 수행 기간이 동일하게 복사-붙여넣기 오타 표기된 디테일 검수 미흡도 보완해야 합니다.",
        "agents": {
            "samsung_sds": {
                "rating": "C", "fit_score": 45,
                "summary": "CS 경력 기반의 CRM 도메인 이해도는 훌륭하나, 코어 코딩 및 백엔드 데이터베이스 최적화 구현 수준이 낮아 대용량 CRM 가용성 면접 및 알고리즘 코딩테스트 보완이 시급함.",
                "strengths": [
                    {"title": "사용자 편의적 안전망 기획", "content": "정서 케어 AI 개발 시 Function Calling을 도입하여 위기 상황을 실시간 감지하겠다는 논리 구조는 비즈니스 안전성 관점에서 준수함."}
                ],
                "weaknesses": [
                    {"title": "코어 엔지니어링 구현력 입증 실패", "content": "기술 스택에는 Kafka, Docker 등을 명시했으나 실제 본인의 기여는 '기획, UI/UX 설계, 발표, 단순 Prompt 작성'에 머물러 있어, 실제 백엔드 데이터 처리나 프레임워크 구현 역량을 전혀 파악할 수 없음."}
                ],
                "advice": ["단순 AI API 연동 기획에서 벗어나 Java/Spring Boot 또는 Python/FastAPI 기반의 API 설계, ORM 쿼리 튜닝 등 실질적인 코드 기여 내역을 코드로 증명할 것."]
            },
            "lg_cns": {
                "rating": "B-", "fit_score": 62,
                "summary": "고객 경험(UX) 최적화를 위한 RAG 챗봇 및 Roberta Zero-shot 접목 기획력은 좋으나, CRM 서버 실시간 API의 동시성 제어 및 인프라 디버깅(삽질) 기록이 없음.",
                "strengths": [
                    {"title": "트렌디한 AI 기술 시도", "content": "단순 별점 추천의 한계를 극복하기 위해 Roberta-base 모델의 Zero-shot 텍스트 문맥 이해 기능을 도입하고 RAG AI 챗봇을 설계하려 한 시도는 긍정적임."}
                ],
                "weaknesses": [
                    {"title": "CRM 특화 데이터 분석력 부재", "content": "CRM 지망임에도 불구하고, 실제 고객 분석에 필수적인 정량적 데이터 분석 기법(예: RFM 세그먼테이션, 고객 이탈 예측 ML 모델링)을 파이썬 코드로 직접 구현해 분석한 이력이 없음."}
                ],
                "advice": ["RAG 아키텍처 구성 외에, 고객 마케팅 데이터를 대상으로 한 정량적 Cohort 분석 또는 RFM 분류 알고리즘 구현 내역을 포트폴리오에 서술할 것."]
            },
            "shinsegae_inc": {
                "rating": "A-", "fit_score": 90,
                "summary": "고객센터 경력을 살린 강력한 고객 중심 마인드, 다차원 가중치 기반 개인화 추천 UI 설계 등 리테일/e-Commerce CRM 및 MarTech 분야에서 최상의 시너지를 낼 인재로 판단됨.",
                "strengths": [
                    {"title": "최상의 비즈니스 가치 포착 및 UI 설계", "content": "ME슐랭 서비스 개발 시 맛, 서비스, 분위기 등 5가지 다차원 가중치 조절 슬라이더 UI를 배치하여 개인화 추천의 편의성을 극대화한 점은 리테일테크 기획의 정석임."},
                    {"title": "공감 기반의 설득 및 소통 리더십", "content": "고객센터 경력의 도메인을 살려 고객 중심 마인드로 팀의 목표를 조율하고, 2차례의 발표를 통해 비즈니스 가치를 ROI 수치로 설득한 협업 리더십이 탁월함."}
                ],
                "weaknesses": [
                    {"title": "개발 기여 명세의 얇음", "content": "리테일테크 기획가로서는 만점이나, 엔지니어 지원자임에도 백엔드 시스템 동시성 처리나 로직의 예외 처리 등 핵심 개발 역량 서술이 매우 얇은 상태임."}
                ],
                "advice": ["비전공 코어 백엔드 개발자 직군 외에, 기술과 비즈니스를 잇는 CDP(고객데이터플랫폼) 솔루션 엔지니어 또는 CRM 데이터 분석가(DA) 직무로의 지원도 적극 고려할 것."]
            },
            "lotte_innovate": {
                "rating": "B-", "fit_score": 68,
                "summary": "임상급 정서 데이터를 다룰 때 개인정보 노출 우려를 방어하기 위해 AES-256-GCM 양방향 암호화를 기획하고 DB 격리 구조를 구상한 보안 안정 설계는 훌륭하나, 3개 프로젝트의 수행 기간이 동일한 오타 오류로 세부 꼼꼼함 검수 신뢰도가 약함.",
                "strengths": [
                    {"title": "데이터 보안 고려 설계", "content": "임상급 정서 데이터를 다룰 때 개인정보 노출 우려를 방어하기 위해 AES-256-GCM 양방향 암호화를 기획하고 DB 격리 구조를 구상한 안전 지향성은 칭찬함."}
                ],
                "weaknesses": [
                    {"title": "장표 세부 검수 오타 방치", "content": "3개 프로젝트 수행 기간이 모두 동일한 날짜(2026.02.12 - 2026.02.27)로 중복 기재되어 있어, 복사-붙여넣기 후 최종 검수를 누락한 듯한 인상을 주며 규격 신뢰도를 떨어뜨림."}
                ],
                "advice": ["각 프로젝트별 실제 다른 수행 일정을 정확히 기입하여 장표의 디테일 검수 신뢰도를 회복하십시오."]
            },
            "cj_olivenetworks": {
                "rating": "A-", "fit_score": 85,
                "summary": "CS 현장 경험을 최신 AI 에이전트 트렌드와 결합해 낸 '하고잡이' 성장 스토리가 돋보이며, CJ 멤버십 등 그룹사 CRM 분석가 및 마케팅 솔루션 엔지니어로 추천함.",
                "strengths": [
                    {"title": "ONLYONE 스토리를 담은 전향 노력", "content": "단순 기획에 멈추지 않기 위해 CS 직무 역량에 RAG 챗봇 및 감정 케어 에이전트와 같은 최신 기술 트렌드를 학습하여 도입한 진정성 있는 성장 궤적이 눈에 띔."}
                ],
                "weaknesses": [
                    {"title": "코딩 구현 깊이 보강 필요", "content": "기획력과 트렌드 캐치 능력에 비해 코드를 직접 설계하고 아키텍처 전문성을 해결한 디테일이 얇아, 주도적 1인 개발 역량을 더 보여줄 필요가 있음."}
                ],
                "advice": ["단순 API를 호출하는 프론트 뷰 중심 구현에서 나아가, 챗봇 대화 이력을 효율적으로 파이프라인화하여 데이터 레이크에 저장하는 흐름을 개발해 이력을 다변화해 보세요."]
            }
        }
    },
    "한정현": {
        "title_desc": "데이터/AI 엔지니어 지망 (정보통신공학 전공자)",
        "summary": "FastAPI 백엔드 전환 후 asyncio.to_thread 비동기 논블로킹 최적화, 메모리 캐시 및 RuntimeError 시 데이터 무결성을 보장하는 예외 격리 처리 등 탄탄한 전공자 수준의 아키텍처 설계 능력을 보여줍니다. 특히 분석 결과를 AWS S3에 적재하고 19슬라이드 PPT로 무편집 자동 조립·생성하는 파이프라인 개발은 SI 실무 관점에서 자동화 가치(ROI)가 높은 훌륭한 결과물입니다. 다만, 팀원(어창선)과 프로젝트 목록이 완전히 겹치기 때문에 '백엔드 비동기 및 자동화 엔진 전문성'을 서두에 배치해 어창선(인프라/검증 특화)과 역할을 쪼개는 정체성 세팅이 필요합니다. 또한 강사님 편지에 썼던 '5-Tier 자가치유 하네스(Guardian v2)'와 'pgvector 자가학습 RAG'는 본인의 최대 무기인데 포트폴리오 본문에 누락되었으므로 즉시 통합해야 하며, 마미코 장표의 이미지 겹침 오타와 캐주얼한 Notion 대문 표지는 정밀하고 정갈한 PDF 규격으로 교체할 필요가 있습니다.",
        "agents": {
            "samsung_sds": {
                "rating": "A-", "fit_score": 86,
                "summary": "비결정적인 LLM 출력을 고정 ID 라우팅으로 통제하고, try/except 슬라이드 단위 격리로 단일 오류 전파를 차단하는 등 대형 SI 인프라에 필수적인 예외 복구 및 자동화 성능 설계가 매우 논리적입니다.",
                "strengths": [
                    {"title": "시스템 예외 고립화 설계", "content": "단일 컴포넌트의 에러가 시스템 전체 붕괴로 번지지 않도록 슬라이드별 try/except 격리를 설계하고, 데이터 누수를 일으킬 수 있는 id-like 컬럼을 자동으로 필터링하도록 가드레일을 짠 점은 삼성SDS가 추구하는 아키텍처 정밀성에 정확히 부합함."},
                    {"title": "실질적 개발 자동화 공헌", "content": "결과물을 S3와 연동해 19페이지 PPT로 무편집 조립하는 엔진을 구현한 것은 비즈니스 효율성(ROI) 측면에서 매우 설득력 있는 강점임."}
                ],
                "weaknesses": [
                    {"title": "팀원과의 차별화 부족", "content": "동일 팀원과 동일한 프로젝트 세트를 기재하여 각자의 독자적인 엔지니어링 공헌도가 무엇인지 첫눈에 구분하기 어려움."}
                ],
                "advice": ["FastAPI 비동기 성능 최적화(논블로킹 IO)와 파이프라인 자동화 모듈러 개발 능력을 포트폴리오 전반에 전진 배치하여 특화시킬 것."]
            },
            "lg_cns": {
                "rating": "A", "fit_score": 92,
                "summary": "FastAPI 비동기 논블로킹 전환 및 qwen2.5/Claude CLI 기반의 5-Tier 자가치유 에러 복구 하네스(Guardian v2) 설계 등 최신 클라우드/AI 아키텍처 트렌드를 적극 활용한 최고의 Game Changer형 신입 엔지니어입니다.",
                "strengths": [
                    {"title": "도전적인 자가치유 하네스 설계", "content": "과거 코드 실패 및 중단 이력을 pgvector 임베딩 검색으로 찾아와 로컬 LLM을 거쳐 자동으로 복구 코드를 적용하는 하네스 인프라를 구상한 도전적 시도는 LG CNS 채용팀이 가장 눈독 들일 만한 훌륭한 무기임."},
                    {"title": "비동기 서버 전환 및 성능 최적화", "content": "Flask에서 FastAPI로 전면 전환하고, asyncio.to_thread를 적용하여 무거운 CPU-bound 작업이 서버를 블로킹하지 않도록 논블로킹 처리한 삽질 과정이 우수함."}
                ],
                "weaknesses": [
                    {"title": "핵심 기술의 장표 배치 부족", "content": "자가치유 하네스 및 pgvector 자가학습 이력이 포트폴리오 본문에서 다소 배제되거나 축소되어 있어 핵심 설계 성과가 충분히 조명되지 않음."}
                ],
                "advice": ["자가치유 하네스(Harness) 5단계 에러 자가복구 다이어그램과 핵심 코드 조각을 포트폴리오에 무조건 1~2페이지 할당해 적극 전진 배치할 것."]
            },
            "shinsegae_inc": {
                "rating": "B+", "fit_score": 78,
                "summary": "개인화 날씨 추천 TPO 엔진 및 캐시/폴백 구조를 깔끔하게 연동한 점이 훌륭하나, 마미코(AI 스타일리스트) 프로젝트 등에서 사용자의 상세 경험적 성과(UX)나 리테일 서비스의 실제적 비즈니스 가치 평가가 보완되어야 합니다.",
                "strengths": [
                    {"title": "생활 밀착형 백엔드 서비스 구현", "content": "날씨 기반 개인 맞춤형 스타일 서비스를 제공하기 위해 기상청 API 연동 회차별 메모리 캐시 및 폴백 구조를 깔끔하게 결합하여 서비스 안정성을 챙김."}
                ],
                "weaknesses": [
                    {"title": "디테일 시각화 검수 미흡", "content": "마미코 아키텍처 슬라이드 배경에 이전 프로젝트(ADA)의 다이어그램이 겹쳐 인쇄되는 등 꼼꼼한 마무리가 아쉬움."}
                ],
                "advice": ["리테일테크 분야의 대량 동시 주문 상황 등을 고려해 캐시 무력화(Cache Invalidation) 전략 및 분산 락(Distributed Lock) 활용 경험을 보완할 것."]
            },
            "lotte_innovate": {
                "rating": "B+", "fit_score": 82,
                "summary": "데이터 업로드 정합성 보장(RuntimeError 예외 격리) 및 무편집 슬라이드 조립 엔진 등 안전하고 신뢰성 높은 시스템 설계 역량은 훌륭하나, 아키텍처 설명 장표의 이미지 겹침 오점은 반드시 수정해야 합니다.",
                "strengths": [
                    {"title": "데이터 무결성을 챙긴 예외 처리", "content": "이미지 업로드 실패 시 깨진 쓰레기 데이터가 DB에 영속화되지 않도록 RuntimeError 예외 격리를 설계하여 데이터 정합성 가드를 탄탄히 확보함."}
                ],
                "weaknesses": [
                    {"title": "사소한 세부 검수 결여", "content": "마미코 아키텍처 설명 장표의 배경 이미지가 이전 프로젝트의 시스템 흐름도로 들어가 있어, 서류 완성도와 꼼꼼한 마무리 부분에서 신뢰성이 하락함."}
                ],
                "advice": ["장표의 중복 이미지 에러를 정정하고, 백엔드 API 설계 규격서(Swagger) 및 테스트 케이스 목록을 문서에 보완 추가할 것."]
            },
            "cj_olivenetworks": {
                "rating": "A-", "fit_score": 85,
                "summary": "단순 챗봇을 넘어 PPT 자동 완성 조립 엔진 등 독창적이고 주도적인 솔루션(ONLYONE) 개발을 리딩한 성과를 높이 평가합니다. 다만 표지의 캐주얼함은 다듬을 필요가 있습니다.",
                "strengths": [
                    {"title": "독창적 자동화 엔진 개발 리딩", "content": "정형 데이터 분석 결과를 기반으로 19슬라이드 PPT를 실시간으로 조립해 무편집으로 조립해 주는 엔진을 고안하고 개발해 낸 주도성과 개성이 독보적임."}
                ],
                "weaknesses": [
                    {"title": "지나치게 캐주얼한 대문 구성", "content": "포트폴리오 표지에 노션 링크 캡처본을 배치한 것은 전공자의 심도 있는 기술 아키텍처 내실에 비해 다소 가벼운 첫인상을 줄 우려가 있음."}
                ],
                "advice": ["첫 페이지에 본인의 핵심 기술 역량과 강점을 3가지 키워드로 압축한 정식 포트폴리오 커버 페이지를 설계해 적용하십시오."]
            }
        }
    },
    "현다은": {
        "title_desc": "Data Analyst 및 AI 서비스 개발자 지망 (비전공자)",
        "summary": "인문학적 배경(문화인류학)에서 출발하여 머신러닝, 자연어처리(NLP), 컴퓨터 비전(CV), LLM 등 AI 전 영역의 기술 스택을 주도적으로 학습하고 접목한 '하고잡이' 성장 궤적이 매우 훌륭합니다. 특히 팀 프로젝트의 깃허브 관리자(Release Manager) 역할을 맡아 브랜치 머지 전략 수립과 CI/CD 구축을 리딩한 협업 경험과 퍼스널컬러 KNN 모델의 가중치 튜닝을 통해 오탐을 해결한 논리적 트러블슈팅이 우수합니다. 다만 여러 분야의 AI 모델을 얕게 경험하여 기술적 깊이가 분산되어 보일 수 있고, 대규모 분산 서버나 데이터베이스 최적화 기여 이력이 약하므로 본인만의 코어 기술 분야를 명확히 세울 필요가 있습니다. 동아리 예산 1,000만 원 관리 등 인문학적 소통 경험을 서비스 기획 및 개발 리더십과 엮은 스토리텔링은 훌륭한 차별화 요소입니다.",
        "agents": {
            "samsung_sds": {
                "rating": "B", "fit_score": 75,
                "summary": "비전공자임에도 다양한 AI 분야(ML, NLP, CV, LLM)를 두루 다뤄본 경험과 GitHub Release Manager로서의 브랜치 관리 역량은 좋으나, 삼성SDS 코어 백엔드/SI 분야에 요구되는 컴퓨터 사이언스(CS) 깊이와 대용량 트래픽 설계 검증이 보완되어야 합니다.",
                "strengths": [
                    {"title": "체계적인 형상 관리 리딩", "content": "7개 브랜치에 걸친 소스 코드 머지 전략 수립, PR 리뷰 및 버전 배포를 직접 리딩하는 형상 관리자 역할을 수행한 점은 대형 프로젝트 협업 관점에서 훌륭한 아웃풋임."},
                    {"title": "다양한 인공지능 프레임워크 경험", "content": "BERTopic, OpenCV, MediaPipe, LoRA 파인튜닝 등 분야별 기술을 직접 구동하고 서비스 백엔드(FastAPI)와 연동해 본 넓은 기술 이해도를 보유함."}
                ],
                "weaknesses": [
                    {"title": "기술적 스택의 깊이 분산", "content": "인공지능의 네 가지 분야를 모두 기재하여 신입 지원자로서 한 우물을 깊게 파지 못한 '넓고 얕은' 지식 구조로 보일 우려가 있으며, 코어 자료구조 및 DB 분산 락 등에 대한 기술적 어필이 약함."}
                ],
                "advice": ["자료구조와 알고리즘 문제를 해결하는 실질적 코딩 역량 강화 및 데이터 아키텍처 이론 보완 요망."]
            },
            "lg_cns": {
                "rating": "A-", "fit_score": 87,
                "summary": "GitHub Action 기반 CI/CD 구축 시도와 퍼스널컬러 알고리즘 K값 튜닝 과정 등 수치 중심의 디버깅/트러블슈팅 이력이 논리적이고 우수하여 CNS의 DX 기술 직무에 적합합니다.",
                "strengths": [
                    {"title": "실질적 DevOps 인프라 기여", "content": "부트캠프 과정 중 CI/CD 배포 파이프라인 설계에 참여하고, Docker 및 GitHub 협업 인프라를 구축하려 한 시도가 실무적임."},
                    {"title": "알고리즘 일반화 및 최적화 경험", "content": "퍼스널컬러 진단 모델의 눈 영역 과의존 오류를 수정하기 위해 가중치를 조절(100%->5%)하고 K값을 최적화하여 윈터 판정 편향을 해결한 수리적 개선 이력이 우수함."}
                ],
                "weaknesses": [
                    {"title": "Cerebras API 활용 깊이의 아쉬움", "content": "Cerebras를 활용한 정서 케어 RAG 챗봇 구축 시, 프롬프트 엔지니어링 외에 모델 서빙 최적화나 벡터 데이터 파이프라인의 실질적 구현 흔적이 적음."}
                ],
                "advice": ["Kubernetes(K8s) 오케스트레이션 개념 및 IaC(Terraform) 기술을 추가 학습해 DevOps 역량을 차별화할 것."]
            },
            "shinsegae_inc": {
                "rating": "B+", "fit_score": 80,
                "summary": "리뷰 감성분석 기반 식당 추천과 퍼스널컬러 기반 화장품 립 추천 등 리테일 및 e-Commerce 서비스 도메인과의 융합 가치가 돋보입니다.",
                "strengths": [
                    {"title": "리테일테크 융합 프로젝트 우수", "content": "ME슐랭의 고객 리뷰 토픽 모델링 추천 및 이미지 분석 기반의 맞춤형 립 제품 추천 시스템은 e-Commerce 커머스 플랫폼과 즉시 연계 가능한 매력적인 리테일 도메인 프로젝트임."}
                ],
                "weaknesses": [
                    {"title": "대규모 비즈니스 가용성 입증 부족", "content": "FastAPI와 PostgreSQL을 도입했으나, 결제 대기열 처리나 분산 트랜잭션, Redis 캐시 활용과 같은 대규모 동시 접속 환경을 가정한 개발 흔적이 적음."}
                ],
                "advice": ["추천 서버의 실시간 응답성 확보를 위해 캐싱 전략(Redis)을 가미하거나 데이터 인덱싱 최적화 방안을 추가 보완하십시오."]
            },
            "lotte_innovate": {
                "rating": "B+", "fit_score": 83,
                "summary": "문제 정의부터 솔루션, 수치적 결과까지 논리정연하게 작성된 문서화 완성도가 매우 우수하며, 형상 관리 원칙을 준수하려는 태도와 수치 튜닝을 통한 에러 대처 꼼꼼함이 돋보입니다.",
                "strengths": [
                    {"title": "논리정연한 문제 해결과 문서화", "content": "포트폴리오의 각 프로젝트 장표가 Problem -> Solution -> Result의 계량적 수치 기반으로 깔끔하게 레이아웃이 정돈되어 있어 성실함과 꼼꼼함을 보여줌."}
                ],
                "weaknesses": [
                    {"title": "코드 안정성 테스트 부재", "content": "인프라와 깃 관리는 철저하나, 시스템의 코드가 제대로 동작하는지 빌드 시 확인해 주는 단위 테스트(Unit Test) 작성 및 커버리지 이력이 명시되지 않음."}
                ],
                "advice": ["PyTest 등을 활용한 단위 테스트 커버리지 갱신 이력 및 TDD 개발 사례를 한 페이지 보완하십시오."]
            },
            "cj_olivenetworks": {
                "rating": "A-", "fit_score": 86,
                "summary": "인문학적 통찰(고고문화인류 동아리 리더십)을 기술과 결합하여 감성적인 립 추천, 감정 케어 시스템을 구현해 낸 ONLYONE 성장 궤적이 참신합니다.",
                "strengths": [
                    {"title": "인문-기술 융합형 '하고잡이' 역량", "content": "동아리 예산 1,000만 원 확보 및 유물 전산화 전시회 기획 등 인문학적 소통 역량을 갖추었으며, 이를 감성 분석 기술(하트비트, ME슐랭)에 녹여내어 개성 있는 스토리를 구축함."}
                ],
                "weaknesses": [
                    {"title": "직무 전문성 포커싱 조율", "content": "NLP, CV, ML, LLM 스택이 혼재되어 있어 향후 입사 시 백엔드 엔지니어링 혹은 데이터 분석가 중 어떤 포지션의 전문성을 주도할지 경계가 흐려질 위험이 있음."}
                ],
                "advice": ["자신의 인문학적 소통력을 강점으로 삼아 '데이터와 사용자를 연결하는 AI 서비스 풀스택 엔지니어'로 아이덴티티를 명확히 포지셔닝해 보십시오."]
            }
        }
    }
}

# =====================================================================
# 🎨 2. 다자 에이전트 프리미엄 HTML 리포트 템플릿 생성 함수
# =====================================================================
def get_student_report_html(student_name, student_meta):
    title_desc = student_meta["title_desc"]
    summary = student_meta["summary"]
    agents = student_meta["agents"]
    
    # 등급별 뱃지 색상 매핑
    rating_colors = {
        "S": {"bg": "#E8F5E9", "text": "#2E7D32", "border": "#A5D6A7"},
        "A": {"bg": "#E3F2FD", "text": "#1565C0", "border": "#90CAF9"},
        "A-": {"bg": "#E3F2FD", "text": "#1565C0", "border": "#90CAF9"},
        "B+": {"bg": "#FFF3E0", "text": "#EF6C00", "border": "#FFCC80"},
        "B": {"bg": "#FFF3E0", "text": "#EF6C00", "border": "#FFCC80"},
        "B-": {"bg": "#FFF3E0", "text": "#EF6C00", "border": "#FFCC80"},
        "C+": {"bg": "#F3E5F5", "text": "#6A1B9A", "border": "#CE93D8"},
        "C": {"bg": "#FFEBEE", "text": "#C62828", "border": "#EF9A9A"},
        "D": {"bg": "#FFEBEE", "text": "#C62828", "border": "#EF9A9A"}
    }
    
    # 요약 테이블 생성
    table_rows_html = ""
    company_details = {
        "samsung_sds": {"name": "삼성SDS", "recruiter": "*** 책임"},
        "lg_cns": {"name": "LG CNS", "recruiter": "*** 책임전문위원"},
        "shinsegae_inc": {"name": "신세계I&C", "recruiter": "*** 과장"},
        "lotte_innovate": {"name": "롯데이노베이트", "recruiter": "*** 수석"},
        "cj_olivenetworks": {"name": "CJ올리브네트웍스", "recruiter": "*** 과장"}
    }
    
    for key, c_info in company_details.items():
        agent_data = agents[key]
        r = agent_data["rating"]
        b = rating_colors.get(r, {"bg": "#F5F5F5", "text": "#616161", "border": "#E0E0E0"})
        table_rows_html += f"""
        <tr>
            <td style="font-weight: 700; color: #ffffff; padding: 12px 10px; border-bottom: 1px solid rgba(255,255,255,0.15);">{c_info['name']}</td>
            <td style="color: #63b3ed; font-weight: 600; padding: 12px 10px; border-bottom: 1px solid rgba(255,255,255,0.15);">{c_info['recruiter']}</td>
            <td style="color: #cbd5e1; padding: 12px 10px; border-bottom: 1px solid rgba(255,255,255,0.15); font-size: 0.85rem; line-height: 1.45; text-align: left;">{agent_data['summary']}</td>
            <td style="padding: 12px 10px; border-bottom: 1px solid rgba(255,255,255,0.15); text-align: center;">
                <span style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.05rem; color: #ffffff;">{agent_data['fit_score']}점</span>
            </td>
            <td style="padding: 12px 10px; border-bottom: 1px solid rgba(255,255,255,0.15); text-align: center;">
                <span style="background-color: {b['bg']}; color: {b['text']}; border: 1px solid {b['border']}; padding: 3px 8px; border-radius: 4px; font-weight: 800; font-family: 'Outfit', sans-serif; font-size: 0.85rem;">{r}</span>
            </td>
        </tr>
        """
        
    # 각 기업 에이전트 상세 피드백 페이지 HTML 생성
    agent_pages_html = ""
    agent_meta_definitions = {
        "samsung_sds": {
            "company": "삼성SDS",
            "role_title": "책임",
            "department": "인사팀",
            "experience": "경력 11년 차",
            "quote": "기초가 흔들리는 아키텍처는 사상누각일 뿐입니다. 자료구조와 알고리즘, CS 기본기를 철저히 검증합니다.",
            "color_primary": "#0A2540",
            "color_secondary": "#0056B3",
            "color_bg": "#f4f7fa"
        },
        "lg_cns": {
            "company": "LG CNS",
            "role_title": "책임전문위원",
            "department": "DX인재개발팀",
            "experience": "경력 12년 차",
            "quote": "안주하지 않는 자가 DX 판도를 바꿉니다. 당신이 겪은 시행착오(Troubleshooting)와 기술적 도전의 크기를 보여주세요.",
            "color_primary": "#A50034",
            "color_secondary": "#4E5B6A",
            "color_bg": "#faf4f5"
        },
        "shinsegae_inc": {
            "company": "신세계I&C",
            "role_title": "과장",
            "department": "Retail Tech 인사파트",
            "experience": "경력 10년 차",
            "quote": "아무리 훌륭한 기술이라도 고객에게 닿지 못하면 무용지물입니다. 비즈니스 실용성과 완성도를 확인합니다.",
            "color_primary": "#B9975B",
            "color_secondary": "#111111",
            "color_bg": "#f9f7f4"
        },
        "lotte_innovate": {
            "company": "롯데이노베이트",
            "role_title": "수석",
            "department": "HR혁신팀",
            "experience": "경력 13년 차",
            "quote": "시스템의 기본은 타협 없는 안정성과 빈틈없는 예외 처리입니다. 성실함이 깃든 테스트 코드가 신뢰를 증명합니다.",
            "color_primary": "#E11B22",
            "color_secondary": "#2C3E50",
            "color_bg": "#fcf5f5"
        },
        "cj_olivenetworks": {
            "company": "CJ올리브네트웍스",
            "role_title": "과장",
            "department": "테크HR파트",
            "experience": "경력 10년 차",
            "quote": "남들이 하지 않은 차별화된 독창성(ONLYONE)과 주도적인 학습 태도(하고잡이)에서 진짜 개발자의 잠재력이 드러납니다.",
            "color_primary": "#E06F1D",
            "color_secondary": "#22B14C",
            "color_bg": "#f5faf6"
        }
    }
    
    for key, meta in agent_meta_definitions.items():
        data = agents[key]
        r = data["rating"]
        badge = rating_colors.get(r, {"bg": "#F5F5F5", "text": "#616161", "border": "#E0E0E0"})
        
        strengths_sub_html = ""
        for s in data["strengths"]:
            strengths_sub_html += f"""
            <div class="card strength-card">
                <div class="card-header">
                    <svg class="icon-success" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <h3>{s['title']}</h3>
                </div>
                <div class="card-body">
                    <p>{s['content']}</p>
                </div>
            </div>
            """
            
        weaknesses_sub_html = ""
        for w in data["weaknesses"]:
            weaknesses_sub_html += f"""
            <div class="card weakness-card">
                <div class="card-header">
                    <svg class="icon-danger" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                    </svg>
                    <h3>{w['title']}</h3>
                </div>
                <div class="card-body">
                    <p>{w['content']}</p>
                </div>
            </div>
            """
            
        advice_sub_html = ""
        for a in data["advice"]:
            advice_sub_html += f"""
            <li class="advice-item">
                <svg class="icon-info" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="color: {meta['color_secondary']};">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
                <span>{a}</span>
            </li>
            """
            
        agent_pages_html += f"""
        <div class="page-break" style="page-break-before: always; padding-top: 1cm;">
            <!-- Header -->
            <div class="header" style="border-bottom: 2px solid {meta['color_primary']};">
                <div class="header-left">
                    <span class="company-badge" style="color: {meta['color_primary']};">{meta['company']}</span>
                    <h1 class="report-title">포트폴리오 개별 평가 리포트</h1>
                </div>
                <div class="candidate-info">
                    <strong>지원자:</strong> {student_name}님 &nbsp;&nbsp;|&nbsp;&nbsp; <strong>진단 분야:</strong> SW 개발
                </div>
            </div>

            <!-- Recruiter Profile -->
            <div class="profile-section" style="border-left: 4px solid {meta['color_primary']}; background-color: {meta['color_bg']};">
                <div class="profile-container">
                    <div class="avatar" style="background-color: {meta['color_primary']}; font-size: 1.1rem;">HR</div>
                    <div class="profile-details">
                        <div class="recruiter-meta">
                            <span class="recruiter-name">*** {meta['role_title']}</span>
                            <span class="recruiter-role" style="border: 1px solid var(--border-color); color: var(--text-light);">{meta['department']}</span>
                            <span class="recruiter-role" style="border: 1px solid var(--border-color); color: var(--text-light);">{meta['experience']}</span>
                        </div>
                        <p class="recruiter-quote" style="color: #475569;">"{meta['quote']}"</p>
                    </div>
                </div>
            </div>

            <!-- Score & Summary -->
            <div class="score-section">
                <div class="rating-box" style="border: 2px solid {badge['border']}; background-color: {badge['bg']};">
                    <span class="rating-label" style="color: {badge['text']};">평가 등급</span>
                    <span class="rating-value" style="color: {badge['text']};">{r}</span>
                </div>
                <div class="score-box" style="border: 1px solid var(--border-color);">
                    <div class="fit-score-container">
                        <div class="fit-score-header">
                            <span class="fit-score-label">인재상 부합도</span>
                            <span class="fit-score-value" style="color: {meta['color_primary']};">{data['fit_score']}점</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="background: linear-gradient(90deg, {meta['color_primary']}, {meta['color_secondary']}); width: {data['fit_score']}%;"></div>
                        </div>
                    </div>
                    <p class="summary-text">
                        <strong>[총평]</strong> {data['summary']}
                    </p>
                </div>
            </div>

            <!-- Strengths -->
            <h2 class="section-title" style="border-left: 5px solid {meta['color_primary']};">👍 좋은 점 (Strengths)</h2>
            {strengths_sub_html}

            <!-- Weaknesses -->
            <h2 class="section-title" style="border-left: 5px solid {meta['color_primary']};">⚠️ 부족한 점 및 개선 사항 (Areas for Improvement)</h2>
            {weaknesses_sub_html}

            <!-- Advice -->
            <h2 class="section-title" style="border-left: 5px solid {meta['color_primary']};">💡 인사담당자 실무자의 합격 조언</h2>
            <ul class="advice-list">
                {advice_sub_html}
            </ul>

            <!-- Footer -->
            <div class="footer">
                <span>&copy; 2026 {meta['company']} HR Expert Feedback. All rights reserved.</span>
                <span>Confidential | For Coaching Purpose Only</span>
            </div>
        </div>
        """

    # 전체 HTML 결합
    full_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>[피드백 리포트] {student_name}님 포트폴리오 심층진단</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.8/dist/web/static/pretendard-dynamic-subset.css');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');

        :root {{
            --primary: #0A2540;
            --secondary: #0056B3;
            --text-dark: #2c3e50;
            --text-light: #64748b;
            --card-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.03);
            --border-color: #e2e8f0;
        }}

        body {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
            color: var(--text-dark);
            background-color: #ffffff;
            margin: 0;
            padding: 0;
            line-height: 1.6;
            -webkit-print-color-adjust: exact;
        }}

        .container {{
            max-width: 850px;
            margin: 0 auto;
            padding: 2rem;
        }}

        /* Header Area */
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 1.2rem;
            margin-bottom: 1.8rem;
        }}

        .header-left {{
            display: flex;
            flex-direction: column;
        }}

        .company-badge {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 1.4rem;
            letter-spacing: -0.05em;
            margin: 0 0 0.2rem 0;
        }}

        .report-title {{
            font-size: 1.7rem;
            font-weight: 700;
            color: #0f172a;
            margin: 0;
        }}

        .candidate-info {{
            font-size: 0.95rem;
            color: var(--text-light);
            margin-top: 0.5rem;
        }}

        /* Recruiter Profile Card */
        .profile-section {{
            border-radius: 12px;
            padding: 1.3rem;
            margin-bottom: 2rem;
            box-shadow: var(--card-shadow);
        }}

        .profile-container {{
            display: flex;
            align-items: flex-start;
            gap: 1rem;
        }}

        .avatar {{
            width: 55px;
            height: 55px;
            border-radius: 50%;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            font-weight: bold;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}

        .profile-details {{
            flex: 1;
        }}

        .recruiter-meta {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.25rem;
        }}

        .recruiter-name {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #0f172a;
            margin: 0;
        }}

        .recruiter-role {{
            font-size: 0.85rem;
            background: #ffffff;
            padding: 0.1rem 0.5rem;
            border-radius: 4px;
        }}

        .recruiter-quote {{
            font-style: italic;
            margin: 0.4rem 0 0 0;
            font-size: 0.92rem;
            line-height: 1.5;
        }}

        /* Evaluation Score Summary */
        .score-section {{
            display: grid;
            grid-template-columns: 1fr 2.5fr;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .rating-box {{
            border-radius: 12px;
            padding: 1.2rem;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}

        .rating-label {{
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 0.4rem;
        }}

        .rating-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 3.2rem;
            font-weight: 800;
            line-height: 1;
        }}

        .score-box {{
            border-radius: 12px;
            padding: 1.2rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .fit-score-container {{
            margin-bottom: 0.8rem;
        }}

        .fit-score-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.4rem;
        }}

        .fit-score-label {{
            font-size: 0.92rem;
            font-weight: 700;
            color: #0f172a;
        }}

        .fit-score-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
        }}

        .progress-bar {{
            height: 8px;
            background: #f1f5f9;
            border-radius: 999px;
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            border-radius: 999px;
        }}

        .summary-text {{
            font-size: 0.92rem;
            color: #334155;
            margin: 0;
            line-height: 1.5;
        }}

        /* Section Titles */
        .section-title {{
            font-size: 1.2rem;
            font-weight: 700;
            color: #0f172a;
            padding-left: 0.6rem;
            margin: 2rem 0 1rem 0;
        }}

        /* Cards Design */
        .card {{
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.1rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
            page-break-inside: avoid;
        }}

        .card-header {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.6rem;
        }}

        .card-header h3 {{
            font-size: 1rem;
            font-weight: 700;
            color: #0f172a;
            margin: 0;
        }}

        .card-body p {{
            font-size: 0.92rem;
            color: #334155;
            margin: 0;
            line-height: 1.5;
        }}

        .strength-card {{
            border-left: 4px solid #22c55e;
        }}

        .weakness-card {{
            border-left: 4px solid #ef4444;
        }}

        /* Icons */
        .icon-success {{
            width: 18px;
            height: 18px;
            color: #22c55e;
        }}

        .icon-danger {{
            width: 18px;
            height: 18px;
            color: #ef4444;
        }}

        .icon-info {{
            width: 20px;
            height: 20px;
            flex-shrink: 0;
        }}

        /* Advice List */
        .advice-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .advice-item {{
            display: flex;
            align-items: flex-start;
            gap: 0.6rem;
            background: #f8fafc;
            border-radius: 6px;
            padding: 0.8rem;
            margin-bottom: 0.6rem;
            font-size: 0.92rem;
            color: #334155;
            line-height: 1.5;
            page-break-inside: avoid;
        }}

        /* Footer */
        .footer {{
            margin-top: 3rem;
            border-top: 1px solid var(--border-color);
            padding-top: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.78rem;
            color: var(--text-light);
        }}

        /* Cover Page Styling */
        .cover-page {{
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 3rem 2rem;
            box-sizing: border-box;
            background: linear-gradient(135deg, #0A2540 0%, #1A365D 50%, #2A4365 100%);
            color: #ffffff;
        }}

        .cover-top {{
            border-bottom: 1px solid rgba(255,255,255,0.15);
            padding-bottom: 2rem;
        }}

        .cover-title {{
            font-size: 2.3rem;
            font-weight: 800;
            line-height: 1.35;
            margin: 0 0 1rem 0;
            letter-spacing: -0.03em;
        }}

        .cover-subtitle {{
            font-size: 1.2rem;
            color: #63b3ed;
            margin: 0;
        }}

        .cover-middle {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem 0;
        }}

        .cover-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 2rem;
            width: 100%;
        }}

        .cover-card-title {{
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 1.2rem;
            border-bottom: 2px solid #63b3ed;
            padding-bottom: 0.5rem;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1.5fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }}

        .info-label {{
            font-size: 0.85rem;
            color: #cbd5e1;
            margin-bottom: 0.25rem;
        }}

        .info-value {{
            font-size: 1.15rem;
            font-weight: 700;
        }}

        .cover-bottom {{
            font-size: 0.85rem;
            color: #94a3b8;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 1.2rem;
        }}

        @media print {{
            .cover-page {{
                height: 100vh;
                page-break-after: always;
            }}
            .page-break {{
                page-break-after: always;
            }}
            .page-break:last-child {{
                page-break-after: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 📄 PAGE 1: COVER PAGE -->
        <div class="cover-page">
            <div class="cover-top">
                <h1 class="cover-title">SW 개발자 포트폴리오<br>다자(Multi-Agent) 심층 진단 보고서</h1>
                <p class="cover-subtitle">5대 IT 대기업 채용담당자 공동 심사 결과</p>
            </div>
            
            <div class="cover-middle">
                <div class="cover-card">
                    <h2 class="cover-card-title">평가 대상자 및 핵심 요약</h2>
                    <div class="info-grid">
                        <div>
                            <div class="info-label">지원 학생명</div>
                            <div class="info-value" style="color: #63b3ed; font-size: 1.3rem;">{student_name}님</div>
                        </div>
                        <div>
                            <div class="info-label">지원 분야 및 타깃 상태</div>
                            <div class="info-value">{title_desc}</div>
                        </div>
                    </div>
                    
                    <h3 style="font-size: 1.05rem; font-weight: 700; color: #e2e8f0; margin-bottom: 0.5rem;">📋 다차원 종합 총평</h3>
                    <p style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.55; margin: 0;">
                        {summary}
                    </p>
                </div>
            </div>
            
            <div style="margin-top: 1rem; background: rgba(255,255,255,0.02); border-radius: 12px; padding: 1.2rem; border: 1px solid rgba(255,255,255,0.05); page-break-inside: avoid;">
                <h3 style="font-size: 1.05rem; color: #ffffff; margin-top: 0; margin-bottom: 0.8rem; text-align: center;">📊 기업별 인사담당자 의견 및 평가 요약</h3>
                <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left;">
                    <thead>
                        <tr style="border-bottom: 2px solid rgba(255,255,255,0.15);">
                            <th style="padding: 10px; color: #cbd5e1; width: 15%;">평가 기업</th>
                            <th style="padding: 10px; color: #cbd5e1; width: 18%;">담당자</th>
                            <th style="padding: 10px; color: #cbd5e1; width: 47%;">인사담당자 피드백 의견</th>
                            <th style="padding: 10px; color: #cbd5e1; width: 10%; text-align: center;">부합도</th>
                            <th style="padding: 10px; color: #cbd5e1; width: 10%; text-align: center;">추천 등급</th>
                        </tr>
                    </thead>
                    <tbody style="color: #cbd5e1;">
                        {table_rows_html}
                    </tbody>
                </table>
            </div>

            <div class="cover-bottom">
                <span>DMDG AI & Cloud Boot Camp | Portfolio Multi-Evaluation Report</span>
                <span>Confidential</span>
            </div>
        </div>

        <!-- 📄 PAGES 2-6: AGENT DETAILS -->
        {agent_pages_html}
    </div>
</body>
</html>
"""
    return full_html

# =====================================================================
# 🚀 3. 메인 실행 함수
# =====================================================================
def main():
    print("=" * 60)
    print("🤖 API Key 없이 구동하는 4대 학생 통합 포트폴리오 PDF 생성기 (개선판) 🤖")
    print("=" * 60)

    # 출력 폴더 생성
    output_dir = "portfolio_feedbacks"
    os.makedirs(output_dir, exist_ok=True)
    
    # 임시 HTML 캐시 폴더 생성
    html_cache_dir = "html_cache_feedbacks"
    os.makedirs(html_cache_dir, exist_ok=True)

    # 브라우저 경로 탐색
    browser_path = find_browser_path()
    if not browser_path:
        print("⚠️ 에러: 시스템에서 Google Chrome 또는 Microsoft Edge를 찾을 수 없습니다.")
        print("👉 HTML 파일만 생성되고 PDF 변환은 건너뜁니다.")
    else:
        print(f"🎯 발견된 브라우저 엔진: {browser_path}")

    # 학생별 리포트 생성 및 인쇄
    for student_name, student_meta in FEEDBACK_DATA.items():
        print(f"\n👉 [{student_name}] 학생 다자 에이전트 피드백 리포트 작성 중...")
        
        # HTML 생성
        html_content = get_student_report_html(student_name, student_meta)
        
        # HTML 저장
        html_filename = f"{student_name}_다면_평가_통합_리포트.html"
        html_path = os.path.join(html_cache_dir, html_filename)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"   ✓ HTML 생성 완료: {html_path}")
        
        # PDF 변환
        if browser_path:
            pdf_filename = f"[피드백 리포트] {student_name}_포트폴리오_심층진단.pdf"
            pdf_path = os.path.abspath(os.path.join(output_dir, pdf_filename))
            abs_html_path = os.path.abspath(html_path)
            
            # 크롬 격리 프로필 설정
            profile_dir = os.path.abspath(os.path.join(html_cache_dir, f"profile_print_{student_name}"))
            file_url = "file:///" + abs_html_path.replace("\\", "/")
            
            cmd = [
                browser_path,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                f"--user-data-dir={profile_dir}",
                f"--print-to-pdf={pdf_path}",
                "--no-pdf-header-footer",
                file_url
            ]
            
            try:
                subprocess.run(cmd, check=True, timeout=40, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"   ✨ PDF 리포트 인쇄 완료! -> {pdf_path}")
            except Exception as pe:
                print(f"   ❌ PDF 변환 중 오류 발생: {pe}")
        else:
            print("   👉 PDF 인쇄 엔진 부재로 변환을 중단합니다.")

    print("\n" + "=" * 60)
    print("🎉 모든 작업이 완료되었습니다!")
    print(f"📂 최종 PDF 보관 위치: {os.path.abspath(output_dir)}")
    print("=" * 60)

def find_browser_path():
    """윈도우 환경에서 Chrome 또는 Edge 브라우저의 설치 경로를 검색합니다."""
    candidate_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe")
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            return path
    return None

if __name__ == "__main__":
    main()
