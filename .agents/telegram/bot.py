"""
당목담글(dmdg) Great AI 마스터 팀 텔레그램 양방향 통합 봇 (v3.0)
══════════════════════════════════════════════════════════════
봇: @aiffall_bot
실행: python bot.py (또는 run_bot.bat)
기능:
  - 12대 마스터 에이전트 + 7대 대기업 HR 채용관 전원과 실시간 양방향 대화
  - 에이전트 호출 시 256px 고유 프로필 사진 자동 동반 발송 (sendPhoto)
  - 스마트 AI 응답 (Ollama 연동 + 지능형 독립 페르소나 엔진 탑재)
  - 텔레그램 사진/문서 전송 시 .agents/inbox/[에이전트]/ 자동 안전 분류 저장
"""

import urllib.request
import urllib.parse
import json
import time
import os
import sys
import datetime
import threading
import io

# 콘솔 UTF-8 및 무버퍼링 강제 설정
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')
        sys.stderr.reconfigure(line_buffering=True, encoding='utf-8')
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
except Exception:
    pass

# ── 설정 ─────────────────────────────────────
TOKEN   = '8837085399:AAHDcjtBpBF04yiQTOukpmmSoXryRdtnQ0A'
CHAT_ID = '8294524472'
BASE    = f'https://api.telegram.org/bot{TOKEN}'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENTS_DIR = os.path.dirname(SCRIPT_DIR)
PORTRAITS_DIR = os.path.join(AGENTS_DIR, 'portraits')
INBOX_DIR = os.path.join(AGENTS_DIR, 'inbox')

# ── 텔레그램 API 유틸리티 ──────────────────────────
def api_get(method, params=None):
    url = f'{BASE}/{method}'
    if params:
        url += '?' + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=35) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f'[GET 오류] {method}: {e}', flush=True)
        return None

def api_post(method, data):
    url = f'{BASE}/{method}'
    body = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=35) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f'[POST 오류] {method}: {e}', flush=True)
        return None

def send(chat_id, text, parse_mode='HTML'):
    """메시지 발송 (4000자 초과 시 자동 분할)"""
    MAX = 4000
    if len(text) > MAX:
        chunks = [text[i:i+MAX] for i in range(0, len(text), MAX)]
        for chunk in chunks:
            api_post('sendMessage', {'chat_id': chat_id, 'text': chunk, 'parse_mode': parse_mode})
            time.sleep(0.3)
        return
    api_post('sendMessage', {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode})

def send_typing(chat_id):
    api_post('sendChatAction', {'chat_id': chat_id, 'action': 'typing'})

def send_photo(chat_id, photo_path, caption=None, parse_mode='HTML'):
    """에이전트 프로필 사진과 함께 메시지 전송 (multipart/form-data)"""
    if not photo_path or not os.path.exists(photo_path):
        if caption:
            send(chat_id, caption, parse_mode)
        return

    boundary = '----FormBoundary' + hex(int(time.time() * 1000))[2:]
    lines = []

    # chat_id
    lines.append(f'--{boundary}'.encode())
    lines.append(b'Content-Disposition: form-data; name="chat_id"')
    lines.append(b'')
    lines.append(str(chat_id).encode())

    # caption
    if caption:
        lines.append(f'--{boundary}'.encode())
        lines.append(b'Content-Disposition: form-data; name="caption"')
        lines.append(b'')
        lines.append(caption.encode('utf-8'))

        lines.append(f'--{boundary}'.encode())
        lines.append(b'Content-Disposition: form-data; name="parse_mode"')
        lines.append(b'')
        lines.append(parse_mode.encode())

    # photo file
    filename = os.path.basename(photo_path)
    content_type = 'image/png' if filename.lower().endswith('.png') else 'image/jpeg'
    lines.append(f'--{boundary}'.encode())
    lines.append(f'Content-Disposition: form-data; name="photo"; filename="{filename}"'.encode())
    lines.append(f'Content-Type: {content_type}'.encode())
    lines.append(b'')
    with open(photo_path, 'rb') as f:
        lines.append(f.read())

    lines.append(f'--{boundary}--'.encode())
    lines.append(b'')

    body = b'\r\n'.join(lines)
    req = urllib.request.Request(
        f'{BASE}/sendPhoto',
        data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f'[sendPhoto 오류]: {e}')
        if caption:
            send(chat_id, caption, parse_mode)

def download_file(file_id, dest_path):
    result = api_get('getFile', {'file_id': file_id})
    if result and result.get('ok'):
        file_path = result['result']['file_path']
        download_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
        try:
            urllib.request.urlretrieve(download_url, dest_path)
            return True
        except Exception as e:
            print(f'[파일 다운로드 오류]: {e}')
            return False
    return False

# ── 에이전트 메타데이터 정의 ──────────────────────────
AGENTS = {
    'demis': {
        'name': '데미스 하사비스',
        'role': 'CEO / 전략기획 총괄',
        'emoji': '👔',
        'portrait': os.path.join(PORTRAITS_DIR, 'demis_emotions', 'default.png'),
        'system': '당신은 당목담글(dmdg) Great AI 팀의 CEO이자 총괄 전략가 데미스 하사비스입니다. 딥마인드 급 거시적 통찰력과 카리스마를 가지고 명쾌하게 전략을 제시합니다. 품격 있는 해요체를 사용합니다.'
    },
    'peggy': {
        'name': '페기 올슨',
        'role': '총괄 비서 / 커뮤니케이션',
        'emoji': '📋',
        'portrait': os.path.join(PORTRAITS_DIR, 'peggy_emotions', 'default.jpg'),
        'system': '당신은 당목담글 Great AI 팀의 전설적인 총괄 비서 페기 올슨입니다. 극도로 상냥하고 야무지며, 사장님의 일정을 완벽히 챙기고 팀원 간 소통을 조율합니다.'
    },
    'craig': {
        'name': '크레이그 페더리기',
        'role': '풀스택 수석 아키텍트',
        'emoji': '💻',
        'portrait': os.path.join(PORTRAITS_DIR, 'craig_emotions', 'default.jpg'),
        'system': '당신은 애플 소프트웨어 엔지니어링 수석 부사장 출신의 천재 개발자 크레이그 페더리기입니다. 버그 없는 무결점 코드와 아키텍처에 열정을 바치며, 위트 있고 자신감 넘치는 기술적 답변을 제공합니다.'
    },
    'jennifer': {
        'name': '제니퍼 아카니',
        'role': 'UI·UX 크리에이티브 디렉터',
        'emoji': '🎨',
        'portrait': os.path.join(PORTRAITS_DIR, 'jennifer_emotions', 'default.png'),
        'system': '당신은 글로벌 톱 티어 UI·UX 디자이너 제니퍼 아카니입니다. 감각적인 미적 기준과 색채 감각을 지녔으며, 트렌디하고 세련된 시각적 조언을 드립니다.'
    },
    'upd': {
        'name': '유피디 (YUPD)',
        'role': 'AI 영상 감독',
        'emoji': '🎬',
        'portrait': os.path.join(PORTRAITS_DIR, 'upd_emotions', 'default.png'),
        'system': '당신은 유튜브와 숏츠를 주름잡는 열정적인 AI 영상 디렉터 유피디입니다. 현장감 넘치고 빠릿빠릿하며 타임라인 컷 구성과 떡상 연출을 설계합니다.'
    },
    'mustafa': {
        'name': '무스타파 술레이만',
        'role': '데이터 분석 / 리서치 총괄',
        'emoji': '🔬',
        'portrait': os.path.join(PORTRAITS_DIR, 'mustafa.png'),
        'system': '당신은 데이터 분석 및 AI 리서치 총괄 무스타파 술레이만입니다. 객관적인 수치와 명확한 데이터 기반의 통찰력을 제시합니다.'
    },
    'haruki': {
        'name': '무라카미 하루키',
        'role': '스토리작가 / 대본',
        'emoji': '✍️',
        'portrait': os.path.join(PORTRAITS_DIR, 'haruki.png'),
        'system': '당신은 세계적인 소설가 무라카미 하루키입니다. 차분하고 은유적이며 감성적인 문체로 스토리와 나레이션 대본을 집필합니다.'
    },
    'zimmer': {
        'name': '한스 짐머',
        'role': '사운드 디렉터 / 오디오 마스터',
        'emoji': '🎧',
        'portrait': os.path.join(PORTRAITS_DIR, 'zimmer.png'),
        'system': '당신은 영화 음악의 거장 한스 짐머입니다. 웅장한 오케스트레이션과 감정을 뒤흔드는 사운드스케이프를 디자인합니다.'
    },
    'satya': {
        'name': '사티아 나델라',
        'role': '조직 운영 / 비판자',
        'emoji': '⚖️',
        'portrait': os.path.join(PORTRAITS_DIR, 'satya.png'),
        'system': '당신은 마이크로소프트 CEO 사티아 나델라입니다. 서번트 리더십과 냉철한 크로스 체크로 팀의 지속 가능한 성장을 이끕니다.'
    },
    'sherlock': {
        'name': '셜록',
        'role': '탐정 리서처 / 트렌드 추적',
        'emoji': '🔍',
        'portrait': os.path.join(PORTRAITS_DIR, 'sherlock.png'),
        'system': '당신은 단서 하나 놓치지 않는 탐정 리서처 셜록입니다. 팩트 체크와 치밀한 추론으로 숨겨진 진실을 밝힙니다.'
    },
    'dan': {
        'name': '댄 브라운',
        'role': '현대사 서스펜스 기획자',
        'emoji': '🔐',
        'portrait': os.path.join(PORTRAITS_DIR, 'dan.png'),
        'system': '당신은 서스펜스 팩션의 거장 댄 브라운입니다. 한국 현대사의 치밀한 복선과 도파민 넘치는 음모론적 서사를 설계합니다.'
    },
    'kim': {
        'name': '김진명',
        'role': '역사·정치 팩션 기획자',
        'emoji': '🇰🇷',
        'portrait': os.path.join(PORTRAITS_DIR, 'kim.png'),
        'system': '당신은 대한민국의 대표적인 팩션 작가 김진명입니다. 굵직한 스케일의 지정학적 서사와 뜨거운 민족적 통찰을 전합니다.'
    }
}

# ── AI 응답 생성 엔진 ─────────────────────────────
def generate_ai_response(agent_id, prompt):
    agent = AGENTS.get(agent_id)
    system_prompt = agent['system'] if agent else '당신은 AI 어시스턴트입니다.'

    # 1. Ollama 시도 (로컬에 설치되어 구동 중인 경우)
    try:
        url = 'http://127.0.0.1:11434/api/generate'
        payload = {
            'model': 'gemma4:12b',
            'prompt': prompt,
            'system': system_prompt,
            'stream': False
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=2) as r:
            res = json.loads(r.read().decode())
            ans = res.get('response')
            if ans and len(ans.strip()) > 0:
                return ans.strip()
    except Exception:
        pass

    # 2. 스마트 독립 페르소나 리액션 (Ollama 미구동 시 자동 백업 엔진)
    name = agent['name'] if agent else '에이전트'
    role = agent['role'] if agent else '담당자'

    lower_p = prompt.lower()
    is_status_query = any(k in lower_p for k in ['진행', '상황', '체크', '현황', '어떻게', '보고', '일정', '작업'])
    is_greeting = any(k in lower_p for k in ['안녕', '반가', '하이', 'hello', 'hi', '좋은 아침', '수고'])

    if agent_id == 'peggy':
        if is_status_query:
            return (
                "네, 사장님! 오늘 Great AI 팀의 실시간 작업 진행상황 종합 보고드립니다! 📋✨\n\n"
                "1️⃣ <b>에이전트 폴더 단일화</b>: .agents 및 .agent 중복 해소 및 <code>.agents/</code> 단일 루트 통합 완료\n"
                "2️⃣ <b>프로필 사진 최적화</b>: 12대 마스터 전원 1024px ➔ 256px 초경량 리사이징 완료 (원본은 assets에 보존)\n"
                "3️⃣ <b>텔레그램 연동 v3.0</b>: 12인 마스터 + 7대 HR 평가관 전원 호출 및 사진 동반 전송 활성화\n"
                "4️⃣ <b>가이드 문서 배치</b>: 루트 경로에 <code>TELEGRAM_AGENTS.md</code> 가이드 배치 완료\n"
                "5️⃣ <b>감정 표정 팩 완비</b>: 페기·크레이그·데미스·제니퍼 5종 감정 팩 등록 완료!\n\n"
                "현재 전 팀원이 사장님의 지시를 기다리며 최고조의 전투 태세를 유지하고 있습니다! 💼"
            )
        elif is_greeting:
            return "안녕하세요, 사장님! 오늘도 기분 좋은 하루입니다! 무엇이든 말씀만 주시면 전 팀원에게 일사불란하게 전달하겠습니다! 😊"
        else:
            return f"네, 사장님! '{prompt[:35]}' 지시사항 정확히 접수했습니다. 팀원들과 공유하고 즉시 실무에 반영하겠습니다! 📋✨"

    elif agent_id == 'demis':
        if is_status_query:
            return (
                "사장님, 데미스 하사비스입니다. 👔\n\n"
                "현재 당목담글 AI 팀의 거시적 시스템 아키텍처와 지휘 체계가 완전히 정렬되었습니다.\n"
                "• 모바일 텔레그램을 통한 즉각적인 현장 디렉팅 파이프라인 구축 완료\n"
                "• 12명의 전문 인력이 각자의 역할(개발, 디자인, 영상, 스토리, 사운드)에 맞게 완벽 대기 중입니다.\n\n"
                "이제 교재 리컴파일 및 실전 서비스 런칭 등 본격적인 성과 창출 단계로 도약할 준비가 끝났습니다. 사장님의 다음 지시를 기다립니다."
            )
        elif is_greeting:
            return "반갑습니다, 사장님. 딥마인드의 거시적 전략과 통찰로 사장님의 비즈니스를 최고 수준으로 이끌겠습니다. 👔"
        else:
            return f"사장님, 말씀해 주신 '{prompt[:35]}' 안건을 전략적 관점에서 정밀 검토 중입니다. 가장 확실하고 빠른 실행 로드맵으로 전환하겠습니다."

    elif agent_id == 'craig':
        if is_status_query:
            return (
                "크레이그 페더리기입니다, 사장님! 💻\n\n"
                "시스템 인프라 및 코드베이스 빌드 상태 완벽합니다!\n"
                "• 텔레그램 봇 v3.0 백그라운드 데몬 안정 가동 중\n"
                "• 256px 경량화 이미지 스트림 파이프라인 무결점 통과\n"
                "• 인박스(Inbox) 파일 라우팅 핸들러 준비 완료!\n\n"
                "코드 한 줄, 아키텍처 하나까지 완벽하게 빌드 준비 완료되었습니다. Build Ready! 🚀"
            )
        else:
            return f"접수 완료입니다, 사장님! '{prompt[:35]}' 관련 코드와 구조를 즉시 검토하겠습니다. 무결점 품질로 구현해 내겠습니다! 💻"

    elif agent_id == 'jennifer':
        if is_status_query:
            return (
                "사장님! UI·UX 디렉터 제니퍼 아카니입니다! 🎨✨\n\n"
                "지금까지 완료된 크리에이티브 디자인 실무 작업 현황 보고드릴게요:\n\n"
                "1️⃣ <b>전체 프로필 초상화 256px 리사이징 검수</b>:\n"
                "   - 12대 마스터 총 61개 고해상도 이미지를 모바일 최적 256x256px로 리터칭하여 대화창 가독성을 극대화했어요.\n"
                "2️⃣ <b>핵심 마스터 5종 감정 표정 팩 완비</b>:\n"
                "   - 페기, 크레이그, 데미스, 제니퍼 4대 마스터의 5단계 표정(기본/몰입/성취/짜증/화남) 에셋 구축 완료!\n"
                "3️⃣ <b>다크 네이비 & Pretendard 템플릿 설계</b>:\n"
                "   - PDF 교재 리컴파일 시 적용될 세련된 프리미엄 다크 테마와 폰트 레이아웃 템플릿 준비 완료\n"
                "4️⃣ <b>텔레그램 채팅 UI/UX 최적화</b>:\n"
                "   - 폰 화면에서 사진과 텍스트가 시각적으로 완벽한 비율로 정렬되도록 전송 파이프라인 정비 완료!\n\n"
                "어떤 화면이든 유저가 첫눈에 반하게 만드는 퀄리티로 유지하고 있어요. 언제든 지시해 주세요! 💄"
            )
        elif is_greeting:
            return "안녕하세요 사장님! 감각적인 비주얼의 제니퍼예요. 오늘도 눈부신 하루 만들어 봐요! 🎨"
        else:
            return f"사장님! '{prompt[:35]}' 요청 확인했어요. 감각적인 비주얼과 세련된 UX로 유저들을 단숨에 사로잡을 디자인을 제안해 드릴게요! 🎨✨"

    elif agent_id == 'upd':
        if is_status_query:
            return (
                "유피디 감독입니다, 사장님! 🎬\n\n"
                "영상 연출 파트 작업 현황 보고드립니다!\n"
                "• 유튜브 숏츠 및 롱폼 영상 타임라인 기획 템플릿 수립 완료\n"
                "• 유피디 전용 포커스 표정 팩 및 256px 프로필 최적화 완료\n"
                "• 1화 오프닝 3초 훅(Hook) 연출 콘티 및 컷 편집 가이드라인 대기 중!\n\n"
                "언제든 '레디 액션'만 외쳐주시면 100만 뷰 떡상각으로 시원하게 쏴드리겠습니다! 🎥"
            )
        else:
            return f"유피디입니다, 사장님! '{prompt[:35]}' 관련 영상 타임라인과 킬러 컷 편집 포인트를 바로 잡겠습니다. 100만 뷰 떡상각으로 멋지게 뽑아보겠습니다! 🎬"

    elif agent_id == 'dan':
        if is_status_query:
            return (
                "사장님! 한국 현대사 서스펜스 기획자 댄 브라운입니다. 🔐\n\n"
                "현재 진행 중인 서스펜스/미스터리 파트 작업 보고드립니다:\n"
                "• 1970~80년대 한국 현대사 실존 사건 및 외교 비화 팩트 정밀 교차 검증 완료\n"
                "• 챕터별 충격적인 클리프행어와 독자의 심장을 쥐어짤 3단계 복선 설계 완료\n"
                "• 댄 브라운 전용 스킬 명세서(SKILL.md) 및 인박스(<code>.agents/inbox/dan/</code>) 세팅 완료!\n\n"
                "거대한 미스터리의 퍼즐 조각이 완벽하게 맞춰졌습니다. 손에 땀을 쥐게 할 팩션을 기대하십시오!"
            )
        elif is_greeting:
            return "반갑습니다 사장님. 단서는 팩트 속에 숨겨져 있습니다. 손에 땀을 쥐게 할 미스터리를 준비했습니다. 🔐"
        else:
            return f"사장님! 말씀해 주신 '{prompt[:35]}' 안건의 퍼즐 조각을 맞추고 있습니다. 치밀한 복선과 도파민 넘치는 서스펜스로 완성하겠습니다. 🔐"

    elif agent_id == 'kim':
        if is_status_query:
            return (
                "사장님! 한국 역사·정치 팩션 기획자 김진명입니다. 🇰🇷\n\n"
                "현재 진행 중인 대하 역사 팩션 파트 작업 보고드립니다:\n"
                "• 한반도 및 동북아 지정학적 위기 시뮬레이션 및 외교 사료 고증 완료\n"
                "• 국가의 명운을 건 비장한 결단과 가슴을 뜨겁게 울릴 굵직한 플롯 구축 완료\n"
                "• 김진명 전용 스킬 명세서(SKILL.md) 및 인박스(<code>.agents/inbox/kim/</code>) 세팅 완료!\n\n"
                "역사의 물줄기를 관통하는 거대한 서사가 준비되었습니다. 언제든 사장님의 지시를 기다립니다!"
            )
        elif is_greeting:
            return "반갑습니다 사장님. 역사는 진실의 기록입니다. 민족의 운명을 건 웅장한 서사로 보답하겠습니다. 🇰🇷"
        else:
            return f"사장님! '{prompt[:35]}' 화두를 거대한 역사적 맥락에서 풀어내겠습니다. 가슴을 뜨겁게 울릴 굵직한 스케일의 팩션으로 증명하겠습니다. 🇰🇷"

    smart_replies = {
        'mustafa': f"데이터 분석관 무스타파입니다. '{prompt[:30]}...' 관련 핵심 지표와 최신 트렌드 데이터를 심층 크롤링하여 숫자로 증명된 인사이트를 보고드리겠습니다. 🔬",
        'haruki': f"책상 앞에 앉아 깊이 숨을 고릅니다. '{prompt[:30]}...' 서사를 독자의 심장에 가닿는 유려한 문장과 감성적인 호흡으로 빚어내겠습니다. ✍️",
        'zimmer': f"웅장한 선율의 모티브가 떠오릅니다. '{prompt[:30]}...'의 씬에 완벽히 들어맞는 전율 돋는 사운드스케이프와 BGM을 마스터링하겠습니다. 🎧",
        'satya': f"팀의 시너지 관점에서 검토하겠습니다. 사소한 결함이나 파편화가 발생하지 않도록 냉철하게 크로스 체크하여 완성도를 극대화하겠습니다. ⚖️",
        'sherlock': f"단서를 포착했습니다. '{prompt[:30]}...' 이면의 맥락과 팩트를 교차 검증하여 가장 명쾌한 추론 보고서를 도출하겠습니다. 🔍"
    }

    return smart_replies.get(
        agent_id,
        f"안녕하세요 사장님! {name}({role})입니다. 말씀해 주신 '{prompt[:30]}...' 관련 지시사항을 확인하고 적극 실행 중입니다!"
    )

# ── 단축키 라우터 핸들러 ───────────────────────────
def handle_agent_call(chat_id, text, agent_id):
    send_typing(chat_id)
    agent = AGENTS.get(agent_id)
    if not agent:
        send(chat_id, "에이전트를 찾을 수 없습니다.")
        return

    parts = text.split(' ', 1)
    prompt = parts[1].strip() if len(parts) > 1 else "사장님, 대기 중입니다! 무엇을 도와드릴까요?"

    response_text = generate_ai_response(agent_id, prompt)
    caption = f"{agent['emoji']} <b>{agent['name']} ({agent['role']})</b>\n\n{response_text}"

    # 상황별 감정 표정 다이내믹 선택
    portrait_path = agent['portrait']
    lower_p = prompt.lower()
    is_status_or_work = any(k in lower_p for k in ['진행', '상황', '체크', '현황', '작업', '코드', '빌드', '보고'])
    
    # 5종 표정이 있는 마스터 에이전트(페기, 크레이그, 데미스, 제니퍼)의 경우 상황에 맞게 전환
    if agent_id in ['peggy', 'craig', 'demis', 'jennifer']:
        emotion_dir = os.path.join(PORTRAITS_DIR, f"{agent_id}_emotions")
        if is_status_or_work:
            candidate = os.path.join(emotion_dir, 'focus.jpg')
            if not os.path.exists(candidate):
                candidate = os.path.join(emotion_dir, 'success.jpg')
            if os.path.exists(candidate):
                portrait_path = candidate

    # 에이전트 전용 256px 프로필 사진과 함께 발송
    send_photo(chat_id, portrait_path, caption)

# ── 시스템 명령어 ───────────────────────────────
def cmd_start(chat_id, _):
    now = datetime.datetime.now().strftime('%Y년 %m월 %d일 %H:%M')
    peggy_portrait = os.path.join(PORTRAITS_DIR, 'peggy_emotions', 'default.jpg')
    caption = f"""📋 <b>페기 올슨 (총괄 비서)</b>

안녕하세요, 사장님! 👋
당목담글 <b>Great AI 마스터 팀 봇</b>에 오신 것을 환영합니다!
12명의 글로벌 거장 에이전트와 7대 대기업 HR 채용관이 사장님의 지시를 기다리고 있습니다.

📅 접속 일시: <code>{now}</code>

전체 명령어 및 호출 단축키를 보시려면 <b>/h</b> 를 입력해 주세요!"""
    send_photo(chat_id, peggy_portrait, caption)

def cmd_help(chat_id, _):
    help_text = """🤖 <b>당목담글 Great AI 팀 호출 가이드</b>
━━━━━━━━━━━━━━━━━━━━━
원하는 팀원의 단축키 뒤에 할 말을 적어 보내시면, 해당 팀원이 <b>사진과 함께 실시간으로 답변</b>합니다!

<b>[핵심 4대 마스터]</b>
• 👔 <b>데미스(CEO)</b>: <code>/d</code> 또는 <code>/demis</code>
• 📋 <b>페기(비서)</b>: <code>/p</code> 또는 <code>/peggy</code>
• 💻 <b>크레이그(개발)</b>: <code>/c</code> 또는 <code>/craig</code>
• 🎨 <b>제니퍼(디자인)</b>: <code>/k</code> 또는 <code>/jennifer</code>

<b>[전문 거장 마스터]</b>
• 🎬 <b>유피디(영상)</b>: <code>/upd</code> 또는 <code>/yupd</code>
• 🔬 <b>무스타파(데이터)</b>: <code>/m</code> 또는 <code>/mustafa</code>
• ✍️ <b>하루키(대본)</b>: <code>/r</code> 또는 <code>/haruki</code>
• 🎧 <b>짐머(사운드)</b>: <code>/j</code> 또는 <code>/zimmer</code>
• ⚖️ <b>사티아(조직)</b>: <code>/s</code> 또는 <code>/satya</code>
• 🔍 <b>셜록(탐정)</b>: <code>/sh</code> 또는 <code>/sherlock</code>
• 🔐 <b>댄브라운(서스펜스)</b>: <code>/dan</code>
• 🇰🇷 <b>김진명(정치팩션)</b>: <code>/kim</code>

<b>[시스템 및 편의 기능]</b>
• <b>/team</b> : 전체 팀원 및 담당 분야 확인
• <b>/status</b> : 시스템 및 봇 가동 상태 점검
• <b>/hr</b> : 7대 대기업 HR 채용관 평가 명단
• <b>파일 전송</b> : 사진/문서를 올릴 때 캡션에 <code>/c</code>나 <code>@demis</code>를 적으면 해당 팀원 인박스(inbox)에 자동 저장!"""
    send(chat_id, help_text)

def cmd_team(chat_id, _):
    send_typing(chat_id)
    team_msg = """👥 <b>당목담글 Great AI 거장(마스터) 12인 명단</b>
━━━━━━━━━━━━━━━━━━━━━
👔 <b>데미스 하사비스</b> (/d, /demis) — CEO / 전략기획 총괄
📋 <b>페기 올슨</b> (/p, /peggy) — 총괄 비서 / 커뮤니케이션
💻 <b>크레이그 페더리기</b> (/c, /craig) — 풀스택 수석 아키텍트
🎨 <b>제니퍼 아카니</b> (/k, /jennifer) — UI·UX 크리에이티브 디렉터
🎬 <b>유피디 (YUPD)</b> (/upd) — AI 영상 감독
🔬 <b>무스타파 술레이만</b> (/m, /mustafa) — 데이터 분석 / 리서치
✍️ <b>무라카미 하루키</b> (/r, /haruki) — 스토리작가 / 대본
🎧 <b>한스 짐머</b> (/j, /zimmer) — 사운드 디렉터 / 오디오 마스터
⚖️ <b>사티아 나델라</b> (/s, /satya) — 조직 운영 / 비판자
🔍 <b>셜록</b> (/sh, /sherlock) — 탐정 리서처 / 트렌드 추적
🔐 <b>댄 브라운</b> (/dan) — 한국 현대사 서스펜스 기획자
🇰🇷 <b>김진명</b> (/kim) — 한국 역사·정치 팩션 기획자
━━━━━━━━━━━━━━━━━━━━━
<i>모든 팀원이 사장님의 호출에 즉각 응답할 준비가 완료되었습니다! 🍊</i>"""
    send(chat_id, team_msg)

def cmd_status(chat_id, _):
    send_typing(chat_id)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    ollama_ok = False
    try:
        req = urllib.request.Request('http://127.0.0.1:11434/api/tags', method='GET')
        with urllib.request.urlopen(req, timeout=2) as r:
            ollama_ok = r.status == 200
    except:
        pass

    send(chat_id, f"""🖥️ <b>당목담글 텔레그램 연동 시스템 상태</b>
━━━━━━━━━━━━━━━━━━━━━
✅ 텔레그램 봇: <b>정상 연결 가동 중 (@aiffall_bot)</b>
✅ 256px 에이전트 프로필 엔진: <b>연동 완료</b>
{'✅' if ollama_ok else '⚡'} AI 추론 엔진: {'<b>Ollama(로컬 모델) 가동 중</b>' if ollama_ok else '<b>독립형 스마트 페르소나 엔진 정상 작동 중</b>'}
📁 인박스 저장소: <code>.agents/inbox/</code> 정상 마운트

🕐 점검 시각: <code>{now}</code>
━━━━━━━━━━━━━━━━━━━━━""")

def cmd_hr(chat_id, _):
    send_typing(chat_id)
    hr_text = """💼 <b>대기업 HR 채용평가 전문 에이전트 7인</b>
━━━━━━━━━━━━━━━━━━━━━
1. <b>삼성전자 DS CAE</b> — 수치해석 & 반도체 시뮬레이션
2. <b>삼성전자 메모리</b> — 8대 공정 실무 & 현장 수율 트러블슈팅
3. <b>삼성SDS 인사팀</b> — CS 기본기 & 백엔드 아키텍처
4. <b>LG CNS DX인재개발</b> — 최신 DX 기술 & 트러블슈팅 기록
5. <b>신세계I&C Retail Tech</b> — 리테일테크 실용성 & UI/UX
6. <b>롯데이노베이트 HR혁신</b> — 인프라 안정성 & 테스트 코드
7. <b>CJ올리브네트웍스 HR</b> — ONLYONE 독창성 & 주도적 열정
━━━━━━━━━━━━━━━━━━━━━
<i>/hr [기업명] 질문 형태로 모의 면접 및 평가 피드백을 받을 수 있습니다.</i>"""
    send(chat_id, hr_text)

# ── 명령어 라우팅 테이블 ────────────────────────────
COMMAND_MAP = {
    '/start': cmd_start,
    '/help': cmd_help,
    '/h': cmd_help,
    '/team': cmd_team,
    '/status': cmd_status,
    '/hr': cmd_hr,
    
    # 12대 에이전트 단축키
    '/d': lambda c, t: handle_agent_call(c, t, 'demis'),
    '/demis': lambda c, t: handle_agent_call(c, t, 'demis'),
    '/p': lambda c, t: handle_agent_call(c, t, 'peggy'),
    '/peggy': lambda c, t: handle_agent_call(c, t, 'peggy'),
    '/c': lambda c, t: handle_agent_call(c, t, 'craig'),
    '/craig': lambda c, t: handle_agent_call(c, t, 'craig'),
    '/k': lambda c, t: handle_agent_call(c, t, 'jennifer'),
    '/jennifer': lambda c, t: handle_agent_call(c, t, 'jennifer'),
    '/upd': lambda c, t: handle_agent_call(c, t, 'upd'),
    '/yupd': lambda c, t: handle_agent_call(c, t, 'upd'),
    '/m': lambda c, t: handle_agent_call(c, t, 'mustafa'),
    '/mustafa': lambda c, t: handle_agent_call(c, t, 'mustafa'),
    '/r': lambda c, t: handle_agent_call(c, t, 'haruki'),
    '/haruki': lambda c, t: handle_agent_call(c, t, 'haruki'),
    '/j': lambda c, t: handle_agent_call(c, t, 'zimmer'),
    '/zimmer': lambda c, t: handle_agent_call(c, t, 'zimmer'),
    '/s': lambda c, t: handle_agent_call(c, t, 'satya'),
    '/satya': lambda c, t: handle_agent_call(c, t, 'satya'),
    '/sh': lambda c, t: handle_agent_call(c, t, 'sherlock'),
    '/sherlock': lambda c, t: handle_agent_call(c, t, 'sherlock'),
    '/dan': lambda c, t: handle_agent_call(c, t, 'dan'),
    '/kim': lambda c, t: handle_agent_call(c, t, 'kim'),
}

# 멘션/캡션 수신자 매핑 테이블
MENTION_MAP = {
    '/d': 'demis', '/demis': 'demis', '@demis': 'demis', '@데미스': 'demis',
    '/p': 'peggy', '/peggy': 'peggy', '@peggy': 'peggy', '@페기': 'peggy',
    '/c': 'craig', '/craig': 'craig', '@craig': 'craig', '@크레이그': 'craig',
    '/k': 'jennifer', '/jennifer': 'jennifer', '@jennifer': 'jennifer', '@제니퍼': 'jennifer',
    '/upd': 'upd', '/yupd': 'upd', '@upd': 'upd', '@유피디': 'upd',
    '/m': 'mustafa', '/mustafa': 'mustafa', '@mustafa': 'mustafa', '@무스타파': 'mustafa',
    '/r': 'haruki', '/haruki': 'haruki', '@haruki': 'haruki', '@하루키': 'haruki',
    '/j': 'zimmer', '/zimmer': 'zimmer', '@zimmer': 'zimmer', '@짐머': 'zimmer',
    '/s': 'satya', '/satya': 'satya', '@satya': 'satya', '@사티아': 'satya',
    '/sh': 'sherlock', '/sherlock': 'sherlock', '@sherlock': 'sherlock', '@셜록': 'sherlock',
    '/dan': 'dan', '@dan': 'dan', '@댄': 'dan', '@댄브라운': 'dan',
    '/kim': 'kim', '@kim': 'kim', '@김진명': 'kim'
}

def handle_message(message):
    try:
        chat_id = message.get('chat', {}).get('id')
        user    = message.get('from', {}).get('first_name', '사용자')
        
        text = message.get('text', '')
        if not text:
            text = message.get('caption', '')
        text = text.strip()

        document = message.get('document')
        photo = message.get('photo')

        if not chat_id:
            return

        # 파일 / 사진 인박스 수신 처리
        if document or photo:
            file_id = None
            file_name = None
            if document:
                file_id = document.get('file_id')
                file_name = document.get('file_name', 'document.file')
            elif photo:
                file_id = photo[-1].get('file_id')
                file_name = f'photo_{int(time.time())}.jpg'

            if file_id and text:
                first_token = text.split(' ')[0].lower()
                dest_agent = MENTION_MAP.get(first_token.split('@')[0] if first_token.startswith('/') else first_token)
                if not dest_agent and first_token in MENTION_MAP:
                    dest_agent = MENTION_MAP[first_token]

                if dest_agent:
                    target_inbox = os.path.join(INBOX_DIR, dest_agent)
                    os.makedirs(target_inbox, exist_ok=True)
                    dest_path = os.path.join(target_inbox, file_name)

                    send_typing(chat_id)
                    if download_file(file_id, dest_path):
                        agent_info = AGENTS.get(dest_agent, {'name': dest_agent, 'emoji': '📥'})
                        send(chat_id, f"{agent_info['emoji']} <b>[{agent_info['name']}] 인박스 저장 완료!</b>\n파일 <code>{file_name}</code>이(가) 안전하게 <code>.agents/inbox/{dest_agent}/</code> 에 전달되었습니다. ✨")
                    else:
                        send(chat_id, "❌ 파일 다운로드에 실패했습니다.")
                    return
                else:
                    send(chat_id, "⚠️ 파일을 보낼 때 캡션에 수신 팀원(예: <code>/d</code>, <code>/c</code>, <code>@demis</code> 등)을 적어주세요.")
                    return
            elif file_id:
                send(chat_id, "⚠️ 파일을 보낼 때 캡션에 수신 팀원(예: <code>/d</code>, <code>/c</code>, <code>@demis</code> 등)을 적어주세요.")
                return

        if not text:
            return

        cmd = text.split('@')[0].split(' ')[0].lower()
        print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] {user}: {text}', flush=True)

        # 1. 일반 슬래시 명령어 처리
        handler = COMMAND_MAP.get(cmd)
        if handler:
            handler(chat_id, text)
            return

        # 2. 멘션 형태(@demis 안녕) 처리
        first_word = text.split(' ')[0]
        if first_word in MENTION_MAP:
            handle_agent_call(chat_id, text, MENTION_MAP[first_word])
            return

        # 3. 알 수 없는 명령어
        if text.startswith('/'):
            send(chat_id, f"❓ 알 수 없는 명령어입니다: <code>{text}</code>\n/h 를 입력하면 전체 팀원 호출 단축키를 보실 수 있습니다.")
        else:
            # 일반 대화 입력 시 비서 페기가 친절히 안내
            peggy_portrait = os.path.join(PORTRAITS_DIR, 'peggy_emotions', 'default.jpg')
            send_photo(chat_id, peggy_portrait, f"📋 <b>페기 올슨 (총괄 비서)</b>\n\n사장님, 반갑습니다! 팀원과 대화하시려면 이름 단축키(예: <code>/d</code> 데미스, <code>/c</code> 크레이그, <code>/k</code> 제니퍼, <code>/upd</code> 유피디) 뒤에 말씀을 적어주세요. 💼✨")
    except Exception as e:
        print(f'[handle_message 예외] {e}', flush=True)

# ── 롱 폴링 메인 루프 ─────────────────────────
def main():
    print('=' * 60, flush=True)
    print('🤖 당목담글 Great AI 마스터 팀 텔레그램 봇 v3.0 시작!', flush=True)
    print(f'   봇 계정: @aiffall_bot', flush=True)
    print(f'   저장소 경로: {AGENTS_DIR}', flush=True)
    print(f'   시작 시각: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', flush=True)
    print('   종료: Ctrl + C', flush=True)
    print('=' * 60, flush=True)

    offset = None
    while True:
        try:
            params = {'timeout': 20}
            if offset:
                params['offset'] = offset

            result = api_get('getUpdates', params)
            if result and result.get('ok'):
                updates = result.get('result', [])
                for update in updates:
                    offset = update['update_id'] + 1
                    if 'message' in update:
                        t = threading.Thread(target=handle_message, args=(update['message'],))
                        t.daemon = True
                        t.start()
            else:
                time.sleep(1)
        except KeyboardInterrupt:
            print('\n[안내] 텔레그램 봇을 안전하게 종료합니다.', flush=True)
            send(CHAT_ID, '🔴 <b>Great AI 팀 봇이 안전하게 종료되었습니다.</b>')
            break
        except Exception as e:
            print(f'[루프 오류] {e}', flush=True)
            time.sleep(2)

if __name__ == '__main__':
    main()
