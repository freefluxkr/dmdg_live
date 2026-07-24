import os
import sys
import re
import json
import subprocess
import argparse
from urllib.parse import urljoin

# =====================================================================
# 📦 1. 라이브러리 자동 의존성 확인 및 설치 함수
# =====================================================================
def check_dependencies():
    """스크립트 구동에 필요한 외부 라이브러리 존재 여부를 확인하고 없으면 자동 설치합니다."""
    # google-generativeai 확인
    try:
        import google.generativeai as genai
    except ImportError:
        print("💡 [Dependency] 'google-generativeai' 라이브러리가 없습니다. 자동 설치를 시작합니다...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "google-generativeai"], check=True)
            print("✓ 'google-generativeai' 설치 완료.")
        except Exception as e:
            print(f"❌ 라이브러리 설치 실패: {e}")
            print("👉 수동 설치 명령어: pip install google-generativeai")
            sys.exit(1)

    # pypdf 확인
    try:
        import pypdf
    except ImportError:
        print("💡 [Dependency] 'pypdf' 라이브러리가 없습니다. 자동 설치를 시작합니다...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pypdf"], check=True)
            print("✓ 'pypdf' 설치 완료.")
        except Exception as e:
            print(f"❌ 라이브러리 설치 실패: {e}")
            print("👉 수동 설치 명령어: pip install pypdf")
            sys.exit(1)

# 의존성 체크 실행
check_dependencies()

import google.generativeai as genai
from pypdf import PdfReader

# =====================================================================
# 🔍 2. 크롬 / 엣지 브라우저 경로 검색 함수 (PDF 인쇄용)
# =====================================================================
def find_browser_path():
    """윈도우 환경에서 Chrome 또는 Edge 브라우저의 설치 경로를 검색합니다."""
    candidate_paths = [
        # Google Chrome
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        # Microsoft Edge
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe")
    ]
    
    for path in candidate_paths:
        if os.path.exists(path):
            return path
    return None

# =====================================================================
# 📂 3. 다양한 확장자 파일에서 텍스트 추출 함수
# =====================================================================
def extract_text_from_file(file_path):
    """파일의 확장자에 따라 텍스트를 추출합니다. (.txt, .md, .pdf 지원)"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in ['.txt', '.md']:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    elif ext == '.pdf':
        print(f"📄 [PDF Reader] PDF 파일 분석 중: {file_path}")
        reader = PdfReader(file_path)
        text_content = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
        return "\n".join(text_content)
        
    else:
        raise ValueError(f"지원하지 않는 파일 형식입니다 ({ext}). .txt, .md, .pdf 형식만 지원합니다.")

# =====================================================================
# 🤖 4. 에이전트 정보 및 시스템 프롬프트 정의
# =====================================================================
AGENTS = {
    "samsung_sds": {
        "company": "삼성SDS",
        "agent_name": "김도현",
        "role": "인사팀 책임 (경력 11년 차)",
        "mbti": "INTJ",
        "quote": "기초가 흔들리는 아키텍처는 사상누각일 뿐입니다. 자료구조와 알고리즘, CS 기본기를 철저히 검증합니다.",
        "color_primary": "#0A2540",
        "color_secondary": "#0056B3",
        "color_bg": "#f4f7fa",
        "system_instruction": """
당신은 대한민국 최고의 IT 서비스 대기업인 삼성SDS의 11년 차 채용 담당자 김도현 책임(MBTI: INTJ)입니다. 
당신의 성향과 규칙은 다음과 같습니다:
1. 공통 역할: IT 분야 인사/채용 담당자로서 주니어 개발자의 포트폴리오를 날카롭고 꼼꼼하게 평가합니다.
2. 기업 문화 반영: 컴퓨터 사이언스(CS) 기본기, 알고리즘 및 자료구조, 데이터베이스 최적화, 백엔드 아키텍처의 설계 논리성과 확장성, 클린 코드 원칙 준수 여부를 극히 중요하게 봅니다.
3. 성격: 합리적인 비판을 지향하며, 옳고 그름이 명확하고 논리적입니다. 뜬구름 잡는 소리나 추상적인 자기소개는 싫어하며 객관적인 수치와 기술적 아키텍처 중심으로 지적합니다.
4. 말투/어조: 매우 차분하고 차가우면서도 정중하며 격식 있는 존댓말을 구사합니다. 번호와 목록으로 피드백을 깔끔하게 구조화하여 설명하십시오.

지원자의 포트폴리오를 분석하고, 반드시 아래 제공된 JSON 포맷에 맞추어 응답을 작성하세요.
JSON 응답에는 마크다운 코드 블록(```json)을 포함하지 말고, 순수 JSON 데이터만 반환해야 합니다.
JSON 스키마:
{
  "rating": "S/A/B/C/D 중 하나",
  "fit_score": 0~100 사이의 정수,
  "summary": "김도현 책임의 총평 (2~3문장)",
  "strengths": [
    {
      "title": "좋은 점 제목",
      "content": "이유와 구체적인 분석 내용"
    }
  ],
  "weaknesses": [
    {
      "title": "부족한 점 제목",
      "content": "논리적 맹점이나 아쉬운 코드/설계적 부분 지적"
    }
  ],
  "advice": [
    "삼성SDS 합격을 위해 구체적으로 채워야 할 기술적 조언 1",
    "구체적인 조언 2"
  ]
}
"""
    },
    "lg_cns": {
        "company": "LG CNS",
        "agent_name": "최민우",
        "role": "DX인재개발팀 책임전문위원 (경력 12년 차)",
        "mbti": "ENTP",
        "quote": "안주하지 않는 자가 DX 판도를 바꿉니다. 당신이 겪은 시행착오(Troubleshooting)와 기술적 도전의 크기를 보여주세요.",
        "color_primary": "#A50034",
        "color_secondary": "#4E5B6A",
        "color_bg": "#faf4f5",
        "system_instruction": """
당신은 국내 클라우드 및 DX 기술을 리딩하는 LG CNS의 12년 차 채용 담당자 최민우 책임전문위원(MBTI: ENTP)입니다.
당신의 성향과 규칙은 다음과 같습니다:
1. 공통 역할: IT 분야 인사/채용 담당자로서 주니어 개발자의 포트폴리오를 날카롭고 꼼꼼하게 평가합니다.
2. 기업 문화 반영: 최신 IT 기술(Cloud, MSA, DevOps, AI 연동 등) 도입에 대한 시도와 열정을 중요하게 봅니다. 단순히 기술을 쓴 것을 넘어 직면한 에러나 문제를 해결해 나간 구체적인 트러블슈팅(Troubleshooting/삽질) 기록이 있는지를 중점 평가합니다.
3. 성격: 날카롭고 예리하며 비판적이지만, 새로운 도전과 기술적 도전을 한 흔적이 보이면 크게 호평합니다. 주관이 뚜렷하고 개방적이며 논리적인 논쟁을 즐깁니다.
4. 말투/어조: 다소 에너제틱하고 직설적이지만 따뜻함이 묻어나는 어조입니다. 핵심을 찌르는 직설적인 조언과 함께 발전을 자극하는 유머나 열정적인 문체를 사용합니다.

지원자의 포트폴리오를 분석하고, 반드시 아래 제공된 JSON 포맷에 맞추어 응답을 작성하세요.
JSON 응답에는 마크다운 코드 블록(```json)을 포함하지 말고, 순수 JSON 데이터만 반환해야 합니다.
JSON 스키마:
{
  "rating": "S/A/B/C/D 중 하나",
  "fit_score": 0~100 사이의 정수,
  "summary": "최민우 책임의 총평 (2~3문장)",
  "strengths": [
    {
      "title": "좋은 점 제목",
      "content": "이유와 구체적인 분석 내용"
    }
  ],
  "weaknesses": [
    {
      "title": "부족한 점 제목",
      "content": "논리적 맹점이나 아쉬운 코드/설계적 부분 지적"
    }
  ],
  "advice": [
    "LG CNS DX 인재상에 부합하기 위해 구체적으로 채워야 할 기술적 조언 1",
    "구체적인 조언 2"
  ]
}
"""
    },
    "shinsegae_inc": {
        "company": "신세계I&C",
        "agent_name": "이서윤",
        "role": "Retail Tech 인사파트 과장 (경력 10년 차)",
        "mbti": "ESFJ",
        "quote": "아무리 훌륭한 기술이라도 고객에게 닿지 못하면 무용지물입니다. 비즈니스 실용성과 완성도를 확인합니다.",
        "color_primary": "#B9975B",
        "color_secondary": "#111111",
        "color_bg": "#f9f7f4",
        "system_instruction": """
당신은 국내 리테일테크 분야의 최강자인 신세계I&C의 10년 차 채용 담당자 이서윤 과장(MBTI: ESFJ)입니다.
당신의 성향과 규칙은 다음과 같습니다:
1. 공통 역할: IT 분야 인사/채용 담당자로서 주니어 개발자의 포트폴리오를 날카롭고 꼼꼼하게 평가합니다.
2. 기업 문화 반영: 철저한 비즈니스 실용성(이 서비스가 실제 이커머스나 리테일 매장에서 쓰일 법한가?), UI/UX의 편의성 및 시각적 완성도, 다른 이들과 조화롭게 소통하고 협업한 내역을 중시합니다.
3. 성격: 상냥하고 공감 능력이 높지만, 비즈니스 가치 창출 관점에서는 뼈를 때리듯 냉정하게 허점을 잡아내는 합리적인 성격입니다.
4. 말투/어조: 상냥하고 배려 섞인 친절한 말투이나, 지적 사항은 얼버무리지 않고 논리적이고 명확하게 전달합니다. 문장에 부드러운 연결어미를 사용하되 분석은 엄격하게 하십시오.

지원자의 포트폴리오를 분석하고, 반드시 아래 제공된 JSON 포맷에 맞추어 응답을 작성하세요.
JSON 응답에는 마크다운 코드 블록(```json)을 포함하지 말고, 순수 JSON 데이터만 반환해야 합니다.
JSON 스키마:
{
  "rating": "S/A/B/C/D 중 하나",
  "fit_score": 0~100 사이의 정수,
  "summary": "이서윤 과장의 총평 (2~3문장)",
  "strengths": [
    {
      "title": "좋은 점 제목",
      "content": "이유와 구체적인 분석 내용"
    }
  ],
  "weaknesses": [
    {
      "title": "부족한 점 제목",
      "content": "논리적 맹점이나 아쉬운 코드/설계적 부분 지적"
    }
  ],
  "advice": [
    "신세계I&C Retail Tech 직무에 부합하기 위해 구체적으로 채워야 할 기술적 조언 1",
    "구체적인 조언 2"
  ]
}
"""
    },
    "lotte_innovate": {
        "company": "롯데이노베이트",
        "agent_name": "박성준",
        "role": "HR혁신팀 수석 (경력 13년 차)",
        "mbti": "ISTJ",
        "quote": "시스템의 기본은 타협 없는 안정성과 빈틈없는 예외 처리입니다. 성실함이 깃든 테스트 코드가 신뢰를 증명합니다.",
        "color_primary": "#E11B22",
        "color_secondary": "#2C3E50",
        "color_bg": "#fcf5f5",
        "system_instruction": """
당신은 안정적이고 신뢰성 높은 인프라 및 SI 서비스를 운영하는 롯데이노베이트(구 롯데정보통신)의 13년 차 채용 담당자 박성준 수석(MBTI: ISTJ)입니다.
당신의 성향과 규칙은 다음과 같습니다:
1. 공통 역할: IT 분야 인사/채용 담당자로서 주니어 개발자의 포트폴리오를 날카롭고 꼼꼼하게 평가합니다.
2. 기업 문화 반영: 시스템의 안정성, 철저한 예외 처리(Exception Handling), 테스트 코드 구축(TDD 포함), 상세한 문서화 수준(API 명세서, README 구조화), 보안 취약점 대처 여부를 집중적으로 확인합니다.
3. 성격: 지극히 보수적이고 규칙을 중시하며 꼼꼼합니다. 정돈되지 않은 문장이나 누락된 테스트 데이터에 대해 확실한 피드백을 줍니다. 과장된 기술 포장보다는 꼼꼼한 기본 마무리를 높이 평가합니다.
4. 말투/어조: 매우 차분하고 엄격하며 신중한 어조입니다. 전통적인 격식체 문장(~습니다, ~됩니다)을 주로 사용하며 간결하고 명확한 문장을 선호합니다.

지원자의 포트폴리오를 분석하고, 반드시 아래 제공된 JSON 포맷에 맞추어 응답을 작성하세요.
JSON 응답에는 마크다운 코드 블록(```json)을 포함하지 말고, 순수 JSON 데이터만 반환해야 합니다.
JSON 스키마:
{
  "rating": "S/A/B/C/D 중 하나",
  "fit_score": 0~100 사이의 정수,
  "summary": "박성준 수석의 총평 (2~3문장)",
  "strengths": [
    {
      "title": "좋은 점 제목",
      "content": "이유와 구체적인 분석 내용"
    }
  ],
  "weaknesses": [
    {
      "title": "부족한 점 제목",
      "content": "논리적 맹점이나 아쉬운 코드/설계적 부분 지적"
    }
  ],
  "advice": [
    "롯데이노베이트 합격에 기여하기 위해 채워야 할 기술적 조언 1",
    "구체적인 조언 2"
  ]
}
"""
    },
    "cj_olivenetworks": {
        "company": "CJ올리브네트웍스",
        "agent_name": "한지민",
        "role": "테크HR파트 과장 (경력 10년 차)",
        "mbti": "INFJ",
        "quote": "남들이 하지 않은 차별화된 독창성(ONLYONE)과 주도적인 학습 태도(하고잡이)에서 진짜 개발자의 잠재력이 드러납니다.",
        "color_primary": "#E06F1D",
        "color_secondary": "#22B14C",
        "color_bg": "#f5faf6",
        "system_instruction": """
당신은 트렌디한 라이프스타일 테크 서비스를 개척하는 CJ올리브네트웍스의 10년 차 채용 담당자 한지민 과장(MBTI: INFJ)입니다.
당신의 성향과 규칙은 다음과 같습니다:
1. 공통 역할: IT 분야 인사/채용 담당자로서 주니어 개발자의 포트폴리오를 날카롭고 꼼꼼하게 평가합니다.
2. 기업 문화 반영: 프로젝트의 차별성 및 참신함(CJ그룹의 ONLYONE 정신), 주도적으로 파고들어 공부하는 자세(하고잡이 정신), 트렌디한 프레임워크/라이브러리 및 최신 기술 활용 역량, 미래 잠재력을 가장 중요하게 봅니다.
3. 성격: 공감하면서도 깊은 통찰력을 보이며 비판합니다. 지원자의 숨겨진 잠재력이나 성장 궤적을 꿰뚫어 보며, 아키텍처 이면에 숨어 있는 고민의 깊이를 읽어냅니다.
4. 말투/어조: 차분하고 섬세하며, 비유와 은유가 섞인 감각적이면서도 전문적인 문체를 구사합니다. 마음을 움직이는 조언과 진정성 있는 통찰을 조근조근 제공합니다.

지원자의 포트폴리오를 분석하고, 반드시 아래 제공된 JSON 포맷에 맞추어 응답을 작성하세요.
JSON 응답에는 마크다운 코드 블록(```json)을 포함하지 말고, 순수 JSON 데이터만 반환해야 합니다.
JSON 스키마:
{
  "rating": "S/A/B/C/D 중 하나",
  "fit_score": 0~100 사이의 정수,
  "summary": "한지민 과장의 총평 (2~3문장)",
  "strengths": [
    {
      "title": "좋은 점 제목",
      "content": "이유와 구체적인 분석 내용"
    }
  ],
  "weaknesses": [
    {
      "title": "부족한 점 제목",
      "content": "논리적 맹점이나 아쉬운 코드/설계적 부분 지적"
    }
  ],
  "advice": [
    "CJ올리브네트웍스의 ONLYONE 인재가 되기 위해 필요한 구체적 조언 1",
    "구체적인 조언 2"
  ]
}
"""
    }
}

# =====================================================================
# 🎨 5. 프리미엄 HTML 리포트 템플릿 생성 함수
# =====================================================================
def generate_html_report(student_name, agent_key, data):
    """특정 에이전트의 피드백 데이터를 활용하여 아름다운 프리미엄 스타일의 HTML 보고서를 생성합니다."""
    agent_info = AGENTS[agent_key]
    
    # 등급별 뱃지 색상 매핑
    rating_colors = {
        "S": {"bg": "#E8F5E9", "text": "#2E7D32", "border": "#A5D6A7"},
        "A": {"bg": "#E3F2FD", "text": "#1565C0", "border": "#90CAF9"},
        "B": {"bg": "#FFF3E0", "text": "#EF6C00", "border": "#FFCC80"},
        "C": {"bg": "#F3E5F5", "text": "#6A1B9A", "border": "#CE93D8"},
        "D": {"bg": "#FFEBEE", "text": "#C62828", "border": "#EF9A9A"}
    }
    
    rating = data.get("rating", "B").upper()
    badge = rating_colors.get(rating, {"bg": "#F5F5F5", "text": "#616161", "border": "#E0E0E0"})
    
    strengths_html = ""
    for item in data.get("strengths", []):
        strengths_html += f"""
        <div class="card strength-card">
            <div class="card-header">
                <svg class="icon-success" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <h3>{item.get('title')}</h3>
            </div>
            <div class="card-body">
                <p>{item.get('content')}</p>
            </div>
        </div>
        """
        
    weaknesses_html = ""
    for item in data.get("weaknesses", []):
        weaknesses_html += f"""
        <div class="card weakness-card">
            <div class="card-header">
                <svg class="icon-danger" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
                <h3>{item.get('title')}</h3>
            </div>
            <div class="card-body">
                <p>{item.get('content')}</p>
            </div>
        </div>
        """
        
    advice_html = ""
    for item in data.get("advice", []):
        advice_html += f"""
        <li class="advice-item">
            <svg class="icon-info" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
            <span>{item}</span>
        </li>
        """

    html_content = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>[{agent_info['company']}] {student_name}님 포트폴리오 피드백</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.8/dist/web/static/pretendard-dynamic-subset.css');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');

        :root {{
            --primary: {agent_info['color_primary']};
            --secondary: {agent_info['color_secondary']};
            --bg-light: {agent_info['color_bg']};
            --text-dark: #2c3e50;
            --text-light: #64748b;
            --card-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.03);
            --border-color: #e2e8f0;
        }}

        body {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
            color: var(--text-dark);
            background-color: #ffffff;
            margin: 0;
            padding: 0;
            line-height: 1.6;
            -webkit-print-color-adjust: exact;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2.5rem 2rem;
        }}

        /* Header Area */
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 2px solid var(--primary);
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
        }}

        .header-left {{
            display: flex;
            flex-direction: column;
        }}

        .company-badge {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 1.5rem;
            color: var(--primary);
            letter-spacing: -0.05em;
            margin: 0 0 0.25rem 0;
        }}

        .report-title {{
            font-size: 1.8rem;
            font-weight: 700;
            color: #0f172a;
            margin: 0;
        }}

        .candidate-info {{
            font-size: 0.95rem;
            color: var(--text-light);
            margin-top: 0.5rem;
        }}

        /* Recruiter Profile Card */
        .profile-section {{
            background: var(--bg-light);
            border-left: 4px solid var(--primary);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2.5rem;
            box-shadow: var(--card-shadow);
        }}

        .profile-container {{
            display: flex;
            align-items: flex-start;
            gap: 1rem;
        }}

        .avatar {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background-color: var(--primary);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: bold;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}

        .profile-details {{
            flex: 1;
        }}

        .recruiter-meta {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.25rem;
        }}

        .recruiter-name {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #0f172a;
            margin: 0;
        }}

        .recruiter-role {{
            font-size: 0.85rem;
            color: var(--text-light);
            background: #ffffff;
            padding: 0.1rem 0.5rem;
            border-radius: 4px;
            border: 1px solid var(--border-color);
        }}

        .mbti-badge {{
            font-family: 'Outfit', sans-serif;
            font-size: 0.8rem;
            font-weight: 600;
            background-color: var(--secondary);
            color: #ffffff;
            padding: 0.1rem 0.4rem;
            border-radius: 4px;
        }}

        .recruiter-quote {{
            font-style: italic;
            color: #475569;
            margin: 0.5rem 0 0 0;
            font-size: 0.95rem;
            line-height: 1.5;
        }}

        /* Evaluation Score Summary */
        .score-section {{
            display: grid;
            grid-template-columns: 1fr 2.5fr;
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }}

        .rating-box {{
            background: #ffffff;
            border: 2px solid {badge['border']};
            background-color: {badge['bg']};
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}

        .rating-label {{
            font-size: 0.85rem;
            font-weight: 600;
            color: {badge['text']};
            margin-bottom: 0.5rem;
        }}

        .rating-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 3.5rem;
            font-weight: 800;
            color: {badge['text']};
            line-height: 1;
        }}

        .score-box {{
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .fit-score-container {{
            margin-bottom: 1rem;
        }}

        .fit-score-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }}

        .fit-score-label {{
            font-size: 0.95rem;
            font-weight: 700;
            color: #0f172a;
        }}

        .fit-score-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--primary);
        }}

        .progress-bar {{
            height: 10px;
            background: #f1f5f9;
            border-radius: 999px;
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            border-radius: 999px;
            width: {data.get('fit_score', 50)}%;
        }}

        .summary-text {{
            font-size: 0.95rem;
            color: #334155;
            margin: 0;
            line-height: 1.6;
        }}

        /* Section Titles */
        .section-title {{
            font-size: 1.3rem;
            font-weight: 700;
            color: #0f172a;
            border-left: 5px solid var(--primary);
            padding-left: 0.75rem;
            margin: 2.5rem 0 1.25rem 0;
        }}

        /* Cards Design */
        .card {{
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
            page-break-inside: avoid;
        }}

        .card-header {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.75rem;
        }}

        .card-header h3 {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #0f172a;
            margin: 0;
        }}

        .card-body p {{
            font-size: 0.95rem;
            color: #334155;
            margin: 0;
            line-height: 1.6;
        }}

        .strength-card {{
            border-left: 4px solid #22c55e;
        }}

        .weakness-card {{
            border-left: 4px solid #ef4444;
        }}

        /* Icons */
        .icon-success {{
            width: 20px;
            height: 20px;
            color: #22c55e;
        }}

        .icon-danger {{
            width: 20px;
            height: 20px;
            color: #ef4444;
        }}

        .icon-info {{
            width: 22px;
            height: 22px;
            color: var(--secondary);
            flex-shrink: 0;
        }}

        /* Advice List */
        .advice-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .advice-item {{
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            background: var(--bg-light);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            font-size: 0.95rem;
            color: #334155;
            line-height: 1.5;
            page-break-inside: avoid;
        }}

        /* Footer */
        .footer {{
            margin-top: 3.5rem;
            border-top: 1px solid var(--border-color);
            padding-top: 1.25rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: var(--text-light);
        }}

        /* Print optimization */
        @media print {{
            body {{
                background-color: #ffffff;
            }}
            .container {{
                padding: 1.5cm;
            }}
            .card, .profile-section, .rating-box, .score-box {{
                box-shadow: none !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="header-left">
                <span class="company-badge">{agent_info['company']}</span>
                <h1 class="report-title">포트폴리오 심층 진단 리포트</h1>
            </div>
            <div class="candidate-info">
                <strong>지원자:</strong> {student_name}님 &nbsp;&nbsp;|&nbsp;&nbsp; <strong>진단 분야:</strong> SW 개발
            </div>
        </div>

        <!-- Recruiter Profile -->
        <div class="profile-section">
            <div class="profile-container">
                <div class="avatar">{agent_info['agent_name'][0]}</div>
                <div class="profile-details">
                    <div class="recruiter-meta">
                        <span class="recruiter-name">{agent_info['agent_name']} {agent_info['role'].split(' ')[1]}</span>
                        <span class="recruiter-role">{agent_info['role'].split(' ')[0]}</span>
                        <span class="mbti-badge">{agent_info['mbti']}</span>
                    </div>
                    <p class="recruiter-quote">"{agent_info['quote']}"</p>
                </div>
            </div>
        </div>

        <!-- Score & Summary -->
        <div class="score-section">
            <div class="rating-box">
                <span class="rating-label">종합 평가 등급</span>
                <span class="rating-value">{rating}</span>
            </div>
            <div class="score-box">
                <div class="fit-score-container">
                    <div class="fit-score-header">
                        <span class="fit-score-label">인재상 부합도</span>
                        <span class="fit-score-value">{data.get('fit_score', 50)}점</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                </div>
                <p class="summary-text">
                    <strong>[총평]</strong> {data.get('summary', '')}
                </p>
            </div>
        </div>

        <!-- Strengths -->
        <h2 class="section-title">👍 좋은 점 (Strengths)</h2>
        {strengths_html}

        <!-- Weaknesses -->
        <h2 class="section-title">⚠️ 부족한 점 및 개선 사항 (Areas for Improvement)</h2>
        {weaknesses_html}

        <!-- Advice -->
        <h2 class="section-title">💡 {agent_info['agent_name']} 실무자의 합격 조언</h2>
        <ul class="advice-list">
            {advice_html}
        </ul>

        <!-- Footer -->
        <div class="footer">
            <span>&copy; 2026 {agent_info['company']} HR Expert Feedback. All rights reserved.</span>
            <span>Confidential | For Coaching Purpose Only</span>
        </div>
    </div>
</body>
</html>
"""
    return html_content

# =====================================================================
# 🚀 6. 메인 런타임 로직
# =====================================================================
def main():
    parser = argparse.ArgumentParser(description="IT 대기업 5개사 채용담당자 페르소나 포트폴리오 피드백 생성기")
    parser.add_argument("portfolio_path", help="피드백을 생성할 포트폴리오 파일 경로 (.txt, .md, .pdf)")
    parser.add_argument("--student", default="지원자", help="학생 이름 (기본값: 지원자)")
    parser.add_argument("--api-key", help="Gemini API Key (기본값: 환경 변수 GEMINI_API_KEY)")
    parser.add_argument("--output-dir", default="portfolio_feedbacks", help="결과 PDF가 저장될 폴더 경로")
    
    args = parser.parse_args()

    # API 키 검증
    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ 에러: Gemini API Key가 제공되지 않았습니다.")
        print("👉 --api-key 인자를 사용하거나 환경변수 'GEMINI_API_KEY'를 설정해주세요.")
        sys.exit(1)

    # Gemini 구성
    genai.configure(api_key=api_key)

    # 포트폴리오 텍스트 추출
    try:
        portfolio_text = extract_text_from_file(args.portfolio_path)
        print(f"✓ 포트폴리오 파일 로드 성공: {args.portfolio_path} (길이: {len(portfolio_text)}자)")
    except Exception as e:
        print(f"❌ 포트폴리오 파일 로드 중 에러 발생: {e}")
        sys.exit(1)

    # 출력 폴더 생성
    student_output_dir = os.path.join(args.output_dir, args.student)
    os.makedirs(student_output_dir, exist_ok=True)
    
    # 임시 HTML 캐시 폴더 생성
    html_cache_dir = "html_cache_feedbacks"
    os.makedirs(html_cache_dir, exist_ok=True)

    # 크롬/엣지 브라우저 경로 탐색
    browser_path = find_browser_path()
    if not browser_path:
        print("⚠️ 경고: 시스템에서 Google Chrome 또는 Microsoft Edge를 찾을 수 없습니다.")
        print("👉 피드백 HTML 파일은 생성되지만, PDF 변환은 수행되지 않습니다.")
    else:
        print(f"🎯 발견된 브라우저 엔진: {browser_path}")

    # 5개 에이전트 순차 호출 및 PDF 생성
    print("\n" + "="*50)
    print(f"🤖 {args.student}님의 포트폴리오 다면 에이전트 평가 시작 🤖")
    print("="*50)

    for idx, (agent_key, agent_meta) in enumerate(AGENTS.items(), 1):
        print(f"\n[{idx}/5] {agent_meta['company']} - {agent_meta['agent_name']} 에이전트 분석 중...")
        
        # 모델 생성
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=agent_meta["system_instruction"]
        )
        
        prompt = f"""
아래는 신입 SW 개발자로 지원하는 [{args.student}]님의 포트폴리오 본문입니다. 
당신의 페르소나와 지침에 따라 철저하게 분석하고 피드백을 작성해 주세요. 
반드시 명시된 스키마 형식의 JSON만 반환하고, 마크다운 코드 블록(```json)이나 다른 설명글은 포함하지 마십시오.

--- 포트폴리오 본문 ---
{portfolio_text}
"""
        
        success = False
        parsed_data = {}
        for retry in range(3):
            try:
                response = model.generate_content(prompt)
                resp_text = response.text.strip()
                
                # 가끔 모델이 마크다운 블록 안에 넣어서 주면 정제
                if resp_text.startswith("```json"):
                    resp_text = resp_text[7:]
                if resp_text.endswith("```"):
                    resp_text = resp_text[:-3]
                resp_text = resp_text.strip()
                
                parsed_data = json.loads(resp_text)
                success = True
                break
            except Exception as e:
                print(f"   ⚠️ Gemini 호출 시도 {retry+1} 실패 (재시도 중...): {e}")
                
        if not success:
            print(f"   ❌ {agent_meta['company']} 에이전트 피드백 생성 실패. 다음 에이전트로 넘어갑니다.")
            continue
            
        print(f"   ✓ 피드백 생성 완료 (등급: {parsed_data.get('rating')}, 부합도: {parsed_data.get('fit_score')}%)")
        
        # HTML 리포트 생성
        html_content = generate_html_report(args.student, agent_key, parsed_data)
        
        # HTML 임시 파일 저장
        html_filename = f"{args.student}_{agent_key}.html"
        html_path = os.path.join(html_cache_dir, html_filename)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # PDF 변환 실행
        if browser_path:
            pdf_filename = f"[{agent_meta['company']}] {agent_meta['agent_name']}_{args.student}_포트폴리오_피드백.pdf"
            
            # 윈도우 파일명 금지 문자 정제
            pdf_filename = re.sub(r'[\/:*?"<>|]', '', pdf_filename)
            pdf_path = os.path.abspath(os.path.join(student_output_dir, pdf_filename))
            abs_html_path = os.path.abspath(html_path)
            
            # 크롬 독립 프로필 격리
            profile_dir = os.path.abspath(os.path.join(html_cache_dir, f"profile_{agent_key}"))
            file_url = "file:///" + abs_html_path.replace("\\", "/")
            
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
            
            try:
                subprocess.run(cmd, check=True, timeout=30, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"   ✨ PDF 변환 완료 -> {pdf_path}")
            except Exception as pe:
                print(f"   ❌ PDF 변환 중 에러 발생: {pe}")
        else:
            print(f"   👉 PDF 변환 엔진 부재로 HTML만 생성되었습니다: {html_path}")

    print("\n" + "="*50)
    print("🎉 모든 에이전트 피드백 생성 작업이 완료되었습니다!")
    print(f"📂 최종 PDF 보관 폴더: {os.path.abspath(student_output_dir)}")
    print("="*50)

if __name__ == "__main__":
    main()
