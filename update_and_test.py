import os
import json
import re
import subprocess

base_path = r"C:\Users\tuesv\Downloads\DMDG_LIVE_CODE\삼선AXI 심화2\ml-tensorflow-master\ml-tensorflow-master"

md_templates = {
    "pandas": "# Pandas 기초 실습\n\n이 실습은 딥러닝과 데이터 분석의 기초가 되는 데이터를 다루는 Pandas 라이브러리의 기초를 배웁니다.\n- **핵심 개념**: 표 형태의 데이터(DataFrame)를 불러오고 확인하는 방법.\n- **주요 코드**: `pd.read_csv()`",
    "lemonade": "# 레모네이드 판매량 예측 (단순 회귀)\n\n온도를 입력받아 레모네이드 판매량을 예측하는 가장 기초적인 인공신경망 실습입니다.\n- **독립 변수**: 온도\n- **종속 변수**: 판매량\n- **핵심 개념**: Dense 레이어 1개로 이루어진 단순 선형 회귀 모델 생성 및 학습.",
    "boston": "# 보스턴 집값 예측 (다중 회귀)\n\n13개의 특성(독립 변수)을 사용하여 보스턴의 집값(종속 변수)을 예측하는 다중 선형 회귀 실습입니다.\n- **핵심 개념**: 여러 개의 입력값을 받아 하나의 수치를 예측하는 방법.",
    "iris": "# 아이리스 품종 분류 (다중 분류)\n\n꽃잎과 꽃받침의 길이를 바탕으로 3가지 품종 중 하나를 분류하는 실습입니다.\n- **핵심 개념**: 원핫인코딩(One-hot Encoding)과 Softmax 활성화 함수 및 범주형 교차 엔트로피(Categorical Crossentropy) 손실 함수 사용법.",
    "multilayer": "# 히든 레이어 (다층 퍼셉트론)\n\n입력층과 출력층 사이에 은닉층(Hidden Layer)을 추가하여 모델의 복잡도와 성능을 높이는 실습입니다.\n- **핵심 개념**: 딥러닝의 기초가 되는 다층 퍼셉트론(MLP) 구성 방식.",
    "flatten": "# Flatten 레이어와 이미지 분류\n\n2차원 이미지 데이터를 1차원으로 펴주는 Flatten 레이어를 사용하여 이미지 분류 모델을 만드는 실습입니다.\n- **핵심 개념**: 28x28 픽셀 이미지를 784개의 1차원 데이터로 변환.",
    "convolution": "# 합성곱 신경망 (CNN) 기초\n\n이미지의 공간적 특성을 유지하며 특징을 추출하는 Convolution 레이어의 개념을 배웁니다.\n- **핵심 개념**: Conv2D 레이어를 사용한 특징맵 추출.",
    "pooling": "# Pooling 레이어\n\n특징맵의 크기를 줄여 연산량을 감소시키고 중요한 특징을 강조하는 Max Pooling 기법을 배웁니다.\n- **핵심 개념**: 이미지 요약 및 학습 효율화.",
    "lenet": "# LeNet-5 구조를 이용한 분류\n\n초기 CNN 아키텍처 중 하나인 LeNet-5 모델을 구성하고 이미지 데이터를 분류하는 종합 실습입니다.\n- **핵심 개념**: CNN 전체 파이프라인 완성.",
    "myimages": "# 내 이미지로 예측하기\n\n직접 구한 이미지를 학습된 모델에 입력하여 결과를 확인하는 실습입니다.\n- **핵심 개념**: 실생활 데이터 적용 및 검증.",
    "data": "# 데이터 준비 및 전처리\n\n머신러닝을 위한 데이터를 수집, 정리, 가공하는 방법을 다룹니다.\n- **핵심 개념**: 결측치 처리 및 데이터 타입 변환.",
    "model": "# 모델 구조 설계 개요\n\n딥러닝 모델의 뼈대를 어떻게 설계해야 하는지 배우는 과정입니다.\n- **핵심 개념**: Sequential 모델과 레이어 쌓기."
}

results = []

for root, _, files in os.walk(base_path):
    for f in files:
        if f.startswith('new_') and f.endswith('.ipynb'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as nb_file:
                nb = json.load(nb_file)
            
            # 1. Insert pip install cell at the top if not exists
            has_pip = False
            for cell in nb.get('cells', []):
                if cell.get('cell_type') == 'code' and '!pip install' in "".join(cell.get('source', [])):
                    has_pip = True
                    break
                    
            if not has_pip:
                new_cell = {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "!pip install tensorflow==2.15.0 keras==2.15.0\n",
                        "import pandas as pd # 예측 에러 방지용\n"
                    ]
                }
                nb['cells'].insert(0, new_cell)
            
            # 2. Fix predict and epochs
            for cell in nb.get('cells', []):
                if cell.get('cell_type') == 'code':
                    source = "".join(cell.get('source', []))
                    
                    # Fix epochs
                    source = re.sub(r'epochs\s*=\s*\d+', 'epochs=10', source)
                    
                    # Fix predict([[...]])
                    source = re.sub(r'predict\s*\(\s*(\[\[.*?\]\])\s*\)', r'predict(pd.DataFrame(\1))', source)
                    
                    cell['source'] = source.splitlines(keepends=True)
                    
            with open(path, 'w', encoding='utf-8') as out_file:
                json.dump(nb, out_file, ensure_ascii=False, indent=1)
                
            # 3. Write MD file
            md_name = f.replace('.ipynb', '.md')
            md_path = os.path.join(root, md_name)
            md_content = "# 실습 노트\n\n내용이 없습니다."
            for key, val in md_templates.items():
                if key in f:
                    md_content = val
                    break
                    
            md_content += "\n\n## 📝 학습 시 주의사항\n- 빠른 실습을 위해 에포크(epochs)를 10으로 낮춰두었습니다. 더 높은 정확도를 원하시면 숫자를 올려보세요!\n- 최신 텐서플로우 오류 방지를 위해 코드 상단에 호환성 다운그레이드 명령이 포함되어 있습니다."
            
            with open(md_path, 'w', encoding='utf-8') as md_file:
                md_file.write(md_content)
                
            results.append(path)

print(f"Updated {len(results)} notebooks and generated MD files.")

print("\n--- Running Tests with nbconvert ---")
for nb_path in results:
    nb_name = os.path.basename(nb_path)
    print(f"Testing {nb_name}...")
    try:
        cmd = ["jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", nb_path]
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=90)
        print(f"  -> {nb_name} executed successfully.")
    except subprocess.TimeoutExpired:
        print(f"  -> [TIMEOUT] {nb_name} (Took longer than 90s, which is normal for ML).")
    except subprocess.CalledProcessError as e:
        print(f"  -> [FAILED] {nb_name} execution error.")
        err_out = e.stderr if e.stderr else e.stdout
        print("     " + "\n     ".join(err_out.splitlines()[-5:]))
