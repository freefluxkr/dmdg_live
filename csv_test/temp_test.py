import os
import datetime
import pandas as pd
import yfinance as yf
import xml.etree.ElementTree as ET
import urllib.request
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import platform
from deep_translator import GoogleTranslator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon', quiet=True)

current_os = platform.system()

KOREAN_TICKERS = {
    "005930.KS": "삼성전자",
    "000660.KS": "SK하이닉스",
    "005380.KS": "현대자동차",
}

def fetch_stock_and_news(ticker="005930.KS"):
    print(f"📥 {ticker} 데이터 수집...")
    ticker_obj = yf.Ticker(ticker)
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=365)
    df = ticker_obj.history(start=start_date, end=today)

    if df.empty:
        raise ValueError("주가 로드 실패")

    ticker_clean = ticker.split('.')[0]
    news_data = []
    
    if ticker_clean.isdigit():
        stock_name = KOREAN_TICKERS.get(ticker, "국내주식")
        print(f"🔍 국내 종목 감지: {stock_name}")
        headers = {"User-Agent": "Mozilla/5.0"}
        one_year_ago = today - datetime.timedelta(days=365)
        page = 1
        stop_crawling = False
        raw_collected = []
        
        while not stop_crawling and page <= 5: # 검증을 위해 빠르게 5페이지까지만 크롤링
            url = f"https://finance.naver.com/item/news_news.naver?code={ticker_clean}&page={page}"
            req = urllib.request.Request(url, headers=headers)
            try:
                html = urllib.request.urlopen(req).read()
                soup = BeautifulSoup(html, 'html.parser')
                titles = soup.select('.title a')
                dates = soup.select('.date')
                
                if not titles:
                    break
                    
                for t, d in zip(titles, dates):
                    title = t.text.strip()
                    date_str = d.text.strip()
                    pub_date = pd.to_datetime(date_str.split()[0], format="%Y.%m.%d").date()
                    
                    if pub_date < one_year_ago:
                        stop_crawling = True
                        break
                        
                    raw_collected.append({
                        "title": title,
                        "pubDate": pub_date.strftime("%Y-%m-%d")
                    })
                page += 1
            except Exception as e:
                print(f"크롤링 에러: {e}")
                break
        
        temp_df = pd.DataFrame(raw_collected)
        if not temp_df.empty:
            temp_df = temp_df.drop_duplicates(subset=["pubDate"], keep="first")
            news_data = temp_df.to_dict(orient="records")
            
    return df, news_data

def analyze_news_sentiment(news_data):
    print("⚙️ VADER 감성 분석 시작...")
    if not news_data:
        return pd.DataFrame(columns=["Date", "Sentiment"]), pd.DataFrame(columns=["Date", "Title", "Sentiment"])

    translator = GoogleTranslator(source="auto", target="en")
    sia = SentimentIntensityAnalyzer()
    analyzed_news = []

    for item in news_data[:10]: # 검증을 위해 최대 10개만 샘플 번역 실행
        title = item.get("title", "")
        pub_date_str = item.get("pubDate")
        pub_date = pd.to_datetime(pub_date_str).date() if pub_date_str else datetime.date.today()

        try:
            translated_title = translator.translate(title)
            if not translated_title:
                translated_title = title
        except Exception:
            translated_title = title

        sentiment_score = sia.polarity_scores(translated_title)["compound"]
        analyzed_news.append({
            "Date": pd.to_datetime(pub_date),
            "Title": title,
            "Sentiment": sentiment_score,
        })

    news_df = pd.DataFrame(analyzed_news)
    daily_sentiment = news_df.groupby("Date")["Sentiment"].mean().reset_index()
    return daily_sentiment, news_df

def plot_stock_with_sentiment(price_df, sentiment_df, ticker="NVDA"):
    print("🎨 차트 이미지 저장 검증...")
    price_df_clean = price_df.copy()
    if price_df_clean.index.tz is not None:
        price_df_clean.index = price_df_clean.index.tz_localize(None)

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(price_df_clean.index, price_df_clean["Close"], color="black", alpha=0.6)
    
    # 임시 검증 차트 저장
    plt.savefig("csv_test/temp_validation_chart.png")
    print("✓ 차트 저장 완료!")

if __name__ == "__main__":
    df, news = fetch_stock_and_news("005930.KS")
    print(f"수집된 뉴스 개수: {len(news)}")
    if news:
        print(f"첫번째 뉴스 샘플: {news[0]}")
    summary, detailed = analyze_news_sentiment(news)
    print(f"요약 데이터 크기: {summary.shape}")
    plot_stock_with_sentiment(df, summary, "005930.KS")
    print("✨ 검증 스크립트 실행 완료!")
