import urllib.request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = "https://m-letter.or.kr/happy-contents/?category=I6d504u2k1"

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')
        a_tags = soup.find_all('a')
        print(f"Total a tags found: {len(a_tags)}")
        
        for i, a in enumerate(a_tags):
            href = a.get('href')
            text = a.get_text().strip()
            if href:
                if 'idx=' in href or 'bmode=' in href or 'category=' in href:
                    print(f"[{i}] text: {text} | href: {href}")
except Exception as e:
    print(f"Error: {e}")
