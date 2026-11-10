# -*- coding: utf-8 -*-
"""
[심화 1 / Book 22015] 《자율주행 AI 자동차 빅데이터 레이크하우스 실무 가이드》
실전 변별력 객관식 30문항 (5대 영역 × 6문항)
"""

EXAM_META_22015 = {
    "id": "smartcar_lakehouse",
    "book_id": 22015,
    "title": "심화 1: 자율주행 AI 빅데이터 레이크하우스 역량 평가 (30문항)",
    "subtitle": "Docker 8-Container · Hadoop HDFS · Apache Kafka · HiveServer2 · Pydeck 3D · OLS 회귀 & 3-Class DNN",
    "book_url": "https://wikidocs.net/book/22015",
    "sim_url": "sim_smartcar_lakehouse.html",
    "accent": "#38bdf8",
    "accent_secondary": "#10b981",
    "categories": [
        "1. 도커·WSL2·Poetry 인프라",
        "2. HDFS 분산저장·센서 시뮬레이션",
        "3. Kafka 스트리밍·Hive 웨어하우스",
        "4. GPS 정제·Streamlit·Pydeck 3D",
        "5. OLS 회귀·3-Class DNN·트러블슈팅"
    ],
    # 각 영역 점수를 A.C.E.S 6대 역량 [수학, SW코딩, 데이터인프라, GenAI, 비즈니스기획, 아키텍처]로 매핑하는 가중치 행렬
    "aces_weights": {
        "1. 도커·WSL2·Poetry 인프라":      [0.05, 0.25, 0.35, 0.05, 0.05, 0.25],
        "2. HDFS 분산저장·센서 시뮬레이션": [0.10, 0.25, 0.40, 0.05, 0.05, 0.15],
        "3. Kafka 스트리밍·Hive 웨어하우스":[0.05, 0.20, 0.45, 0.05, 0.10, 0.15],
        "4. GPS 정제·Streamlit·Pydeck 3D":  [0.10, 0.30, 0.25, 0.10, 0.15, 0.10],
        "5. OLS 회귀·3-Class DNN·트러블슈팅":[0.35, 0.25, 0.20, 0.05, 0.10, 0.05]
    }
}

QUESTIONS_22015 = [
    # 영역 1: 도커·WSL2·Poetry 인프라 (Q01~Q06)
    {
        "id": 1,
        "category": "1. 도커·WSL2·Poetry 인프라",
        "chapter": "Ch 01",
        "difficulty": "초급",
        "question": "과거 가상머신(VirtualBox/VMware에 CentOS 3대 설치) 방식과 비교했을 때, 모던 도커(Docker) 컨테이너 기반 클러스터가 노트북 실습 환경에서 압도적으로 유리한 핵심 기술적 이유는?",
        "code": "# 호스트 OS(WSL2 리눅스 커널) 1개를 공유하여 8대 빅데이터 서버 컨테이너 격리 실행",
        "options": [
            "컨테이너마다 독립된 OS 커널을 매번 부팅할 필요 없이 호스트 리눅스 커널을 공유하므로 RAM 점유율이 획기적으로 낮고 수 초 만에 8대 서버를 기동할 수 있다.",
            "도커는 모든 서버 코드를 윈도우 레지스트리에 직접 컴파일하므로 리눅스 커널이 전혀 필요 없다.",
            "도커를 사용하면 HDFS 블록 크기가 128MB에서 1KB로 자동 축소되어 디스크가 절약된다.",
            "가상머신은 Python을 지원하지 않지만 도커만 Python 3.12를 지원하기 때문이다."
        ],
        "answer": 0,
        "explanation": "가상머신(VM)은 각 게스트마다 완전한 OS 커널을 띄워야 하므로 16~32GB 이상 메모리를 소모하지만, 도커 컨테이너는 호스트 리눅스 커널을 공유하고 프로세스 격리만 수행하므로 일반 노트북에서도 8대 빅데이터 컨테이너를 쾌적하게 가동할 수 있습니다."
    },
    {
        "id": 2,
        "category": "1. 도커·WSL2·Poetry 인프라",
        "chapter": "Ch 01",
        "difficulty": "초급",
        "question": "윈도우 WSL2(Ubuntu-22.04) 환경에서 실습 프로젝트를 생성할 때 `/mnt/c/Users/PC` 경로 대신 리눅스 홈 경로(`~/smartcar-pilot`)로 반드시 이동해야 하는 이유로 가장 올바른 것은?",
        "code": "pc@DESKTOP-NUVH6QH:/mnt/c/Users/PC$ cd ~/smartcar-pilot\npc@DESKTOP-NUVH6QH:~/smartcar-pilot$ pwd",
        "options": [
            "윈도우 마운트 경로(/mnt/c)는 NTFS 파일시스템 브릿지를 거쳐 파일 I/O 속도가 매우 느리고 리눅스 실행 권한(chmod) 충돌이 발생하지만, 리눅스 홈(~)은 네이티브 ext4 파일시스템 위에서 초고속 I/O와 완전한 POSIX 권한을 보장하기 때문이다.",
            "/mnt/c 경로에서는 git clone 명령어가 문법적으로 차단되어 있기 때문이다.",
            "리눅스 홈 경로(~)에 파일을 저장하면 자동으로 도커 허브에 업로드되기 때문이다.",
            "/mnt/c 경로는 읽기 전용(Read-Only)이라서 텍스트 파일을 생성할 수 없기 때문이다."
        ],
        "answer": 0,
        "explanation": "WSL2에서 Windows 드라이브(/mnt/c) 접근은 9P 프로토콜 변환 오버헤드로 인해 Python 가상환경 생성 및 대용량 파일 처리가 수십 배 느려집니다. 반면 `~` 경로는 가상 디스크의 네이티브 ext4 파일시스템이므로 압도적인 성능을 발휘합니다."
    },
    {
        "id": 3,
        "category": "1. 도커·WSL2·Poetry 인프라",
        "chapter": "Ch 01",
        "difficulty": "중급",
        "question": "WSL2 환경의 우분투 내부에 직접 `docker-ce` 데몬을 설치하는 대신, Windows용 Docker Desktop의 'WSL Integration(Ubuntu)' 연동 기능을 사용하는 아키텍처상의 핵심 이점은?",
        "code": "# Docker Desktop -> Settings -> Resources -> WSL Integration -> Ubuntu 활성화",
        "options": [
            "WSL2 터미널을 닫더라도 백그라운드 데몬 종료 위험이 없고, 윈도우 브라우저에서 localhost:8501 / 9870 포트 포워딩 및 동적 RAM/OOM 관리가 매끄럽게 유지된다.",
            "Docker Desktop을 쓰면 카프카(Kafka)가 주키퍼(Zookeeper) 없이 단일 파일로 자동 변환된다.",
            "WSL2에서는 docker-ce가 TCP 포트를 최대 2개까지만 열 수 있는 커널 제한이 있기 때문이다.",
            "Docker Desktop이 파이썬 코드를 자동으로 GPU CUDA 바이너리로 컴파일해 주기 때문이다."
        ],
        "answer": 0,
        "explanation": "WSL2는 윈도우 터미널 창 종료 시 백그라운드 프로세스 유지가 까다로운 반면, Docker Desktop 백엔드를 공유하면 Windows 브라우저와의 localhost 포트 포워딩, 메모리(RAM) 할당 제어, 컨테이너 영속성이 안정적으로 보장됩니다."
    },
    {
        "id": 4,
        "category": "1. 도커·WSL2·Poetry 인프라",
        "chapter": "Ch 02",
        "difficulty": "초급",
        "question": "기존 `pip install + requirements.txt` 방식 대비 모던 파이썬 의존성 관리 도구인 **Poetry**가 실무 빅데이터 프로젝트에서 채택되는 가장 결정적인 이유는?",
        "code": "poetry add pandas kafka-python pydeck\n# 생성 파일: pyproject.toml + poetry.lock",
        "options": [
            "poetry.lock 파일에 모든 직·간접 의존성 패키지의 정확한 버전과 SHA-256 해시를 잠금 기록하여 어떤 팀원의 리눅스 서버에서도 100% 동일한 재현성(Reproducibility)을 보장한다.",
            "Poetry는 C++ 컴파일러이므로 파이썬 인터프리터 없이도 .py 파일을 실행한다.",
            "Poetry를 사용하면 TensorFlow 모델의 학습 정확도가 자동으로 10% 향상된다.",
            "Poetry는 도커 컨테이너 내부의 방화벽 포트를 자동으로 개방하는 보안 도구이다."
        ],
        "answer": 0,
        "explanation": "Poetry는 `pyproject.toml`과 `poetry.lock`을 통해 하위 라이브러리 간 버전 충돌을 사전에 해결(Dependency Resolution)하고, 해시값까지 고정하여 팀 내 환경 불일치('내 PC에선 됐는데?') 문제를 원천 차단합니다."
    },
    {
        "id": 5,
        "category": "1. 도커·WSL2·Poetry 인프라",
        "chapter": "Ch 03",
        "difficulty": "중급",
        "question": "본 도서 `docker-compose.yml`에서 Zookeeper와 Kafka를 안정적으로 구동하기 위해 채택한 공식 도커 이미지 및 `depends_on` 오케스트레이션 설정으로 옳은 것은?",
        "code": "services:\n  zookeeper:\n    image: confluentinc/cp-zookeeper:7.5.0\n  kafka:\n    image: confluentinc/cp-kafka:7.5.0\n    depends_on:\n      - zookeeper",
        "options": [
            "confluentinc/cp-zookeeper:7.5.0 과 cp-kafka:7.5.0 을 사용하며, Kafka가 실행되기 전 Zookeeper가 먼저 시작되도록 depends_on으로 의존 순서를 지정한다.",
            "Kafka가 Zookeeper보다 반드시 먼저 실행된 후 10분 뒤에 Zookeeper를 수동 실행한다.",
            "bitnami/kafka 이미지를 쓰면서 Zookeeper 포트를 9870으로 변경해야만 브로커가 실행된다.",
            "Kafka 컨테이너는 네트워크 격리를 위해 ports 매핑을 완전히 제거해야 localhost:9092 접속이 가능하다."
        ],
        "answer": 0,
        "explanation": "구형 Kafka 브로커는 메타데이터 및 브로커 코디네이션을 위해 Zookeeper(2181)가 선행 기동되어야 합니다. `confluentinc/cp-zookeeper:7.5.0`과 `cp-kafka:7.5.0` 조합에 `depends_on: [zookeeper]`를 명시하면 안정적으로 기동됩니다."
    },
    {
        "id": 6,
        "category": "1. 도커·WSL2·Poetry 인프라",
        "chapter": "Ch 03",
        "difficulty": "고급",
        "question": "Docker Compose의 Kafka 설정에서 `KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092,PLAINTEXT_INTERNAL://kafka:29092` 처럼 리스너를 2개로 분리하는 이유는?",
        "code": "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_INTERNAL:PLAINTEXT\nKAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092,PLAINTEXT_INTERNAL://kafka:29092",
        "options": [
            "우분투 호스트(외부)에서 실행하는 Python 스크립트는 localhost:9092로 접속하고, 같은 Docker 브리지 네트워크 안의 다른 컨테이너는 서비스명 kafka:29092로 동시 통신할 수 있게 라우팅하기 위함이다.",
            "9092 포트는 읽기 전용이고 29092 포트는 삭제 전용이기 때문이다.",
            "하나의 포트로 초당 10건 이상 메시지가 들어오면 자동 차단되기 때문이다.",
            "Zookeeper가 29092 포트로 GPU 데이터를 전송하기 때문이다."
        ],
        "answer": 0,
        "explanation": "Kafka 클라이언트는 초기 연결 후 브로커가 알려주는 `ADVERTISED_LISTENERS` 주소로 재접속합니다. 호스트 PC의 Python 프로세스(localhost:9092)와 도커 내부 컨테이너(kafka:29092)가 각각 올바른 주소를 반환받도록 리스너를 분리 설계합니다."
    },

    # 영역 2: HDFS 분산저장·센서 시뮬레이션 (Q07~Q12)
    {
        "id": 7,
        "category": "2. HDFS 분산저장·센서 시뮬레이션",
        "chapter": "Ch 04",
        "difficulty": "초급",
        "question": "하둡 분산 파일시스템(HDFS) 아키텍처에서 **NameNode(네임노드)**와 **DataNode(데이터노드)**의 역할 분담으로 가장 정확한 설명은?",
        "code": "docker exec namenode hdfs dfs -ls /smartcar/data",
        "options": [
            "NameNode는 파일의 디렉터리 구조와 블록 위치 매핑 정보(메타데이터)를 관리하는 관제탑이고, DataNode는 실제 분할된 데이터 블록들을 디스크에 물리적으로 저장하는 창고 작업자이다.",
            "NameNode가 모든 영상 파일을 직접 저장하고, DataNode는 SQL 쿼리 파싱만 담당한다.",
            "DataNode가 죽더라도 NameNode를 삭제하면 자동으로 데이터가 복구된다.",
            "NameNode는 카프카 토픽을 생성하고 DataNode는 Streamlit 웹 서버를 띄운다."
        ],
        "answer": 0,
        "explanation": "HDFS는 Master-Worker 구조로, NameNode가 파일명·권한·블록 ID 매핑 등 메타데이터를 메모리에 유지하고, 실제 128MB 단위 데이터 블록 I/O는 다수의 DataNode가 분산 처리합니다."
    },
    {
        "id": 8,
        "category": "2. HDFS 분산저장·센서 시뮬레이션",
        "chapter": "Ch 04",
        "difficulty": "중급",
        "question": "HDFS에서 대용량 자율주행 주행 로그 파일을 저장할 때 기본 **복제 계수(Replication Factor = 3)**를 유지하는 근본적인 목적은?",
        "code": "# HDFS 기본 블록 크기: 128MB | 기본 복제 계수(dfs.replication): 3",
        "options": [
            "특정 DataNode 하드웨어나 디스크가 고장 나더라도 다른 노드에 복제된 블록을 통해 데이터 유실 없이 즉각적인 장애 허용(Fault Tolerance)과 병렬 읽기 성능 향상을 보장하기 위함이다.",
            "파일 용량을 3분의 1로 압축하여 저장하기 위함이다.",
            "한 파일당 최대 3명의 사용자만 읽을 수 있도록 접근 제한을 걸기 위함이다.",
            "리눅스 파일시스템의 3글자 확장자 제한을 우회하기 위함이다."
        ],
        "answer": 0,
        "explanation": "분산 클러스터에서는 개별 서버의 디스크 고장이 일상적으로 발생합니다. 블록을 3개의 서로 다른 노드에 복제해 두면 1~2대 노드가 장애를 일으켜도 무중단 서비스 및 데이터 무결성이 유지됩니다."
    },
    {
        "id": 9,
        "category": "2. HDFS 분산저장·센서 시뮬레이션",
        "chapter": "Ch 04",
        "difficulty": "초급",
        "question": "우분투 터미널에서 로컬 디렉터리에 있는 `CarMaster2Income.txt` 파일을 하둡 HDFS의 `/smartcar/master/` 경로로 업로드할 때 사용하는 올바른 명령어는?",
        "code": "docker cp CarMaster2Income.txt namenode:/tmp/\ndocker exec namenode hdfs dfs -____ /tmp/CarMaster2Income.txt /smartcar/master/",
        "options": [
            "-put (또는 -copyFromLocal)",
            "-get (또는 -copyToLocal)",
            "-rm -r",
            "-chmod 400"
        ],
        "answer": 0,
        "explanation": "HDFS에서 로컬 파일을 분산 파일시스템으로 올릴 때는 `hdfs dfs -put` (또는 `-copyFromLocal`)을 사용하고, HDFS에서 로컬로 내려받을 때는 `-get` (또는 `-copyToLocal`)을 사용합니다."
    },
    {
        "id": 10,
        "category": "2. HDFS 분산저장·센서 시뮬레이션",
        "chapter": "Ch 05",
        "difficulty": "중급",
        "question": "도로 위 자율주행차 10대(`CAR-001` ~ `CAR-010`) 센서 시뮬레이터가 생성하는 실시간 텔레메트리 데이터 중, 차량의 **주행 위험도 및 급정거/급선회 패턴**을 판별하는 핵심 CAN-Bus 물리 지표 묶음은?",
        "code": "{\"car_num\": \"CAR-001\", \"speed\": 118, \"brake_pressure\": 82, \"steering_angle\": 34, \"lat\": 37.4979, \"lon\": 127.0276}",
        "options": [
            "차속(speed), 제동 압력(brake_pressure), 조향각(steering_angle)",
            "운전자 성별(sex), 차량 연식(year), 자동차세 납부액",
            "도커 컨테이너 ID, 리눅스 커널 버전, CPU 온도",
            "와이파이 SSID, 블루투스 MAC 주소, 화면 밝기"
        ],
        "answer": 0,
        "explanation": "고속 주행 중 높은 제동 압력(급브레이크)과 큰 조향각(급핸들 조작)이 동시에 관측되면 추돌 회피 또는 아차사고(Near-Miss) 패턴으로 분류하는 핵심 물리 피처가 됩니다."
    },
    {
        "id": 11,
        "category": "2. HDFS 분산저장·센서 시뮬레이션",
        "chapter": "Ch 05",
        "difficulty": "중급",
        "question": "자율주행 테스트 차량 시뮬레이터에서 간헐적으로 발생하는 **터널 진입 GPS 음영 결측치** 패킷의 특징적인 좌표값은 무엇인가?",
        "code": "# 정상: lat=37.4979, lon=127.0276\n# 터널 음영 구간 센서 두절 시 발생 값: ?",
        "options": [
            "위도(lat) = 0.0, 경도(lon) = 0.0 (적도 기니만 부근 Null Island 좌표)",
            "위도(lat) = 90.0, 경도(lon) = 180.0",
            "위도(lat) = -37.5, 경도(lon) = -127.0",
            "문자열 'SEOUL_STATION'"
        ],
        "answer": 0,
        "explanation": "위성 신호가 끊긴 상태에서 GPS 수신기 기본값이나 파싱 오류 시 `(0.0, 0.0)` 좌표가 유입되는 경우가 많으며, 이를 필터링하지 않으면 Pydeck 3D 지도 궤적이 서울에서 대서양(Null Island)으로 날아가는 직선 왜곡이 발생합니다."
    },
    {
        "id": 12,
        "category": "2. HDFS 분산저장·센서 시뮬레이션",
        "chapter": "Ch 14",
        "difficulty": "고급",
        "question": "Ch 14 엔터프라이즈 파이프라인에서 Hadoop HDFS 상에 적재한 핵심 마스터 및 사고 데이터 파일(`CarMaster2Income.txt`, `CarDrivingIncidentInfo.csv`)과 Hive 테이블의 역할 연결로 올바른 것은?",
        "code": "HDFS: /smartcar/master/CarMaster2Income.txt  <---> Hive Table: car_income\nHDFS: /smartcar/incident/CarDrivingIncidentInfo.csv <---> Hive Table: car_incident",
        "options": [
            "CarMaster2Income.txt는 차량 제원·운전자 소득 회귀 모델(car_income)의 학습 원천이며, CarDrivingIncidentInfo.csv는 주행 사고 3-Class DNN 분류기(car_incident)의 학습 원천이다.",
            "두 파일 모두 Streamlit의 CSS 배경 테마 설정만을 저장하는 JSON 파일이다.",
            "CarMaster2Income.txt는 도커 컨테이너를 강제 종료하는 쉘 스크립트이다.",
            "HDFS에 올린 파일은 Hive 테이블에서 SQL SELECT 문으로 조회할 수 없다."
        ],
        "answer": 0,
        "explanation": "엔터프라이즈 레이크하우스 구조에서는 원천 데이터를 HDFS에 분산 저장한 뒤 Hive 외부 테이블로 스키마를 씌워 각각 OLS 회귀(`car_income`) 및 심층신경망 분류(`car_incident`) 파이프라인으로 공급합니다."
    },

    # 영역 3: Kafka 스트리밍·Hive 웨어하우스 (Q13~Q18)
    {
        "id": 13,
        "category": "3. Kafka 스트리밍·Hive 웨어하우스",
        "chapter": "Ch 06",
        "difficulty": "중급",
        "question": "자율주행 실시간 센서 파이프라인에서 휘발성 메시지 큐(Redis Pub/Sub 등) 대신 **Apache Kafka**를 채택하는 아키텍처상의 3대 핵심 근거로 옳은 것은?",
        "code": "# Kafka Producer -> Topic: smartcar-status -> Multiple Consumer Groups (Hive / Streamlit / AI Interlock)",
        "options": [
            "디스크 오프셋(Offset) 기반 데이터 영속성(장애 시 재현 Replay 가능), 다중 컨슈머 그룹의 독립적 병렬 소비, 차량 ID 키 해싱을 통한 파티션 수평 확장 및 패킷 순서 보장",
            "Kafka는 SQL 데이터베이스보다 그래프 최단 경로(shortestPath) 탐색 속도가 빠르기 때문",
            "Kafka는 별도 디스크 저장 없이 RAM에만 데이터를 1초 보관 후 자동 삭제하기 때문",
            "Kafka를 쓰면 Pydeck WebGL 렌더링 시 Mapbox 유료 토큰을 무료로 우회해 주기 때문"
        ],
        "answer": 0,
        "explanation": "Redis Pub/Sub은 구독자가 잠시 끊기면 메시지가 증발하지만, Kafka는 디스크 로그에 오프셋으로 영구 기록하므로 장애 복구·다중 소비(레이크하우스 적재 + 대시보드 + AI 감시 동시 소비)·차량별 패킷 순서 보장이 가능합니다."
    },
    {
        "id": 14,
        "category": "3. Kafka 스트리밍·Hive 웨어하우스",
        "chapter": "Ch 06",
        "difficulty": "고급",
        "question": "Kafka 컨슈머가 특정 차량(`car_num = 'CAR-001'`)이 보낸 시계열 주행 패킷의 **시간 순서(Ordering)**가 뒤섞이지 않고 정확히 보낸 순서대로 처리받으려면 프로듀서가 어떻게 메시지를 발행해야 하는가?",
        "code": "producer.send('smartcar-status', key=b'CAR-001', value=payload_bytes)",
        "options": [
            "동일한 차량 ID(car_num)를 메시지 키(Key)로 지정하여, 해시 파티셔닝에 의해 해당 차량의 모든 패킷이 항상 같은 파티션(Partition)에 순차 적재되도록 한다.",
            "모든 차량의 메시지를 매번 랜덤한 토픽 이름으로 새로 생성해 발행한다.",
            "acks=0 으로 설정하고 브로커 파티션 개수를 1000개로 늘린 뒤 키(Key)를 None으로 비워둔다.",
            "Zookeeper 포트를 2181에서 9092로 변경한다."
        ],
        "answer": 0,
        "explanation": "Kafka는 토픽 전체가 아니라 **개별 파티션(Partition) 내부**에서만 엄격한 FIFO 순서를 보장합니다. 따라서 `key=car_num`을 지정하면 동일 차량 데이터는 항상 동일 파티션으로 해싱되어 시간 역전을 방지할 수 있습니다."
    },
    {
        "id": 15,
        "category": "3. Kafka 스트리밍·Hive 웨어하우스",
        "chapter": "Ch 07",
        "difficulty": "중급",
        "question": "Apache Hive에서 **내부 테이블(Managed Table)**과 비교할 때, **외부 테이블(External Table)**로 HDFS 데이터를 연동할 때의 가장 결정적인 장점은?",
        "code": "CREATE EXTERNAL TABLE car_income (...)\nROW FORMAT DELIMITED FIELDS TERMINATED BY '|'\nLOCATION '/smartcar/master/';",
        "options": [
            "DROP TABLE 명령으로 하이브 테이블 스키마를 삭제하더라도, HDFS 상의 실제 원본 데이터 파일(/smartcar/master/)은 삭제되지 않고 안전하게 보존된다.",
            "외부 테이블은 SQL SELECT 문 대신 NoSQL Cypher 문법으로만 조회해야 한다.",
            "외부 테이블을 쓰면 Zookeeper 없이도 Kafka 브로커가 자동 복제된다.",
            "외부 테이블은 데이터를 100바이트 이하로만 저장할 수 있다."
        ],
        "answer": 0,
        "explanation": "레이크하우스 환경에서는 여러 엔진(Hive, Spark, Python 등)이 HDFS의 원천 데이터를 공유합니다. External Table은 스키마 메타데이터만 관리하므로 테이블을 드롭해도 원천 빅데이터가 안전하게 유지됩니다."
    },
    {
        "id": 16,
        "category": "3. Kafka 스트리밍·Hive 웨어하우스",
        "chapter": "Ch 08",
        "difficulty": "초급",
        "question": "Ch 08~12 실습에서 우분투 호스트 터미널로부터 도커 컨테이너 안의 하이브(`hive-server`)에 접속하여 `car_income` 테이블 데이터를 즉시 SQL로 조회하는 올바른 명령어는?",
        "code": "pc@DESKTOP-NUVH6QH:~/smartcar-pilot$ ______",
        "options": [
            "docker exec hive-server hive -e \"SELECT car_num, sex, age, capacity, year, income FROM car_income LIMIT 5;\"",
            "hdfs dfs -select \"SELECT * FROM car_income LIMIT 5;\"",
            "kafka-console-consumer --query \"SELECT * FROM car_income\"",
            "poetry run streamlit hive-query car_income"
        ],
        "answer": 0,
        "explanation": "`docker exec hive-server hive -e \"...\"` 명령을 통해 실행 중인 하이브 서버 컨테이너 내부의 Hive CLI에 SQL 문을 직접 전달하고 실행 결과를 터미널에 출력할 수 있습니다."
    },
    {
        "id": 17,
        "category": "3. Kafka 스트리밍·Hive 웨어하우스",
        "chapter": "Ch 09",
        "difficulty": "중급",
        "question": "HiveQL로 자율주행 차량별 운행 지표를 분석할 때, 수십억 건의 주행 로그가 쌓여 있어도 특정 날짜(`dt='2026-11-10'`) 데이터만 스캔하여 쿼리 속도를 수십 배 빠르게 만드는 테이블 설계 기법은?",
        "code": "SELECT car_num, AVG(speed) FROM smartcar_logs\nWHERE dt = '2026-11-10'\nGROUP BY car_num;",
        "options": [
            "파티셔닝(PARTITIONED BY (dt STRING)) 적용을 통한 Full Table Scan 방지 및 파티션 프루닝(Partition Pruning)",
            "테이블의 모든 숫자 컬럼을 STRING 타입으로 변환",
            "LIMIT 1000000 을 모든 서브쿼리에 삽입",
            "NameNode 컨테이너를 2개 이상 중복 실행"
        ],
        "answer": 0,
        "explanation": "Hive에서 `PARTITIONED BY`를 설정하면 HDFS 내부에서 날짜별 하위 디렉터리(`/dt=2026-11-10/`)로 물리 분리 저장되므로, WHERE 조건 시 해당 폴더만 읽어 Full Scan 비용을 제거합니다."
    },
    {
        "id": 18,
        "category": "3. Kafka 스트리밍·Hive 웨어하우스",
        "chapter": "Ch 08",
        "difficulty": "고급",
        "question": "카프카(`smartcar-status`)에서 하이브 창고(HDFS 적재 경로)로 실시간 데이터를 자동 적재하는 마이크로 배치 컨슈머 파이프라인에서, 메시지 소비 도중 프로세스가 비정상 종료되었을 때 데이터 유실이나 중복을 통제하기 위한 핵심 설정 개념은?",
        "code": "consumer = KafkaConsumer('smartcar-status', group_id='hive-loader-group', enable_auto_commit=False)",
        "options": [
            "HDFS 파일 쓰기(Flush/Commit)가 성공적으로 완료된 직후에만 수동으로 오프셋을 커밋(consumer.commit())하는 At-Least-Once 보장 전략",
            "메시지를 읽기도 전에 무조건 1초마다 오프셋을 랜덤 값으로 초기화하는 전략",
            "컨슈머 group_id를 매번 None으로 두어 브로커가 기억하지 못하게 하는 전략",
            "토픽의 모든 파티션을 0개로 줄이는 전략"
        ],
        "answer": 0,
        "explanation": "`enable_auto_commit=False`로 설정하고 실제 HDFS 저장이 완료된 후 `commit()`을 호출해야, 저장 전 크래시가 발생했을 때 마지막 커밋 지점부터 다시 읽어 데이터 유실을 막을 수 있습니다."
    },

    # 영역 4: GPS 정제·Streamlit·Pydeck 3D (Q19~Q24)
    {
        "id": 19,
        "category": "4. GPS 정제·Streamlit·Pydeck 3D",
        "chapter": "Ch 10",
        "difficulty": "초급",
        "question": "Ch 10 실습에서 Streamlit 실시간 관제 센터(`localhost:8501`)와 센서 시뮬레이터, 적재 파이프라인을 동시에 가동하기 위한 올바른 멀티 터미널 운영 구성은?",
        "code": "# 터미널 1: 파이프라인/컨슈머 적재 | 터미널 2: 10대 차량 센서 발생기 | 터미널 3: Streamlit 관제 대시보드",
        "options": [
            "3개의 독립된 우분투 터미널 탭에서 백엔드 스트리밍 발생기, 정제 적재기, Streamlit 프론트엔드 웹 서버를 각각 병렬 실행한 뒤 브라우저에서 localhost:8501로 접속한다.",
            "반드시 단일 터미널 하나에서 3개 스크립트를 세미콜론(;)으로 이어 순차 실행해야 한다.",
            "Streamlit 실행 후 윈도우 Docker Desktop을 완전히 종료해야 포트가 열린다.",
            "Streamlit은 터미널 텍스트만 출력하므로 웹 브라우저로는 접속할 수 없다."
        ],
        "answer": 0,
        "explanation": "스트리밍 생산자, 소비자, 대시보드 웹 서버는 모두 무한 루프로 상시 동작하는 프로세스이므로 각각 별도의 터미널 창(또는 백그라운드 프로세스)에서 동시 실행해야 실시간 데이터 흐름을 관제할 수 있습니다."
    },
    {
        "id": 20,
        "category": "4. GPS 정제·Streamlit·Pydeck 3D",
        "chapter": "Ch 10",
        "difficulty": "중급",
        "question": "최근 파이썬 3.12 및 최신 데이터 분석 라이브러리 환경에서 Streamlit / PyArrow 연동 시 종종 발생하는 **`NumPy 2.0` 호환성 충돌(`AttributeError` / ABI 불일치)**을 해결하는 표준 조치는?",
        "code": "# Error: A module that was compiled using NumPy 1.x cannot be run in NumPy 2.x...",
        "options": [
            "poetry add \"numpy<2.0\" 명령으로 NumPy 버전을 1.26.x 계열로 안전하게 다운그레이드 고정한다.",
            "파이썬 대신 Java 8 JDK를 poetry로 설치한다.",
            "도커 컨테이너의 모든 볼륨 마운트를 삭제한다.",
            "numpy 대신 math 표준 모듈을 pandas 내부 코드에 덮어쓴다."
        ],
        "answer": 0,
        "explanation": "일부 C-확장 기반 라이브러리(구형 pyarrow, tensorflow 등)가 NumPy 1.x ABI로 컴파일되어 있는 경우 NumPy 2.0+ 환경에서 바이너리 호환성 오류가 발생하므로 `numpy<2.0` 제약 조건을 명시해 해결합니다."
    },
    {
        "id": 21,
        "category": "4. GPS 정제·Streamlit·Pydeck 3D",
        "chapter": "Ch 11",
        "difficulty": "중급",
        "question": "Ch 11 Pydeck 3D 지도 시각화에서 유료 Mapbox API 토큰 부재로 **흰 화면(Blank Map)**이 뜨는 문제를 100% 해결하기 위해 본 도서에서 전면 도입한 오픈소스 WebGL 지도 타일 엔진 설정은?",
        "code": "view = pdk.Deck(\n    map_provider=____,\n    map_style=____,\n    initial_view_state=view_state,\n    layers=[path_layer, column_layer]\n)",
        "options": [
            "map_provider=\"carto\", map_style=\"dark\" (Carto Dark-Matter 엔진, API 키 불필요)",
            "map_provider=\"mapbox\", map_style=\"mapbox://styles/mapbox/dark-v11\" (유료 토큰 필수)",
            "map_provider=\"google_earth\", map_style=\"3d_paid\"",
            "map_provider=\"none\", map_style=\"white\""
        ],
        "answer": 0,
        "explanation": "Mapbox는 API 키가 없거나 만료되면 배경 지도가 흰 화면으로 렌더링됩니다. Carto 오픈소스 타일 공급자(`map_provider=\"carto\"`, `map_style=\"dark\"`)를 사용하면 별도 가입이나 토큰 없이 즉시 다크 3D WebGL 지도가 출력됩니다."
    },
    {
        "id": 22,
        "category": "4. GPS 정제·Streamlit·Pydeck 3D",
        "chapter": "Ch 11",
        "difficulty": "고급",
        "question": "Ch 11.2 실시간 카프카 스트리밍 GPS 정제 파이프라인(`smartcar_kafka_gps_clean.py`)에서 서울·수도권 외곽의 이상치 및 터널 결측 좌표를 차단하는 **Bounding Box** 판별 조건으로 올바른 것은?",
        "code": "# 정상 수도권 좌표 범위 판별 (위도 lat, 경도 lon)\nis_valid = (____ <= lat <= ____) and (____ <= lon <= ____)",
        "options": [
            "37.35 <= lat <= 37.75 and 126.80 <= lon <= 127.25",
            "0.0 <= lat <= 10.0 and 0.0 <= lon <= 10.0",
            "-90.0 <= lat <= 0.0 and -180.0 <= lon <= 0.0",
            "126.80 <= lat <= 127.25 and 37.35 <= lon <= 37.75"
        ],
        "answer": 0,
        "explanation": "서울 및 수도권 중심부의 위도(Latitude)는 약 37.35~37.75, 경도(Longitude)는 약 126.80~127.25 범위입니다. 위도와 경도 숫자를 뒤바꾸지 않도록 주의해야 하며, 이 범위를 벗어난 `(0.0, 0.0)` 등은 즉시 차단합니다."
    },
    {
        "id": 23,
        "category": "4. GPS 정제·Streamlit·Pydeck 3D",
        "chapter": "Ch 11",
        "difficulty": "중급",
        "question": "Pydeck `PathLayer`와 `ColumnLayer`에서 마우스를 올렸을 때 툴팁에 **`undefined`**가 출력되는 치명적인 버그를 해결하기 위해 반드시 지켜야 할 데이터 매핑 규칙은?",
        "code": "tooltip={\"html\": \"<b>차량:</b> {car_num}<br/><b>속도:</b> {speed} km/h\"}",
        "options": [
            "tooltip HTML 템플릿에 기재한 `{컬럼명}` 키 이름이 실제 Layer에 전달한 DataFrame(또는 dict 리스트)의 컬럼명과 대소문자까지 정확히 일치해야 한다.",
            "tooltip 문자열 안에 JavaScript alert() 함수를 반드시 포함시켜야 한다.",
            "Layer의 pickable=False 로 설정해야 툴팁 텍스트가 정상 렌더링된다.",
            "모든 숫자 데이터를 NaN으로 치환해 전달해야 한다."
        ],
        "answer": 0,
        "explanation": "Pydeck은 `pickable=True` 상태에서 hover된 객체의 속성을 `{key}` 템플릿으로 바인딩합니다. DataFrame에 없는 컬럼명을 적거나 nested 속성을 잘못 참조하면 `undefined`가 표시됩니다."
    },
    {
        "id": 24,
        "category": "4. GPS 정제·Streamlit·Pydeck 3D",
        "chapter": "Ch 11",
        "difficulty": "초급",
        "question": "`CAR-001`부터 `CAR-010`까지 **10대 자율주행차의 주행 궤적**을 Pydeck 3D 지도에 한눈에 구분되게 시각화할 때 가장 효과적인 색상/레이어 설계 전략은?",
        "code": "# 각 차량 ID별 고유 RGB 네온 컬러 배열 매핑 (get_color='color')",
        "options": [
            "차량별로 서로 다른 고대비 네온 RGB 색상 배열 컬럼을 부여해 PathLayer로 궤적을 그리고, 주요 랜드마크/위험 지점은 3D ColumnLayer의 elevation으로 높이 표현한다.",
            "10대 차량 모두를 배경과 똑같은 검은색([0, 0, 0])으로 칠한다.",
            "모든 차량의 위경도를 평균 내어 지도 중앙에 점 1개만 찍는다.",
            "pitch(기울기)를 0도로 고정하고 텍스트 표만 출력한다."
        ],
        "answer": 0,
        "explanation": "다중 차량 관제에서는 차량별 고유 색상 컬럼(`color`)을 `PathLayer`의 `get_color`에 바인딩하고, `pitch=45` 이상의 3D 시야각에서 `ColumnLayer` 높이를 결합해야 궤적 겹침 없이 입체적인 관제가 가능합니다."
    },

    # 영역 5: OLS 회귀·3-Class DNN·트러블슈팅 (Q25~Q30)
    {
        "id": 25,
        "category": "5. OLS 회귀·3-Class DNN·트러블슈팅",
        "chapter": "Ch 12",
        "difficulty": "중급",
        "question": "Ch 12 `smartcar_hive_regression.py`에서 하이브 `car_income` 테이블 데이터를 기반으로 운전자 연소득(`income`)을 예측할 때, 결정계수 **$R^2 = 74.6\\%$**가 의미하는 통계적 해석은?",
        "code": "model = smf.ols('income ~ age + capacity + year + C(sex)', data=df).fit()\n# R-squared: 0.746, Prob (F-statistic): 1.2e-180",
        "options": [
            "차량 배기량(capacity), 운전자 나이(age), 연식(year), 성별 등 독립변수가 전체 고객 소득 변동성(분산)의 약 74.6%를 통계적으로 유의하게 설명한다는 뜻이다.",
            "모델이 예측한 금액이 실제 소득과 항상 정확히 74.6원 차이가 난다는 뜻이다.",
            "학습 데이터 중 74.6%를 임의로 삭제했다는 뜻이다.",
            "과적합이 발생하여 모델이 전혀 쓸모없다는 뜻이다."
        ],
        "answer": 0,
        "explanation": "결정계수 $R^2$(R-squared)는 종속변수(소득)의 전체 분산 중 회귀 모형이 설명해 내는 분산의 비율(0~1)입니다. 사회과학·마케팅 실무 데이터에서 $R^2=0.746$은 매우 높은 설명력입니다."
    },
    {
        "id": 26,
        "category": "5. OLS 회귀·3-Class DNN·트러블슈팅",
        "chapter": "Ch 12",
        "difficulty": "중급",
        "question": "Ch 12.4 실시간 소득 예측 프로그램(`smartcar_predict_income.py`)에서 운전자 성별(`sex`: `'M'`, `'F'`) 같은 범주형 문자열 변수를 OLS 회귀식에 안전하게 반영하기 위해 사용하는 `statsmodels` 공식 문법은?",
        "code": "formula = 'income ~ age + capacity + year + ____(sex)'",
        "options": [
            "C(sex) — 자동 더미 변수(One-Hot / Categorical Coding) 변환",
            "INT(sex) — ASCII 코드 곱셈",
            "DROP(sex) — 문자열 컬럼 강제 삭제",
            "HASH(sex) — SHA-256 해시화"
        ],
        "answer": 0,
        "explanation": "`statsmodels.formula.api`에서 `C(컬럼명)`을 사용하면 범주형 변수를 자동으로 더미(Dummy) 변수로 인코딩하여 회귀 계수를 산출해 줍니다."
    },
    {
        "id": 27,
        "category": "5. OLS 회귀·3-Class DNN·트러블슈팅",
        "chapter": "Ch 13",
        "difficulty": "중급",
        "question": "Ch 13~14에서 자율주행 차량의 10대 센서 특성을 입력받아 **정상 주행(0), 아차사고 경고(1), 추돌 위험(2)**의 **3-Class 다중 분류 심층신경망(DNN)**을 설계할 때, 출력층(Output Layer)의 활성화 함수와 손실 함수의 올바른 조합은?",
        "code": "model.add(Dense(3, activation=____))\nmodel.compile(optimizer='adam', loss=____, metrics=['accuracy'])",
        "options": [
            "activation='softmax', loss='sparse_categorical_crossentropy' (정수 라벨 0, 1, 2 기준)",
            "activation='sigmoid', loss='mean_squared_error'",
            "activation='relu', loss='binary_crossentropy'",
            "activation='linear', loss='mae'"
        ],
        "answer": 0,
        "explanation": "상호 배타적인 3개 클래스 확률 분포(합=1.0)를 출력하려면 `softmax`가 필수이며, 정답 타깃이 정수(0, 1, 2) 형태일 때는 `sparse_categorical_crossentropy`를 사용해야 원-핫 인코딩 없이 정확히 손실을 계산합니다."
    },
    {
        "id": 28,
        "category": "5. OLS 회귀·3-Class DNN·트러블슈팅",
        "chapter": "Ch 13",
        "difficulty": "고급",
        "question": "차속(`0~180`), 배기량(`998~5000`), 조향각(`-60~60`)처럼 물리 단위와 스케일이 제각각인 센서 데이터를 DNN에 입력하기 전 반드시 **`StandardScaler`** 등으로 스케일링(정규화)해야 하는 이유는?",
        "code": "scaler = StandardScaler()\nX_train_scaled = scaler.fit_transform(X_train)\nX_test_scaled = scaler.transform(X_test)  # 주의: 테스트셋에는 transform만!",
        "options": [
            "특정 큰 수치 변수(배기량 등)가 가중치 기울기(Gradient)를 지배해 경사하강법 수렴이 느려지거나 발산하는 것을 막기 위함이며, 데이터 누수(Data Leakage) 방지를 위해 테스트셋에는 학습셋 기준으로 transform만 호출해야 한다.",
            "StandardScaler를 통과하면 모든 결측 문자열이 자동으로 한국어로 번역되기 때문이다.",
            "테스트셋에도 fit_transform을 매번 새로 호출해야 모델 성능이 공정하게 올라가기 때문이다.",
            "스케일링은 딥러닝의 파라미터 개수를 3배로 늘리기 위한 기법이다."
        ],
        "answer": 0,
        "explanation": "입력 스케일이 다르면 손실 곡면이 찌그러져 학습이 불안정해집니다. 또한 테스트셋에 `fit_transform()`을 쓰면 테스트 데이터의 평균/분산 정보가 유출(Data Leakage)되므로 반드시 학습셋 기준 통계량으로 `transform()`만 적용합니다."
    },
    {
        "id": 29,
        "category": "5. OLS 회귀·3-Class DNN·트러블슈팅",
        "chapter": "Ch 14",
        "difficulty": "고급",
        "question": "Ch 14에서 Hive 레이크하우스와 직접 연동한 `smartcar_hive_dnn.py`가 **99.80%**의 높은 테스트 정확도를 달성한 뒤, 실제 운영 환경에서 **특정 소수 클래스(추돌위험 Class 2)의 재현율(Recall)**이 떨어지지 않는지 추가 검증해야 할 가장 중요한 평가지표는?",
        "code": "from sklearn.metrics import classification_report, confusion_matrix",
        "options": [
            "혼동 행렬(Confusion Matrix)과 Class 2(추돌위험)에 대한 정밀도(Precision)·재현율(Recall)·F1-Score 확인 (실제 사고를 정상으로 놓치는 False Negative 최소화)",
            "단순 학습 시간(초)만 확인하고 나머지는 무시",
            "모든 예측값을 무조건 Class 0으로 고정했을 때의 정확도",
            "HDFS 블록 개수와 Docker 이미지 용량 비교"
        ],
        "answer": 0,
        "explanation": "자율주행 안전 도메인에서는 정상 주행 비율이 압도적(클래스 불균형)이므로 전체 Accuracy만 보면 사고 미탐지(False Negative)를 놓칠 수 있습니다. 반드시 혼동 행렬과 위험 클래스의 Recall을 검증해야 합니다."
    },
    {
        "id": 30,
        "category": "5. OLS 회귀·3-Class DNN·트러블슈팅",
        "chapter": "Ch 15",
        "difficulty": "초급",
        "question": "Ch 15 트러블슈팅: 파이썬 스크립트에서 HiveServer2(`localhost:10000`)에 접속할 때 `TTransportException: Could not connect to localhost:10000` 오류가 발생했을 때 가장 먼저 점검해야 할 조치는?",
        "code": "pc@DESKTOP-NUVH6QH:~/smartcar-pilot$ docker ps -a | grep hive",
        "options": [
            "docker ps 및 docker logs hive-server 로 Hive 컨테이너와 선행 의존성인 Postgres 메타스토어·HDFS NameNode가 정상 기동(Up/Healthy) 완료되었는지 확인한다.",
            "인터넷 공유기 전원을 뽑고 컴퓨터 BIOS로 진입한다.",
            "C 드라이브의 모든 Python 파일을 삭제한다.",
            "Hadoop 포트 번호를 10000에서 80으로 강제 수정한다."
        ],
        "answer": 0,
        "explanation": "HiveServer2는 기동 시 PostgreSQL 메타스토어와 HDFS SafeMode 해제를 기다리기 때문에 초기 부팅에 30~60초가 걸릴 수 있습니다. `docker ps`와 `docker logs hive-server`로 기동 완료 및 포트 바인딩 상태를 확인하는 것이 정석입니다."
    }
]

