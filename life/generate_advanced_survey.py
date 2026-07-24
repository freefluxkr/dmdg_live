import pandas as pd
import numpy as np
import random

# ==============================================================
# [가중치 직접 설정 영역]
# 사용자가 각 항목별로 만족도에 미치는 가중치(영향력)를 직접 수정할 수 있습니다.
# (양수는 긍정적 영향, 음수는 부정적 영향을 의미)
# ==============================================================
CUSTOM_WEIGHTS = {
    'Area_Size': 0.15,         # 면적이 클수록 만족도 증가 (+15%)
    'House_Age': -0.10,        # 연식이 오래될수록 만족도 감소 (-10%)
    'Transport_Score': 0.20,   # 교통이 편리할수록 만족도 증가 (+20%)
    'Safety_Score': 0.25,      # 안전할수록 만족도 증가 (+25%)
    'Noise_Level': -0.15,      # 소음이 클수록 만족도 감소 (-15%)
    'Age_Impact': 0.05,        # 나이가 많을수록 약간 만족도 변동
}

# 범주형 변수의 점수 가산점 설정 (직업, 성별, 건축물유형 등)
CATEGORICAL_IMPACT = {
    'Gender': {'Male': 0, 'Female': 2},        # 여성이 보안/안전 등으로 인해 변동될 수 있는 기본 점수
    'Job': {'Office': 2, 'Freelance': -1, 'Student': 0, 'None': -3}, # 직업별 여유도/만족도 가산점
    'Building_Type': {'Apartment': 10, 'Villa': -2, 'Officetel': 2, 'House': 5} # 아파트 선호 현상 반영
}
# ==============================================================

def generate_custom_survey(num_records=5000):
    save_path = "C:\\Users\\user\\Downloads\\DMDG_LIVE\\life\\synthetic_survey_data_custom.csv"
    np.random.seed(42)
    random.seed(42)
    
    print(f"{num_records}개의 가상 주거실태조사 데이터 생성을 시작합니다 (사용자 정의 가중치 반영)...")
    
    # 1. 기본 숫자형 피처 생성
    df = pd.DataFrame()
    df['User_ID'] = [f"SYN_{i:04d}" for i in range(1, num_records + 1)]
    df['Area_Size'] = np.random.normal(loc=60, scale=20, size=num_records).clip(10, 200).round(1)
    df['House_Age'] = np.random.randint(0, 40, size=num_records)
    df['Transport_Score'] = np.random.randint(1, 101, size=num_records)
    df['Safety_Score'] = np.random.randint(1, 101, size=num_records)
    df['Noise_Level'] = np.random.randint(1, 101, size=num_records)
    df['Age'] = np.random.randint(19, 80, size=num_records)
    
    # 2. 범주형 피처 생성
    df['Gender'] = np.random.choice(['Male', 'Female'], size=num_records)
    df['Job'] = np.random.choice(['Office', 'Freelance', 'Student', 'None'], size=num_records, p=[0.5, 0.2, 0.2, 0.1])
    df['Building_Type'] = np.random.choice(['Apartment', 'Villa', 'Officetel', 'House'], size=num_records, p=[0.5, 0.3, 0.1, 0.1])
    
    # 3. 만족도 점수 계산 (가중치 적용)
    satisfaction = 50.0  # 기본 시작 점수
    
    # 숫자형 가중치 합산
    satisfaction += (df['Area_Size'] * CUSTOM_WEIGHTS['Area_Size'])
    satisfaction += (df['House_Age'] * CUSTOM_WEIGHTS['House_Age'])
    satisfaction += (df['Transport_Score'] * CUSTOM_WEIGHTS['Transport_Score'])
    satisfaction += (df['Safety_Score'] * CUSTOM_WEIGHTS['Safety_Score'])
    satisfaction += (df['Noise_Level'] * CUSTOM_WEIGHTS['Noise_Level'])
    satisfaction += (df['Age'] * CUSTOM_WEIGHTS['Age_Impact'])
    
    # 범주형 가산점 합산
    satisfaction += df['Gender'].map(CATEGORICAL_IMPACT['Gender'])
    satisfaction += df['Job'].map(CATEGORICAL_IMPACT['Job'])
    satisfaction += df['Building_Type'].map(CATEGORICAL_IMPACT['Building_Type'])
    
    # 노이즈 추가 및 클리핑 (0 ~ 100점 사이)
    satisfaction += np.random.normal(0, 5, num_records)
    df['Satisfaction_Score'] = np.clip(satisfaction, 0, 100).round(2)
    
    # ==============================================================
    # 4. 성별 및 개별 중요도에 따른 [고도화된 맞춤형 거주지 추천] 로직
    # ==============================================================
    recommendations = []
    
    for i in range(num_records):
        gender = df.loc[i, 'Gender']
        t_score = df.loc[i, 'Transport_Score']
        s_score = df.loc[i, 'Safety_Score']
        n_score = df.loc[i, 'Noise_Level']
        sat_score = df.loc[i, 'Satisfaction_Score']
        
        # 현재 만족도가 매우 높으면 유지
        if sat_score >= 85:
            rec = "현재 거주지 유지 권장 (만족도 최상)"
        else:
            # 교통, 치안, 소음(낮을수록 좋게 간주) 중 무엇을 가장 중요시/필요로 하는지 평가
            # 여기서는 점수가 가장 낮은(불만족스러운) 항목을 '개선이 시급한 최우선 고려사항'으로 가정
            scores = {'교통': t_score, '치안': s_score, '소음': (100 - n_score)} 
            top_priority = min(scores, key=scores.get) # 가장 점수가 낮은 항목 찾기
            
            if top_priority == '교통':
                if gender == 'Male':
                    rec = "[도심 역세권 오피스텔/빌라] - 출퇴근 시간 단축 극대화"
                else:
                    rec = "[역세권 대로변 대단지 아파트] - 교통편의와 야간 안전 동시 확보"
            elif top_priority == '치안':
                if gender == 'Female':
                    rec = "[보안 우수 신축 아파트 단지] - CCTV 및 자체 경비원 필수"
                else:
                    rec = "[치안 양호 주택가] - 방범창 및 기본 보안시설 완비 구역"
            else: # 소음 문제
                rec = "[외곽 숲세권 전원주택/빌라] - 도심 소음 회피 및 쾌적한 환경"
                
        recommendations.append(rec)
        
    df['Recommendation'] = recommendations
    
    # CSV 저장
    df.to_csv(save_path, index=False, encoding='utf-8-sig')
    print(f"\n{num_records}명의 가상 데이터가 성공적으로 생성되어 저장되었습니다!")
    print(f"저장 경로: {save_path}")

if __name__ == "__main__":
    generate_custom_survey(5000)
