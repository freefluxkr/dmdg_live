import os
import sys

# =====================================================================
# 📦 python-pptx 라이브러리 자동 설치 검사
# =====================================================================
try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
except ImportError:
    print("   [System] python-pptx 라이브러리가 존재하지 않습니다. 자동 설치를 시작합니다...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor
        from pptx.enum.text import PP_ALIGN
        from pptx.enum.shapes import MSO_SHAPE
        print("   ✓ python-pptx 설치 성공!")
    except Exception as e:
        print(f"   ❌ 라이브러리 설치 실패: {e}")
        print("   👉 수동으로 'pip install python-pptx'를 실행하신 후 스크립트를 다시 돌려주세요.")
        sys.exit(1)

# =====================================================================
# 🎨 1. PPT 디자인 테마 설정
# =====================================================================
FONT_TITLE = "Malgun Gothic"
FONT_BODY = "Malgun Gothic"
FONT_CODE = "Consolas"

# 색상 팔레트
COLOR_NAVY = RGBColor(30, 65, 90)       # 주 색상 (헤더, 타이틀 배경)
COLOR_YELLOW = RGBColor(245, 195, 65)   # 포인트 색상 (강조)
COLOR_WHITE = RGBColor(255, 255, 255)   # 흰색
COLOR_CHARCOAL = RGBColor(44, 62, 80)   # 본문 텍스트 색상
COLOR_CODE_BG = RGBColor(40, 44, 52)    # 코드 블록 어두운 배경 (One Dark 테마)
COLOR_CODE_FG = RGBColor(224, 108, 117) # 코드 강조 텍스트 색상
COLOR_LIGHT_GRAY = RGBColor(245, 246, 247) # 슬라이드 기본 연회색 배경

# =====================================================================
# 📝 2. PPT 요약용 데이터 구조 정의
# =====================================================================
PPT_DATA = [
    {
        "chapter_num": "06",
        "chapter_title": "파이썬 프로그래밍, 어떻게 시작해야 할까?",
        "slides": [
            {
                "section": "06-1. 프로그램 요구사항 분석과 설계",
                "bullets": [
                    "프로그래밍을 시작하기 전, 문제에 대한 로직을 설계해야 합니다.",
                    "입력값(Input)과 출력값(Output)이 무엇인지 명확하게 정의합니다.",
                    "구구단 만들기: 입력은 '단(2~9)', 출력은 '해당 단의 계산 목록'입니다.",
                    "3과 5의 배수 합하기: 1000 미만의 자연수 중 조건에 맞는 배수만 필터링합니다."
                ],
                "code": "# 구구단 함수 및 3과 5의 배수 합 구하기 예제\ndef gugu(n):\n    result = []\n    for i in range(1, 10):\n        result.append(n * i)\n    return result\n\n# 3과 5의 배수 합 계산\ntotal = 0\nfor n in range(1, 1000):\n    if n % 3 == 0 or n % 5 == 0:\n        total += n\n\nprint('3단 결과:', gugu(3)[:3])\nprint('배수 합:', total)"
            },
            {
                "section": "06-2. 게시판 페이징 및 메모장 프로그램",
                "bullets": [
                    "게시판 페이징(Paging): 게시물 수와 한 페이지에 보여줄 목록 수로",
                    "  총 페이지 수를 계산하는 공식을 구현합니다.",
                    "  공식: 총 페이지 = (총 게시물 // 한 페이지 게시물) + (1 if 나머지 else 0)",
                    "메모장 만들기: 텍스트 파일 입출력을 활용해 콘솔 기반의",
                    "  간단한 파일 작성 및 조회 프로그램을 구축합니다."
                ],
                "code": "# 1. 페이징 계산 함수\ndef get_total_page(m, n):\n    if m % n == 0:\n        return m // n\n    return m // n + 1\n\nprint('게시물30/페이지10:', get_total_page(30, 10))\nprint('게시물31/페이지10:', get_total_page(31, 10))\n\n# 2. 간단한 메모장 추가 모드 예제\nwith open('memo.txt', 'a', encoding='utf-8') as f:\n    f.write('새로운 메모를 작성합니다.\\n')"
            },
            {
                "section": "06-3. 하위 디렉토리 검색과 os.walk",
                "bullets": [
                    "특정 폴더의 하위 경로를 탐색하면서 특정 확장자(.py 등)의",
                    "  파일들만 골라내는 프로그램을 만듭니다.",
                    "os.listdir()와 os.path.isdir()을 이용해 재귀적으로 탐색하거나",
                    "파이썬 내장 라이브러리인 os.walk()를 쓰면 매우 간편하게",
                    "  하위 디렉토리 구조와 파일 목록을 한 번에 가져올 수 있습니다."
                ],
                "code": "# os.walk를 활용한 디렉토리 파일 검색\nimport os\n\ndef search_py_files(dirname):\n    for (path, dir, files) in os.walk(dirname):\n        for filename in files:\n            ext = os.path.splitext(filename)[-1]\n            if ext == '.py':\n                # 파이썬 파일 경로 출력\n                print(os.path.join(path, filename))\n\n# search_py_files('.') # 실행 시 현재 폴더 탐색"
            }
        ]
    },
    {
        "chapter_num": "07",
        "chapter_title": "파이썬 날아오르기",
        "slides": [
            {
                "section": "07-1. pip 패키지 매니저와 외부 패키지",
                "bullets": [
                    "pip(Pip Installs Packages): 파이썬 공식 외부 라이브러리 관리 툴입니다.",
                    "명령어 예시: pip install [패키지명] (패키지 설치)",
                    "PyPI(Python Package Index) 저장소에서 수많은 모듈을 다운로드합니다.",
                    "설치된 패키지 확인 및 삭제:",
                    "  - pip list: 현재 설치되어 있는 패키지 목록 조회",
                    "  - pip uninstall [패키지명]: 해당 패키지 시스템에서 삭제"
                ],
                "code": "# pip 사용 예시 (터미널 명령어)\n# 1. 특정 버전의 패키지 설치\n# pip install requests==2.31.0\n\n# 2. 설치된 패키지를 텍스트 파일로 저장하여 관리\n# pip freeze > requirements.txt\n\n# 3. requirements.txt에 등록된 모든 패키지 일괄 설치\n# pip install -r requirements.txt"
            },
            {
                "section": "07-2. 실전 코딩 도장 (문제 풀이 예제)",
                "bullets": [
                    "다양한 실전 프로그래밍 문제를 풀며 논리력을 키웁니다.",
                    "대표적인 문제 유형:",
                    "  - 자릿수 합하기: 숫자를 입력받아 각 자릿수의 합 구하기",
                    "  - 중복 문자 제거: 연속해서 나타나는 문자열 압축하기",
                    "  - 369 게임: 3, 6, 9가 들어가는 숫자를 판단해 짝 박수 구현"
                ],
                "code": "# 숫자의 각 자릿수 합을 구하는 간단 알고리즘\ndef sum_digits(n):\n    # 숫자를 문자열로 변환하여 각각 더하기\n    return sum(int(digit) for digit in str(n))\n\n# 문자열 압축 예제 (aaabbbcc -> a3b3c2)\nprint('1234의 자릿수 합:', sum_digits(1234))  # 10"
            }
        ]
    },
    {
        "chapter_num": "08",
        "chapter_title": "정규표현식",
        "slides": [
            {
                "section": "08-1. 정규표현식의 필요성과 메타 문자",
                "bullets": [
                    "정규표현식(Regular Expressions)은 복잡한 문자열 패턴을",
                    "  검색, 추출, 변환할 때 사용하는 강력한 도구입니다.",
                    "대표적인 메타 문자(특수 의미를 갖는 문자):",
                    "  - . (줄바꿈 문자를 제외한 모든 문자 1개 매칭)",
                    "  - * (0회 이상 반복), + (1회 이상 반복), ? (0회 또는 1회 존재)",
                    "  - ^ (문자열의 시작), $ (문자열의 끝)",
                    "  - [] (괄호 안의 문자들 중 하나와 매치)"
                ],
                "code": "# 정규표현식 패턴과 메타 문자 기호 매핑\nimport re\n\n# [a-z]+ : 소문자가 1회 이상 반복되는 패턴\np = re.compile('[a-z]+')\n\nm1 = p.match('python')\nprint(m1.group() if m1 else '매칭 실패')  # 'python'\n\nm2 = p.match('3 python')\nprint(m2.group() if m2 else '매칭 실패')  # '매칭 실패' (숫자 시작)"
            },
            {
                "section": "08-2. re 모듈과 정규식 검색 메서드",
                "bullets": [
                    "match(): 문자열의 처음부터 정규식과 매치되는지 조사합니다.",
                    "search(): 문자열 전체를 검색하여 정규식과 매치되는지 조사합니다.",
                    "findall(): 매치되는 모든 문자열을 리스트 형태로 반환합니다.",
                    "finditer(): 매치되는 모든 결과를 반복 가능한 객체(Iterator)로 반환합니다.",
                    "메서드 그룹 활용: group(), start(), end(), span()을 통해 위치 상세 파악 가능"
                ],
                "code": "# match() vs search() 및 findall() 예제\nimport re\np = re.compile('[a-z]+')\n\n# search는 처음이 부합하지 않아도 전체에서 매칭부를 찾음\nm = p.search('3 python')\nprint('search 결과:', m.group())  # 'python'\n\n# 모든 알파벳 단어 추출\nwords = p.findall('life is too short')\nprint('findall 결과:', words)  # ['life', 'is', 'too', 'short']"
            }
        ]
    },
    {
        "chapter_num": "09",
        "chapter_title": "부록 - 가상 환경과 바이트코드",
        "slides": [
            {
                "section": "09-1. 파이썬 가상 환경(venv)과 의존성 관리",
                "bullets": [
                    "가상 환경(Virtual Environment)은 프로젝트별로 독립적인",
                    "  파이썬 실행 환경과 라이브러리 버전을 분리 관리하는 기술입니다.",
                    "서로 다른 버전을 요구하는 라이브러리 충돌을 원천적으로 예방합니다.",
                    "가상 환경 구축 명령어 및 활성화:",
                    "  - python -m venv [환경이름] (가상 환경 폴더 생성)",
                    "  - Window 활성화: [환경이름]\\Scripts\\activate.bat",
                    "  - Mac/Linux 활성화: source [환경이름]/bin/activate"
                ],
                "code": "# 가상 환경 생성 및 진입 (터미널 명령어)\n# 1. 'myenv'라는 이름의 가상 환경 생성\n# python -m venv myenv\n\n# 2. 윈도우 파워쉘에서 가상 환경 활성화\n# .\\myenv\\Scripts\\Activate.ps1\n\n# 3. 활성화 상태에서 라이브러리 설치\n# (myenv) pip install requests\n\n# 4. 가상 환경 비활성화\n# deactivate"
            }
        ]
    },
    {
        "chapter_num": "10",
        "chapter_title": "정답 및 풀이",
        "slides": [
            {
                "section": "10-1. 되새김 문제 풀이와 학습 마무리",
                "bullets": [
                    "각 장의 끝에 수록된 되새김 문제를 스스로 풀어보며 복습합니다.",
                    "정답 풀이 코드를 통해 자신의 로직과 비교하고 리팩토링합니다.",
                    "예제 코드에 제시된 오류 상황이나 경계 조건(Edge cases)을 점검합니다.",
                    "  - 예: 빈 리스트 입력, 0으로 나누기, 파일 미존재 예외 처리 등",
                    "학습 마무리: 파이썬의 기본기를 바탕으로 대형 프레임워크나",
                    "  데이터 분석 라이브러리로 나아갈 수 있는 단단한 발판이 마련되었습니다."
                ],
                "code": "# 대표적인 문제 유형: 문자열 역순 출력 및 리팩토링 예시\ndef reverse_string(s):\n    # 가장 간단한 파이썬 다운(Pythonic) 방식\n    return s[::-1]\n\n# 리스트 역순 정렬 예제\na = [1, 3, 5, 4, 2]\na.sort(reverse=True)\nprint('정렬결과:', a)  # [5, 4, 3, 2, 1]\nprint('역순문자:', reverse_string('hello'))  # 'olleh'"
            }
        ]
    }
]

# =====================================================================
# 🚀 3. PPTX 생성기 핵심 구현부
# =====================================================================
def create_presentation():
    prs = Presentation()
    
    # 16:9 와이드스크린 비율 설정
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6] # 완전 빈 슬라이드 레이아웃
    
    # -----------------------------------------------------------------
    # 🎨 [표지 슬라이드] 생성
    # -----------------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    
    # 어두운 네이비 배경 생성
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = COLOR_NAVY
    bg_shape.line.fill.background()
    
    # 노란색 포인트 장식 선
    line_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(2.2), Inches(10.333), Inches(0.1)
    )
    line_shape.fill.solid()
    line_shape.fill.fore_color.rgb = COLOR_YELLOW
    line_shape.line.fill.background()
    
    # 대제목
    title_box = slide.shapes.add_textbox(Inches(1.5), Inches(2.5), Inches(10.333), Inches(2.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "점프 투 파이썬 (Jump to Python)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.LEFT
    
    # 소제목
    subtitle_box = slide.shapes.add_textbox(Inches(1.5), Inches(4.2), Inches(10.333), Inches(1.0))
    tf_sub = subtitle_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "06장 ~ 10장 핵심 요약 및 실전 예제 가이드"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(22)
    p_sub.font.color.rgb = COLOR_YELLOW
    p_sub.alignment = PP_ALIGN.LEFT
    
    # 작성자 정보
    author_box = slide.shapes.add_textbox(Inches(1.5), Inches(5.8), Inches(10.333), Inches(0.8))
    tf_auth = author_box.text_frame
    p_auth = tf_auth.paragraphs[0]
    p_auth.text = "AI 시대의 핵심 프로그래밍 학습 요약 가이드 (Part 2)"
    p_auth.font.name = FONT_BODY
    p_auth.font.size = Pt(14)
    p_auth.font.color.rgb = RGBColor(170, 190, 205)
    p_auth.alignment = PP_ALIGN.LEFT
    
    # -----------------------------------------------------------------
    # 🎨 [본문 슬라이드] 생성 루프
    # -----------------------------------------------------------------
    for ch in PPT_DATA:
        ch_num = ch["chapter_num"]
        ch_title = ch["chapter_title"]
        
        # [장 구분 슬라이드 (Section Header)]
        sec_slide = prs.slides.add_slide(blank_layout)
        
        # 어두운 배경
        sec_bg = sec_slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
        )
        sec_bg.fill.solid()
        sec_bg.fill.fore_color.rgb = COLOR_NAVY
        sec_bg.line.fill.background()
        
        # 장 레이블 박스 (노란색 글자)
        lbl_box = sec_slide.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.333), Inches(1.0))
        lbl_tf = lbl_box.text_frame
        lbl_p = lbl_tf.paragraphs[0]
        lbl_p.text = f"CHAPTER {ch_num}"
        lbl_p.font.name = FONT_TITLE
        lbl_p.font.size = Pt(28)
        lbl_p.font.bold = True
        lbl_p.font.color.rgb = COLOR_YELLOW
        
        # 장 제목 박스 (흰색 글자)
        title_box = sec_slide.shapes.add_textbox(Inches(1.5), Inches(3.2), Inches(10.333), Inches(2.5))
        title_tf = title_box.text_frame
        title_tf.word_wrap = True
        title_p = title_tf.paragraphs[0]
        title_p.text = ch_title
        title_p.font.name = FONT_TITLE
        title_p.font.size = Pt(44)
        title_p.font.bold = True
        title_p.font.color.rgb = COLOR_WHITE
        
        # [세부 내용 슬라이드 추가]
        for slide_data in ch["slides"]:
            content_slide = prs.slides.add_slide(blank_layout)
            
            # 연한 회색 배경
            c_bg = content_slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
            )
            c_bg.fill.solid()
            c_bg.fill.fore_color.rgb = COLOR_LIGHT_GRAY
            c_bg.line.fill.background()
            
            # 1. 상단 타이틀 텍스트 박스
            t_box = content_slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.0))
            t_tf = t_box.text_frame
            t_tf.word_wrap = True
            t_p = t_tf.paragraphs[0]
            t_p.text = slide_data["section"]
            t_p.font.name = FONT_TITLE
            t_p.font.size = Pt(24)
            t_p.font.bold = True
            t_p.font.color.rgb = COLOR_NAVY
            
            # 장 카테고리 표시용 서브 텍스트
            sub_lbl_box = content_slide.shapes.add_textbox(Inches(0.8), Inches(0.15), Inches(5.0), Inches(0.4))
            sub_lbl_tf = sub_lbl_box.text_frame
            sub_lbl_p = sub_lbl_tf.paragraphs[0]
            sub_lbl_p.text = f"Chapter {ch_num}. {ch_title}"
            sub_lbl_p.font.name = FONT_BODY
            sub_lbl_p.font.size = Pt(11)
            sub_lbl_p.font.bold = True
            sub_lbl_p.font.color.rgb = RGBColor(140, 150, 160)
            
            # 상단 경계 장식 라인
            dec_line = content_slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(11.733), Inches(0.04)
            )
            dec_line.fill.solid()
            dec_line.fill.fore_color.rgb = COLOR_NAVY
            dec_line.line.fill.background()
            
            # 2. 좌측: 핵심 요약 텍스트 영역 (Bullets)
            text_box = content_slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.2))
            text_tf = text_box.text_frame
            text_tf.word_wrap = True
            
            for b_idx, bullet in enumerate(slide_data["bullets"]):
                p_bullet = text_tf.paragraphs[0] if b_idx == 0 else text_tf.add_paragraph()
                p_bullet.text = bullet
                p_bullet.font.name = FONT_BODY
                p_bullet.font.size = Pt(14)
                p_bullet.font.color.rgb = COLOR_CHARCOAL
                p_bullet.space_after = Pt(14) # 줄 간격 조절
                
                # 서브 불릿 들여쓰기 셋업 (띄어쓰기 2개인 경우 들여쓰기 1레벨 지정)
                if bullet.startswith("  -") or bullet.startswith("  "):
                    p_bullet.level = 1
                    p_bullet.font.size = Pt(13)
                    p_bullet.font.color.rgb = RGBColor(80, 95, 110)
                else:
                    p_bullet.level = 0
            
            # 3. 우측: 예제 코드 블록 영역 (배경 박스 + 텍스트)
            # 어두운 배경 상자 그리기
            code_bg_shape = content_slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2)
            )
            code_bg_shape.fill.solid()
            code_bg_shape.fill.fore_color.rgb = COLOR_CODE_BG
            code_bg_shape.line.fill.background()
            
            # 박스 상단에 "Python Code" 라벨
            label_box = content_slide.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(3.0), Inches(0.4))
            label_tf = label_box.text_frame
            label_p = label_tf.paragraphs[0]
            label_p.text = "📎 파이썬 실전 예제"
            label_p.font.name = FONT_BODY
            label_p.font.size = Pt(11)
            label_p.font.bold = True
            label_p.font.color.rgb = COLOR_YELLOW
            
            # 코드 텍스트 박스 얹기
            code_box = content_slide.shapes.add_textbox(Inches(6.8), Inches(2.1), Inches(5.533), Inches(4.5))
            code_tf = code_box.text_frame
            code_tf.word_wrap = True
            code_p = code_tf.paragraphs[0]
            code_p.text = slide_data["code"]
            code_p.font.name = FONT_CODE
            code_p.font.size = Pt(11.5)
            code_p.font.color.rgb = COLOR_WHITE
            code_p.line_spacing = 1.2
            
    # PPTX 파일 저장
    output_filename = "점프_투_파이썬_요약_part2.pptx"
    prs.save(output_filename)
    print(f"\n🎉 PPTX 프레젠테이션 파일이 생성되었습니다!")
    print(f"📂 저장 경로: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    create_presentation()
