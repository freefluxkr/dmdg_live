import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_naver_movies():
    url = "https://search.naver.com/search.naver?query=박스오피스"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        movie_list = []
        title_elements = soup.select(".name, .tit")
        
        for el in title_elements:
            title = el.text.strip()
            if title and len(title) > 1 and title not in ["더보기", "예매"]:
                if not any(m['영화 제목'] == title for m in movie_list):
                    movie_list.append({"순위": len(movie_list) + 1, "영화 제목": title, "출처": "네이버"})
        
        df = pd.DataFrame(movie_list[:10])
        
        return df if not df.empty else pd.DataFrame()
        
    except Exception as e:
        print(f"네이버 크롤링 에러: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    print(get_naver_movies())