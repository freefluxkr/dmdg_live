import pandas as pd
import numpy as np
import pickle
try:
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, mean_squared_error
    from sklearn.preprocessing import LabelEncoder
except ImportError:
    print("scikit-learn 라이브러리가 설치되어 있지 않습니다. pip install scikit-learn 을 실행해주세요.")
    # Exit gracefully if missing
    import sys; sys.exit(0)

def train_model():
    file_path = r"c:\my_work\life\2024년 서울시 주거실태조사 마이크로데이터.CSV"
    print("마이크로데이터를 불러오는 중입니다...")
    
    try:
        df = pd.read_csv(file_path, encoding='cp949')
    except:
        df = pd.read_csv(file_path, encoding='utf-8')
    
    # 1. 사용할 특성(Features)과 타겟(Target - 만족도) 설정
    # 이 부분은 실제 데이터셋의 컬럼명에 맞게 조정이 필요합니다.
    # 여기서는 예시로 많이 쓰이는 공통 변수명 규칙을 가정하여 필터링합니다.
    
    # 타겟 변수 찾기 (만족도)
    target_candidates = [c for c in df.columns if '만족' in c]
    if not target_candidates:
        target_candidates = df.columns[-1:] # 찾지 못하면 마지막 컬럼을 임시 타겟으로 사용
    target_col = target_candidates[0]
    
    # 독립 변수 찾기 (예: 주택유형, 거주면적, 소득 등)
    # 실제 컬럼명이 복잡하므로 숫자형 데이터 위주로 선택합니다.
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # 타겟을 제외한 10개의 숫자형 피처 임의 선택 (결측치가 많은 컬럼 제외)
    features = [c for c in numeric_cols if c != target_col and df[c].isnull().sum() < len(df)*0.1][:10]
    
    print(f"선택된 타겟(만족도) 변수: {target_col}")
    print(f"선택된 피처 변수들: {features}")
    
    # 데이터 전처리 (결측치 제거)
    df_clean = df[features + [target_col]].dropna()
    
    if len(df_clean) < 100:
        print("결측치를 제거한 후 데이터가 너무 적어 모델 학습이 어렵습니다.")
        return
        
    X = df_clean[features]
    y = df_clean[target_col]
    
    # 타겟 변수가 범주형인지 연속형인지 판단
    is_classification = len(y.unique()) < 10
    
    # 학습/테스트 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("\n모델 학습을 시작합니다 (Random Forest)...")
    if is_classification:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        print(f"학습 완료! 분류 정확도(Accuracy): {acc:.2f}")
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)
        print(f"학습 완료! 회귀 평균제곱오차(MSE): {mse:.2f}")
        
    # 특성 중요도 출력
    importances = model.feature_importances_
    for name, imp in zip(features, importances):
        print(f" - {name}: {imp:.4f}")
        
    # 모델 저장
    model_save_path = "C:\\Users\\user\\Downloads\\DMDG_LIVE\\satisfaction_model.pkl"
    with open(model_save_path, 'wb') as f:
        pickle.dump({'model': model, 'features': features, 'target_col': target_col, 'is_classification': is_classification}, f)
    
    print(f"\n학습된 모델이 '{model_save_path}'에 저장되었습니다.")

if __name__ == "__main__":
    train_model()
