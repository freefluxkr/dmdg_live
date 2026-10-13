import urllib.request, urllib.parse, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TOKEN = '8837085399:AAHDcjtBpBF04yiQTOukpmmSoXryRdtnQ0A'
CHAT_ID = '8294524472'

lines = [
    "✅ [영숙 비서 보고] 사장님! 지시하신 K-Virtual Journey V2 핵심 기능 개편이 모두 완료되었습니다!",
    "",
    "🚀 1. 장바구니식 일정 담기 도입",
    "   이제 지도를 클릭해 방문하고 싶은 곳들을 모두 모은 뒤, [선택한 일정 여행 시작하기] 버튼을 통해 한 번에 여행을 떠납니다.",
    "",
    "🎯 2. Point & Click 핫스팟 시스템 (인천공항 테스트 적용)",
    "   단순 1:1 대화가 아니라 방탈출 게임처럼 안내데스크, 카페 등 화면 곳곳에 배치된 핫스팟 포인트(빨간 원)를 클릭하며 돌아다닐 수 있도록 구현했습니다.",
    "",
    "로컬 환경 (새로고침) 에서 바로 테스트해 보실 수 있습니다!"
]

msg = "\n".join(lines)
data = urllib.parse.urlencode({'chat_id': CHAT_ID, 'text': msg}).encode('utf-8')
req = urllib.request.Request(
    f'https://api.telegram.org/bot{TOKEN}/sendMessage',
    data=data, method='POST'
)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        result = json.loads(r.read())
        print('OK' if result.get('ok') else str(result))
except Exception as e:
    print(str(e))
