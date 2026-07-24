import pandas as pd
import numpy as np

def analyze():
    file_path = r"c:\my_work\life\2024년 서울시 주거실태조사 마이크로데이터.CSV"
    print("데이터를 불러오는 중입니다 (약 32MB)...")
    
    try:
        df = pd.read_csv(file_path, encoding='cp949')
    except:
        df = pd.read_csv(file_path, encoding='utf-8')
        
    # 만족도 관련 컬럼 탐색
    satisfaction_cols = [c for c in df.columns if '만족' in c or '만족도' in c]
    if not satisfaction_cols:
        # '만족' 키워드가 없다면 주거환경 평가 관련 공통 질문을 찾습니다.
        # 서울시 주거실태조사에서는 보통 "현재 주택에 대한 만족도" 문항이 존재합니다.
        satisfaction_cols = [c for c in df.columns if '문' in c and ('주거' in c or '환경' in c) and ('평가' in c or '정도' in c)]
        
    print(f"\n[분석 결과] 데이터 형태: {df.shape[0]}행, {df.shape[1]}열")
    print(f"발견된 만족도 관련 문항(컬럼) 목록:")
    for col in satisfaction_cols:
        print(f" - {col}")
        
    # 첫 번째 만족도 관련 컬럼을 기준으로 분포 분석
    if satisfaction_cols:
        target_col = satisfaction_cols[0]
        print(f"\n[{target_col}] 컬럼의 요약 통계량:")
        # 숫자로 변환 가능한 경우 변환
        try:
            numeric_col = pd.to_numeric(df[target_col], errors='coerce')
            print(numeric_col.describe())
            
            # 만족도 % 환산 예시 (만약 1~4점 척도라면)
            # 1: 매우불만족, 2: 불만족, 3: 만족, 4: 매우만족 이라고 가정할 때 비율
            print("\n항목별 응답 비율(%):")
            print((numeric_col.value_counts(normalize=True).sort_index() * 100).round(2))
        except:
            print(df[target_col].value_counts())
    else:
        print("\n'만족' 이라는 키워드를 포함한 컬럼을 찾지 못했습니다. 컬럼 목록(columns.txt)을 수동으로 확인해 정확한 컬럼명을 모델 학습에 지정해야 합니다.")

if __name__ == "__main__":
    analyze()
