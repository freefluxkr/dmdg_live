# 심화 3: 지속 메모리 & 모델 정렬 역량 평가 (30문항)
> 출처 도서: https://wikidocs.net/book/22037 | 총 30문항

---
### Q01. [1. LLM 건망증·2단계 응고화·망각 방어 | Ch 01 | 초급] 배포된 일반 LLM이 세션(채팅창)을 새로 열 때마다 어제 지시한 사용자의 코딩 스타일과 아키텍처 결정을 완전히 잊어버리는(Amnesia) 근본적인 구조적 원인은?
```python
# Inference Mode: model.eval(), W_frozen (Delta W = 0)
```
1. 추론 시점의 신경망 가중치 행렬(W)은 완전히 동결되어 업데이트되지 않으며(Stateless), 이전 대화를 기억하는 것처럼 보이는 현상은 단지 클라이언트가 과거 텍스트를 매번 프롬프트에 이어 붙이기(Prompt Stuffing) 때문이다. ✅ **(정답)**
2. GPU 메모리가 1시간마다 자동으로 전원을 껐다 켜기 때문이다. 
3. 파이썬의 가비지 컬렉터(GC)가 매일 자정에 모델 가중치 파일을 삭제하기 때문이다. 
4. LLM은 한국어 단어 중 '기억'이라는 토큰을 생성할 수 없기 때문이다. 
> **해설**: 사전학습된 LLM은 추론 중에 가중치가 전혀 변하지 않는 무상태(Stateless) 함수입니다. 채팅 기록을 매번 컨텍스트 윈도우에 다시 밀어 넣는 것(Prompt Stuffing)이 일반 챗봇 기억의 실체입니다.

---
### Q02. [1. LLM 건망증·2단계 응고화·망각 방어 | Ch 01 | 중급] 대화 이력을 무조건 컨텍스트 윈도우에 이어 붙이는 **프롬프트 스터핑(Prompt Stuffing)** 방식이 30일 이상 장기 누적될 때 발생하는 3대 치명적 한계에 해당하지 **않는** 것은?
```python
# Day 30 누적 토큰: 135,000 Tokens -> Self-Attention 복잡도 O(L^2)
```
1. 시간축 상태가 바뀐 과거 정보와 최신 정보가 한 프롬프트에 섞여도 LLM이 스스로 100% 최신 상태만 완벽하게 판별하고 연산 비용이 0으로 수렴한다. ✅ **(정답)**
2. 토큰 길이 L에 대해 Self-Attention 연산량과 KV-Cache 비용이 O(L^2) 수준으로 폭증하고 첫 토큰 지연(TTFT)이 급격히 느려진다. 
3. 프롬프트 중간 부분에 위치한 과거 의사결정 기억의 회상 정확도가 40~60%대로 추락하는 Lost-in-the-Middle 현상이 발생한다. 
4. 매 턴 수만 토큰의 과거 로그를 재전송해야 하므로 API/GPU 서빙 원가가 폭증한다. 
> **해설**: 프롬프트 스터핑은 길이가 길어질수록 $O(L^2)$ 연산 폭증, 중간 맥락 망각(Lost-in-the-Middle), 그리고 과거 정정 전/후 정보의 충돌 환각이 심각해집니다.

---
### Q03. [1. LLM 건망증·2단계 응고화·망각 방어 | Ch 02 | 초급] 신경과학의 보완적 학습 시스템(CLS) 이론을 모사한 본 도서의 **2단계 기억 응고화(Two-Stage Memory Consolidation)**에서 **해마(Tier 1)**와 **대뇌피질(Tier 2)**의 역할 매핑으로 올바른 것은?
```python
# Tier 1 (Fast Learner) <---> Tier 2 (Slow Learner)
```
1. Tier 1 해마는 Neo4j 시간축 지식 그래프로 단기 에피소드를 0.01초 만에 즉각 기록·회상하고, Tier 2 대뇌피질은 Unsloth QLoRA+DPO로 검증된 장기 습관·철학을 모델 가중치에 야간 각인한다. ✅ **(정답)**
2. Tier 1 해마는 LoRA 학습을 담당하고, Tier 2 대뇌피질은 단순 메모장 텍스트 파일을 담당한다. 
3. Tier 1과 Tier 2 모두 매 대화 턴마다 7B 모델 전체 파라미터를 풀 파인튜닝한다. 
4. Tier 1 해마는 이미지만 저장하고 Tier 2 대뇌피질은 오디오만 저장한다. 
> **해설**: 가중치 손상 없이 단 한 번의 경험(One-Shot)을 즉시 저장하는 고속 해마(Temporal KG)와, 반복·중요 기억만 밤사이 가중치로 천천히 내재화하는 대뇌피질(QLoRA/DPO)의 이원화가 핵심입니다.

---
### Q04. [1. LLM 건망증·2단계 응고화·망각 방어 | Ch 02 | 중급] Ch 02 `hippocampus_cortex_router.py`에서 해마(Tier 1)에 기록된 수많은 에피소드 중 어떤 기억을 대뇌피질(Tier 2 LoRA 학습 큐)로 **승격(Consolidation)**시킬지 판별할 때 결합하는 핵심 지표가 아닌 것은?
```python
score = (recall_count * 0.12) + (salience_score * 0.45) + (min(days_active, 14) * 0.025) + cat_bonus
```
1. 사용자의 하드디스크 전체 남은 용량(Free Bytes) ✅ **(정답)**
2. 누적 회상 횟수(recall_count) 
3. 중요도 가중치(salience_score) 및 기억 성격(core_preference 여부) 
4. 지속 유지 일수(days_active) 
> **해설**: 핵심 선호도(`core_preference`)이면서 여러 날 동안 반복적으로 회상(`recall_count`)되고 중요도(`salience_score`)가 높은 기억일수록 대뇌피질(Tier 2) 가중치로 영구 응고화할 가치가 높습니다.

---
### Q05. [1. LLM 건망증·2단계 응고화·망각 방어 | Ch 03 | 고급] 신규 지식 데이터셋 $D_{new}$만 가지고 모델을 추가 파인튜닝할 때 기존 모델이 가지고 있던 범용 추론 및 코딩 능력이 급격히 붕괴하는 현상(파괴적 망각)을 방어하기 위한 **EWC(탄성 가중치 공고화)** 손실 함수에서 피셔 정보 행렬 $F_i$의 역할은?
```python
# L(theta) = L_new(theta) + sum( (lambda/2) * F_i * (theta_i - theta_old_i)^2 )
```
1. 과거 핵심 지식 수행에 결정적으로 기여한 가중치 파라미터일수록 큰 F_i 값을 부여해, 신규 학습 시 원래 위치(theta_old)에서 멀어지지 않도록 강한 용수철 페널티를 거는 중요도 가중치 역할 ✅ **(정답)**
2. 모든 파라미터를 0으로 초기화하여 모델 크기를 줄이는 가지치기 행렬 
3. 학습률(Learning Rate)을 무한대로 증폭시켜 발산을 유도하는 행렬 
4. JSON 문자열의 구문 오류를 교정하는 정규표현식 행렬 
> **해설**: 피셔 정보(Fisher Information $F_i$)가 높은 가중치일수록 기존 능력 보존에 중요하므로, 정규화 항 $\frac{\lambda}{2}F_i(\theta_i - \theta^*_{old,i})^2$를 통해 변동을 억제하여 파괴적 망각을 방어합니다.

---
### Q06. [1. LLM 건망증·2단계 응고화·망각 방어 | Ch 04 | 초급] Ch 04에서 구축하는 로컬 지속 메모리 인프라에서 외부 유료 API 서버에 사내 회의록·코딩 스타일 데이터를 유출하지 않고 100% 프라이빗하게 운영하는 2대 로컬 컴포넌트 조합은?
```python
# Tier 1 DB: Neo4j 5.18 (bolt://localhost:7687)
# Tier 2 Inference: Ollama / vLLM + ./lora_adapters
```
1. Docker로 격리된 Neo4j 5.18 해마 그래프 DB + 로컬 LLM 추론 엔진(Ollama/vLLM) 및 로컬 어댑터 저장소 ✅ **(정답)**
2. 구글 스프레드시트 공개 링크 + 공용 FTP 서버 
3. 인메모리 Python list 변수 + 이메일 첨부파일 전송 
4. Windows 메모장 + TCP 80번 평문 브로드캐스트 
> **해설**: 사내 기밀과 개인화 기억을 완벽히 소유하기 위해 로컬 Docker Neo4j 컨테이너(Tier 1)와 로컬 SLM 서빙(Tier 2)을 결합한 온프레미스/로컬 아키텍처를 구축합니다.

---
### Q07. [2. Temporal KG·FastMCP 회상·기억 감쇠 | Ch 05 | 초급] Ch 05 실시간 대화 에피소드 파서(`episode_stream_parser.py`)가 일상적인 잡담("오늘 날씨 좋네")을 걸러내고 해마 그래프에 저장하는 3가지 고가치 기억 스키마 범주로 올바른 것은?
```python
# Extracted Fields: subject, predicate, object_val, rationale, salience
```
1. 코딩/스타일 선호도(CODING_PREFERENCE), 아키텍처 기술 결정(ARCH_DECISION), 업무 규칙/제약조건(WORKFLOW_RULE) ✅ **(정답)**
2. 점심 메뉴 영수증, 스팸 광고 문자, 날씨 예보 기사 
3. OS 커널 어셈블리 덤프, 마우스 클릭 좌표, 화면 해상도 
4. 랜덤 UUID 목록, 무의미한 공백 줄, HTML 주석 태그 
> **해설**: 모든 문장을 저장하면 해마 그래프가 노이즈로 오염됩니다. 사용자의 지속적인 선호도·의사결정·업무 제약조건과 그 인과 사유(`rationale`)만 정밀 추출해야 높은 기억 품질을 유지합니다.

---
### Q08. [2. Temporal KG·FastMCP 회상·기억 감쇠 | Ch 06 | 중급] 사용자가 과거에는 `pip`을 썼지만 오늘부터 `Poetry`를 쓰겠다고 선호도를 변경했을 때, **시간축 지식 그래프(Temporal KG)**가 과거 데이터를 완전히 `DELETE` 하지 않고 유지하는 정석 상태 전이 방식은?
```python
MATCH (u:User)-[r:PREFERS {category: 'PACKAGE_MANAGER', is_active: true}]->(old)
SET r.is_active = ____, r.valid_to = $timestamp
CREATE (u)-[:PREFERS {is_active: ____, valid_from: $timestamp, valid_to: 'PRESENT'}]->(new)
```
1. 기존 엣지의 is_active = false, valid_to = 현재시각으로 마감(Archive)하고, 새로운 엣지를 is_active = true, valid_from = 현재시각으로 생성한다. ✅ **(정답)**
2. 기존 User 노드와 전체 그래프를 DETACH DELETE로 초기화한다. 
3. 두 엣지 모두 is_active = true로 두어 LLM이 매번 동전 던지기로 고르게 한다. 
4. valid_from을 미래의 연도(2099년)로 설정해 검색되지 않게 만든다. 
> **해설**: Temporal KG의 핵심은 '현재 유효한 진실(`is_active=true`)'을 즉시 조회하면서도, '과거에 왜 변경되었는지(`is_active=false`, `valid_from~valid_to`)' 역사적 감사 이력과 DPO `Rejected` 쌍 원천까지 함께 보존하는 것입니다.

---
### Q09. [2. Temporal KG·FastMCP 회상·기억 감쇠 | Ch 07 | 중급] Ch 07 FastMCP 서버(`memory_fastmcp_server.py`)의 `@mcp.tool() recall_user_context()` 가 사용자의 현재 활성 기억을 조회할 때, Cypher 내부에서 동시에 **`SET r.recall_count = coalesce(r.recall_count, 0) + 1`** 를 실행하는 중요한 목적은?
```python
MATCH (u:User {id: $uid})-[r:PREFERS {is_active: true}]->(t:Tool)
SET r.recall_count = coalesce(r.recall_count, 0) + 1
```
1. 자주 회상(사용)되는 기억일수록 회상 카운트(recall_count)를 누적시켜 에빙하우스 망각 곡선의 반감기를 늘리고, 밤사이 Tier 2 대뇌피질(LoRA) 승격 우선순위를 높이기 위함이다. ✅ **(정답)**
2. 회상 횟수가 10회가 되면 해당 기억을 즉시 영구 삭제하기 위함이다. 
3. Neo4j의 라이선스 만료 날짜를 하루씩 연장하기 위함이다. 
4. 파이썬의 메모리 누수를 고의로 발생시키기 위함이다. 
> **해설**: 인간의 뇌에서 반복 인출(Retrieval Practice)되는 기억의 시냅스가 강화되듯, MCP 도구가 기억을 회상할 때마다 `recall_count`를 증가시켜 망각을 막고 LoRA 각인 후보로 우선 승격시킵니다.

---
### Q10. [2. Temporal KG·FastMCP 회상·기억 감쇠 | Ch 08 | 고급] Ch 08 에빙하우스 망각 곡선 수식 $R(t) = \exp\left(-\frac{\Delta t}{S \cdot (1 + \alpha \cdot C_{recall})}\right)$ 에서 **시간 $\Delta t$가 많이 지났음에도 보유율 $R(t)$가 0.8 이상으로 높게 유지되는 기억**의 조건은?
```python
stability = salience * (1.0 + 0.65 * recalls)
r = math.exp(-days_elapsed / stability)
```
1. 초기 중요도(Salience)가 높고 누적 회상 횟수(C_recall)가 많아 분모인 안정성(Stability)이 크게 확보된 기억 ✅ **(정답)**
2. 초기 중요도(Salience)가 0.1이고 회상 횟수가 0회인 일회성 잡담 
3. 경과 일수(delta t)가 1,000일 이상이고 회상 횟수가 음수(-)인 기억 
4. alpha 가중치가 0이고 분모가 0에 수렴하는 기억 
> **해설**: 지수 감쇠 함수 $e^{-\Delta t / \text{Stability}}$에서 `salience`와 `recalls`가 클수록 `Stability`가 커져 시간이 흘러도 $R(t)$가 1에 가깝게 유지됩니다. 반면 중요도·회상 빈도가 낮은 잡담은 급격히 0에 수렴해 압축 대상이 됩니다.

---
### Q11. [2. Temporal KG·FastMCP 회상·기억 감쇠 | Ch 08 | 중급] 보유율 $R(t)$가 임계치(0.30) 아래로 떨어진 오래된 일회성 에피소드들을 완전히 날려버리지 않고 **`SemanticSummary` 노드로 계층적 압축(Hierarchical Summarization)**을 수행하는 이유는?
```python
# [EP-103, EP-104] -> [Summary-2026-10: '10월 임시 테스트 및 식사 기록 요약']
```
1. 세부 에피소드 노이즈와 엣지 폭증을 정리하여 그래프 탐색 성능을 쾌적하게 유지하면서도, 장기적 월간/분기별 문맥 요약 정보는 손실 없이 보존하기 위함이다. ✅ **(정답)**
2. 그래프 노드 개수를 무조건 1억 개 이상으로 부풀리기 위함이다. 
3. 텍스트 압축을 통해 JPG 이미지 파일을 생성하기 위함이다. 
4. FastMCP 서버의 포트를 80번으로 변경하기 위함이다. 
> **해설**: 계층적 요약 압축을 통해 해마 그래프가 비대해져 검색이 느려지는 것을 방지하면서도 거시적인 과거 흐름을 잃지 않을 수 있습니다.

---
### Q12. [2. Temporal KG·FastMCP 회상·기억 감쇠 | Ch 07 | 초급] Ch 07 `memory_fastmcp_server.py`를 우분투 터미널에서 Standalone MCP 클라이언트 없이 개발자 혼자 단품으로 즉각 동작 점검하고 싶을 때 사용하도록 설계된 실행 옵션은?
```python
pc@DESKTOP-NUVH6QH:~/memory-lab$ poetry run python memory_fastmcp_server.py ____
```
1. --self-test (if "--self-test" in sys.argv: recall_user_context 직접 호출 출력) ✅ **(정답)**
2. --format-disk 
3. --kill-neo4j 
4. --disable-python 
> **해설**: FastMCP 서버는 기본 실행 시 `stdio` 파이프 대기 상태에 들어가므로, `--self-test` 플래그를 분기 구현해 두면 터미널에서 즉시 Neo4j 회상 결과를 눈으로 검증할 수 있습니다.

---
### Q13. [3. 트리플 합성·CoT·7:3 Replay·Pydantic 검증 | Ch 09 | 중급] Ch 09에서 Neo4j 지식 그래프의 단 1개 트리플 `(User:Hamilton)-[:PREFERS]->(Poetry)`를 그대로 1건의 문답으로 학습시키지 않고 **`DIRECT_SETUP`, `CODE_REVIEW` 등 다각도 관점(Multi-Perspective)으로 증강**하는 이유는?
```python
# 1 Triple -> Setup 질문형 + Code Review 교정형 + Audit 점검형으로 다양화
```
1. 특정 질문 문구 한 가지에만 암기(Overfitting)되는 것을 방지하고, 초기 세팅·코드 리뷰·트러블슈팅 등 어떤 형태로 질문을 받아도 사용자의 표준 철학을 일반화하여 적용하도록 만들기 위함이다. ✅ **(정답)**
2. 데이터 용량을 늘려 GPU VRAM 부족 오류를 고의로 유발하기 위함이다. 
3. 단 하나의 질문 형식 외에는 파이썬 JSON 파서가 저장을 거부하기 때문이다. 
4. DPO 알고리즘이 영문 문장 1개만 입력받기 때문이다. 
> **해설**: 동일한 지식을 다양한 역할과 질문 어조로 변주하여 학습(Multi-Perspective Augmentation)해야, 모델이 실전 대화에서 변형된 질문이 들어와도 일관된 의사결정을 내릴 수 있습니다.

---
### Q14. [3. 트리플 합성·CoT·7:3 Replay·Pydantic 검증 | Ch 10 | 중급] Ch 10 `cot_trace_injector.py`에서 SFT 학습 데이터의 Assistant 응답 앞부분에 **`<thought> ... </thought>` 사고사슬(Chain-of-Thought) 블록**을 삽입하여 학습시킬 때 얻는 가장 큰 추론 이점은?
```python
<thought>
1. [기억 탐색] 활성 시간축 규칙 확인
2. [충돌 검증] 만료된 구형 방식(pip) 배제
3. [응답 구성] 사유(Rationale) 포함 제시
</thought>
```
1. 7B~8B 소형 모델(SLM)이 정답을 성급히 내뱉기 전에 '활성 기억 확인 $\rightarrow$ 구형 규칙 배제 $\rightarrow$ 사유 기반 답변'의 논리적 중간 계산 단계를 거쳐 환각을 크게 줄인다. ✅ **(정답)**
2. <thought> 태그를 넣으면 학습 토큰 수가 0개로 압축되어 0.001초 만에 학습이 끝난다. 
3. HTML 웹브라우저에서 텍스트 색상을 무지개색으로 바꿔주는 CSS 기능이다. 
4. GPU 온도를 영하로 낮춰주는 냉각 프로토콜이다. 
> **해설**: LLM은 출력 토큰을 한 글자씩 생성할 때마다 연산을 수행합니다. `<thought>` 블록으로 먼저 생각할 토큰 공간(Scratchpad)을 열어주면 소형 모델도 복잡한 제약조건 충돌을 정확히 피해 갑니다.

---
### Q15. [3. 트리플 합성·CoT·7:3 Replay·Pydantic 검증 | Ch 11 | 초급] Ch 11 `replay_buffer_mixer.py`에서 야간 학습 코퍼스를 구성할 때, 오늘 새로 합성한 개인화 에피소드(약 70%)에 반드시 **기존 범용 코딩/리눅스 상식 앵커 데이터(약 30%)**를 섞어(Shuffle) 학습시키는 핵심 목적은?
```python
# combined = new_episodic_memories (70%) + general_anchor_buffer (30%)
# random.shuffle(combined)
```
1. 신규 사내 규칙에 대한 분포 편향(Distribution Shift)을 완화하여 모델의 기존 일반 코딩 능력과 언어 유창성을 유지(파괴적 망각 방어)하기 위함이다. ✅ **(정답)**
2. 파일 크기를 정확히 10MB로 맞추기 위함이다. 
3. 새로운 기억을 모델이 잊어버리게 유도하기 위함이다. 
4. 랜덤 셔플을 하지 않으면 Neo4j 컨테이너가 정지하기 때문이다. 
> **해설**: 신규 개인화 데이터만 100% 몰아서 학습시키면 모델이 기존 범용 능력(`asyncio`, 리눅스 명령 등)을 잃어버립니다. Replay Buffer에서 30% 비율로 기존 앵커 지식을 함께 복습(Rehearsal)시켜 안정성을 지킵니다.

---
### Q16. [3. 트리플 합성·CoT·7:3 Replay·Pydantic 검증 | Ch 12 | 중급] Ch 12 `pydantic_jsonl_validator.py`에서 야간 파인튜닝 시작 전 Pydantic 스키마로 모든 샘플을 전수 검사하는 이유와, 불량 샘플이 발견되었을 때의 올바른 처리 방식은?
```python
@field_validator("output")
def check_thought_tags(cls, v: str) -> str:
    if "<thought>" not in v or "</thought>" not in v:
        raise ValueError(...)
```
1. 새벽 무인 GPU 학습 도중 결손/불량 포맷 데이터로 인한 배치 크래시 및 모델 오염(Garbage-In, Garbage-Out)을 막기 위해, 검증 실패 샘플만 예외 처리로 격리·차단하고 무결점 샘플만 .jsonl로 내보낸다. ✅ **(정답)**
2. 불량 샘플 1건이 발견되면 전체 파이프라인과 리눅스 서버를 포맷한다. 
3. 검증 실패 시 `<thought>` 태그 없이 빈 문자열 `""` 로 강제 덮어써서 학습시킨다. 
4. Pydantic 검증기를 끄고 사람이 새벽 3시에 매번 눈으로 1만 줄을 검수한다. 
> **해설**: 무인 자동화 배치(Crontab)에서는 단 1건의 불량 JSON이나 추론 태그 누락이 전체 파인튜닝을 망칠 수 있습니다. Pydantic 게이트키퍼가 불량 데이터만 정밀 차단하고 정상 데이터만 ChatML `.jsonl`로 내보냅니다.

---
### Q17. [3. 트리플 합성·CoT·7:3 Replay·Pydantic 검증 | Ch 12 | 초급] Unsloth / HuggingFace SFTTrainer에 데이터를 공급할 때 일반 `.json` 배열 파일 대신 **`.jsonl` (JSON Lines)** 포맷을 표준으로 사용하는 기술적 장점은?
```python
{"messages": [{"role": "system", ...}, {"role": "user", ...}, {"role": "assistant", ...}]}
{"messages": [...]}
```
1. 한 줄(Line)이 곧 하나의 독립된 JSON 학습 레코드이므로 대용량 파일 전체를 메모리에 한꺼번에 파싱하지 않고 줄 단위 스트리밍 로딩과 병합(Append)이 매우 빠르다. ✅ **(정답)**
2. .jsonl 파일은 자동으로 GPU 텐서로 하드웨어 압축되기 때문이다. 
3. .json 파일은 한글 UTF-8 인코딩을 전혀 지원하지 않기 때문이다. 
4. .jsonl 포맷만 비밀번호 암호화 해시를 지원하기 때문이다. 
> **해설**: JSON Lines(`.jsonl`)는 파일 전체의 대괄호 `[...]`를 열고 닫을 필요 없이 줄 단위로 스트리밍 읽기와 Append가 가능하여 대규모 LLM 학습 데이터셋의 산업 표준으로 쓰입니다.

---
### Q18. [3. 트리플 합성·CoT·7:3 Replay·Pydantic 검증 | Ch 12 | 고급] ChatML 학습 레코드 내 `messages` 배열에서 `{"role": "system", "content": "당신은 User:Hamilton의 코딩 철학을 공유하는..."}` 처럼 **System Prompt 페르소나**를 일관되게 포함시키는 이유는?
```python
"messages": [{"role": "system", "content": "..."}, {"role": "user", ...}, {"role": "assistant", ...}]
```
1. 추론 시 동일한 System 지시문과 결합될 때 파인튜닝된 어댑터 가중치가 영구 자아(Alter-Ego) 페르소나 모드로 가장 정확하고 안정적으로 활성화되도록 조건부 분포를 정렬하기 위함이다. ✅ **(정답)**
2. System 메시지가 없으면 파이썬 `json.dumps()`가 SyntaxError를 발생시키기 때문이다. 
3. System 메시지에 적힌 단어 수만큼 VRAM 사용량이 줄어들기 때문이다. 
4. User와 Assistant 역할을 서로 뒤바꾸어 학습시키기 위함이다. 
> **해설**: 학습 시 사용한 Chat Template(System/User/Assistant 구조)과 추론 시 입력하는 프롬프트 포맷이 일치해야 파인튜닝된 어댑터의 지능이 100% 발휘됩니다.

---
### Q19. [4. Unsloth QLoRA·DPO 정렬·야간 수면 배치 | Ch 13 | 초급] Ch 13 `slm_model_selector.py` 비교 결과, 한국어 사내 규정 및 파이썬 FastMCP 코드 생성을 겸하는 로컬 영구 자아 베이스 모델로 `Meta Llama-3.1 8B` 대신 **`Qwen2.5-7B-Instruct-bnb-4bit`**를 1순위로 추천한 핵심 근거는?
```python
# Qwen2.5-7B: 한국어 토큰비 1.28x, 코딩 벤치 92.7%, 4-bit VRAM 5.8GB
```
1. 한국어 토크나이저 압축 효율(어절당 토큰 소비량)이 훨씬 뛰어나 동일 컨텍스트에 더 많은 기억을 담을 수 있고, 코딩 정확도(92.7%)가 높으며 VRAM도 5.8GB로 더 적게 소모하기 때문이다. ✅ **(정답)**
2. Qwen2.5-7B는 GPU 없이 8비트 CPU만으로 1초 만에 1만 에폭 학습이 끝나기 때문이다. 
3. Llama 모델은 리눅스 우분투 환경에서 실행이 전면 금지되어 있기 때문이다. 
4. Qwen2.5-7B는 파라미터가 7000억(700B)개라서 더 크기 때문이다. 
> **해설**: 한국어 토크나이저 효율이 낮으면 같은 한국어 문장도 토큰이 2배 가까이 쪼개져 속도와 기억 효율이 떨어집니다. Qwen2.5-7B는 우수한 한국어 토큰 효율과 강력한 코딩 유전자, 낮은 VRAM(5.8GB)의 3박자를 갖췄습니다.

---
### Q20. [4. Unsloth QLoRA·DPO 정렬·야간 수면 배치 | Ch 14 | 중급] **Unsloth** 프레임워크가 표준 HuggingFace PEFT/Transformers 대비 단일 GPU(RTX 3090/4090 등)에서 **VRAM 소모를 최대 70% 줄이고 학습 속도를 2배 이상 가속**하는 핵심 엔지니어링 비결은?
```python
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen2.5-7B-Instruct-bnb-4bit", load_in_4bit=True
)
```
1. 4-bit NF4 양자화와 함께 모든 역전파 수학 공식을 수동 미분 유도하여 OpenAI Triton 커스텀 GPU 커널로 직접 작성(불필요한 중간 텐서 할당 제거)하고 자체 그래디언트 체크포인팅을 제공하기 때문이다. ✅ **(정답)**
2. 학습 데이터의 90%를 무작위로 버리고 첫 10줄만 학습하기 때문이다. 
3. 모델 가중치를 로컬 GPU가 아닌 타인의 PC로 몰래 전송해 분산 학습하기 때문이다. 
4. 부동소수점 계산을 전부 문자열 덧셈으로 대체했기 때문이다. 
> **해설**: Unsloth는 PyTorch의 범용 Autograd 그래프 오버헤드를 우회해 수동으로 유도한 행렬 미분 Triton 커널과 최적화된 RoPE·CrossEntropy·Smart Checkpointing을 적용함으로써 정확도 손실(`0%`) 없이 압도적 속도/메모리 효율을 달성합니다.

---
### Q21. [4. Unsloth QLoRA·DPO 정렬·야간 수면 배치 | Ch 14 | 고급] QLoRA 설정에서 **`r = 16`, `lora_alpha = 32`**로 설정하고 `target_modules`에 어텐션(`q,k,v,o_proj`)뿐만 아니라 MLP 게이트(`gate,up,down_proj`)까지 모두 포함하는 이유는?
```python
FastLanguageModel.get_peft_model(model, r=16, lora_alpha=32,
  target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"])
```
1. 트랜스포머에서 사실적 지식은 주로 MLP(FFN) 계층에 저장되고 문맥 라우팅은 Attention이 담당하므로, 모든 선형 투영층에 LoRA 어댑터를 부착해야 새로운 사내 지식을 온전히 각인할 수 있다. (alpha/r = 2.0 스케일링 적용) ✅ **(정답)**
2. q_proj만 지정하면 문법 오류가 발생하여 Python이 실행되지 않기 때문이다. 
3. r=16이면 원본 모델의 100% 전체 가중치를 덮어쓰는 Full Fine-Tuning과 같기 때문이다. 
4. target_modules를 늘리면 파일 크기가 1바이트로 줄어들기 때문이다. 
> **해설**: 연구 결과 Attention(`q,k,v,o`)만 학습하는 것보다 지식이 응집되는 FFN/MLP(`gate,up,down_proj`)까지 함께 어댑터를 부착할 때 신규 지식 주입 성능이 Full Fine-Tuning에 필적할 만큼 높아집니다.

---
### Q22. [4. Unsloth QLoRA·DPO 정렬·야간 수면 배치 | Ch 15 | 고급] SFT(지도 미세조정) 이후 **DPO(Direct Preference Optimization)** 정렬 단계를 추가로 수행해야 하는 결정적인 이유와, Neo4j Temporal KG로부터 **`Chosen` / `Rejected`** 학습 쌍을 자동 추출하는 원리는?
```python
# Chosen  <- is_active=true  (예: Poetry + cat << 'EOF')
# Rejected <- is_active=false (예: pip + requirements.txt)
```
1. SFT는 정답 문장 확률만 높일 뿐 과거 구형 습관 확률을 직접 깎지 못하지만, DPO는 시간축 그래프의 최신 활성 기억(Chosen) 보상은 높이고 만료된 과거 기억(Rejected) 보상은 직접 억제하여 구형 습관 재발을 차단한다. ✅ **(정답)**
2. DPO는 별도의 거대한 보상 모델(Reward Model)을 4개 이상 추가 학습시켜야만 작동하므로 단순하다. 
3. DPO는 사용자의 선호도가 아닌 랜덤 문자열을 Chosen으로 강제 학습시킨다. 
4. SFT보다 GPU 메모리를 10배 더 많이 써서 학습을 느리게 만들기 위함이다. 
> **해설**: Temporal KG는 이미 '과거에 쓰다 버린 방식(`is_active=false`)'과 '현재 채택한 방식(`is_active=true`)'을 쌍으로 갖고 있습니다. 이를 그대로 DPO `rejected`/`chosen`으로 먹이면 모델이 구형 습관을 완벽히 버리게 됩니다.

---
### Q23. [4. Unsloth QLoRA·DPO 정렬·야간 수면 배치 | Ch 15 | 중급] DPO 손실 함수 $\mathcal{L}_{DPO}$의 하이퍼파라미터 **$\beta$ (beta, 예: `0.1`)**가 제어하는 역할은 무엇인가?
```python
# L_DPO = -log sigmoid( beta * (log(pi_theta(y_w)/pi_ref(y_w)) - log(pi_theta(y_l)/pi_ref(y_l))) )
```
1. 현재 학습 중인 정책 모델(pi_theta)이 기존 참조 모델(pi_ref)의 언어 분포로부터 너무 극단적으로 벗어나지 않도록 KL-Divergence 제약 강도를 조절하는 온도/규제 계수이다. ✅ **(정답)**
2. 학습할 에폭(Epoch)의 총 횟수를 지정하는 정수이다. 
3. GPU 팬 속도를 RPM 단위로 설정하는 하드웨어 제어 상수이다. 
4. Neo4j의 Bolt 포트 번호를 결정하는 상수이다. 
> **해설**: $\beta$는 참조 모델($\pi_{ref}$) 대비 이탈 허용 정도(KL 페널티 강도)를 제어합니다. 일반적으로 `0.1` 전후의 값을 사용해 기존 언어 능력을 지키는 선에서 `Chosen`과 `Rejected` 보상 마진을 벌립니다.

---
### Q24. [4. Unsloth QLoRA·DPO 정렬·야간 수면 배치 | Ch 16 | 초급] 리눅스 서버에서 야간 수면 기억 응고화 스크립트(`nightly_sleep_consolidation.sh`)를 **매일 밤 새벽 03시 00분**에 자동으로 무인 실행하도록 `crontab -e`에 등록하는 올바른 크론 표현식은?
```python
# 분 시 일 월 요일  실행명령
```
1. 0 3 * * * /home/pc/memory-lab/nightly_sleep_consolidation.sh ✅ **(정답)**
2. 3 0 * * * /home/pc/memory-lab/nightly_sleep_consolidation.sh 
3. * * 3 * * /home/pc/memory-lab/nightly_sleep_consolidation.sh 
4. 0 0 3 0 * /home/pc/memory-lab/nightly_sleep_consolidation.sh 
> **해설**: Crontab은 왼쪽부터 `분(0~59) 시(0~23) 일(1~31) 월(1~12) 요일(0~7)` 순서입니다. `0 3 * * *`가 매일 새벽 03시 00분을 의미합니다. (`3 0 * * *`는 자정 00시 03분이므로 주의해야 합니다.)

---
### Q25. [5. LoRA 핫스왑·Standalone 영구 자아(Alter-Ego) | Ch 17 | 중급] Ch 17 `lora_hot_swapper.py`에서 새벽 학습을 마친 신규 LoRA 어댑터(`alter_ego_v1`)를 서비스 중단(Downtime) 없이 **0.002초 만에 실시간 교체(Hot-Swapping)**할 수 있는 아키텍처 원리는?
```python
os.symlink(os.path.abspath(target_dir), './lora_adapters/current_active')
```
1. 수 GB 크기의 동결된 4-bit 베이스 모델 가중치(W_0)는 VRAM에 그대로 유지한 채, 수십 MB에 불과한 저랭크 어댑터(Delta W) 경로의 심볼릭 링크만 원자적으로 교체하여 동적 라우팅하기 때문이다. ✅ **(정답)**
2. 7B 베이스 모델 전체 가중치를 매번 0부터 다시 다운로드해 컴파일하기 때문이다. 
3. 어댑터 교체를 위해 리눅스 운영체제 커널을 강제 재부팅하기 때문이다. 
4. LoRA 어댑터는 CPU 캐시 메모리를 전혀 사용하지 않고 모니터에 픽셀로 저장되기 때문이다. 
> **해설**: 베이스 모델 VRAM 재할당이 필요 없고, 어댑터 가중치 $\Delta W = B \cdot A$만 갈아끼우면 되므로 원자적 심볼릭 링크 전환과 vLLM/추론 서버의 멀티 LoRA 핫스왑으로 무중단 두뇌 업그레이드가 가능합니다.

---
### Q26. [5. LoRA 핫스왑·Standalone 영구 자아(Alter-Ego) | Ch 18 | 초급] 외부 상용 IDE 종속성을 완전히 제거하고, 순수 파이썬 에이전트(`standalone_memory_client.py`)가 **`memory_fastmcp_server.py`**에 연결하여 사용자의 최신 활성 선호도를 회상할 때 사용하는 MCP SDK 호출 패턴은?
```python
async with stdio_client(server_params) as (r, w):
    async with ClientSession(r, w) as session:
        await session.initialize()
        res = await session.____("recall_user_context", {"user_id": "User:Hamilton"})
```
1. call_tool ✅ **(정답)**
2. send_email 
3. drop_database 
4. exec_shell 
> **해설**: Standalone MCP 호스트는 `ClientSession` 초기화 후 `await session.call_tool("도구명", 인자딕셔너리)` 표준 비동기 호출만으로 해마 FastMCP 서버의 기억을 즉각 인출합니다.

---
### Q27. [5. LoRA 핫스왑·Standalone 영구 자아(Alter-Ego) | Ch 19 | 중급] Ch 19 실전 프로젝트 `alter_ego_agent_cli.py`가 **Tier 1 해마(FastMCP)**와 **Tier 2 대뇌피질(Hot-Swapped LoRA)**을 동시에 결합하여 회의록과 코드를 대리 작성할 때 나타나는 시너지 효과로 가장 정확한 설명은?
```python
# Tier 1: 방금 10분 전 바뀐 최신 프로젝트 규칙/금지사항 즉시 반영
# Tier 2: 오랜 기간 축적된 사용자의 말투, <thought> 논리 전개, 코딩 철학 자연 발현
```
1. 방금 대화에서 바뀐 최신 사실·일정은 Tier 1 해마가 0.02초 만에 보충하고, 오랜 코딩 습관·문체·판단 기준은 Tier 2 가중치에서 별도 시스템 프롬프트 낭비 없이 자연스럽게 발현된다. ✅ **(정답)**
2. Tier 1과 Tier 2가 서로 다른 답변을 출력해 매번 2개 중 하나가 깨진다. 
3. 사용자가 매 채팅마다 자신의 취향을 1,000단어씩 다시 복붙해서 알려줘야 한다. 
4. 회의록은 Tier 1이 쓰고 코드 에러만 Tier 2가 고의로 삽입한다. 
> **해설**: 단기/가변적 최신 맥락은 해마(Temporal KG)가, 장기/불변적 성격과 철학은 대뇌피질(LoRA/DPO)이 분담하여 공명(Resonance)하는 것이 진정한 영구 자아(Alter-Ego) AI의 완성형입니다.

---
### Q28. [5. LoRA 핫스왑·Standalone 영구 자아(Alter-Ego) | Ch 16 & 19 | 중급] 야간 수면 학습 배치(`nightly_sleep_consolidation.sh`) 상단에 **`set -euo pipefail`** 옵션을 반드시 선언하여 쉘 스크립트를 방어적으로 작성하는 이유는?
```python
#!/usr/bin/env bash
set -euo pipefail
```
1. 중간 단계(예: Pydantic 검증 실패 등)에서 0이 아닌 에러 코드가 발생하거나 미정의 변수를 참조할 경우 즉시 배치를 중단하여, 불량 데이터로 LoRA 가중치가 오염·덮어쓰기 되는 사고를 막기 위함이다. ✅ **(정답)**
2. 에러가 나더라도 무조건 무시하고 빈 어댑터를 강제 덮어쓰기 위함이다. 
3. 스크립트를 백그라운드에서 영원히 정지시키기 위함이다. 
4. 모든 파일의 권한을 777로 변경하기 위함이다. 
> **해설**: `set -e`(에러 시 즉시 중단), `-u`(미정의 변수 에러), `-o pipefail`(파이프 중간 에러 감지)은 무인 야간 배치에서 앞 단계 실패가 뒤 단계 데이터/모델 오염으로 전파되는 것을 막는 필수 안전벨트입니다.

---
### Q29. [5. LoRA 핫스왑·Standalone 영구 자아(Alter-Ego) | Ch 20 | 고급] 평생 학습(Lifelong Learning) 루프를 장기 운영하는 과정에서, 새벽마다 새로운 LoRA 어댑터를 계속 덧대기만 하지 않고 **수 개월 주기로 다수의 LoRA 체크포인트를 베이스 모델과 병합(Merge)하거나 리플레이 버퍼 기반 재조정(Re-consolidation)**을 수행해야 하는 이유는?
```python
# Merge & Re-consolidate Cycle (Every 30 Days)
```
1. 오래 누적된 수십 개의 미시 어댑터 간 가중치 간섭과 메모리 단편화를 해소하고, 에빙하우스 감쇠로 걸러진 핵심 정수 지식만 깔끔하게 정규화된 단일 코어 가중치로 재정렬하기 위함이다. ✅ **(정답)**
2. 모델이 너무 똑똑해지면 리눅스 커널이 실행을 거부하기 때문이다. 
3. Neo4j의 모든 과거 이력을 0으로 지워야만 DPO가 작동하기 때문이다. 
4. 7B 모델을 0.1B 모델로 강제 축소해 지능을 없애기 위함이다. 
> **해설**: 장기간 지속 메모리 시스템을 운용할 때는 주기적인 Re-consolidation을 통해 낡고 모순된 어댑터 잔여물을 정리하고, 핵심 앵커 지식과 최신 에피소드 정수의 균형을 재최적화해야 평생 학습 안정성이 유지됩니다.

---
### Q30. [5. LoRA 핫스왑·Standalone 영구 자아(Alter-Ego) | Ch 20 | 초급] Ch 20 `lifelong_evolution_monitor.py` 종합 감사 스크립트가 영구 두뇌 AI의 건강한 진화 상태를 최종 검증하기 위해 동시에 확인하는 2가지 핵심 지표 축은?
```python
active_cnt = ... # Tier 1 Neo4j 활성 기억 수
lora = json.load(...) # Tier 2 current_active 어댑터 Loss & Config
```
1. Tier 1 해마(Neo4j)의 활성/아카이빙 기억 엣지 균형 상태 + Tier 2 대뇌피질(current_active LoRA 어댑터)의 학습 손실(Loss) 및 정상 핫스왑 연동 상태 ✅ **(정답)**
2. 모니터 화면 주사율(Hz) + 마우스 DPI 설정값 
3. 윈도우 바탕화면 배경 이미지 파일 크기 + C 드라이브 휴지통 용량 
4. 유튜브 구독자 수 + 브라우저 북마크 개수 
> **해설**: 지속 메모리 AI는 외장 그래프(Tier 1)와 내재 가중치(Tier 2) 두 바퀴가 함께 맞물려 돌아가므로, 양쪽의 기억 건수와 활성 어댑터의 수렴 손실(Loss)·정렬 상태를 통합 관제해야 합니다.

---
