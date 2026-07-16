import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_daum_movies():
    url = "https://search.daum.net/search?w=tot&q=박스오피스"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        movie_list = []
        
        # [수정됨] 다음 영화 제목을 잡기 위한 '다중 그물망' 구조 
        # 클래스 이름이 조금이라도 바뀌어도 무조건 걸려들게 만듭니다.
        elements = soup.select(".c-title, .tit_main, .tit_item, a.tit, strong.tit, .p-title")

        for el in elements:
            title = el.text.strip()
            # 필요 없는 버튼이나 메뉴 이름 필터링
            if title and len(title) > 1 and title not in ["더보기", "예매", "상세보기", "박스오피스", "통합검색"]:
                if not any(m['영화 제목'] == title for m in movie_list):
                    movie_list.append({"순위": len(movie_list) + 1, "영화 제목": title, "출처": "다음"})

        df = pd.DataFrame(movie_list[:10])
        
        # 완벽하게 리턴합니다.
        return df if not df.empty else pd.DataFrame()
        
    except Exception as e:
        print(f"다음 크롤링 에러: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    print(get_daum_movies())