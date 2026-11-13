import json
import ssl
import time
import urllib.request

TOKEN = "a85dcdacf7b3a2a9966ae3bef8fd4e5af3aecd5b"
BASE_URL = "https://wikidocs.net/napi"
HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Content-Type": "application/json",
}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

posts = [
    {
        "title": "[말쌈 단행본 1권 샘플] 1990 삐삐에서 2026 릴스까지, 대한민국 신조어 연대기 200 (K-상황극 포함)",
        "tags": "말쌈,신조어,한국어,상황극,K컬처,DMDG",
        "file": r"c:\DMDG_Jobs\DMDG_PRJ\dmdg_live_dot_com\malssam\BOOK1_신조어_샘플챕터_20261113.md",
    },
    {
        "title": "[말쌈 단행본 2권 샘플] 영어엔 없는 한국인의 마음: 눈치부터 정(情)까지 K-소울 118 (크로스컬처 상황극 포함)",
        "tags": "말쌈,K정서,번역불가한국어,눈치,정,DMDG",
        "file": r"c:\DMDG_Jobs\DMDG_PRJ\dmdg_live_dot_com\malssam\BOOK2_K정서_샘플챕터_20261113.md",
    },
]

for p in posts:
    with open(p["file"], "r", encoding="utf-8") as f:
        content = f.read()

    req1 = urllib.request.Request(f"{BASE_URL}/blog/create/", data=b"{}", headers=HEADERS, method="POST")
    with urllib.request.urlopen(req1, context=ctx) as resp:
        blog_id = json.loads(resp.read().decode("utf-8"))["id"]

    payload = {
        "title": p["title"],
        "content": content,
        "is_public": True,
        "tags": p["tags"],
    }
    req2 = urllib.request.Request(
        f"{BASE_URL}/blog/{blog_id}/",
        data=json.dumps(payload).encode("utf-8"),
        headers=HEADERS,
        method="PUT",
    )
    with urllib.request.urlopen(req2, context=ctx) as resp:
        json.loads(resp.read().decode("utf-8"))
        print(f"PUBLISHED: {p['title']}")
        print(f"  -> https://dmdg.wikidocs.net/blog/{blog_id}/")
        print(f"  -> https://wikidocs.net/blog/@dmdg/{blog_id}/")
    time.sleep(1)

