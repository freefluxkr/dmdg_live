import os
import re
import sys
import time
import urllib.request
import urllib.error
import subprocess
from bs4 import BeautifulSoup

# =====================================================================
# 📚 1. 책 챕터별 페이지 범위 정의 (15개 장 + 해설 노트)
# =====================================================================
CHAPTERS = [
    {"name": "01장_Hello_Python", "start": 1, "end": 29},
    {"name": "02장_데이터_입력하고_결과_출력하기", "start": 30, "end": 67},
    {"name": "03장_변수로_데이터_저장하기", "start": 68, "end": 120},
    {"name": "04장_조건에_따라_해야_할_일이_다를_때_조건문", "start": 121, "end": 171},
    {"name": "05장_같은_일을_여러_번_반복해야_할_때_반복문", "start": 172, "end": 241},
    {"name": "06장_여러_데이터를_한_번에_묶어_표현하기_리스트", "start": 242, "end": 318},
    {"name": "07장_문자_기준으로_데이터_묶기_딕셔너리", "start": 319, "end": 368},
    {"name": "08장_그래프로_데이터_시각화하기", "start": 369, "end": 438},
    {"name": "09장_데이터_분석_기초", "start": 439, "end": 502},
    {"name": "10장_프로젝트_로드맵_그리기", "start": 503, "end": 521},
    {"name": "11장_프로젝트로_파이썬_완성하기_핫플레이스_인구_분석", "start": 522, "end": 588},
    {"name": "12장_위치_정보_시각화하기_folium", "start": 589, "end": 640},
    {"name": "13장_명령어_직접_만들어_사용하기_사용자_정의_함수", "start": 641, "end": 710},
    {"name": "14장_데이터와_함수를_한_단위로_묶어_재사용하기_클래스와_객체", "start": 711, "end": 767},
    {"name": "15장_프로그램_화면_구성하기_tkinter", "start": 768, "end": 859},
    {"name": "16장_해설_노트", "start": 860, "end": 860}
]

# 설정 변수
BOOK_ID = "080251"
BASE_URL = f"https://thebook.io/{BOOK_ID}"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# 폴더 생성
CACHE_DIR = "html_cache"
CHAPTERS_DIR = "html_chapters"
PDF_DIR = "pdf_chapters"

for directory in [CACHE_DIR, CHAPTERS_DIR, PDF_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# =====================================================================
# 🎨 2. 인쇄 및 화면 최적화 전용 CSS 스타일
# =====================================================================
PRINT_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&family=Source+Code+Pro:wght@400;600&display=swap');

body {
    font-family: 'Nanum Gothic', 'Malgun Gothic', '맑은 고딕', sans-serif;
    font-size: 14px;
    line-height: 1.8;
    color: #2b2b2b;
    margin: 0;
    padding: 2cm;
    background-color: #fff;
}

/* 개별 페이지 조각 간 페이지 분할 */
.book-page-fragment {
    page-break-before: always;
    padding-top: 1cm;
}
.book-page-fragment:first-child {
    page-break-before: avoid;
    padding-top: 0;
}

/* 코드 블록 스타일 */
pre, code, .cd {
    font-family: 'Source Code Pro', Consolas, Monaco, monospace;
}
.cd {
    background-color: #f5f5f5;
    padding: 0.1em 0.3em;
    border: 1px solid #d3d3d3;
    border-radius: 3px;
    font-size: 0.9em;
}
.highlight, .highlight4, .highlight7 {
    background-color: #f8f9fa;
    border-top: 1px solid #e9ecef;
    border-bottom: 1px solid #e9ecef;
    border-left: 4px solid #adb5bd;
    padding: 1em;
    margin: 1.5em 0;
    border-radius: 4px;
}
pre {
    margin: 0;
    white-space: pre-wrap;
    word-break: break-all;
    font-size: 0.9em;
}

/* 책 내부 안내 박스 스타일 */
.box_brown, .box_brown2, .box_brown3, .box_brown4, .box_brown5, .box_brown6, .box_yellow, .box_pink {
    background-color: #fcfcfc;
    border: 2px solid #e2e2e2;
    padding: 1.5em;
    margin: 1.5em 0;
    border-radius: 8px;
}
.box_brown {
    background-color: #b5b5b5;
    color: #fff;
}
.box_brown h1, .box_brown p, .box_brown span {
    color: #fff !important;
}

/* 이미지 및 캡션 */
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
}
.txts2 {
    font-size: 0.9em;
    color: #6c757d;
    text-align: center;
    margin-top: -0.5em;
    margin-bottom: 2em;
}

/* 테이블 스타일 */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5em 0;
}
table, th, td {
    border: 1px solid #dee2e6;
    padding: 0.6em;
}
th {
    background-color: #f1f3f5;
    font-weight: bold;
}

/* 인쇄 최적화 설정 */
@media print {
    body {
        padding: 0;
    }
    .thebook-content {
        box-shadow: none !important;
        border: none !important;
        width: 100% !important;
        margin: 0 !important;
    }
    /* 인쇄 시 페이지가 이상하게 잘리는 문제 방지 */
    pre, .highlight, .box_brown, .box_brown5, table, img {
        page-break-inside: avoid;
    }
    h1, h2, h3, h4, h5 {
        page-break-after: avoid;
    }
}
</style>
"""

# =====================================================================
# 🕸️ 3. 개별 페이지 수집 및 캐싱 함수
# =====================================================================
def get_page_html(page_num):
    """지정한 페이지 번호의 HTML 본문만 다운로드하거나 캐시에서 읽어옵니다."""
    cache_file = os.path.join(CACHE_DIR, f"{page_num:04d}.html")
    
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read()
            
    # 로컬 캐시에 없는 경우 다운로드
    url = f"{BASE_URL}/{page_num:04d}/"
    headers = {"User-Agent": USER_AGENT}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        print(f"   [Crawl] {page_num:04d} 페이지 다운로드 중... ({url})")
        with urllib.request.urlopen(req, timeout=10) as res:
            html = res.read()
            soup = BeautifulSoup(html, "html.parser")
            
            # 본문 영역 탐색
            content_div = soup.select_one(".thebook-content, #page_content")
            if not content_div:
                print(f"⚠️ {page_num:04d}페이지 본문 영역을 찾을 수 없습니다. 전체 HTML을 사용합니다.")
                content_div = soup.body
                
            if content_div:
                # 팝업 배너, 네비게이션 버튼, 하단 광고 등 불필요한 태그 제거
                for el in content_div.select(".newsletter-banner, .gas, .mdl-mega-footer, #recommended-books, #page_banner, script, noscript"):
                    el.decompose()
                
                # 이미지 경로를 절대 주소로 변환
                for img in content_div.find_all("img"):
                    src = img.get("src")
                    if src and not src.startswith("http"):
                        # /img/080251/028.jpg 형태로 오기 때문에 prefix를 붙여줍니다.
                        if src.startswith("/"):
                            img["src"] = f"https://thebook.io{src}"
                        elif src.startswith(".."):
                            clean_src = src.replace("../", "")
                            img["src"] = f"https://thebook.io/{clean_src}"
                        else:
                            img["src"] = f"https://thebook.io/img/{BOOK_ID}/{src}"
                
                # 본문 HTML 텍스트화
                content_html = str(content_div)
                
                # 로컬 캐시에 저장
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(content_html)
                    
                time.sleep(0.15)  # 서버 부하 방지를 위한 딜레이
                return content_html
            
    except urllib.error.HTTPError as he:
        print(f"❌ {page_num:04d}페이지 HTTP 에러 발생: {he.code} {he.reason}")
    except Exception as e:
        print(f"❌ {page_num:04d}페이지 수집 실패: {e}")
        
    return ""

# =====================================================================
# 🔍 4. 윈도우 크롬 / 엣지 브라우저 경로 검색 함수
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
# 🚀 5. 실행 제어 함수 (메인 로직)
# =====================================================================
def run_pdf_generator(test_mode=False):
    print("=" * 60)
    print("      🍊 thebook.io 도서 PDF 장별 생성기 (당목담글 개발용) 🍊")
    print("=" * 60)
    
    # 080251.css 다운로드 시도 (스타일 동적 연동용)
    print("🎨 기본 도서 스타일시트 수집 중...")
    css_content = ""
    try:
        css_url = f"https://thebook.io/css/book/{BOOK_ID}.css"
        req = urllib.request.Request(css_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=5) as res:
            css_content = f"<style>{res.read().decode('utf-8')}</style>"
            print("   ↳ 080251.css 다운로드 및 통합 완료!")
    except Exception as e:
        print(f"   ⚠️ 기본 CSS 다운로드 실패 ({e}), 인쇄 전용 CSS만 사용합니다.")

    # 브라우저 확인
    browser_path = find_browser_path()
    if not browser_path:
        print("\n⚠️ 시스템에서 Google Chrome 또는 Microsoft Edge를 찾을 수 없습니다.")
        print("👉 HTML 챕터 파일은 정상적으로 생성되나, PDF 변환은 수동(브라우저에서 직접 인쇄)으로 하셔야 합니다.\n")
    else:
        print(f"🎯 발견된 브라우저 엔진: {browser_path}")

    # 실행할 챕터 정의
    chapters_to_run = CHAPTERS
    if test_mode:
        print("\n🛠️ [테스트 모드 활성화] 1장(1~5페이지)만 시범적으로 수집 및 빌드합니다.")
        chapters_to_run = [{"name": "01장_Hello_Python_테스트", "start": 1, "end": 5}]

    for idx, chap in enumerate(chapters_to_run, 1):
        name = chap["name"]
        start = chap["start"]
        end = chap["end"]
        
        print(f"\n[{idx}/{len(chapters_to_run)}] {name} 작업 시작 ({start}p ~ {end}p)...")
        
        # 1. 챕터별 HTML 조각 모아서 단일 HTML 생성
        combined_fragments = []
        for p in range(start, end + 1):
            html_frag = get_page_html(p)
            if html_frag:
                # 각 조각을 구별할 수 있는 div로 감싸고, 페이지 번호 속성 부여
                wrapped_frag = f'<div class="book-page-fragment" data-page="{p}">\n{html_frag}\n</div>'
                combined_fragments.append(wrapped_frag)
            else:
                print(f"   ⚠️ {p:04d} 페이지가 누락되었습니다.")
        
        if not combined_fragments:
            print(f"❌ {name}에 수집된 페이지 내용이 없습니다. 다음 챕터로 넘어갑니다.")
            continue
            
        # 단일 완성형 HTML 조립
        chapter_html_content = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>{name}</title>
    {css_content}
    {PRINT_STYLE}
</head>
<body>
    <div class="thebook-content">
        {"".join(combined_fragments)}
    </div>
</body>
</html>
"""
        
        # HTML 파일 저장
        html_filename = f"{name}.html"
        html_path = os.path.join(CHAPTERS_DIR, html_filename)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(chapter_html_content)
            
        print(f"   ✓ HTML 파일 작성 완료: {html_path}")
        
        # 2. Chrome/Edge를 사용하여 PDF로 즉시 변환
        if browser_path:
            pdf_filename = f"{name}.pdf"
            pdf_path = os.path.abspath(os.path.join(PDF_DIR, pdf_filename))
            abs_html_path = os.path.abspath(html_path)
            
            # 크롬 프로필 락킹 방지를 위해 독립된 임시 프로필 폴더 설정
            profile_dir = os.path.abspath(os.path.join(CACHE_DIR, "chrome_profile"))
            # 로컬 HTML 파일을 URL 형식으로 변환 (경로의 백슬래시를 슬래시로 변경)
            file_url = "file:///" + abs_html_path.replace("\\", "/")
            
            # Chrome headless print command 실행
            # --no-pdf-header-footer 옵션으로 날짜, URL 등 브라우저 인쇄 기본 머리글/바닥글 제거
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
                print("   [Render] PDF 변환 엔진(브라우저) 실행 중...")
                # 대용량 페이지의 경우 다소 시간이 걸릴 수 있으므로 타임아웃을 30초로 설정
                subprocess.run(cmd, check=True, timeout=30, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"   ✓ PDF 생성 완료! ✨ -> {pdf_path}")
            except subprocess.TimeoutExpired:
                print("   ❌ PDF 변환 시간 초과 (브라우저가 응답하지 않습니다).")
                print("   👉 팁: 크롬 브라우저가 백그라운드에서 멈춰있을 수 있습니다. 작업 관리자에서 Chrome 프로세스를 모두 종료하거나")
                print("      명령 프롬프트에서 `taskkill /f /im chrome.exe` 또는 `taskkill /f /im msedge.exe`를 실행 후 다시 시도해 주세요.")
            except Exception as pe:
                print(f"   ❌ PDF 변환 중 에러 발생: {pe}")
        else:
            print("   👉 PDF 엔진이 없어 PDF 변환을 건너뜁니다.")

        # 각 장이 끝난 후 사용자 입력을 기다려 일시 중지
        if idx < len(chapters_to_run):
            print(f"\n📢 {name} 생성이 완료되었습니다.")
            try:
                input("👉 다음 챕터 작업을 진행하시려면 [엔터(Enter)] 키를 누르세요... (중단하려면 Ctrl+C)")
            except (KeyboardInterrupt, SystemExit):
                print("\n👋 사용자가 작업을 수동으로 중단했습니다.")
                sys.exit(0)

    print("\n" + "=" * 60)
    print("🎉 모든 작업이 성공적으로 완료되었습니다!")
    print(f"📂 병합된 HTML 파일 위치: .\\{CHAPTERS_DIR}\\")
    if browser_path:
        print(f"📂 최종 PDF 파일 위치: .\\{PDF_DIR}\\")
    print("=" * 60)

# 실행 진입점
if __name__ == "__main__":
    # 명령어 파라미터에 test가 포함되어 있으면 테스트 모드로 실행
    is_test = len(sys.argv) > 1 and sys.argv[1].lower() == "test"
    run_pdf_generator(test_mode=is_test)
