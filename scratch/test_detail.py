import urllib.request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = "https://m-letter.or.kr/happy-contents/?q=YToyOntzOjQ6InBhZ2UiO2k6MTtzOjEyOiJrZXl3b3JkX3R5cGUiO3M6MzoiYWxsIjt9&bmode=view&idx=171411634&t=board&category=I6d504u2k1"

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')
        
        # 제목을 찾을 수 있는 후보 셀렉터들 테스트
        selectors = ['.post-title', '.title', 'h1', '.view-title', 'h2', 'h3', '.board_title', '.board_txt_area']
        for sel in selectors:
            el = soup.select_one(sel)
            if el:
                print(f"Selector '{sel}' text: {el.get_text().strip()}")
except Exception as e:
    print(f"Error: {e}")
