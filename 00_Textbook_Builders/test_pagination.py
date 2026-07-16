import urllib.request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

detail_url = "https://m-letter.or.kr/happy-contents/?q=YToyOntzOjQ6InBhZ2UiO2k6MTtzOjEyOiJrZXl3b3JkX3R5cGUiO3M6MzoiYWxsIjt9&bmode=view&idx=171411634&t=board&category=I6d504u2k1"
print(f"🔗 상세 페이지 요청: {detail_url}")

try:
    req = urllib.request.Request(detail_url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        
        # 새로운 셀렉터 테스트
        selector = ".board_txt_area"
        content_area = soup.select_one(selector)
        
        if content_area:
            print(f"✅ 셀렉터 '{selector}' 매칭 성공!")
            # 이미지 태그 제거
            for img in content_area.find_all('img'):
                img.decompose()
            # 줄바꿈 포함 텍스트 추출
            text = content_area.get_text().strip()
            print(f"✅ 본문 길이: {len(text)}자")
            print("--- 본문 내용 미리보기 ---")
            print(text[:300])
            print("-------------------------")
        else:
            print(f"❌ 셀렉터 '{selector}' 매칭 실패")
            
except Exception as e:
    print(f"❌ 에러 발생: {e}")
