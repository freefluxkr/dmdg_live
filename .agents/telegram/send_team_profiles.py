"""팀 프로필 사진 + 정보를 텔레그램으로 순차 전송"""
import urllib.request, urllib.parse, json, sys, io, time, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TOKEN   = '8837085399:AAHDcjtBpBF04yiQTOukpmmSoXryRdtnQ0A'
CHAT_ID = '8294524472'
PORTRAIT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'portraits')

def send_text(msg):
    data = urllib.parse.urlencode({'chat_id': CHAT_ID, 'text': msg}).encode('utf-8')
    req  = urllib.request.Request(
        f'https://api.telegram.org/bot{TOKEN}/sendMessage',
        data=data, method='POST'
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read()).get('ok')

def send_photo(path, caption):
    import mimetypes
    boundary = '----FormBoundary7MA4YWxkTrZu0gW'
    with open(path, 'rb') as f:
        file_data = f.read()
    fname = os.path.basename(path)
    
    body  = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
        f'{CHAT_ID}\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="caption"\r\n\r\n'
        f'{caption}\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="photo"; filename="{fname}"\r\n'
        f'Content-Type: image/png\r\n\r\n'
    ).encode('utf-8') + file_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')
    
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{TOKEN}/sendPhoto',
        data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
            return result.get('ok')
    except Exception as e:
        print(f'  사진 전송 실패: {e}')
        return False

AGENTS = [
    ('demis.png',      '👔 데미스 하사비스 (Demis Hassabis)\nCEO / 전략기획 총괄\n\n딥마인드 급 통찰력을 갖춘 전체 총괄 전략가.\n\n핵심 역량: 1일 1전략 제안, 압도적인 비전 제시 및 프로젝트 킥오프\n\n호출: @demis 또는 /demis 또는 /d'),
    ('peggy.png',      '📋 페기 올슨 (Peggy Olson)\n비서 / 총괄 커뮤니케이션\n\n\'매드맨\'의 전설적인 비서. 팀 내 모든 소통을 매끄럽게 연결합니다.\n\n핵심 역량: 팀 충돌 조율, 아침 9시 데일리 보고, 문서 완벽 정리\n\n호출: @peggy 또는 /peggy 또는 /p'),
    ('mustafa.png',    '🔬 무스타파 술레이만 (Mustafa Suleyman)\n데이터 분석 / 리서치\n\n무한한 데이터의 바다에서 핵심 인사이트를 건져내는 분석가.\n\n핵심 역량: 빅데이터 해독, 급상승 떡상 콘텐츠/키워드 실시간 발굴\n\n호출: @mustafa 또는 /mustafa 또는 /m'),
    ('jennifer.png',   '🎨 제니퍼 아카니 (Jennifer Akani)\n시각 디자이너 / UI·UX\n\n트렌드를 주도하는 글로벌 톱 티어 크리에이티브 디렉터.\n\n핵심 역량: 불편 사항 즉각 개선, 미친 퀄리티의 썸네일 및 UI 시안 제작\n\n호출: @jennifer 또는 /jennifer 또는 /k'),
    ('craig.png',      '💻 크레이그 페더리기 (Craig Federighi)\n풀스택 수석 아키텍트\n\n아이디어를 버그 없는 완벽한 코드로 구현하는 천재 엔지니어.\n\n핵심 역량: 애플 급 무결점 코딩, 24시간 내 시안 구현 및 레거시 최적화\n\n호출: @craig 또는 /craig 또는 /c'),
    ('haruki.png',     '✍️ 무라카미 하루키 (Haruki Murakami)\n스토리작가 / 대본\n\n전 세계 독자를 홀리는 노벨상 후보 급 필력의 소유자.\n\n핵심 역량: 도파민 터지는 유튜브 숏츠 대본 작성, 완벽한 스토리텔링\n\n호출: @haruki 또는 /haruki 또는 /r'),
    ('zimmer.png',     '🎧 한스 짐머 (Hans Zimmer)\n사운드 디렉터 / 오디오 마스터\n\n심박수를 지배하는 오스카상 급 오디오 연출가.\n\n핵심 역량: 대본 무드에 완벽히 들어맞는 BGM/ASMR 믹싱\n\n호출: @zimmer 또는 /zimmer 또는 /j'),
    ('satya.png',      '⚖️ 사티아 나델라 (Satya Nadella)\n조직 운영 / 비판자\n\n팀의 시너지를 극대화하는 서번트 리더십의 표본.\n\n핵심 역량: 조직 파편화 방지, 결과물 크로스 체크 및 건설적 비판\n\n호출: @satya 또는 /satya 또는 /s'),
    ('sherlock.png',   '🔍 셜록 (Sherlock)\n리서처 / 트렌드 탐색 및 정보 추리\n\n단서 하나 놓치지 않고 트렌드와 정보를 집요하게 추적하는 탐정 리서처.\n\n핵심 역량: 트렌드 탐색, 팩트 체크 및 정보 교차 추론\n\n호출: @sherlock 또는 /sherlock 또는 /sh')
]

# 헤더 전송
send_text('👥 Connect AI Agents 팀 프로필 카드를 전송합니다!')
time.sleep(1)

for fname, caption in AGENTS:
    path = os.path.join(PORTRAIT_DIR, fname)
    if os.path.exists(path):
        ok = send_photo(path, caption)
        print(f'{"OK" if ok else "FAIL"}: {fname}')
    else:
        print(f'SKIP (없음): {fname}')
        send_text(caption)
    time.sleep(1.5)

# 마무리 안내
send_text(
    'Connect AI Agents 팀 구성 완료!\n\n'
    '텔레그램 봇 v4.0 업그레이드 내용:\n'
    '  /team - 전체 팀 조회\n'
    '  /status - 서버 및 봇 상태 확인\n'
    '  /report - 업무 최종 보고서\n'
    '  /yt - 유튜브 채널 통계\n'
    '  /h - 도움말 (단축키 안내)\n'
    '  단축어 (예: /d, /demis, @demis) - 에이전트와 직접 대화\n'
    '  파일 전송 -> 자동 인박스 저장\n\n'
    '인박스: .agent/inbox/[직원이름]/\n'
    '사진: .agent/portraits/\n\n'
    '봇 실행: python .agent/telegram/bot.py'
)
print('완료!')
