import os
import re
import sys
import time
import urllib.request
import urllib.error
import subprocess
from bs4 import BeautifulSoup

# =====================================================================
# 📦 의존성 검사 및 자동 설치
# =====================================================================
def check_dependencies():
    dependencies = {
        "bs4": "beautifulsoup4"
    }
    for module_name, pip_name in dependencies.items():
        try:
            __import__(module_name)
        except ImportError:
            print(f"💡 [Dependency] '{pip_name}' 라이브러리가 없습니다. 자동 설치를 시작합니다...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", pip_name], check=True)
                print(f"✓ '{pip_name}' 설치 완료.")
            except Exception as e:
                print(f"❌ 라이브러리 설치 실패: {e}")
                print(f"👉 수동 설치 명령어: pip install {pip_name}")
                sys.exit(1)

check_dependencies()

# =====================================================================
# 📚 기본 설정 변수
# =====================================================================
BOOK_ID = "080212"
BASE_URL = f"https://thebook.io/{BOOK_ID}"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# 폴더 설정
CACHE_DIR = "html_cache_git"
CHAPTERS_DIR = "html_chapters_git"
OUTPUT_DIR = "Git"

for directory in [CACHE_DIR, CHAPTERS_DIR, OUTPUT_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# =====================================================================
# 🎨 인쇄 및 화면 최적화 전용 CSS 스타일
# =====================================================================
PRINT_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&family=Fira+Code:wght@400;600&display=swap');

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
    font-family: 'Fira Code', 'Source Code Pro', Consolas, Monaco, monospace;
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
# 🕸️ 목차 분석 및 챕터 구조 생성
# =====================================================================
def parse_table_of_contents():
    """책의 메인 페이지에서 목차를 파싱하여 장(Chapter) 및 페이지 목록을 동적으로 구성합니다.
    0619 페이지(자주 사용하는 명령어 모음)까지만 분석합니다."""
    print("🌐 목차(TOC) 분석을 위해 책 메인 페이지를 읽는 중...")
    headers = {"User-Agent": USER_AGENT}
    req = urllib.request.Request(BASE_URL, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            html = res.read()
            soup = BeautifulSoup(html, "html.parser")
            
            # 목차 목록 탐색
            toc_list = soup.select_one("ul#toc, .book-toc")
            if not toc_list:
                print("❌ 에러: 목차(TOC) 영역을 찾을 수 없습니다.")
                sys.exit(1)
                
            chapters = []
            current_chapter = None
            chapter_index = 0
            
            # 목차 내 모든 링크 a 태그 순회
            links = toc_list.find_all("a")
            for link in links:
                href = link.get("href", "")
                text = link.get_text(strip=True)
                
                # URL에서 4자리 페이지 ID 추출 (예: /080212/0002/ -> 0002)
                page_match = re.search(rf"/{BOOK_ID}/(\d{{4}})", href)
                if not page_match:
                    continue
                    
                page_id = page_match.group(1)
                
                # 부모 li 태그의 클래스를 통해 계층 파악
                parent_li = link.find_parent("li")
                classes = parent_li.get("class", []) if parent_li else []
                
                # h2가 시작되거나 최종 '0619' 페이지인 경우 새로운 장으로 정의
                is_new_chapter = "h2" in classes or page_id == "0619"
                
                if is_new_chapter:
                    if current_chapter:
                        chapters.append(current_chapter)
                        
                    chapter_index += 1
                    # 파일명에 유효하지 않은 특수문자 제거
                    clean_text = re.sub(r'[\/:*?"<>|•?]', '_', text)
                    clean_text = re.sub(r'\s+', '_', clean_text).strip('_')
                    chapter_name = f"{chapter_index:02d}_{clean_text}"
                    
                    current_chapter = {
                        "name": chapter_name,
                        "pages": [page_id]
                    }
                else:
                    if current_chapter:
                        if page_id not in current_chapter["pages"]:
                            current_chapter["pages"].append(page_id)
                
                # 0619 페이지를 만나면 목차 수집 완료
                if page_id == "0619":
                    break
            
            # 마지막 장 추가
            if current_chapter and current_chapter not in chapters:
                chapters.append(current_chapter)
                
            print(f"✓ 총 {len(chapters)}개의 장이 식별되었습니다.")
            return chapters
            
    except Exception as e:
        print(f"❌ 목차 분석 실패: {e}")
        sys.exit(1)

# =====================================================================
# 🛠️ 구버전 정보 최신화 함수 (master -> main, PAT 토큰 설명 삽입)
# =====================================================================
def clean_html_content(content_html, page_id):
    """HTML 본문에서 낡은 정보들을 최신화하고 정보/주의 박스를 삽입합니다."""
    soup = BeautifulSoup(content_html, "html.parser")
    
    # 1. 텍스트 및 코드 안의 'master' 키워드를 'main'으로 대체
    # HTML 태그 속성(예: img src)을 건드리지 않기 위해 string 노드만 대상으로 치환합니다.
    for text_node in soup.find_all(text=True):
        if text_node.parent and text_node.parent.name in ['script', 'style']:
            continue
        original = text_node.string
        if original:
            replaced = original
            # master 브랜치명 교체
            replaced = replaced.replace("master 브랜치", "main 브랜치")
            replaced = replaced.replace("master(마스터) 브랜치", "main 브랜치")
            replaced = replaced.replace("마스터 브랜치", "main 브랜치")
            replaced = replaced.replace("마스터(master) 브랜치", "main 브랜치")
            
            # 깃 명령어 및 옵션 교체
            replaced = replaced.replace("origin master", "origin main")
            replaced = replaced.replace("checkout master", "checkout main")
            replaced = replaced.replace("push -u origin master", "push -u origin main")
            replaced = replaced.replace("merge master", "merge main")
            replaced = replaced.replace("rebase master", "rebase main")
            
            # 일반적인 master 단어 교체 (단, 이미지 URL 깨짐 방지를 위해 속성이 아닌 텍스트만)
            replaced = replaced.replace("master", "main")
            replaced = replaced.replace("마스터", "main(마스터)")
            
            if replaced != original:
                text_node.replace_with(replaced)
                
    # 2. 5장 깃허브 가입 및 연동 과정 (특히 원격 등록 및 push 단계인 page_id 0187, 0199 부근)
    # 깃허브 비밀번호 로그인 차단에 따른 Personal Access Token (PAT) 강제 경고문 추가
    if page_id in ["0187", "0199"]:
        pat_tip_html = """
        <div class="highlight" style="border-left: 4px solid #f0ad4e; background-color: #fcf8e3; padding: 15px; margin: 20px 0; border-radius: 6px; font-family: sans-serif; font-size: 0.95em; color: #333;">
            <strong style="color: #c09853; font-size: 1.1em;">⚠️ [최신 깃허브 정책 중요 안내] 비밀번호 로그인 차단 및 PAT 인증 필수</strong><br/>
            현재 GitHub은 보안상의 이유로 계정 패스워드를 통한 HTTPS 인증을 완전히 차단했습니다.<br/>
            터미널이나 소스트리(SourceTree)에서 원격 로그인(비밀번호 입력)을 요구받는 경우, 기존 비밀번호 대신 반드시 <strong>Personal Access Token (PAT)</strong>을 비밀번호 란에 입력해야 합니다.<br/>
            <br/>
            <strong>🔗 토큰 발급 방법:</strong><br/>
            GitHub 우측 상단 프로필 이미지 클릭 ➔ <strong>Settings</strong> ➔ 왼쪽 최하단 <strong>Developer Settings</strong> ➔ <strong>Personal Access Tokens</strong> (Classic 또는 Fine-grained) ➔ <strong>Generate new token</strong> 실행 (필요한 repo 권한 체크 후 생성 및 토큰 값을 복사하여 비밀번호란에 붙여넣기)<br/>
            <a href="https://github.com/settings/tokens" target="_blank" style="color: #2b547e; font-weight: bold; text-decoration: underline;">👉 GitHub 토큰 관리 페이지 바로가기</a>
        </div>
        """
        pat_tip_soup = BeautifulSoup(pat_tip_html, "html.parser")
        # 문서 상단에 삽입
        if soup.contents:
            soup.insert(0, pat_tip_soup)
        else:
            soup.append(pat_tip_soup)
            
    # 3. 기본 브랜치 개념 설명 부근 (0229)
    # 기본 브랜치가 master에서 main으로 변경되었음에 관한 보충 박스 추가
    if page_id in ["0229"]:
        branch_tip_html = """
        <div class="highlight" style="border-left: 4px solid #5bc0de; background-color: #f0f8ff; padding: 15px; margin: 20px 0; border-radius: 6px; font-family: sans-serif; font-size: 0.95em; color: #333;">
            <strong style="color: #31708f; font-size: 1.1em;">💡 [참고] GitHub 기본 브랜치 기본값 변경 (master ➔ main)</strong><br/>
            2020년 10월 이후부터 GitHub을 포함한 대부분의 버전 관리 플랫폼은 새로 생성하는 저장소의 기본 브랜치명을 기존의 <code>master</code>에서 <code>main</code>으로 기본 변경하였습니다.<br/>
            본 교재에서 자동 가공된 명령어 예시들은 <code>main</code> 브랜치로 최신화되어 출력되나, 구버전 Git 클라이언트를 사용하시는 경우 로컬 저장소 생성 시 기본 브랜치가 <code>master</code>로 잡힐 수 있습니다. <br/>
            로컬 브랜치명을 main으로 일치시키기 위해 <code>git branch -M main</code> 명령어를 활용하시기 바랍니다.
        </div>
        """
        branch_tip_soup = BeautifulSoup(branch_tip_html, "html.parser")
        if soup.contents:
            soup.insert(0, branch_tip_soup)
        else:
            soup.append(branch_tip_soup)
            
    return str(soup)

# =====================================================================
# 🕸️ 개별 페이지 수집 및 캐싱
# =====================================================================
def get_page_html(page_id):
    """지정한 페이지 번호의 HTML 본문을 다운로드하거나 캐시에서 읽은 뒤, 최신화 처리를 거쳐 반환합니다."""
    cache_file = os.path.join(CACHE_DIR, f"{page_id}.html")
    
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            raw_html = f.read()
            return clean_html_content(raw_html, page_id)
            
    url = f"{BASE_URL}/{page_id}/"
    headers = {"User-Agent": USER_AGENT}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        print(f"   [Crawl] {page_id} 페이지 다운로드 중... ({url})")
        with urllib.request.urlopen(req, timeout=10) as res:
            html = res.read()
            soup = BeautifulSoup(html, "html.parser")
            
            content_div = soup.select_one(".thebook-content, #page_content")
            if not content_div:
                content_div = soup.body
                
            if content_div:
                # 불필요한 태그 제거
                for el in content_div.select(".newsletter-banner, .gas, .mdl-mega-footer, #recommended-books, #page_banner, script, noscript"):
                    el.decompose()
                
                # 이미지 경로를 절대 주소로 변환
                for img in content_div.find_all("img"):
                    src = img.get("src")
                    if src and not src.startswith("http"):
                        if src.startswith("/"):
                            img["src"] = f"https://thebook.io{src}"
                        elif src.startswith(".."):
                            clean_src = src.replace("../", "")
                            img["src"] = f"https://thebook.io/{clean_src}"
                        else:
                            img["src"] = f"https://thebook.io/img/{BOOK_ID}/{src}"
                
                content_html = str(content_div)
                
                # 원본 다운로드 저장 (캐시)
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(content_html)
                    
                time.sleep(0.3)  # 서버 부담을 줄이기 위한 딜레이
                return clean_html_content(content_html, page_id)
            
    except urllib.error.HTTPError as he:
        print(f"   ❌ {page_id} 페이지 HTTP 에러: {he.code} {he.reason}")
    except Exception as e:
        print(f"   ❌ {page_id} 페이지 수집 실패: {e}")
        
    return ""

# =====================================================================
# 🔍 브라우저 검색
# =====================================================================
def find_browser_path():
    """시스템에서 Chrome 또는 Edge 브라우저 실행 파일의 위치를 찾아 반환합니다."""
    candidate_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe")
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            return path
    return None

# =====================================================================
# 🚀 메인 실행 제어기
# =====================================================================
def main():
    print("=" * 60)
    print("🚀 Git 교과서 PDF 책 빌더 및 최신화 프로세스 시작")
    print("=" * 60)
    
    # 1. 브라우저 엔진 탐색
    browser_path = find_browser_path()
    if not browser_path:
        print("❌ 에러: 시스템에서 Google Chrome 또는 Microsoft Edge를 찾을 수 없습니다.")
        sys.exit(1)
    print(f"🎯 발견된 브라우저 엔진: {browser_path}")
    
    # 2. 목차 분석
    chapters = parse_table_of_contents()
    
    # 3. 각 장별 페이지 다운로드 및 병합
    print("\n" + "=" * 60)
    print("📥 1단계: 각 장의 페이지 수집, 본문 최신화 및 HTML 병합 시작")
    print("=" * 60)
    
    merged_chapters = []
    for idx, chapter in enumerate(chapters):
        print(f"\n[{idx+1}/{len(chapters)}] 📁 장 준비 중: {chapter['name']}")
        
        chapter_html_contents = []
        for page_id in chapter["pages"]:
            page_content = get_page_html(page_id)
            if page_content:
                wrapped_page = f'<div class="book-page-fragment">{page_content}</div>'
                chapter_html_contents.append(wrapped_page)
                
        if not chapter_html_contents:
            print(f"⚠️ 경고: {chapter['name']}에 유효한 페이지가 없어 건너뜁니다.")
            continue
            
        # 단일 장(Chapter) HTML 완성
        merged_body = "\n".join(chapter_html_contents)
        full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>{chapter['name']}</title>
    {PRINT_STYLE}
</head>
<body>
    {merged_body}
</body>
</html>
"""
        
        # 파일 저장
        chapter_html_filename = f"{chapter['name']}.html"
        chapter_html_path = os.path.join(CHAPTERS_DIR, chapter_html_filename)
        with open(chapter_html_path, "w", encoding="utf-8") as f:
            f.write(full_html)
            
        merged_chapters.append({
            "name": chapter["name"],
            "html_path": os.path.abspath(chapter_html_path)
        })
        print(f"   ✓ HTML 최신화 및 병합 완료 -> {chapter_html_path}")
        
    # 4. Chrome Headless를 활용한 PDF 변환
    print("\n" + "=" * 60)
    print("🖨️ 2단계: 크롬 헤드리스 기반 개별 PDF 변환 시작")
    print("=" * 60)
    
    success_count = 0
    for idx, mc in enumerate(merged_chapters):
        pdf_filename = f"{mc['name']}.pdf"
        pdf_path = os.path.abspath(os.path.join(OUTPUT_DIR, pdf_filename))
        file_url = "file:///" + mc["html_path"].replace("\\", "/")
        profile_dir = os.path.abspath(os.path.join(CACHE_DIR, f"profile_{mc['name']}"))
        
        print(f"\n[{idx+1}/{len(merged_chapters)}] 🖨️ PDF 인쇄 중: {pdf_filename}")
        
        # Chrome/Edge PDF 생성 명령
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
            # 윈도우에서 안전하게 subprocess 실행하기 위해 shell=True 적용
            subprocess.run(cmd, shell=True, check=True, timeout=40, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"   ✨ PDF 변환 완료 -> {pdf_path}")
            success_count += 1
        except Exception as e:
            print(f"   ❌ PDF 변환 중 에러 발생: {e}")
            
    print("\n" + "=" * 60)
    print(f"🎉 모든 작업이 완료되었습니다! 총 {success_count}/{len(merged_chapters)}개 PDF 생성 완료.")
    print(f"📂 최종 출력 폴더: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
