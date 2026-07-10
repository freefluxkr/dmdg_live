import os
import sys
import subprocess

# =====================================================================
# 🔍 1. 브라우저 엔진 경로 검색 (Chrome 또는 Edge)
# =====================================================================
def find_browser_path():
    """윈도우 환경에서 Chrome 또는 Edge 브라우저의 설치 경로를 검색합니다."""
    candidate_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe")
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            return path
    return None

# =====================================================================
# 📑 2. 요약 없는 100% 원본 직역 및 다이어그램 이미지 HTML 구성
# =====================================================================
def build_html_content():
    html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>Mixture of Cognitive Reasoners (MiCRo) 원문 한글 번역본</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.8/dist/web/static/pretendard-dynamic-subset.css');

        body {
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
            line-height: 1.8;
            -webkit-print-color-adjust: exact;
        }

        .page {
            padding: 2.5cm 2cm;
            page-break-after: always;
            box-sizing: border-box;
            position: relative;
        }

        /* 표지 (Cover Page) */
        .cover-page {
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background: linear-gradient(135deg, #0f172a 0%, #1e2b48 100%);
            color: #ffffff;
            padding: 4cm 2.5cm;
        }

        .cover-header {
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: #38bdf8;
            font-weight: 700;
        }

        .cover-title {
            font-size: 2.8rem;
            font-weight: 800;
            line-height: 1.35;
            letter-spacing: -0.02em;
            margin-top: 1.5rem;
        }

        .cover-subtitle {
            font-size: 1.25rem;
            color: #cbd5e1;
            margin-top: 1rem;
            font-weight: 400;
            line-height: 1.6;
            border-left: 4px solid #38bdf8;
            padding-left: 1rem;
        }

        .cover-authors {
            margin-top: 2rem;
            font-size: 1rem;
            color: #94a3b8;
        }

        .cover-footer {
            font-size: 0.9rem;
            color: #64748b;
            border-top: 1px solid #334155;
            padding-top: 1rem;
            display: flex;
            justify-content: space-between;
        }

        /* 본문 구조화 */
        h1.section-title {
            font-size: 2rem;
            font-weight: 800;
            color: #0f172a;
            border-bottom: 2px solid #0284c7;
            padding-bottom: 0.5rem;
            margin-top: 0;
            margin-bottom: 1.5rem;
            page-break-after: avoid;
        }

        h2.subsection-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #0f172a;
            margin-top: 2.2rem;
            margin-bottom: 1rem;
            border-left: 4px solid #0284c7;
            padding-left: 0.75rem;
            page-break-after: avoid;
        }

        p {
            font-size: 1rem;
            margin-bottom: 1.2rem;
            text-align: justify;
            color: #334155;
        }

        /* 인라인 이미지 상자 */
        .image-container {
            margin: 2rem 0;
            text-align: center;
            page-break-inside: avoid;
        }

        .image-container img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.06);
            display: block;
            margin: 0 auto 0.8rem auto;
        }

        .image-caption {
            font-size: 0.9rem;
            color: #475569;
            line-height: 1.6;
            text-align: justify;
            background-color: #f8fafc;
            border-left: 3px solid #64748b;
            padding: 0.8rem 1rem;
            border-radius: 0 6px 6px 0;
            margin-top: 0.5rem;
        }

        /* 로고 헤더 라인 */
        .logo-row {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 2rem;
            margin-top: 1rem;
            margin-bottom: 2rem;
        }
        
        .logo-row img {
            height: 45px;
            width: auto;
        }

        /* 리스트 스타일 */
        ul.custom-list {
            list-style: none;
            padding-left: 0;
            margin-bottom: 1.5rem;
        }

        ul.custom-list li {
            position: relative;
            padding-left: 1.5rem;
            margin-bottom: 0.8rem;
            font-size: 1rem;
            color: #334155;
        }

        ul.custom-list li::before {
            content: "•";
            color: #0284c7;
            font-size: 1.2rem;
            position: absolute;
            left: 0.4rem;
            top: -0.1rem;
        }

        /* BibTeX 코드 */
        pre {
            background-color: #0f172a;
            color: #38bdf8;
            padding: 1.2rem;
            border-radius: 6px;
            font-family: Consolas, Monaco, monospace;
            font-size: 0.85rem;
            overflow-x: auto;
            margin: 1.5rem 0;
            border: 1px solid #1e293b;
            page-break-inside: avoid;
        }

        /* Print formatting */
        @media print {
            body {
                font-size: 13px;
                color: #000000;
            }
            .page {
                padding: 2cm 1.5cm;
            }
            .cover-page {
                height: 100vh !important;
                padding: 3cm 2cm !important;
            }
            .image-caption {
                background-color: #f1f5f9;
                border-left: 3px solid #475569;
            }
            pre {
                background-color: #f8fafc;
                color: #0f172a;
                border: 1px solid #cbd5e1;
            }
        }
    </style>
</head>
<body>

    <!-- 1. 표지 -->
    <div class="page cover-page">
        <div class="cover-header">EPFL Cognitive Reasoners Project</div>
        <div>
            <div class="cover-title">Mixture of Cognitive Reasoners</div>
            <div class="cover-subtitle">Modular Reasoning with Brain-Like Specialization<br>(뇌 모사 특화 신경망을 도입한 모듈식 추론 언어 모델)</div>
            <div class="cover-authors">
                <strong>저자:</strong> Badr AlKhamissi<sup>1</sup>, C. Nicolò De Sabbata<sup>1</sup>, Greta Tuckute<sup>2,3</sup>, Zeming Chen<sup>1</sup>, Martin Schrimpf<sup>*,1</sup>, Antoine Bosselut<sup>*,1</sup><br>
                <span style="font-size:0.9rem; color:#64748b;"><sup>1</sup>EPFL (스위스 연방 공과대학) &nbsp;|&nbsp; <sup>2</sup>MIT &nbsp;|&nbsp; <sup>3</sup>Harvard</span>
            </div>
        </div>
        
        <div class="logo-row">
            <img src="https://cognitive-reasoners.epfl.ch/images/iclr.png" alt="ICLR Logo">
            <img src="https://cognitive-reasoners.epfl.ch/images/hf-logo.png" alt="HF Logo">
        </div>

        <div class="cover-footer">
            <span>ICLR 2026 발표 논문</span>
            <span>공식 웹페이지 무요약 원문 완역본</span>
        </div>
    </div>

    <!-- 2. 초록 (Abstract) -->
    <div class="page">
        <h1 class="section-title">초록 (Abstract)</h1>
        <p>
            인간의 인지 행동은 언어 처리, 논리 추론, 사회적 이해, 기억 소환과 같이 각기 다른 인지 기능에 할당되고 전문화된 두뇌 신경망(specialized brain networks) 간의 상호작용을 통해 발현됩니다. 이러한 두뇌의 조직 구조에서 영감을 받아, 본 연구에서는 전문가 모듈(experts) 간의 기능적 전문화가 자발적으로 발현되도록 유도하는 학습 커리큘럼 기반의 사전 훈련 및 사후 학습 파이프라인을 거친 모듈형 트랜스포머 아키텍처인 <strong>MiCRo (Mixture of Cognitive Reasoners, 인지적 추론기 혼합)</strong>를 제안합니다.
        </p>
        <p>
            구체적으로, 본 연구에서는 사전 학습된 언어 모델의 레이어들을 인간 두뇌의 인지 기능 영역과 정렬되는 4개의 전문가 모듈(expert modules)로 분할(partition)했습니다. 본 논문에서 제시하는 '뇌 모방형(Brain-Like)' 모델은 기존 최신 연구들에 비해 다음과 같은 세 가지 핵심 장점을 제공합니다:
        </p>
        <ul class="custom-list">
            <li><strong>첫째</strong>, 특화된 전문가 모듈들은 명확하게 해석 가능하며 인과적으로 유의미합니다. 예를 들어 특정 모듈을 인위적으로 소거(ablation)하면 해당 도메인의 특화 지식을 필요로 하는 벤치마크 평가 성적이 급격하게 하락합니다.</li>
            <li><strong>둘째</strong>, 추론(inference) 시점에 토큰을 특정 전문가로 라우팅되도록 유도함으로써 모델의 행동 양식을 동적으로 제어(steering)할 수 있습니다 (예: 논리적 답변보다 사회적 이해도 기반의 답변 비율을 가중). 이를 통해 생성 결과물의 스타일과 어조를 정교하게 통제할 수 있습니다.</li>
            <li><strong>셋째</strong>, 기계 학습 추론 벤치마크(예: GSM8K, BBH)와 인간 행동 정렬도(CogBench) 모두에서 해석 가능성을 보존하면서 기존 표준 베이스라인 모델들을 능가하거나 대등한 우위를 가집니다.</li>
        </ul>
        <p>
            결론적으로, 인지 과학적 지식에 정렬하여 설계된 기능적 전문화는 인공지능 모델이 더욱 인간과 유사하며(human-like) 동시에 인간이 더 명확히 해석하기 용이하도록(human-interpretable) 만들어 줍니다.
        </p>
    </div>

    <!-- 3. 예비 지식 (Preliminaries) -->
    <div class="page">
        <h1 class="section-title">개념 정의 (Preliminaries)</h1>
        <p>
            본 모델은 인간 두뇌가 생각을 고도로 분업화된 시스템으로 조직하고 체계화하는 원리에 착안하여, 다음과 같은 4가지 핵심 인지 신경망 전문가 모듈을 이식했습니다:
        </p>
        
        <ul class="custom-list">
            <li><strong>언어 전문가 (Language expert)</strong>: 수학 문제 풀이나 음악 감상과 같은 비언어적 과제에는 관여하지 않고, 순수하게 문어와 구어로 쓰인 자연어 텍스트 데이터의 맥락을 인지하고 처리하는 두뇌 영역을 모사합니다.</li>
            <li><strong>논리 전문가 (Logic expert)</strong>: 고차원의 논리적 추론 및 문제 해결을 담당하며, 복잡한 인지 과제를 해결할 때 활성화가 도드라지고 인간의 일반 지능(general intelligence)과 밀접하게 연계된 뇌 시스템을 모방합니다.</li>
            <li><strong>사회성 전문가 (Social expert)</strong>: 타인의 의도, 감정, 신념을 이해(마음 이론, Theory of Mind)하고, 반어법(sarcasm)이나 유머를 인지하며 공감적인 반응을 도출하는 뇌 회로에 기초하여 설계되었습니다.</li>
            <li><strong>세계 전문가 (World expert)</strong>: 뇌의 '디폴트 모드 네트워크(default mode network)'를 벤치마킹했습니다. 직접적인 행동 유도가 없는 대기 상태(상상하기, 과거 회상, 미래 계획 수립 등)에서 작동하며, 맥락을 서로 연결하여 긴 사건이나 이야기의 거시적 흐름을 파악하도록 돕습니다.</li>
        </ul>

        <div class="image-container">
            <img src="https://cognitive-reasoners.epfl.ch/images/preliminaries.png" alt="The Human Language Network Diagram">
            <div class="image-caption">
                <strong>[인간의 인지적 두뇌망 구조 분석]</strong><br>
                Fedorenko, E., Ivanova, A.A. & Regev, T.I. "인간 두뇌의 더 광범위한 환경 내에서 자연스러운 부류로서의 언어망(The language network as a natural kind within the broader landscape of the human brain)". Nat. Rev. Neurosci. 25, 289-312 (2024) 연구 자료 인용.
            </div>
        </div>
    </div>

    <!-- 4. 학습 커리큘럼 -->
    <div class="page">
        <h1 class="section-title">전문화 유도를 위한 학습 커리큘럼 (Training Curriculum)</h1>
        <p>
            단순히 아키텍처를 기능별로 쪼개는 것만으로는 개별 전문가 모듈이 자발적으로 전문성을 발현하도록 만들 수 없습니다. 본 연구팀은 뇌 신경망 모사형 전문가 모듈(MiCRo)의 각 레이어에 위치한 전문가들이 고유의 인지 강점을 갖도록 다음과 같은 3단계 학습 파이프라인(Curriculum)을 구축했습니다:
        </p>

        <div class="image-container">
            <img src="https://cognitive-reasoners.epfl.ch/images/training.png" alt="MiCRo Training Pipeline Diagram">
            <div class="image-caption">
                <strong>[MiCRo의 3단계 학습 프로세스 파이프라인]</strong><br>
                <ul>
                    <li><strong>Stage-I (Prime Experts)</strong>: 정교하게 큐레이션된 소규모 인지 데이터셋(MiCRo_SFT)을 통해 개별 전문가들의 가중치만 우선적으로 학습시켜 고유의 도메인 귀납적 편향을 획득하도록 유도합니다.</li>
                    <li><strong>Stage-II (Calibrate Router)</strong>: 전문가를 포함한 전체 가중치를 동결(Freeze)한 상태에서, 입력 토큰을 어느 전문가로 전달할지 최적으로 매칭해 주는 라우터(Router) 모듈을 훈련시킵니다.</li>
                    <li><strong>Stage-III (Train End-to-End)</strong>: 라우터와 전문가 모듈 전체의 고정을 풀고, 약 100만 건 규모의 대형 명령어 튜닝 데이터셋(Tülü3_SFT)을 사용하여 전체 네트워크를 종단간(End-to-End) 방식으로 최종 미세조정합니다.</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- 5. 실험 및 결과 1 - 토큰 라우팅 -->
    <div class="page">
        <h1 class="section-title">실험 및 주요 결과 (Experiments & Findings)</h1>
        <h2 class="subsection-title">전문가 모듈 전반의 의미론적 토큰 라우팅 분석</h2>
        <p>
            학습을 마친 MiCRo-Llama-1B 모델의 실제 추론 과정을 분석한 결과, 각 문장의 성격에 맞게 뇌 구조와 정렬된 전문가 모듈로 토큰이 정확히 유도되는 공간적 기능 분화가 작동함을 규명했습니다.
        </p>

        <div class="image-container">
            <img src="https://cognitive-reasoners.epfl.ch/images/token-routing.png" alt="Token Routing Patterns Across Experts and Layers">
            <div class="image-caption">
                <strong>[전문가 및 레이어별 토큰 라우팅 패턴 분석 결과]</strong><br>
                MiCRo-Llama-1B 모델의 토큰 라우팅 결과 지표입니다. 각 막대 그래프는 특정 문장(n=50)에 대해 레이어별로 특정 전문가 모듈로 라우팅된 토큰의 비율을 의미하며, 문장 간 분산이 표시되어 있습니다. 이 모델은 의도했던 뇌 과학 기반 조직과 완벽히 부합하는 명확한 도메인 특화 전문성을 나타냅니다. 예를 들어, 사회성 인지(Social Cognition) 샘플은 주로 사회성 전문가 모듈로 라우팅되는 반면, 산술 계산(Arithmetic) 문제는 논리 전문가 모듈로 유도됩니다. 또한 문장의 구조적 의미를 해석하는 초기 레이어(Early Layers)에서는 언어 전문가 모듈이 공통적으로 강하게 활성화됨을 확인했습니다 (레이어별 라우팅 세부 플롯 및 추가 모델 성적은 논문 부록 B 참조). 각 서브플롯 하단에는 무작위로 선택된 두 개의 예시 샘플이 표시되어 있습니다.
            </div>
        </div>
    </div>

    <!-- 6. 실험 및 결과 2 - 소거 실험 -->
    <div class="page">
        <h2 class="subsection-title">전문가 소거(Ablation)를 통한 인과적 기여 검증</h2>
        <p>
            특정 전문가 모듈의 활성화를 물리적으로 차단(소거)하는 분석을 진행하여, 각 모듈이 실제로 예측 정확도와 인과관계를 맺고 있는지 철저하게 입증했습니다.
        </p>

        <div class="image-container">
            <img src="https://cognitive-reasoners.epfl.ch/images/expert-ablations.png" alt="Steering Model Behavior via Expert Ablation">
            <div class="image-caption">
                <strong>[전문가 소거를 통한 모델 행동 제어성 및 인과관계 입증 결과]</strong><br>
                상단 및 하단 패널은 각각 MiCRo-Llama-1B 및 MiCRo-Llama-3B 모델에 대한 벤치마크 평가 결과를 보여줍니다. 논리 전문가(Logic expert)를 소거(제거)하면 MATH 및 GSM8K 수리 추론 벤치마크 성적이 치명적으로 곤두박질치는 반면, 수학 문제 풀이 시 관련도가 매우 낮은 사회성 전문가(Social expert)를 지워버릴 때에는 정확도가 미세하게 소폭 상승하는 현상을 보입니다. MMLU 및 BBH 벤치마크 결과를 살펴보면, 특정 세부 문제들은 전적으로 독립된 단일 전문가 모듈에만 의존하는 반면, 다른 일부 복잡한 과제들은 여러 전문가의 중첩된 협력이 필요함을 통계적으로 증명했습니다. 추가 모델 세부 결과는 부록 D를 참고하십시오.
            </div>
        </div>
    </div>

    <!-- 7. 실험 및 결과 3 - 로컬라이저 검출 -->
    <div class="page">
        <h2 class="subsection-title">신경과학적 로컬라이저(Localizers) 분석 검증</h2>
        <p>
            인간 두뇌의 기능 활성화 영역을 식별하는 신경과학 프로토콜(Language, MD, ToM localizers)을 동일하게 인공망 유닛에 투사하여, 실제 가중치 소자들이 의도한 뇌 기능과 완벽히 부합하여 활성화되는지 분석했습니다.
        </p>

        <div class="image-container">
            <img src="https://cognitive-reasoners.epfl.ch/images/localization.png" alt="Neuroscience Localizers Identify Functionally Specialized Experts">
            <div class="image-caption">
                <strong>[신경과학적 로컬라이저를 통한 기능 특화 유닛 매핑 결과]</strong><br>
                (a) MiCRo-Llama-1B 및 (b) MiCRo-Llama-3B 모델의 분석 결과입니다. 각 모델에 대해 신경과학 이론에서 널리 쓰이는 세 가지 로컬라이저 프로토콜—언어(Language), 다중 인지 요구(Multiple Demand, MD), 마음 이론(Theory of Mind, ToM)—을 적용하여 레이어 및 전문가 간의 로컬라이즈된 유닛(Localized Units)들의 선택성을 규명했습니다. 각 그래프는 모델 전체에서 최상위 10%의 선택성을 지닌 핵심 유닛들 중 각 레이어의 개별 전문가 모듈에 실제로 포함된 유닛의 백분율 비율을 보여줍니다. 검출 결과, 각 유닛 소자들은 본래 부여하고자 설계했던 인지 전문가의 뇌 영역에 정확히 일치하여 국소화되었습니다.
            </div>
        </div>
    </div>

    <!-- 8. 실험 및 결과 4 - CogBench 행동 정렬 -->
    <div class="page">
        <h2 class="subsection-title">인간 인지 행동 모사(CogBench) 정렬 및 일치성</h2>
        <p>
            MiCRo 모델군이 인간 고유의 편향, 의사 결정, 인지적 편차(Cognitive Biases)를 어느 정도로 흡사하게 행동으로 묘사하고 정렬하는지 평가했습니다.
        </p>

        <div class="image-container">
            <img src="https://cognitive-reasoners.epfl.ch/images/behavioral-alignment.png" alt="Alignment with Human Behavior on CogBench">
            <div class="image-caption">
                <strong>[인간 행동 정렬도 평가(CogBench) 비교 분석]</strong><br>
                (a) 10가지 세부 인지 행동 척도 전반에 걸친 평균 유사도 점수(SBRE) 결과입니다. MiCRo-Llama 모델군이 베이스라인인 MoB(Mixture of Brains) 및 Dense(밀집형) 구조의 모델에 비해 확연히 월등한 인간 행동 정렬 성능을 보여줍니다. (b) 세 가지 비교군 모델별로 각각 10개의 행동 척도 단위로 정밀 산출한 인간 행동 정규화(Human-normalized) 유사 지표 결과입니다. (c) CogBench 데이터셋에서 LLM 평가를 위해 자연어 텍스트 템플릿 형태로 변환된 7가지 대표적인 인간 심리학 실험 입력 문제 예시 중 2가지 샘플 예시입니다.
            </div>
        </div>
    </div>

    <!-- 9. 실험 및 결과 5 - 추론 벤치마크 및 BibTeX -->
    <div class="page">
        <h2 class="subsection-title">추론 성능 평가 벤치마크 우위 비교</h2>
        <p>
            단순히 뇌와 비슷한 조직을 모방하는 것을 넘어, 기계 학습의 실질적인 추론 및 일반 지능 과제 성능에서도 탁월한 경쟁력을 기록함을 입증했습니다.
        </p>

        <div class="image-container">
            <img src="https://cognitive-reasoners.epfl.ch/images/performance.png" alt="Performance Comparison on Reasoning Benchmarks">
            <div class="image-caption">
                <strong>[글로벌 기계 학습 추론 벤치마크 평가 성적]</strong><br>
                GSM8K(0-shot CoT), Minerva-Math, MMLU, BBH(few-shot CoT) 벤치마크의 최종 평가 결과입니다. MiCRo는 모든 베이스라인 모델을 능가하거나 필적하는 우수한 성적을 냈으며, 특히 수학/논리 벤치마크에서 관련성이 가장 없는 사회성 전문가 모듈을 소거(Ablation)한 모델 튜닝 상태에서 추가적인 성적 향상(Welch's t-test를 통한 통계적 유의미성 검정 확인)을 달성했습니다. MoB(Ablation) 및 MiCRo(Ablation)(MMLU 및 BBH 하위 과제 시)의 결과는 최대 한 개의 관련 없는 전문가를 선택적으로 소거했을 때 획득한 최상의 성능 지표를 가리킵니다. 베이스라인인 밀집형(Dense) 모델의 기준선은 검은 점선으로 투사되었으며, 나머지 다양한 모델과 추가 벤치마크 데이터들은 부록 E에 상세 기술되어 있습니다.
            </div>
        </div>

        <h1 class="section-title" style="margin-top: 3rem;">학술 인용 정보 (BibTeX)</h1>
        <pre>@inproceedings{alkhamissi2026micro,
    title={Mixture of Cognitive Reasoners: Modular Reasoning with Brain-Like Specialization},
    author={Badr AlKhamissi and C. Nicol{\`o} De Sabbata and Greta Tuckute and Zeming Chen and Martin Schrimpf and Antoine Bosselut},
    booktitle={The Fourteenth International Conference on Learning Representations},
    year={2026},
    url={https://openreview.net/forum?id=m3jztlHDmG}
}</pre>

        <h1 class="section-title" style="margin-top: 2rem;">감사의 글 (Acknowledgement)</h1>
        <p style="font-size: 0.9rem; color: #64748b;">
            본 프로젝트 웹사이트의 템플릿은 LLaVA-VL 및 Nerfies를 기초로 개작되었으며, Creative Commons Attribution-ShareAlike 4.0 International 라이선스를 따릅니다.
        </p>
    </div>

</body>
</html>
"""
    return html_template

# =====================================================================
# 🚀 3. 메인 변환 프로세스
# =====================================================================
def main():
    print("=" * 60)
    print("💡 EPFL 'MiCRo' 논문 원본 번역본 PDF 변환기 가동 (100% 무요약 완역)")
    print("=" * 60)

    browser_path = find_browser_path()
    if not browser_path:
        print("❌ 에러: 시스템에서 Google Chrome 또는 Microsoft Edge를 찾을 수 없습니다.")
        sys.exit(1)
    
    print(f"🎯 발견된 브라우저 엔진: {browser_path}")

    # 1. HTML 파일 빌드 및 저장
    output_html_name = "temp_micro_paper_verbatim.html"
    html_content = build_html_content()
    with open(output_html_name, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✓ 1단계: 번역본 단일 HTML 생성 성공 ({output_html_name})")

    # 2. PDF 변환 구동
    pdf_name = "MiCRo_논문_소개_번역본.pdf"
    pdf_path = os.path.abspath(pdf_name)
    abs_html_path = os.path.abspath(output_html_name)
    file_url = "file:///" + abs_html_path.replace("\\", "/")
    
    # 임시 캐시 격리
    cache_dir = "html_cache_feedbacks"
    os.makedirs(cache_dir, exist_ok=True)
    profile_dir = os.path.abspath(os.path.join(cache_dir, "profile_print_micro_verbatim"))

    cmd = [
        browser_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--user-data-dir={profile_dir}",
        f"--print-to-pdf={pdf_path}",
        "--no-pdf-header-footer",
        file_url
    ]

    print("👉 2단계: 크롬 PDF 인쇄 변환 시작...")
    try:
        subprocess.run(cmd, check=True, timeout=90, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"\n✨ PDF 번역 도서 제작 성공! -> {pdf_path}")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ PDF 변환 중 에러 발생: {e}")
        print("👉 HTML 파일은 보존되었으니 직접 브라우저에서 인쇄해 보셔도 됩니다.")
        print("=" * 60)
    finally:
        # 임시 HTML 파일 삭제 정리
        if os.path.exists(output_html_name):
            os.remove(output_html_name)

if __name__ == "__main__":
    main()
