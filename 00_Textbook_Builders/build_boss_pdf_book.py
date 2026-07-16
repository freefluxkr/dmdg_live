import os
import re
import sys
import time
import urllib.request
import urllib.error
import subprocess
from bs4 import BeautifulSoup

# =====================================================================
# 📚 1. 책 챕터별 페이지 매핑 정의 (비연속 페이지 ID 반영)
# =====================================================================
CHAPTERS = [
    {
        "name": "Ch0_책_소개(집필_목적)",
        "pages": [135792, 149337]
    },
    {
        "name": "Ch1_목차_및_간략_소개",
        "pages": [135787, 141448, 141445, 141446]
    },
    {
        "name": "Ch2_개발환경_구축",
        "pages": [135781, 135796, 135786, 137959, 137954, 137962]
    },
    {
        "name": "Ch3_업무자동화_관련_패키지",
        "pages": [
            135735, 135788, 135795, 135793, 137969, 141571, 141480, 137927, 149360, 141534,
            135789, 141824, 137937, 157782, 137935, 135798, 153174, 153820, 157969, 156263,
            157756, 159159, 158161, 153821, 157980, 157981, 157982, 157983, 157984, 157985,
            149329, 141353, 153154, 149332, 153155, 149330, 153081, 153080, 153082, 153083,
            153084, 153085, 135790, 137921, 137922, 137923, 137925, 135794, 137919, 137929,
            141607, 137915, 142389, 137914, 149358, 142390, 137928, 153819, 155697, 137924,
            153818
        ]
    },
    {
        "name": "Ch4_업무자동화_프로젝트_사례",
        "pages": [
            152330, 156861, 156319, 151506, 155715, 153173, 153172, 173847, 149338
        ]
    }
]

BASE_URL = "https://wikidocs.net"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# 폴더 생성
CACHE_DIR = "html_cache_boss"
CHAPTERS_DIR = "html_parts_boss"
PDF_DIR = "사장님 몰래 하는 파이썬 업무자동화"

for directory in [CACHE_DIR, CHAPTERS_DIR, PDF_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# =====================================================================
# 🎨 2. 인쇄 및 화면 최적화 전용 CSS 스타일
# =====================================================================
PRINT_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&family=Fira+Code:wght@400;600&display=swap');

body {
    font-family: 'Nanum Gothic', 'Malgun Gothic', '맑은 고딕', sans-serif;
    font-size: 14px;
    line-height: 1.8;
    color: #2c3e50;
    margin: 0;
    padding: 2cm;
    background-color: #fff;
}

/* 개별 페이지 분할 */
.book-page-fragment {
    page-break-before: always;
    padding-top: 1cm;
}
.book-page-fragment:first-child {
    page-break-before: avoid;
    padding-top: 0;
}

/* 코드 블록 스타일 */
pre, code {
    font-family: 'Fira Code', Consolas, Monaco, monospace;
}
code {
    background-color: #f7f9fa;
    color: #e06c75;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-size: 0.9em;
}
pre code {
    background-color: transparent;
    color: inherit;
    padding: 0;
    border-radius: 0;
    font-size: 1em;
}
pre {
    background-color: #282c34;
    color: #abb2bf;
    padding: 1.2em;
    margin: 1.5em 0;
    border-radius: 6px;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-all;
    font-size: 0.9em;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

/* 인용구 스타일 */
blockquote {
    border-left: 4px solid #00adb5;
    background-color: #f8f9fa;
    padding: 1em 1.5em;
    margin: 1.5em 0;
    color: #555;
    font-style: italic;
    border-radius: 0 6px 6px 0;
}

/* 이미지 및 캡션 */
img {
    max-width: 90%;
    height: auto;
    display: block;
    margin: 1.5em auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-radius: 4px;
}

/* 테이블 스타일 */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5em 0;
    font-size: 0.95em;
}
table, th, td {
    border: 1px solid #e9ecef;
    padding: 0.8em;
}
th {
    background-color: #f1f3f5;
    font-weight: bold;
    color: #495057;
}
tr:nth-child(even) {
    background-color: #f8f9fa;
}

/* 제목 스타일 */
h1 {
    font-size: 2.2em;
    color: #1a202c;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 0.4em;
    margin-bottom: 1em;
}
h1.page-subject {
    font-size: 2.2em;
    color: #1a202c;
    margin-top: 0;
    margin-bottom: 0.2em;
    border-bottom: none;
    padding-bottom: 0;
}
.title-divider {
    border: none;
    border-top: 2px solid #00adb5;
    margin-bottom: 1.5em;
}
h2 {
    font-size: 1.6em;
    color: #2d3748;
    margin-top: 1.8em;
    margin-bottom: 0.8em;
    border-bottom: 1px solid #edf2f7;
    padding-bottom: 0.2em;
}
h3 {
    font-size: 1.25em;
    color: #4a5568;
    margin-top: 1.5em;
}

/* 인쇄 최적화 설정 */
@media print {
    body {
        padding: 0;
    }
    pre, blockquote, table, img, tr {
        page-break-inside: avoid;
    }
    h1, h2, h3 {
        page-break-after: avoid;
    }
}
</style>
"""

# =====================================================================
# 🕸️ 3. 개별 페이지 수집 및 캐싱 함수 (광고 차단 필터 및 제목 포함)
# =====================================================================
def get_page_html(page_id):
    """지정한 페이지 ID의 HTML 본문만 다운로드하거나 캐시에서 읽어옵니다."""
    cache_file = os.path.join(CACHE_DIR, f"{page_id}.html")
    
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read()
            
    # 로컬 캐시에 없는 경우 다운로드
    url = f"{BASE_URL}/{page_id}"
    headers = {"User-Agent": USER_AGENT}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        print(f"   [Crawl] {page_id} 페이지 다운로드 중... ({url})")
        with urllib.request.urlopen(req, timeout=10) as res:
            html = res.read()
            soup = BeautifulSoup(html, "html.parser")
            
            # WikiDocs 본문 영역 및 제목(page-subject) 탐색
            content_div = soup.select_one(".page-content, .wiki-content, #write_area")
            subject_h1 = soup.select_one(".page-subject, h1.page-subject")
            
            subject_title = ""
            if subject_h1:
                # 제목 텍스트만 깨끗하게 추출
                subject_text_el = subject_h1.select_one(".page-subject-text")
                if subject_text_el:
                    subject_title = subject_text_el.get_text().strip()
                else:
                    subject_title = subject_h1.get_text().strip()
            
            if not content_div:
                print(f"⚠️ {page_id}페이지 본문 영역을 찾을 수 없습니다. 전체 HTML을 사용합니다.")
                content_div = soup.body
                
            if content_div:
                # 팝업 배너, 구글 애드센스 광고, 스크립트 등 불필요한 태그 일체 제거
                ad_selectors = [
                    "script", "noscript", "iframe", "ins", 
                    ".adsbygoogle", "[class*='adsbygoogle']", "[id*='google_ads']",
                    ".ad", ".ads", ".advertisement", ".widget-ads",
                    ".newsletter-banner", "#back-to-top", ".top-parent", ".bottom-parent"
                ]
                for selector in ad_selectors:
                    for el in content_div.select(selector):
                        el.decompose()
                
                # 이미지 경로를 절대 주소로 변환
                for img in content_div.find_all("img"):
                    src = img.get("src")
                    if src and not src.startswith("http"):
                        if src.startswith("/"):
                            img["src"] = f"https://wikidocs.net{src}"
                        else:
                            img["src"] = f"https://wikidocs.net/{src}"
                
                # 본문 HTML 텍스트화
                content_html = str(content_div)
                
                # 제목이 존재하면 본문 맨 앞에 h1 제목과 구분선 삽입
                if subject_title:
                    title_html = f'<h1 class="page-subject">{subject_title}</h1>\n<hr class="title-divider"/>\n'
                    content_html = title_html + content_html
                
                # 로컬 캐시에 저장
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(content_html)
                    
                time.sleep(0.2)  # WikiDocs 서버 부하 방지를 위한 안정적 딜레이
                return content_html
            
    except urllib.error.HTTPError as he:
        print(f"❌ {page_id}페이지 HTTP 에러 발생: {he.code} {he.reason}")
    except Exception as e:
        print(f"❌ {page_id}페이지 수집 실패: {e}")
        
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
def run_pdf_generator(test_mode=False, pause_mode=False):
    print("=" * 60)
    print(" 🤖 WikiDocs '사장님 몰래 하는 파이썬 업무자동화' PDF 장별 생성기 🤖")
    print("=" * 60)

    # 브라우저 확인
    browser_path = find_browser_path()
    if not browser_path:
        print("\n⚠️ 시스템에서 Google Chrome 또는 Microsoft Edge를 찾을 수 없습니다.")
        print("👉 HTML 파일은 정상적으로 생성되나, PDF 변환은 수동으로 진행하셔야 합니다.\n")
    else:
        print(f"🎯 발견된 브라우저 엔진: {browser_path}")

    # 실행할 Chapter 정의
    chapters_to_run = CHAPTERS
    if test_mode:
        print("\n🛠️ [테스트 모드 활성화] Ch0의 첫 페이지(135792)만 시범적으로 수집 및 빌드합니다.")
        chapters_to_run = [{"name": "Ch0_책_소개_테스트", "pages": [135792]}]

    for idx, chap in enumerate(chapters_to_run, 1):
        name = chap["name"]
        pages = chap["pages"]
        
        print(f"\n[{idx}/{len(chapters_to_run)}] {name} 작업 시작 (총 {len(pages)}개 페이지)...")
        
        # 1. 챕터별 HTML 조각 모아서 단일 HTML 생성
        combined_fragments = []
        for p in pages:
            html_frag = get_page_html(p)
            if html_frag:
                wrapped_frag = f'<div class="book-page-fragment" data-page-id="{p}">\n{html_frag}\n</div>'
                combined_fragments.append(wrapped_frag)
            else:
                print(f"   ⚠️ {p} 페이지가 누락되었습니다.")
        
        if not combined_fragments:
            print(f"❌ {name}에 수집된 페이지 내용이 없습니다. 다음 장으로 넘어갑니다.")
            continue
            
        # 단일 완성형 HTML 조립
        chapter_html_content = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>{name}</title>
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
                print("   [Render] PDF 변환 엔진(브라우저) 실행 중...")
                subprocess.run(cmd, check=True, timeout=50, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"   ✓ PDF 생성 완료! ✨ -> {pdf_path}")
            except subprocess.TimeoutExpired:
                print("   ❌ PDF 변환 시간 초과 (브라우저가 응답하지 않습니다).")
                print("   👉 taskkill /f /im chrome.exe 명령어 등으로 백그라운드 프로세스를 정리 후 다시 시작해 주세요.")
            except Exception as pe:
                print(f"   ❌ PDF 변환 중 에러 발생: {pe}")
        else:
            print("   👉 PDF 엔진이 없어 PDF 변환을 건너뜁니다.")

        # 각 장이 끝난 후 일시 정지 모드가 활성화된 경우에만 대기
        if idx < len(chapters_to_run) and pause_mode:
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
    is_test = len(sys.argv) > 1 and "test" in [arg.lower() for arg in sys.argv]
    is_pause = len(sys.argv) > 1 and "pause" in [arg.lower() for arg in sys.argv]
    run_pdf_generator(test_mode=is_test, pause_mode=is_pause)
