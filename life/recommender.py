import joblib
import pandas as pd
import os

class HousingRecommender:
    def __init__(self, model_path="housing_model.pkl", encoder_path="label_encoder.pkl"):
        self.model_path = model_path
        self.encoder_path = encoder_path
        self.model = None
        self.label_encoder = None
        self.load_model()

    def load_model(self):
        """저장된 XGBoost 모델과 라벨 인코더를 로드합니다."""
        if os.path.exists(self.model_path) and os.path.exists(self.encoder_path):
            self.model = joblib.load(self.model_path)
            self.label_encoder = joblib.load(self.encoder_path)
            print("저장된 모델과 인코더를 성공적으로 불러왔습니다.")
        else:
            print("오류: 저장된 모델이나 인코더를 찾을 수 없습니다. 먼저 학습을 진행해주세요.")

    def recommend(self, user_profile):
        """
        신규 사용자 정보를 받아 최적의 주거 형태를 추천합니다.
        user_profile: Feature들을 담고 있는 딕셔너리
        """
        if self.model is None or self.label_encoder is None:
            return "모델이 로드되지 않아 추천을 진행할 수 없습니다."

        # DataFrame으로 변환 (단일 샘플 예측)
        df = pd.DataFrame([user_profile])
        prediction_num = self.model.predict(df)
        
        # 예측된 숫자를 다시 사람이 읽을 수 있는 텍스트로 변환 (역변환)
        prediction_text = self.label_encoder.inverse_transform(prediction_num)
        return prediction_text[0]
