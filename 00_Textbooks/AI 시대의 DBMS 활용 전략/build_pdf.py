import os
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import subprocess
from bs4 import BeautifulSoup

# =====================================================================
# 📂 1. 경로 정의 및 폴더 구성
# =====================================================================
# 본 스크립트가 위치한 폴더 기준
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(PROJECT_DIR, "images")
OUTPUT_HTML_PATH = os.path.join(PROJECT_DIR, "index.html")
OUTPUT_PDF_PATH = os.path.join(PROJECT_DIR, "AI_DBMS_Strategy.pdf")

# 캐시 HTML 파일 경로 (Antigravity IDE 캐시 경로)
CACHE_HTML_PATH = r"C:\Users\user\.gemini\antigravity-ide\brain\7093b3eb-6a71-4fe5-94c2-cdf191c08212\.system_generated\steps\232\content.md"

# 폴더 생성
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# =====================================================================
# 🎨 2. 고품질 프리미엄 전자책 CSS (Tibero Blue 테마)
# =====================================================================
PRINT_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Fira+Code:wght@400;500;600&display=swap');

/* A4 크기 및 여백 설정 */
@page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
}

body {
    font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif;
    font-size: 14px;
    line-height: 1.8;
    color: #2d3748;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
}

/* 전체 컨테이너 */
.book-container {
    max-width: 800px;
    margin: 0 auto;
}

/* 표지 스타일 */
.book-cover {
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 90vh;
    text-align: center;
    padding: 20px;
    box-sizing: border-box;
}

.book-cover h1 {
    font-size: 2.5em;
    line-height: 1.4;
    color: #1a202c;
    margin: 10px 0 30px 0;
    font-weight: 700;
    word-break: keep-all;
}

.book-cover .meta-info {
    font-size: 13px;
    color: #718096;
    margin-top: 40px;
    line-height: 1.6;
}

.book-cover .divider {
    width: 60px;
    height: 4px;
    background-color: #2525FF;
    margin: 20px auto;
}

/* 장 구분 및 페이지 나눔 */
.article-body {
    padding-top: 10px;
}

/* 제목 스타일 */
h2 {
    font-size: 1.6em;
    color: #1a202c;
    border-left: 5px solid #2525FF;
    padding-left: 12px;
    margin-top: 2em;
    margin-bottom: 0.8em;
    font-weight: 700;
}

h3 {
    font-size: 1.25em;
    color: #2d3748;
    margin-top: 1.8em;
    margin-bottom: 0.6em;
    font-weight: 600;
    border-bottom: 1px solid #edf2f7;
    padding-bottom: 6px;
}

h4 {
    font-size: 1.1em;
    color: #4a5568;
    margin-top: 1.5em;
    font-weight: 600;
}

p {
    margin-bottom: 1.2em;
    text-align: justify;
    word-break: break-all;
}

strong {
    font-weight: 700;
    color: #1a202c;
}

/* 이미지 및 캡션 */
figure {
    margin: 2em 0;
    text-align: center;
}

img {
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    display: block;
    margin: 0 auto;
}

figcaption {
    font-size: 12px;
    color: #718096;
    margin-top: 8px;
    text-align: center;
}

/* 인용구 스타일 */
blockquote {
    border-left: 4px solid #2525FF;
    background-color: #f7fafc;
    padding: 15px 20px;
    margin: 1.8em 0;
    border-radius: 0 6px 6px 0;
}

blockquote p {
    margin: 0;
    font-size: 13.5px;
    color: #4a5568;
}

/* 코드 블록 스타일 */
pre, code {
    font-family: 'Fira Code', Consolas, Monaco, monospace;
}

code {
    background-color: #edf2f7;
    color: #e53e3e;
    padding: 2px 5px;
    border-radius: 4px;
    font-size: 0.85em;
}

pre {
    background-color: #2e3440 !important; /* Nord Dark 배경색 강제 적용 */
    color: #d8dee9 !important;
    padding: 18px;
    margin: 1.8em 0;
    border-radius: 6px;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-all;
    font-size: 0.85em;
    line-height: 1.5;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

pre code {
    background-color: transparent;
    color: inherit;
    padding: 0;
    border-radius: 0;
    font-size: 1em;
}

/* 표(Table) 스타일 */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.8em 0;
    font-size: 13px;
}

table, th, td {
    border: 1px solid #e2e8f0;
    padding: 10px 12px;
}

th {
    background-color: #edf2f7;
    font-weight: 700;
    color: #2d3748;
    text-align: left;
}

tr:nth-child(even) {
    background-color: #f7fafc;
}

/* 링크 스타일 */
a {
    color: #262ACE;
    text-decoration: underline;
}

/* 인쇄 및 PDF 변환 최적화 */
@media print {
    body {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    .book-cover {
        height: 100vh;
    }
    pre, blockquote, table, figure, tr {
        page-break-inside: avoid;
    }
    h2, h3 {
        page-break-after: avoid;
    }
}
</style>
"""

# =====================================================================
# 🕸️ 3. 이미지 안전 다운로드 기능
# =====================================================================
def download_image(url, dest_folder):
    """한글 경로가 포함된 URL도 안전하게 인코딩하여 이미지를 다운로드합니다."""
    parsed = urllib.parse.urlparse(url)
    encoded_path = urllib.parse.quote(parsed.path)
    encoded_url = urllib.parse.urlunparse((
        parsed.scheme, parsed.netloc, encoded_path, 
        parsed.params, parsed.query, parsed.fragment
    ))
    
    # 디코딩하여 로컬에 저장할 원본 파일명 획득
    filename = os.path.basename(urllib.parse.unquote(parsed.path))
    if not filename:
        return None
        
    dest_path = os.path.join(dest_folder, filename)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(encoded_url, headers=headers)
    
    try:
        print(f"   [Download] 이미지 다운로드 중: {filename}")
        with urllib.request.urlopen(req, timeout=3) as response:
            with open(dest_path, "wb") as out_file:
                out_file.write(response.read())
        return filename
    except Exception as e:
        print(f"   ⚠️ 이미지 다운로드 실패: {url} | 에러: {e}")
        return None

# =====================================================================
# 🔍 4. 시스템 브라우저(Chrome/Edge) 탐색 기능
# =====================================================================
def find_browser_path():
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
# 🚀 5. 메인 실행 로직
# =====================================================================
def main():
    print("=" * 60)
    print("   📚 AI 시대의 DBMS 활용 전략 아티클 PDF 빌더 시작 📚")
    print("=" * 60)
    
    # 1. 웹 사이트에서 직접 크롤링 시도 (실패 시 로컬 백업 raw_blog_post.html 활용)
    target_url = "https://tmaxtibero.blog/ai-era-dbms-strategy/"
    backup_path = os.path.join(PROJECT_DIR, "raw_blog_post.html")
    raw_content = ""
    
    try:
        print(f"   [Crawl] 블로그 아티클 실시간 크롤링 중... ({target_url})")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        req = urllib.request.Request(target_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            raw_content = res.read().decode("utf-8")
        
        # 최신본을 로컬에 백업 저장
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(raw_content)
        print(f"✓ 실시간 크롤링 완료 및 백업 저장 완료: {backup_path}")
    except Exception as ce:
        print(f"⚠️ 실시간 크롤링 실패 (오프라인 혹은 네트워크 에러): {ce}")
        # 실패 시 로컬 캐시 또는 기존 백업본 사용 시도
        if os.path.exists(backup_path):
            print(f"👉 로컬 백업본({backup_path})을 사용하여 작업을 계속합니다.")
            with open(backup_path, "r", encoding="utf-8") as f:
                raw_content = f.read()
        elif os.path.exists(CACHE_HTML_PATH):
            print(f"👉 Antigravity IDE 캐시 파일({CACHE_HTML_PATH})을 사용하여 작업을 계속합니다.")
            with open(CACHE_HTML_PATH, "r", encoding="utf-8") as f:
                raw_content = f.read()
        else:
            print("❌ 크롤링할 수 없고 로컬 백업본이나 캐시 파일도 존재하지 않습니다.")
            sys.exit(1)

    # 3. HTML 파싱 및 본문 기사 추출
    soup = BeautifulSoup(raw_content, "html.parser")
    article = soup.find("article", id="post-7978")
    if not article:
        print("⚠️ article#post-7978 요소를 찾을 수 없어 전체 HTML에서 <article> 태그를 탐색합니다.")
        article = soup.find("article")
        
    if not article:
        print("❌ 본문 <article> 영역을 찾을 수 없습니다.")
        sys.exit(1)

    print("✓ 기사 본문 영역 추출 성공!")

    # 4. 불필요한 노이즈 요소 제거 (공유 버튼 등)
    noise_selectors = [
        "script", "noscript", ".single-share-box-container", 
        ".single-author-box-container", ".single-next-prev-posts-container",
        ".comments-container", "input", "button", ".jet-container__overlay"
    ]
    for selector in noise_selectors:
        for tag in article.select(selector):
            tag.decompose()

    # 4-2. 특정 인트로 단락 및 관련 링크 삭제 (요구사항 반영)
    for p in article.find_all("p"):
        p_text = p.get_text()
        if ("DB Lock-in 탈피 전략" in p_text or 
            "Oracle 전환을 위한 현실적인 전략" in p_text or 
            "ULA 기반 통합 DB 전략" in p_text or 
            "이번 글에서 주목할 점은 다음과 같습니다." in p_text):
            p.decompose()

    # 5. 본문 이미지 다운로드 및 로컬 경로 치환
    img_tags = article.find_all("img")
    print(f"🔍 본문 내 이미지 탐색 완료 (총 {len(img_tags)}개)")
    
    for img in img_tags:
        src = img.get("src")
        if not src:
            continue
            
        # 블로그 원본이 상대 경로 혹은 absolute path인 경우 보정
        if src.startswith("/"):
            src = "https://tmaxtibero.blog" + src
        elif not src.startswith("http"):
            src = "https://tmaxtibero.blog/" + src
            
        # mycafe24.com 도메인은 티베로 공식 블로그 도메인으로 치환하여 다운로드 딜레이 방지
        if "tibero26.mycafe24.com" in src:
            src = src.replace("http://tibero26.mycafe24.com", "https://blog.tibero.com")
            
        # 이미지 다운로드 실행
        local_filename = download_image(src, IMAGES_DIR)
        if local_filename:
            # HTML 소스 내의 경로를 상대경로로 치환
            img["src"] = f"images/{local_filename}"
            # 불필요한 속성 정리
            if "srcset" in img.attrs:
                del img["srcset"]
            if "sizes" in img.attrs:
                del img["sizes"]
            print(f"   ✓ 치환 완료: {src} -> images/{local_filename}")

    # 6. 프리미엄 완성형 HTML 조립 (추가 내용 편집 및 주입)
    title_text = "AI 시대의 DBMS 활용 전략"
    
    # 추가 편집하고 싶은 설명 단락 구성
    edited_addition_html = """
    <div class="editor-note" style="margin-top: 3em; border-top: 2px dashed #2525FF; padding-top: 1.5em; page-break-before: always;">
        <h2 class="wp-block-heading" style="font-size: 22px; color: #2525FF;"><strong>💡 [추가 해설] AI 시대 DBMS 선정을 위한 요약 및 조언</strong></h2>
        <p class="wp-block-paragraph">오픈소스 OpenSQL의 <strong>Pgvector/PgvectorScale</strong>과 상용 <strong>Tibero</strong>는 서로 대립하는 솔루션이 아니라, 기업의 인프라 성숙도와 요구되는 보안 통제 레벨에 따라 유연하게 선택 및 병행할 수 있는 상호 보완적 도구입니다.</p>
        
        <blockquote class="wp-block-quote">
            <p><strong>비용 효율성과 최신 오픈 API 호환성이 중요하다면?</strong><br>
            LangChain, LlamaIndex 등 최신 LLM 생태계와 신속하게 연동되는 오픈소스 기반 <strong>OpenSQL(pgvector)</strong>로 신속한 PoC 및 경량 RAG를 구축하는 것이 실용적입니다.</p>
        </blockquote>
        
        <blockquote class="wp-block-quote">
            <p><strong>트랜잭션 무결성과 데이터 보안 거버넌스가 최우선인 금융·공공·의료 도메인이라면?</strong><br>
            기존 업무 조건(OLTP)과 벡터 검색이 자연스럽게 결합되는 <strong>Hybrid Search</strong> 기능을 지원하고, 접근 권한 통제가 내재화된 상용 <strong>Tibero DBMS</strong>로 전환하여 안정적으로 실서비스에 투입하는 전략이 유효합니다.</p>
        </blockquote>
    </div>
    """
    
    # 본문 뒤에 추가 내용 주입
    article_str = str(article) + edited_addition_html
    
    combined_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>{title_text}</title>
    {PRINT_STYLE}
</head>
<body>
    <div class="book-container">
        <!-- 📘 1. 프리미엄 커버 (표지) -->
        <div class="book-cover">
            <div class="divider"></div>
            <h1>AI 시대의<br>DBMS 활용 전략</h1>
            <div class="divider"></div>
            <div class="meta-info">
                <strong>출처</strong>: TmaxTibero 공식 블로그<br>
                <strong>발행일</strong>: 2026년 04월 08일
            </div>
        </div>

        <!-- 📖 2. 본문 컨텐츠 -->
        <div class="article-body">
            {article_str}
        </div>
    </div>
</body>
</html>
"""

    with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(combined_html)
    print(f"✓ 완성형 HTML 빌드 성공! -> {OUTPUT_HTML_PATH}")

    # 7. Chrome/Edge를 사용하여 PDF 변환 시도
    browser_path = find_browser_path()
    if not browser_path:
        print("\n⚠️ 시스템에서 Google Chrome 또는 Microsoft Edge 브라우저를 찾을 수 없습니다.")
        print("👉 생성된 index.html을 브라우저에서 여신 후, [인쇄(Ctrl+P) -> PDF로 저장]을 진행해주세요.\n")
        sys.exit(0)

    print(f"✓ PDF 변환 엔진 발견: {browser_path}")
    profile_dir = os.path.join(PROJECT_DIR, "chrome_profile")
    file_url = "file:///" + OUTPUT_HTML_PATH.replace("\\", "/")

    cmd = [
        browser_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--user-data-dir={profile_dir}",
        f"--print-to-pdf={OUTPUT_PDF_PATH}",
        "--no-pdf-header-footer",
        file_url
    ]

    try:
        print("   [Render] Headless 브라우저 구동하여 PDF 렌더링 중...")
        subprocess.run(cmd, check=True, timeout=40, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"\n✨ PDF 전자책 생성 성공! ✨\n📂 저장 위치: {OUTPUT_PDF_PATH}")
    except Exception as pe:
        print(f"\n❌ PDF 변환 중 에러 발생: {pe}")
        print("👉 생성된 index.html 파일은 정상적이므로 수동으로 브라우저를 통해 PDF 저장을 진행하실 수 있습니다.")

    print("=" * 60)

if __name__ == "__main__":
    main()
