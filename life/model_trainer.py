import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

class ModelTrainer:
    def __init__(self, data_path, model_save_path="housing_model.pkl", encoder_save_path="label_encoder.pkl"):
        self.data_path = data_path
        self.model_save_path = model_save_path
        self.encoder_save_path = encoder_save_path
        self.model = None
        self.label_encoder = None

    def train_model(self):
        """데이터를 불러와 XGBoost 모델을 학습시키고 파일로 저장합니다."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"데이터 파일을 찾을 수 없습니다: {self.data_path}")

        print("데이터 로딩 중...")
        df = pd.read_csv(self.data_path)

        # 예측에 사용할 Feature와 Target 정의
        feature_cols = ['Area_Size', 'House_Age', 'Transport_Score', 'Safety_Score', 
                        'Noise_Level', 'Age', 'Gender', 'Job', 'Building_Type']
        target_col = 'Recommendation'

        X = df[feature_cols]
        y_raw = df[target_col]

        # XGBoost는 타겟값이 문자열이면 오류를 발생시키므로 LabelEncoding을 수행합니다.
        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(y_raw)

        # 범주형 및 수치형 컬럼 분리
        categorical_features = ['Gender', 'Job', 'Building_Type']
        numeric_features = ['Area_Size', 'House_Age', 'Transport_Score', 'Safety_Score', 'Noise_Level', 'Age']

        # 파이프라인 구축 (범주형은 OneHotEncoding 적용)
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', 'passthrough', numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ])

        # Random Forest 대신 고성능 XGBoost 모델로 교체
        self.model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', XGBClassifier(n_estimators=200, learning_rate=0.1, random_state=42, use_label_encoder=False, eval_metric='mlogloss'))
        ])

        print("XGBoost 모델 학습 시작...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

        accuracy = self.model.score(X_test, y_test)
        print(f"학습 완료! 검증 데이터 기반 정확도: {accuracy:.4f}")

        # 모델 및 라벨 인코더 저장
        joblib.dump(self.model, self.model_save_path)
        joblib.dump(self.label_encoder, self.encoder_save_path)
        print(f"모델과 인코더가 성공적으로 저장되었습니다.")
