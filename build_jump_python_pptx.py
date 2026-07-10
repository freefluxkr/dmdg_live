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
        "chapter_num": "01",
        "chapter_title": "파이썬이란 무엇인가?",
        "slides": [
            {
                "section": "01-1. 파이썬의 특징과 매력",
                "bullets": [
                    "파이썬(Python)은 1991년 귀도 반 로섬이 발표한 오픈소스 인터프리터 언어입니다.",
                    "인간의 사고방식과 유사하여 문법이 지극히 간결하고 읽기 쉽습니다.",
                    "개발 속도가 매우 빨라 'Life is too short, you need Python'이라는 명언을 만들어 냈습니다.",
                    "무료이면서 강력하여 시스템 유틸리티, GUI, 웹 개발, 인공지능 분야에 널리 사용됩니다."
                ],
                "code": "# 파이썬의 단순 명료함을 보여주는 예제\nlanguages = ['python', 'perl', 'c', 'java']\n\nfor lang in languages:\n    if lang == 'python':\n        print(f'{lang}은 참 쉽고 강력합니다!')\n    else:\n        print(f'{lang}도 훌륭한 언어입니다.')"
            },
            {
                "section": "01-2. 파이썬으로 할 수 있는 일 & 없는 일",
                "bullets": [
                    "할 수 있는 일:",
                    "  - AI & 머신러닝/데이터분석 (NumPy, Pandas, TensorFlow)",
                    "  - 웹 프로그래밍 및 크롤링 (Django, Flask, BeautifulSoup)",
                    "  - 시스템 유틸리티 제작 및 자동화 스크립트 작성",
                    "할 수 없는 일 (지양해야 하는 분야):",
                    "  - 하드웨어를 직접 제어하는 시스템 프로그램 (C/C++ 권장)",
                    "  - 엄청난 연산 속도가 요구되는 3D 모바일 게임 게임 엔진"
                ],
                "code": "# 간단한 파일 입출력 및 자동화 예제\nimport os\n\n# 현재 폴더의 파일 목록 출력\nfile_list = os.listdir('.')\nprint(f'현재 디렉토리 파일 수: {len(file_list)}')\nfor file in file_list[:3]:\n    print('-', file)"
            }
        ]
    },
    {
        "chapter_num": "02",
        "chapter_title": "파이썬 프로그래밍의 기초, 자료형",
        "slides": [
            {
                "section": "02-1. 숫자형과 문자열 자료형",
                "bullets": [
                    "숫자형: 정수(Integer), 실수(Float), 8진수 및 16진수를 지원합니다.",
                    "문자열 표현: 따옴표( ' 또는 \" )로 감싸며, 3개를 쓰면 줄바꿈이 유지됩니다.",
                    "인덱싱(Indexing): 문자열의 특정 위치를 지정(예: a[0]은 첫 글자, a[-1]은 마지막).",
                    "슬라이싱(Slicing): 문자열 일부를 잘라냄 (예: a[0:5]는 0번부터 4번 인덱스까지).",
                    "포맷팅: f-string(f'{var}') 형식을 통해 직관적으로 변수 값을 대입합니다."
                ],
                "code": "# 문자열 포맷팅 및 슬라이싱 예제\nname = '홍길동'\nage = 30\ninfo = f'제 이름은 {name}이고 나이는 {age}세입니다.'\n\nprint(info)            # 전체 출력\nprint(info[6:9])        # '홍길동'만 슬라이싱\nprint(info[-4:])        # '세입니다.'만 슬라이싱"
            },
            {
                "section": "02-2. 리스트와 튜플 자료형",
                "bullets": [
                    "리스트(List): 대괄호 [ ]를 사용하며, 여러 개의 요소를 순서대로 담아 관리합니다.",
                    "  - 요소를 추가(append), 정렬(sort), 뒤집기(reverse), 제거(remove)할 수 있습니다.",
                    "튜플(Tuple): 소괄호 ( )를 사용하며, 리스트와 유사하지만 요소를 수정/삭제할 수 없습니다.",
                    "  - 요소를 변경할 수 없는 불변의 특징 덕분에 프로그램의 안전성을 보장할 때 주로 쓰입니다."
                ],
                "code": "# 리스트 수정 vs 튜플 수정 불가 예제\na_list = [1, 2, 3]\na_list[0] = 99\na_list.append(4)\nprint('리스트:', a_list)  # [99, 2, 3, 4] 정상 변경\n\na_tuple = (1, 2, 3)\ntry:\n    a_tuple[0] = 99\nexcept TypeError as e:\n    print('튜플 에러:', e)  # 값 변경 시도 시 에러 발생!"
            },
            {
                "section": "02-3. 딕셔너리, 집합, 불 자료형",
                "bullets": [
                    "딕셔너리(Dictionary): Key-Value 한 쌍을 { } 중괄호 구조로 묶어 관리합니다.",
                    "  - 순서가 없으므로 Key를 통해 빠르게 값을 찾아냅니다.",
                    "집합(Set): set() 키워드를 사용하며, 중복을 허용하지 않고 순서가 없는 것이 특징입니다.",
                    "  - 교집합(&), 합집합(|), 차집합(-) 등의 집합 연산에 최적화되어 있습니다.",
                    "불(Bool): True(참)와 False(거짓) 단 두 가지 상태만을 나타내는 자료형입니다."
                ],
                "code": "# 딕셔너리와 집합 연산 예제\n# 1. 딕셔너리\nuser = {'name': 'Alice', 'role': 'Admin'}\nprint(user['name'])\n\n# 2. 집합의 중복 제거 및 연산\ns1 = set([1, 2, 3, 3, 4])\ns2 = set([3, 4, 5, 6])\nprint(s1)           # {1, 2, 3, 4} (중복 자동 제거)\nprint(s1 & s2)      # {3, 4} (교집합)"
            }
        ]
    },
    {
        "chapter_num": "03",
        "chapter_title": "프로그램의 구조를 쌓는다! 제어문",
        "slides": [
            {
                "section": "03-1. if 조건문과 비교/논리 연산자",
                "bullets": [
                    "if문은 주어진 조건식이 참(True)일 때 블록 내부의 명령을 실행합니다.",
                    "파이썬은 들여쓰기(Indentation)가 필수적이며, 보통 4칸 공백을 규격으로 사용합니다.",
                    "비교 연산자: <, >, ==, !=, >=, <=",
                    "논리 연산자: and(둘 다 참), or(하나만 참이어도 참), not(참/거짓 반전)",
                    "멤버십 연산자: in, not in (리스트나 튜플 내에 특정 요소가 존재하는지 확인)"
                ],
                "code": "# if-elif-else 및 in 연산자 활용 예제\npocket = ['paper', 'cellphone', 'money']\n\nif 'money' in pocket:\n    print('택시를 타고 가라')\nelif 'card' in pocket:\n    print('카드를 사용해라')\nelse:\n    print('걸어가라')"
            },
            {
                "section": "03-2. while 반복문과 루프 제어",
                "bullets": [
                    "while문은 조건문이 참(True)인 동안 계속해서 블록의 명령을 반복합니다.",
                    "break: 반복문을 중간에 강제로 탈출할 때 사용합니다.",
                    "continue: 반복문의 맨 처음 조건문 위치로 돌아가 루프를 이어나갈 때 사용합니다.",
                    "무한 루프(Infinite Loop): 조건식을 항상 True로 주어 프로그램이 무한히 돌게 합니다."
                ],
                "code": "# while 루프와 break 예제\ncoffee = 3\nwhile True:\n    print('돈을 받았으니 커피를 줍니다.')\n    coffee -= 1\n    print(f'남은 커피는 {coffee}개입니다.\\n')\n    if coffee == 0:\n        print('커피가 다 떨어졌습니다. 판매를 중단합니다.')\n        break"
            },
            {
                "section": "03-3. for 반복문과 range 함수",
                "bullets": [
                    "for문은 리스트, 튜플, 문자열 등 순회 가능한 객체의 요소를 차례대로 꺼내 돕니다.",
                    "range(start, stop, step): 숫자 시퀀스를 생성하여 특정 횟수만큼 반복할 때 유용합니다.",
                    "리스트 컴프리헨션(List Comprehension): 리스트 내부에 for문과 if문을 넣어",
                    "  한 줄로 간결하고 빠르게 리스트를 생성하는 파이썬의 강력한 문법적 특징입니다."
                ],
                "code": "# 1. range 함수 활용 구구단\nfor i in range(2, 4):\n    for j in range(1, 3):\n        print(f'{i} * {j} = {i*j}')\n\n# 2. 리스트 컴프리헨션\nnumbers = [1, 2, 3, 4]\nresult = [n * 3 for n in numbers if n % 2 == 0]\nprint(result)  # [6, 12] (짝수에만 3을 곱함)"
            }
        ]
    },
    {
        "chapter_num": "04",
        "chapter_title": "파이썬의 입출력",
        "slides": [
            {
                "section": "04-1. 함수(Function)와 입력/출력값",
                "bullets": [
                    "함수(Function): 반복되는 코드 블록을 정의하여 재사용할 수 있게 만드는 뼈대입니다.",
                    "def 키워드로 선언하며, 입력값(매개변수)과 결과값(return)을 가질 수 있습니다.",
                    "가변 매개변수(*args): 입력값의 개수가 정해지지 않았을 때, 튜플 형태로 모두 받아옵니다.",
                    "키워드 매개변수(**kwargs): key=value 형태의 입력을 딕셔너리로 받아 처리합니다."
                ],
                "code": "# 가변 매개변수 및 return 활용 예제\ndef add_many(*args):\n    result = 0\n    for i in args:\n        result += i\n    return result\n\ntotal = add_many(1, 2, 3, 4, 5)\nprint(f'합계: {total}')  # 15 출력"
            },
            {
                "section": "04-2. 사용자 입출력 & 파일 읽고 쓰기",
                "bullets": [
                    "input(): 사용자가 키보드로 입력한 값을 항상 '문자열' 형태로 입력받습니다.",
                    "파일 열기 모드:",
                    "  - 'r' (읽기 모드): 파일의 내용을 읽을 때 사용",
                    "  - 'w' (쓰기 모드): 새로운 내용을 덮어 쓰거나 새 파일을 생성할 때 사용",
                    "  - 'a' (추가 모드): 기존 파일의 끝에 새로운 내용을 덧붙일 때 사용",
                    "with문: 블록을 벗어나면 파일 객체가 자동으로 close되도록 보장하여 안전합니다."
                ],
                "code": "# 파일 생성 및 with문 파일 읽기 예제\n# 1. 파일 쓰기\nwith open('test.txt', 'w', encoding='utf-8') as f:\n    f.write('Life is too short\\nYou need Python')\n\n# 2. 파일 읽기\nwith open('test.txt', 'r', encoding='utf-8') as f:\n    content = f.read()\n    print(content)"
            }
        ]
    },
    {
        "chapter_num": "05",
        "chapter_title": "파이썬 날개 달기",
        "slides": [
            {
                "section": "05-1. 클래스(Class)와 객체지향",
                "bullets": [
                    "클래스(Class): 객체(Instance)를 만들기 위한 일종의 설계도(틀)입니다.",
                    "생성자(__init__): 객체가 생성되는 시점에 자동으로 호출되는 초기화 메서드입니다.",
                    "상속(Inheritance): 기존 클래스의 기능을 그대로 물려받아 새로운 클래스를 생성합니다.",
                    "메서드 오버라이딩(Overriding): 상속받은 부모의 메서드를 자식 클래스에서 재정의합니다."
                ],
                "code": "# 클래스 및 상속, 오버라이딩 예제\nclass Calculator:\n    def __init__(self, val=0):\n        self.value = val\n    def add(self, val):\n        self.value += val\n\nclass UpgradeCalculator(Calculator):\n    def minus(self, val):  # 새로운 기능 추가\n        self.value -= val\n\ncal = UpgradeCalculator(100)\ncal.add(20)\ncal.minus(50)\nprint(cal.value)  # 70"
            },
            {
                "section": "05-2. 모듈, 패키지, 예외 처리",
                "bullets": [
                    "모듈(Module): 함수나 클래스를 모아놓은 파이썬 파일(.py)입니다.",
                    "패키지(Package): 여러 개의 모듈들을 폴더 구조로 묶어 관리하는 것입니다.",
                    "예외 처리(Exception Handling): 프로그램 실행 중 발생하는 오류를 제어합니다.",
                    "  - try: 에러가 발생할 가능성이 있는 코드 영역 실행",
                    "  - except: 지정한 오류가 발생했을 때 대체 동작 수행",
                    "  - finally: 에러 발생 유무와 무관하게 항상 실행할 코드 정의"
                ],
                "code": "# 예외 처리 활용 예제\ntry:\n    a = [1, 2]\n    print(a[3])  # IndexError 유발\n    result = 4 / 0\nexcept IndexError as e:\n    print(f'인덱스 범위 초과! ({e})')\nexcept ZeroDivisionError as e:\n    print(f'0으로 나눌 수 없음! ({e})')\nfinally:\n    print('예외 처리 블록 종료!')"
            },
            {
                "section": "05-3. 내장 함수와 외장 표준 라이브러리",
                "bullets": [
                    "내장 함수: import 없이 언제나 바로 사용할 수 있는 기본 제공 함수들",
                    "  - map(f, list): 모든 요소에 함수 f를 적용하여 결과를 매핑",
                    "  - filter(f, list): 함수 f가 참을 반환하는 요소만 걸러서 반환",
                    "  - zip(*iterable): 동일한 개수의 자료형을 튜플 쌍으로 묶어줌",
                    "표준 라이브러리: 파이썬 설치 시 기본 제공되는 외장 모듈 (sys, os, time 등)"
                ],
                "code": "# map/filter 내장 함수 및 datetime 라이브러리\n# 1. map + lambda\nres1 = list(map(lambda x: x*2, [1, 2, 3]))\nprint(res1)  # [2, 4, 6]\n\n# 2. 표준 라이브러리 활용\nimport datetime\ntoday = datetime.date.today()\nprint(f'오늘 날짜: {today}')"
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
    p_sub.text = "01장 ~ 05장 핵심 요약 및 실전 예제 가이드"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(22)
    p_sub.font.color.rgb = COLOR_YELLOW
    p_sub.alignment = PP_ALIGN.LEFT
    
    # 작성자 정보
    author_box = slide.shapes.add_textbox(Inches(1.5), Inches(5.8), Inches(10.333), Inches(0.8))
    tf_auth = author_box.text_frame
    p_auth = tf_auth.paragraphs[0]
    p_auth.text = "AI 시대의 핵심 프로그래밍 학습 요약 가이드"
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
    output_filename = "점프_투_파이썬_요약.pptx"
    prs.save(output_filename)
    print(f"\n🎉 PPTX 프레젠테이션 파일이 생성되었습니다!")
    print(f"📂 저장 경로: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    create_presentation()
