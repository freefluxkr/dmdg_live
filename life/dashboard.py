import streamlit as st
import pandas as pd
from recommender import HousingRecommender
import os

st.set_page_config(page_title="AI 주거 추천 시스템", page_icon="🏠", layout="wide")

# 모델 초기화 (캐싱하여 속도 최적화)
@st.cache_resource
def load_recommender():
    return HousingRecommender()

recommender = load_recommender()

st.title("🏠 AI 맞춤형 주거 추천 대시보드")
st.markdown("""
**XGBoost 알고리즘**을 활용하여 사용자의 조건(나이, 직업, 필요 인프라 등)에 가장 적합한 거주 형태와 지역을 분석해 드립니다.
좌측 사이드바에서 현재 스펙과 원하는 거주 조건을 설정해보세요!
""")

# 사이드바: 사용자 프로필 입력 영역
st.sidebar.header("👤 사용자 프로필 입력")

age = st.sidebar.slider("나이", min_value=19, max_value=80, value=30)
gender = st.sidebar.selectbox("성별", ["Male", "Female"])
job = st.sidebar.selectbox("직업군", ["Office", "Freelance", "Student", "None"])
building_type = st.sidebar.selectbox("선호 주거 형태", ["Apartment", "Villa", "Officetel", "House"])

st.sidebar.markdown("---")
st.sidebar.header("🏙️ 주거 환경 중요도 점수")
st.sidebar.caption("(0~100점, 숫자가 높을수록 해당 인프라가 잘 갖춰짐)")

area_size = st.sidebar.slider("원하는 면적 (평형 단위 기준 수치)", 10.0, 200.0, 60.0)
house_age = st.sidebar.slider("건물 연식 (년)", 0, 40, 5)
transport_score = st.sidebar.slider("교통 편의성 점수", 0, 100, 80)
safety_score = st.sidebar.slider("치안 안정성 점수", 0, 100, 90)
noise_level = st.sidebar.slider("소음 노출 정도 (낮을수록 좋음)", 0, 100, 30)

# 딕셔너리로 프로필 묶기
user_profile = {
    'Area_Size': area_size,
    'House_Age': house_age,
    'Transport_Score': transport_score,
    'Safety_Score': safety_score,
    'Noise_Level': noise_level,
    'Age': age,
    'Gender': gender,
    'Job': job,
    'Building_Type': building_type
}

st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("입력된 데이터 요약")
    st.json(user_profile)

with col2:
    st.subheader("✨ AI 추천 결과")
    
    # 모델 학습 여부 확인
    if not os.path.exists("housing_model.pkl") or not os.path.exists("label_encoder.pkl"):
        st.warning("⚠️ 학습된 모델 파일이 없습니다. `python main.py`를 실행하여 모델을 먼저 학습시켜주세요.")
    else:
        # 버튼을 눌러 결과 예측
        if st.button("내게 맞는 주거 환경 분석하기", type="primary"):
            with st.spinner("AI가 최적의 조건을 분석 중입니다..."):
                result = recommender.recommend(user_profile)
                
            st.success("분석이 완료되었습니다!")
            st.info(f"**추천 결과:**\n\n### {result}")
            
            st.markdown("""
            > **참고**: 이 추천 결과는 입력하신 프로필 데이터와 수만 건의 과거 가상 설문 기록을 
            > XGBoost가 학습하여 추론한 확률이 가장 높은 선택지입니다.
            """)
