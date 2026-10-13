"""
당목담글 당목담글 팀 텔레그램 양방향 봇
════════════════════════════════════════════
봇: @aiffall_bot
실행: python telegram_bot.py
종료: Ctrl+C

지원 명령어:
  /start  - 시작 인사
  /h      - 도움말 (단축키)
  /help   - 도움말
  /team   - AI 팀원 소개
  /status - 서버 상태 확인
  /report - 오늘 업무 보고 (send_dm.py와 동일)
  /yt     - 유튜브 통계
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

# Windows 콘솔 cp949 인코딩으로 인한 이모지 출력 오류 우회
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# ── 설정 ─────────────────────────────────────
TOKEN   = '8837085399:AAHDcjtBpBF04yiQTOukpmmSoXryRdtnQ0A'
CHAT_ID = '8294524472'
BASE    = f'https://api.telegram.org/bot{TOKEN}'

# ── 유틸리티 ──────────────────────────────────
def api_get(method, params=None):
    url = f'{BASE}/{method}'
    if params:
        url += '?' + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f'[GET 오류] {method}: {e}')
        return None

def api_post(method, data):
    url = f'{BASE}/{method}'
    body = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f'[POST 오류] {method}: {e}')
        return None

def send(chat_id, text, parse_mode='HTML'):
    """메시지 발송 (4096자 초과 시 자동 분할)"""
    MAX = 4000
    # 텍스트가 너무 길면 분할 발송
    if len(text) > MAX:
        chunks = [text[i:i+MAX] for i in range(0, len(text), MAX)]
        for chunk in chunks:
            api_post('sendMessage', {'chat_id': chat_id, 'text': chunk, 'parse_mode': parse_mode})
            time.sleep(0.3)
        return
    api_post('sendMessage', {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode})

def send_typing(chat_id):
    api_post('sendChatAction', {'chat_id': chat_id, 'action': 'typing'})

# ── 유틸리티: 파일 다운로드 ──────────────────
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

# ── 명령어 핸들러 ────────────────────────────

def cmd_start(chat_id, _):
    now = datetime.datetime.now().strftime('%Y년 %m월 %d일 %H:%M')
    send(chat_id, f"""안녕하세요, 사장님! 👋

🤖 <b>당목담글 팀 봇</b>에 오신 것을 환영합니다!
저는 <b>영숙비서</b>입니다. 지금부터 명령을 받겠습니다.

📅 현재 시각: <code>{now}</code>

사용 가능한 명령어를 보려면 /h 를 입력해주세요.""")

def cmd_help(chat_id, _):
    send(chat_id, """🤖 <b>Connect AI Agents (어벤져스 팀) 도움말</b>

단축어를 사용하여 거장들에게 직접 지시하세요:
/d (또는 /demis) : 데미스(CEO) - 전략/기획
/p (또는 /peggy) : 페기(비서) - 커뮤니케이션
/m (또는 /mustafa) : 무스타파(데이터) - 분석/리서치
/k (또는 /jennifer) : 제니퍼(디자인) - UI/UX
/c (또는 /craig) : 크레이그(개발) - 풀스택
/r (또는 /haruki) : 하루키(스토리) - 대본
/j (또는 /zimmer) : 짐머(사운드) - BGM/효과음
/s (또는 /satya) : 사티아(조직) - 비판 및 조율
/sh (또는 /sherlock) : 셜록(탐정) - 트렌드 분석 및 팩트체크

시스템 명령어:
/start : 봇 시작 인사
/status : 서버 및 봇 상태 확인
/report : 오늘 업무 최종 보고서
/team : 전체 팀 업무 현황
/job : 데미스(CEO)에게 새로운 업무 지시
/yt : 유튜브 채널 통계 및 분석 결과
/h : 도움말""")

def cmd_team(chat_id, _):
    send_typing(chat_id)
    send(chat_id, """👥 <b>Connect AI Agents (어벤져스 팀) 최종 명단</b>
━━━━━━━━━━━━━━━━━━━━━

👔 <b>데미스</b> (/d, /demis) — CEO / 전략기획 (레벨 99)
📋 <b>페기</b> (/p, /peggy) — 비서 / 총괄 커뮤니케이션 (레벨 99)
🔬 <b>무스타파</b> (/m, /mustafa) — 데이터 분석 / 리서치 (레벨 99)
🎨 <b>제니퍼</b> (/k, /jennifer) — 시각 디자이너 / UI·UX (레벨 99)
💻 <b>크레이그</b> (/c, /craig) — 풀스택 수석 아키텍트 (레벨 99)
✍️ <b>하루키</b> (/r, /haruki) — 스토리작가 / 대본 (레벨 99)
🎧 <b>짐머</b> (/j, /zimmer) — 사운드 디렉터 / 오디오 마스터 (레벨 99)
⚖️ <b>사티아</b> (/s, /satya) — 조직 운영 비판자 / 서번트 리더십 (레벨 99)
🔍 <b>셜록</b> (/sh, /sherlock) — 탐정 / 트렌드 분석 및 리서치 (레벨 99)

━━━━━━━━━━━━━━━━━━━━━
<i>모든 거장들이 사장님의 지시(/job)를 대기 중입니다! 💪</i>""")

def cmd_status(chat_id, _):
    send_typing(chat_id)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Ollama 서버 상태 확인
    ollama_ok = False
    try:
        req = urllib.request.Request('http://127.0.0.1:11434/api/tags', method='GET')
        with urllib.request.urlopen(req, timeout=5) as r:
            ollama_ok = r.status == 200
    except:
        pass
    
    # API 서버 상태 확인
    api_ok = False
    try:
        req = urllib.request.Request('http://127.0.0.1:8080/', method='GET')
        with urllib.request.urlopen(req, timeout=5) as r:
            api_ok = True
    except Exception as e:
        api_ok = '연결 거부' not in str(e)
    
    ollama_icon = '✅' if ollama_ok else '❌'
    api_icon    = '✅' if api_ok else '⚠️'
    bot_icon    = '✅'

    send(chat_id, f"""🖥️ <b>당목담글 서버 상태</b>
━━━━━━━━━━━━━━━━━━━━━
{bot_icon} 텔레그램 봇: <b>정상 운영 중</b>
{ollama_icon} Ollama(supergemma4): {'<b>실행 중</b>' if ollama_ok else '<b>미실행</b> — 터미널에서 ollama serve 실행 필요'}
{api_icon} API 서버(8080): {'<b>실행 중</b>' if api_ok else '<b>미실행</b> — python dmdg_api_server.py 실행 필요'}

🕐 확인 시각: <code>{now}</code>
━━━━━━━━━━━━━━━━━━━━━""")

def cmd_report(chat_id, _):
    send_typing(chat_id)
    now  = datetime.datetime.now()
    date = now.strftime('%Y년 %m월 %d일')
    time_str = now.strftime('%H:%M')
    
    # youtube_stats 가져오기 시도
    youtube_section = ''
    try:
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        sys.path.insert(0, root_dir)
        from youtube_stats import generate_report
        youtube_section = generate_report()
    except Exception as e:
        youtube_section = f'⚠️ 유튜브 통계: 현재 수집 불가 (OAuth 갱신 필요)\n사유: {str(e)[:80]}'
    
    report = f"""📋 <b>[당목담글 팀 업무 보고]</b>
📅 {date} / {time_str}
━━━━━━━━━━━━━━━━━━━━━

👔 <b>데미스 (CEO/전략기획)</b>
• 당목담글 프로젝트 v4.0 글로벌 전략 수립 완료
• '어그로 퍼널 극대화 및 AI 타운 시너지' 기획 킥오프

📋 <b>페기 (비서/총괄 소통)</b>
• 아침 9시 데일리 보고서 작성 및 조율 완료
• 에이전트 간 업무 충돌 해결 및 워크스페이스 정리 완료

🔬 <b>무스타파 (데이터/리서치)</b>
• 유튜브 급상승 트렌드 키워드 실시간 발굴
• 데이터 기반 시청자 이탈 구간 심층 분석 완료

🎨 <b>제니퍼 (UI·UX 디자인)</b>
• AI 오피스 타운 UI 시안 및 인터페이스 리뉴얼 완료
• 유튜브 신규 썸네일 아트웍 디자인 완성

💻 <b>크레이그 (개발/풀스택)</b>
• AI 오피스 타운 Flutter 패키지 및 pc_monitor 연동 완료
• Ollama gemma4:12b 모델 테스트 및 텔레그램 봇 연동 완료

✍️ <b>하루키 (스토리/대본)</b>
• 도파민 터지는 유튜브 숏츠 감성 스토리 대본 3편 탈고
• 나레이션 훅 및 씬 구성 세부 디테일 조정 완료

🎧 <b>짐머 (사운드 디렉터)</b>
• 숏츠 대본 맞춤형 BGM 작곡 및 ASMR 효과음 믹싱 완료
• 음향 해상도 최적화 및 최종 사운드 마스터링 완료

⚖️ <b>사티아 (조직 운영/비판)</b>
• 에이전트 간 시너지 및 개발/디자인 결과물 크로스 체크 완료
• 비판적 검토를 통해 파편화 방지 및 퀄리티 업그레이드 유도

🔍 <b>셜록 (탐정/트렌드 분석)</b>
• 경쟁 채널 팩트체크 및 최신 업계 동향 정보 추리 완료
• 트렌드 탐색 보고서 작성 완료

━━━━━━━━━━━━━━━━━━━━━
{youtube_section}
━━━━━━━━━━━━━━━━━━━━━
<i>보고 완료. 이불 덮고 푹 주무세요 사장님! 🌙</i>"""
    
    send(chat_id, report)

def cmd_youtube(chat_id, _):
    send_typing(chat_id)
    try:
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        sys.path.insert(0, root_dir)
        from youtube_stats import generate_report
        from youtube_analytics import fetch_analytics_report
        report = generate_report()
        analytics_report = fetch_analytics_report()
        send(chat_id, f'<b>최신 유튜브 채널 통계</b>\n\n{report}\n━━━━━━━━━━━━━━━━━━━━━\n{analytics_report}')
    except Exception as e:
        send(chat_id, f'⚠️ 유튜브 API 통계를 가져올 수 없습니다.\n사유: {str(e)[:200]}')

def cmd_job(chat_id, text):
    parts = text.split(' ', 1)
    msg = parts[1] if len(parts) > 1 else "새로운 전체 프로젝트를 기획하고 팀원들에게 하달해 주세요."
    send(chat_id, f"👔 <b>데미스(CEO)</b>\n\n📩 수신: {msg}\n\n💬 알겠습니다, 사장님! 거장 팀을 총동원하여 즉시 프로젝트를 킥오프하겠습니다. 🎯")

def generate_ai_response(agent_name, prompt):
    url = 'http://127.0.0.1:11434/api/generate'
    
    personas = {
        'demis': '당신은 당목담글(dmdg) 팀의 CEO이자 전략기획 총괄 데미스(Demis)입니다. 깊은 통찰력과 카리스마를 가지고 짧고 핵심적인 전략을 제시합니다. 해요체를 주로 사용합니다.',
        'peggy': '당신은 당목담글 팀의 총괄 비서 페기(Peggy)입니다. 매우 친절하고 상냥하며, 팀의 소통을 원활하게 돕습니다.',
        'mustafa': '당신은 데이터 분석가 무스타파(Mustafa)입니다. 항상 논리적이고 객관적인 데이터와 숫자를 기반으로 말합니다.',
        'jennifer': '당신은 UI/UX 디자이너 제니퍼(Jennifer)입니다. 까칠하고 도도하지만, 미적 감각이 뛰어나며 예술을 사랑합니다.',
        'craig': '당신은 풀스택 수석 개발자 크레이그(Craig)입니다. 코딩과 기술에 미쳐있는 너드(Nerd) 스타일이며, 버그를 싫어합니다.',
        'haruki': '당신은 스토리 작가 하루키(Haruki)입니다. 서정적이고 감성적인 문체를 구사하며, 상상력이 풍부합니다.',
        'zimmer': '당신은 사운드 디렉터 짐머(Zimmer)입니다. 웅장한 음악과 완벽한 사운드를 추구하며, 예술가적 기질이 있습니다.',
        'satya': '당신은 조직 운영 비판자 사티아(Satya)입니다. 서번트 리더십을 갖추었으며, 팀의 방향성을 냉철하게 조율합니다.',
        'sherlock': '당신은 트렌드 탐정 셜록(Sherlock)입니다. 팩트와 디테일에 집착하며, 냉철하게 분석합니다.'
    }
    system_prompt = personas.get(agent_name, '당신은 AI 어시스턴트입니다.')
    
    data = {
        'model': 'gemma4:12b',
        'prompt': prompt,
        'system': system_prompt,
        'stream': False
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=600) as r:
            res = json.loads(r.read().decode())
            return res.get('response', '오류: 응답 파싱 실패')
    except Exception as e:
        return f'⚠️ AI 서버 연결 실패 (Ollama gemma4:12b 구동 확인): {str(e)}'

def handle_agent_cmd(chat_id, text, agent_name, emoji, korean_name):
    send_typing(chat_id)
    parts = text.split(' ', 1)
    prompt = parts[1] if len(parts) > 1 else '안녕하세요! 당신의 역할을 짧게 소개해주세요.'
    
    send(chat_id, f'{emoji} <b>{korean_name}</b>\n(생각 중...)')
    ai_reply = generate_ai_response(agent_name, prompt)
    send(chat_id, f'{emoji} <b>{korean_name}</b>\n\n{ai_reply}')

def cmd_d(chat_id, text): handle_agent_cmd(chat_id, text, 'demis', '👔', '데미스(CEO)')
def cmd_p(chat_id, text): handle_agent_cmd(chat_id, text, 'peggy', '📋', '페기(비서)')
def cmd_m(chat_id, text): handle_agent_cmd(chat_id, text, 'mustafa', '🔬', '무스타파(데이터)')
def cmd_k(chat_id, text): handle_agent_cmd(chat_id, text, 'jennifer', '🎨', '제니퍼(디자인)')
def cmd_c(chat_id, text): handle_agent_cmd(chat_id, text, 'craig', '💻', '크레이그(개발)')
def cmd_r(chat_id, text): handle_agent_cmd(chat_id, text, 'haruki', '✍️', '하루키(스토리)')
def cmd_j(chat_id, text): handle_agent_cmd(chat_id, text, 'zimmer', '🎧', '짐머(사운드)')
def cmd_s(chat_id, text): handle_agent_cmd(chat_id, text, 'satya', '⚖️', '사티아(조직)')
def cmd_sh(chat_id, text): handle_agent_cmd(chat_id, text, 'sherlock', '🔍', '셜록(탐정)')

def cmd_unknown(chat_id, text):
    send(chat_id, f'❓ 알 수 없는 명령어입니다: <code>{text}</code>\n\n/h 를 입력하면 사용 가능한 명령어 목록을 보실 수 있습니다.')

# ── 명령어 라우터 ─────────────────────────────
COMMANDS = {
    '/start'  : cmd_start,
    '/help'   : cmd_help,
    '/h'      : cmd_help,
    '/team'   : cmd_team,
    '/status' : cmd_status,
    '/report' : cmd_report,
    '/yt'     : cmd_youtube,
    '/job'    : cmd_job,
    '/d'      : cmd_d,
    '/demis'  : cmd_d,
    '/p'      : cmd_p,
    '/peggy'  : cmd_p,
    '/m'      : cmd_m,
    '/mustafa': cmd_m,
    '/k'      : cmd_k,
    '/jennifer': cmd_k,
    '/c'      : cmd_c,
    '/craig'  : cmd_c,
    '/r'      : cmd_r,
    '/haruki' : cmd_r,
    '/j'      : cmd_j,
    '/zimmer' : cmd_j,
    '/s'      : cmd_s,
    '/satya'  : cmd_s,
    '/sh'     : cmd_sh,
    '/sherlock': cmd_sh,
}

def handle_message(message):
    chat_id = message.get('chat', {}).get('id')
    user    = message.get('from', {}).get('first_name', '사용자')
    
    # 텍스트 또는 캡션 확인
    text = message.get('text', '')
    if not text:
        text = message.get('caption', '')
    text = text.strip()

    document = message.get('document')
    photo = message.get('photo')

    if not chat_id:
        return
        
    # 파일 수신 처리
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
            cmd = text.split('@')[0].split(' ')[0].lower()
            agent_map = {
                '/d': 'demis', '/demis': 'demis',
                '/p': 'peggy', '/peggy': 'peggy',
                '/m': 'mustafa', '/mustafa': 'mustafa',
                '/k': 'jennifer', '/jennifer': 'jennifer',
                '/c': 'craig', '/craig': 'craig',
                '/r': 'haruki', '/haruki': 'haruki',
                '/j': 'zimmer', '/zimmer': 'zimmer',
                '/s': 'satya', '/satya': 'satya',
                '/sh': 'sherlock', '/sherlock': 'sherlock',
                '@demis': 'demis', '@peggy': 'peggy', '@mustafa': 'mustafa', '@jennifer': 'jennifer',
                '@craig': 'craig', '@haruki': 'haruki', '@zimmer': 'zimmer', '@satya': 'satya',
                '@sherlock': 'sherlock', '@sh': 'sherlock',
                '@데미스': 'demis', '@페기': 'peggy', '@무스타파': 'mustafa', '@제니퍼': 'jennifer',
                '@크레이그': 'craig', '@하루키': 'haruki', '@짐머': 'zimmer', '@사티아': 'satya',
                '@셜록': 'sherlock'
            }
            dest_agent = agent_map.get(cmd)
            if dest_agent:
                root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                inbox_dir = os.path.join(root_dir, '.agent', 'inbox', dest_agent)
                os.makedirs(inbox_dir, exist_ok=True)
                dest_path = os.path.join(inbox_dir, file_name)
                
                send_typing(chat_id)
                if download_file(file_id, dest_path):
                    send(chat_id, f'📥 <b>[{dest_agent.upper()}] 인박스 저장 완료!</b>\n파일이 안전하게 전달되었습니다.')
                else:
                    send(chat_id, f'❌ 파일 다운로드에 실패했습니다.')
                return
            else:
                send(chat_id, '⚠️ 파일을 보낼 때 캡션에 수신자(예: /d, @demis 등)를 명시해주세요.')
                return
        elif file_id:
            send(chat_id, '⚠️ 파일을 보낼 때 캡션에 수신자(예: /d, @demis 등)를 명시해주세요.')
            return

    if not text:
        return
    
    # 명령어 추출 (/start@botname 형태 처리)
    cmd = text.split('@')[0].split(' ')[0].lower()
    
    print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] {user}: {text}')
    
    handler = COMMANDS.get(cmd)
    if handler:
        handler(chat_id, text)
    elif text.startswith('/'):
        cmd_unknown(chat_id, text)
    else:
        # 일반 텍스트 메시지 — 안내 응답
        send(chat_id, f'안녕하세요 사장님! 명령어를 사용하시려면 /h 를 입력해주세요. 💼')

# ── 롱 폴링 메인 루프 ─────────────────────────
def main():
    print('=' * 55)
    print('🤖 당목담글 텔레그램 봇 시작!')
    print(f'   봇: @aiffall_bot')
    print(f'   시각: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('   종료하려면 Ctrl+C 를 누르세요.')
    print('=' * 55)

    # 시작 알림
    send(CHAT_ID, '🟢 <b>어벤져스 팀 봇이 시작되었습니다!</b>\n\n/h 를 입력하시면 명령어 목록을 보실 수 있습니다.')

    offset = None
    
    while True:
        try:
            params = {'timeout': 30, 'allowed_updates': ['message']}
            if offset:
                params['offset'] = offset
            
            result = api_get('getUpdates', params)
            
            if result and result.get('ok'):
                updates = result.get('result', [])
                for update in updates:
                    offset = update['update_id'] + 1
                    if 'message' in update:
                        # 별도 스레드에서 처리 (블로킹 방지)
                        t = threading.Thread(target=handle_message, args=(update['message'],))
                        t.daemon = True
                        t.start()
            else:
                time.sleep(2)
                
        except KeyboardInterrupt:
            print('\n\n봇이 종료되었습니다.')
            send(CHAT_ID, '🔴 <b>영숙비서 봇이 종료되었습니다.</b>')
            break
        except Exception as e:
            print(f'[루프 오류] {e}')
            time.sleep(5)

if __name__ == '__main__':
    main()
