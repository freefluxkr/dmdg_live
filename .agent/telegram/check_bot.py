"""봇 상태 진단 및 양방향 통신 테스트"""
import urllib.request, urllib.parse, json

TOKEN = '8837085399:AAHDcjtBpBF04yiQTOukpmmSoXryRdtnQ0A'
BASE  = f'https://api.telegram.org/bot{TOKEN}'

def get(endpoint, params=''):
    url = f'{BASE}/{endpoint}' + (f'?{params}' if params else '')
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

# 봇 정보
me = get('getMe')['result']
print(f"봇: @{me['username']} ({me['first_name']})")

# 미처리 업데이트
upd = get('getUpdates', 'limit=10&timeout=0')
msgs = upd.get('result', [])
print(f"미처리 메시지: {len(msgs)}개")
for u in msgs:
    msg = u.get('message', {})
    txt = msg.get('text') or msg.get('caption') or '(파일/기타)'
    frm = msg.get('from', {}).get('username', '알수없음')
    print(f"  [{u['update_id']}] @{frm}: {txt[:50]}")
