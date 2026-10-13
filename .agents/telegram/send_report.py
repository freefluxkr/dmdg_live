import urllib.request, urllib.parse, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TOKEN = '8837085399:AAHDcjtBpBF04yiQTOukpmmSoXryRdtnQ0A'
CHAT_ID = '8294524472'

lines = [
    "📋 영숙 비서 보고 - 7가지 처리 완료!",
    "",
    "✅ 1. 사운드디렉터 현수 에이전트 신설",
    "   🎧 BGM·나레이션·SFX 전담",
    "",
    "✅ 2. 국적 → 9개 대륙으로 확장",
    "   동아시아/동남아/유럽/북미 등",
    "",
    "✅ 5. 배경 깨짐 버그 수정",
    "   도시별 그라디언트 폴백 적용",
    "",
    "✅ 6. 뒤로가기 버튼 추가",
    "   체험화면 좌상단 ← 지도로 버튼",
    "",
    "✅ 7. 벤치마킹 리포트 완성",
    "   Duolingo/Teuida/GatherTown 분석",
    "   KVJ 차별화 포인트 도출",
    "",
    "⏳ 3-4. 여정 플래닝 플로우 개선",
    "   (다음 작업 예정)",
    "",
    "모두 GitHub push 완료!",
    "http://localhost:8080/index.html 에서 확인하세요!"
]

msg = "\n".join(lines)
data = urllib.parse.urlencode({'chat_id': CHAT_ID, 'text': msg}).encode('utf-8')
req = urllib.request.Request(
    f'https://api.telegram.org/bot{TOKEN}/sendMessage',
    data=data, method='POST'
)
with urllib.request.urlopen(req, timeout=10) as r:
    result = json.loads(r.read())
    print('OK' if result.get('ok') else str(result))
