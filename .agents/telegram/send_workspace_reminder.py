import urllib.request, urllib.parse, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TOKEN = '8837085399:AAHDcjtBpBF04yiQTOukpmmSoXryRdtnQ0A'
CHAT_ID = '8294524472'

lines = [
    "🏡 [페기 올슨 비서 안내] 사장님! 자택 도착 즉시 수행 리마인더! 🍊",
    "",
    "집에 도착하셔서 컴퓨터를 켜시면 잊지 마시고 아래 2가지 작업을 차례대로 실행해 주세요!",
    "",
    "💻 1. git pull 실행",
    "   - 오늘 최종 완치된 1안/2안 프리미엄 PDF 빌더 파일 및 가이드라인을 싱크합니다.",
    "",
    "🧹 2. python clean_workspace.py 실행",
    "   - 최상위 루트에 난잡하게 널려 있던 60여 개의 빌더 스크립트와 캐시 폴더들이 3개의 그룹 폴더(00_Textbook_Builders, 00_HTML_Caches, 00_Textbooks)로 싹 분류되어 정돈됩니다.",
    "",
    "조심히 퇴근하세요!"
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
        if result.get('ok'):
            print('✓ [성공] 텔레그램으로 리마인더 DM 전송 완료!')
        else:
            print(str(result))
except Exception as e:
    print(str(e))
