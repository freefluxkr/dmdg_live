import urllib.request, urllib.parse, json, os, time

TOKEN='8837085399:AAHDcjtBpBF04yiQTOukpmmSoXryRdtnQ0A'
CHAT_ID='8294524472'

def send_text(msg):
    data=urllib.parse.urlencode({'chat_id':CHAT_ID,'text':msg}).encode('utf-8')
    req=urllib.request.Request(f'https://api.telegram.org/bot{TOKEN}/sendMessage',data=data,method='POST')
    with urllib.request.urlopen(req,timeout=10) as r:
        return json.loads(r.read()).get('ok')

def send_photo(path, caption):
    boundary='----B7MA4'
    with open(path,'rb') as f:
        fd=f.read()
    parts = []
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n{CHAT_ID}\r\n')
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n')
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="photo"; filename="minjun.png"\r\nContent-Type: image/png\r\n\r\n')
    body = ''.join(parts).encode() + fd + f'\r\n--{boundary}--\r\n'.encode()
    req=urllib.request.Request(
        f'https://api.telegram.org/bot{TOKEN}/sendPhoto',
        data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read()).get('ok')
    except Exception as e:
        print(e)
        return False

path = r'c:\Users\user\Downloads\connect_dmdg\.agent\portraits\minjun.png'
caption = (
    "NEW MEMBER! 민준 (Minjun)\n"
    "직책: 비즈니스 어드바이저 / 독립 감사역\n\n"
    "사업을 냉철하게 평가하는 파트너.\n"
    "감정 없이 숫자와 논리로만 판단합니다.\n"
    "불편한 진실도 정확하게 말해주는 역할.\n\n"
    "핵심 스킬: 사업 타당성 / 재무 리스크 / 투자 심사 / 냉정한 피드백\n"
    "호출: @민준"
)
ok = send_photo(path, caption)
print('민준:', 'OK' if ok else 'FAIL')
time.sleep(1)

send_text(
    "17:30 마감 작업 완료 보고!\n\n"
    "완료 목록:\n"
    "✅ 전국 10개 도시 전체 활성화\n"
    "   (전주/강원/경주/안동/여수/수원/인천 추가)\n"
    "   도시별 음식5+문화5 = 100개 스팟 완성\n\n"
    "✅ 지도 핀 위치 한반도 기준 재보정\n\n"
    "✅ 신규 팀원 민준 합류\n"
    "   (냉철한 사업 평가 감사역)\n\n"
    "✅ Second Brain 스토리북 완성\n\n"
    "✅ 미소금융 창업 사업계획서 작성\n\n"
    "✅ 텔레그램 봇 v3.0 업그레이드\n\n"
    "✅ GitHub push 완료\n"
    "   github.com/freefluxkr/dmdg_global\n\n"
    "수고하셨습니다 사장님! 내일도 화이팅!"
)
print('최종 보고 OK')
