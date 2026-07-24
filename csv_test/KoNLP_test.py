### pip install yfinance pandas matplotlib statsmodels nltk deep-translator ###
# 설치한 각 라이브러리에 대한 간단한 설명
"""
yfinance : 야후 파이낸스 데이터 수집기
           인터넷 브라우저로 야후 파이낸스 사이트에 들어가지 않고도, 코드 한 줄로 실시간 주가와 기업 뉴스를 가져오는 도구
pandas : 판다스 - 데이터 전처리 엔진
         파이썬 안에 강력한 '엑셀(Excel)' 처럼 사용할 수 있게 해주는 라이브러리
matplotlib : 맷플롯립 - 데이터 그리기 도구
             수집하고 가공한 데이터를 눈으로 볼 수 있는 차트나 그래프로 그려주는 라이브러리
statsmodels : 계량 통계 분석 도구
              주가 데이터 뒤에 숨겨진 추세, 계절성 등의 패턴을 수학적·통계적으로 쪼개서 분석해 주는 도구
nltk : 자연어 처리 패키지
       컴퓨터가 인간의 언어(특히 영어)를 알아듣고 분석할 수 있게 돕는 가장 역사 깊은 자연어 처리(NLP) 도구 상자
deep-translator : 초간편 번역기
                   파이썬에서 구글 번역, 파파고 등의 번역 엔진을 무료로 제한 없이 쓸 수 있게 해주는 편리한 번역 도구
"""

# 라이브러리 임포트
import datetime
import os
import platform
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# SentimentIntensityAnalyzer : 영어 문장이 가진 감정 점수 감별사
import pandas as pd
import yfinance as yf
from deep_translator import GoogleTranslator

### 한글 깨짐 방지 및 스타일 설정 (구글 코랩 및 다양한 OS 대응) ###
current_os = platform.system()
if current_os == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"
elif current_os == "Darwin":
    plt.rcParams["font.family"] = "AppleGothic"
else:
    # 리눅스/구글 코랩 환경 대응: 나눔고딕 설치 권장 및 기본 폰트 대체
    plt.rcParams["font.family"] = "DejaVu Sans"
    print("💡 리눅스/코랩 환경입니다. 한글 깨짐 방지를 위해 그래프 텍스트가 영어/기본 폰트로 설정됩니다.")

plt.rcParams["axes.unicode_minus"] = False
plt.style.use('seaborn-v0_8-darkgrid')  # 깔끔한 차트 스타일

### NLTK VADER 감성 사전 자동 다운로드 ###
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    print("📥 NLTK VADER 감성 사전 다운로드 중...")
    nltk.download("vader_lexicon", quiet=True)

### [데이터 수집] ###
# 야후 파이낸스에서 최근 1개월 주가와 최신 뉴스 데이터를 가져오는 함수.
def fetch_stock_and_news(ticker="NVDA"):
    print(f"📥 {ticker} 실시간 데이터 수집 중...")
    ticker_obj = yf.Ticker(ticker)

    # 1. 최근 1개월 영업일 기준 종가(Close) 가져오기
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=30)
    df = ticker_obj.history(start=start_date, end=today)

    # 2. 최신 뉴스 데이터 가져오기 (야후 파이낸스 제공)
    news_data = ticker_obj.news

    if df.empty:
        raise ValueError("주가 데이터를 가져오지 못했습니다.")
    if not news_data:
        print("⚠️ 관련 뉴스를 찾을 수 없습니다.")

    return df, news_data

### [데이터 분석] ###
# 한글 뉴스 헤드라인을 번역하고 감성 점수(-1 ~ +1)를 계산하는 함수.
def analyze_news_sentiment(news_data):
    print("⚙️ 뉴스 기사 번역 및 VADER 감성 분석(NLP) 시작 (JDK 불필요!)...")

    translator = GoogleTranslator(source="auto", target="en")  # 언어 자동 감지 -> 영어 번역
    sia = SentimentIntensityAnalyzer()
    analyzed_news = []

    for item in news_data:
        # 최신 yfinance 구조 대응: 뉴스 데이터가 'content' 서브 딕셔너리 내에 위치할 수 있습니다.
        content = item.get("content")
        if content and isinstance(content, dict):
            item_data = content
        else:
            item_data = item

        title = item_data.get("title", "")
        
        # UNIX 타임스탬프를 안전하게 가져와 날짜 형식(YYYY-MM-DD)으로 변환
        pub_time = item_data.get("providerPublishTime")
        if pub_time and pub_time > 0:
            pub_date = pd.to_datetime(pub_time, unit="s").date()
        else:
            # 타임스탬프가 없으면 문자열 날짜(pubDate) 파싱 시도, 둘 다 없으면 오늘 날짜 적용 (1970년 고정 오류 방지)
            pub_date_str = item_data.get("pubDate")
            if pub_date_str:
                try:
                    pub_date = pd.to_datetime(pub_date_str).date()
                except Exception:
                    pub_date = datetime.date.today()
            else:
                pub_date = datetime.date.today()

        # 1. 한글 ➡️ 영어 실시간 번역 (실패 시 원본 기사명 유지하여 감정 왜곡 최소화)
        try:
            translated_title = translator.translate(title)
            if not translated_title:
                translated_title = title
        except Exception:
            translated_title = title

        # 2. VADER 모델로 번역된 영어 감성 점수 계산 (compound score)
        sentiment_score = sia.polarity_scores(translated_title)["compound"]

        analyzed_news.append(
            {
                "Date": pd.to_datetime(pub_date),
                "Title": title,
                "Sentiment": sentiment_score,
            }
        )

    # 데이터프레임으로 변환 후 날짜별 평균 감성 점수 계산 (하루 여러 뉴스 대응)
    news_df = pd.DataFrame(analyzed_news)
    daily_sentiment = news_df.groupby("Date")["Sentiment"].mean().reset_index()

    return daily_sentiment, news_df

### [시각화]
# 주가 라인 차트 위에 뉴스 감성 분석 결과를 긍/부정 포인트로 표시하는 함수.
def plot_stock_with_sentiment(price_df, sentiment_df, ticker="NVDA"):
    print("🎨 주가 및 뉴스 감성 융합 차트 생성 중...")

    # [핵심 버그 수정] yfinance 주가 데이터의 인덱스 타임존(America/New_York) 제거
    price_df_clean = price_df.copy()
    if price_df_clean.index.tz is not None:
        price_df_clean.index = price_df_clean.index.tz_localize(None)

    # 2. 뉴스 데이터 복사 및 타임존 제거
    sentiment_df_clean = sentiment_df.copy()
    if sentiment_df_clean["Date"].dt.tz is not None:
        sentiment_df_clean["Date"] = sentiment_df_clean["Date"].dt.tz_localize(None)

    # 3. [핵심] 뉴스 날짜를 주가 거래일 중 가장 가까운 날짜로 매핑 (pd.merge_asof 활용)
    # asof 조인을 위해 두 데이터프레임 모두 날짜 기준으로 정렬
    price_df_clean = price_df_clean.sort_index()
    price_df_reset = price_df_clean.reset_index().rename(columns={"Date": "Price_Date", "index": "Price_Date"}) # 혹시 인덱스명이 Date일 때를 대비
    sentiment_df_clean = sentiment_df_clean.sort_values("Date")

    # direction="nearest"를 통해 주말이나 장 마감 후 뉴스를 가장 가까운 거래일 주가 날짜로 밀착 병합
    merged_df = pd.merge_asof(
        sentiment_df_clean,
        price_df_reset,
        left_on="Date",
        right_on="Price_Date",
        direction="nearest"
    )

    # 감성 점수 기준으로 긍정/부정/중립 데이터 분류
    positive = merged_df[merged_df["Sentiment"] > 0.1]
    negative = merged_df[merged_df["Sentiment"] < -0.1]
    neutral = merged_df[
        (merged_df["Sentiment"] >= -0.1) & (merged_df["Sentiment"] <= 0.1)
    ]

    fig, ax = plt.subplots(figsize=(14, 7))

    # OS별 차트 텍스트 한글/영문 분기 처리 (코랩/리눅스 한글 깨짐 원천 차단)
    if current_os in ["Windows", "Darwin"]:
        lbl_close = "종가 (Close)"
        lbl_pos = "호재 (긍정 뉴스)"
        lbl_neg = "악재 (부정 뉴스)"
        lbl_neu = "중립 뉴스"
        lbl_xlabel = "날짜"
        lbl_ylabel = "주가 (USD)"
        title_text = f"{ticker} 주가 추이 및 최신 뉴스 감성(Sentiment) 결합 분석"
    else:
        lbl_close = "Close"
        lbl_pos = "Positive News"
        lbl_neg = "Negative News"
        lbl_neu = "Neutral News"
        lbl_xlabel = "Date"
        lbl_ylabel = "Stock Price (USD)"
        title_text = f"{ticker} Stock Price and Sentiment Analysis of Latest News"

    # 1. 주가 선그래프
    ax.plot(
        price_df_clean.index,
        price_df_clean["Close"],
        color="black",
        label=lbl_close,
        alpha=0.6,
        lw=2,
    )

    # 2. 주가 위에 뉴스 발생 지점 포인트 찍기 (매핑된 Price_Date 좌표 기준)
    if not positive.empty:
        ax.scatter(
            positive["Price_Date"],
            positive["Close"],
            color="green",
            s=150,
            label=lbl_pos,
            edgecolors="black",
            zorder=5,
        )
    if not negative.empty:
        ax.scatter(
            negative["Price_Date"],
            negative["Close"],
            color="red",
            s=150,
            label=lbl_neg,
            edgecolors="black",
            zorder=5,
        )
    if not neutral.empty:
        ax.scatter(
            neutral["Price_Date"],
            neutral["Close"],
            color="gray",
            s=100,
            label=lbl_neu,
            edgecolors="black",
            zorder=5,
        )

    # 차트 스타일링 및 타이틀 설정
    ax.set_title(title_text, fontsize=16, fontweight="bold")
    ax.set_xlabel(lbl_xlabel)
    ax.set_ylabel(lbl_ylabel)
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
    print("✨ 분석 및 시각화 프로세스가 성공적으로 완료되었습니다!")


if __name__ == "__main__":
    print("==================================================")
    print("📈 주가-뉴스 감성 융합 분석 파이프라인 실제 구동 스크립트")
    print("==================================================\n")

    try:
        # 분석할 주식 티커 설정 (예: 엔비디아 'NVDA' 등)
        ticker_name = "NVDA"

        # 1. 데이터 수집
        stock_df, raw_news = fetch_stock_and_news(ticker_name)

        # 2. 감성 분석 수행 (번역 -> VADER)
        sentiment_summary, detailed_news = analyze_news_sentiment(raw_news)

        # 3. 분석 결과 요약 콘솔 출력
        print("\n📰 [최신 뉴스 감성 분석 요약 보고서]")
        print("-" * 80)
        print(f"{'날짜':<12} | {'감성':<6} | {'점수':<6} | {'뉴스 제목(헤드라인)'}")
        print("-" * 80)
        for idx, row in detailed_news.head(5).iterrows():
            sentiment_label = (
                "🟢 호재"
                if row["Sentiment"] > 0.1
                else ("🔴 악재" if row["Sentiment"] < -0.1 else "⚪ 중립")
            )
            print(
                f"{row['Date'].strftime('%Y-%m-%d'):<12} | {sentiment_label:<4} | {row['Sentiment']:.2f} | {row['Title']}"
            )
        print("-" * 80 + "\n")

        # 4. 결합 차트 시각화
        plot_stock_with_sentiment(stock_df, sentiment_summary, ticker_name)

    except Exception as e:
        print(f"❌ 프로세스 중 에러 발생: {e}")