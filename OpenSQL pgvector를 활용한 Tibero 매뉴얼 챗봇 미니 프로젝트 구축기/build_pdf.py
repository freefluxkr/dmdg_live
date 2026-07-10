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
OUTPUT_PDF_PATH = os.path.join(PROJECT_DIR, "OpenSQL_pgvector_Tibero_Chatbot_Manual.pdf")

# 캐시 HTML 파일 경로 (Antigravity IDE 캐시 경로)
CACHE_HTML_PATH = r"C:\Users\user\.gemini\antigravity-ide\brain\7093b3eb-6a71-4fe5-94c2-cdf191c08212\.system_generated\steps\160\content.md"
# 만약 위의 캐시가 없을 경우 이전 단계 143의 캐시도 체크
CACHE_HTML_PATH_ALT = r"C:\Users\user\.gemini\antigravity-ide\brain\7093b3eb-6a71-4fe5-94c2-cdf191c08212\.system_generated\steps\143\content.md"

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

.book-cover .brand {
    font-size: 14px;
    font-weight: 700;
    color: #2525FF;
    letter-spacing: 0.15em;
    margin-bottom: 20px;
    text-transform: uppercase;
}

.book-cover h1 {
    font-size: 2.2em;
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
        with urllib.request.urlopen(req, timeout=10) as response:
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
    print("   📚 Tibero 매뉴얼 챗봇 RAG 아티클 PDF 고품질 빌더 시작 📚")
    print("=" * 60)
    
    # 1. 원본 캐시 파일 읽기
    cache_path = CACHE_HTML_PATH
    if not os.path.exists(cache_path):
        cache_path = CACHE_HTML_PATH_ALT
        
    if not os.path.exists(cache_path):
        print(f"❌ 원본 캐시 파일을 찾을 수 없습니다. 경로를 확인해주세요.\n경로: {CACHE_HTML_PATH}")
        sys.exit(1)
        
    print(f"✓ 캐시 파일 로드 완료: {cache_path}")
    with open(cache_path, "r", encoding="utf-8") as f:
        raw_content = f.read()

    # 2. 프로젝트 내에 백업본 복사 저장
    backup_path = os.path.join(PROJECT_DIR, "raw_blog_post.html")
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(raw_content)
    print(f"✓ 원본 백업본 복사 완료: {backup_path}")

    # 3. HTML 파싱 및 본문 기사 추출
    soup = BeautifulSoup(raw_content, "html.parser")
    article = soup.find("article", id="post-8109")
    if not article:
        print("⚠️ article#post-8109 요소를 찾을 수 없어 전체 HTML에서 <article> 태그를 탐색합니다.")
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

    # 작성자 정보 단락 삭제 (18페이지 요구사항 반영)
    for p in article.find_all("p"):
        p_text = p.get_text()
        if "주영지" in p_text or "한영주" in p_text or "Sales Consulting" in p_text:
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

    # 6. 프리미엄 완성형 HTML 조립 (진입장벽 4가지 내용 주입)
    title_text = "OpenSQL pgvector를 활용한 Tibero 매뉴얼 챗봇 미니 프로젝트 구축기"
    
    # 4가지 핵심 진입 장벽 상세 설명 추가
    barrier_html = """
    <div class="barriers-section" style="margin-top: 3em; page-break-before: always;">
        <h2 class="wp-block-heading" style="font-size: 25px;"><strong><span style="text-decoration: underline;">[심층 분석] 프로젝트 구현을 위한 4가지 핵심 진입 장벽</span></strong></h2>
        <p class="wp-block-paragraph">본 RAG 챗봇 미니 프로젝트는 현업 수준의 높은 완성도를 지향하고 있어, 일반 개발 입문자나 인프라 지식이 부족한 비전공자가 직접 구현하기에는 몇 가지 뚜렷한 기술적 장벽이 존재합니다. 실무 적용 시 고려해야 할 4대 진입 장벽은 다음과 같습니다.</p>
        
        <h3 class="wp-block-heading" style="font-size: 20px;">1. 복잡한 DBMS 인프라 및 빌드 구성</h3>
        <p class="wp-block-paragraph">OpenSQL을 VectorDB로 활용하려면 pgvector와 pgvectorscale 모듈 설치가 필요합니다. 이는 단순히 패키지를 다운로드하는 수준을 넘어, 리눅스 VM 환경에 대한 깊은 이해와 쉘 스크립트 실행, 그리고 C 컴파일러 및 빌드 의존성 해결 능력을 요구합니다. 특히 가속기(AVX-512) 제한이 있는 VM 환경의 경우 pgvectorscale 모듈 설치 자체가 불가능할 수 있어 인프라 구성 단계에서 포기하기 쉽습니다.</p>
        
        <h3 class="wp-block-heading" style="font-size: 20px;">2. 데이터베이스 관리자(Superuser) 권한 획득 문제</h3>
        <p class="wp-block-paragraph">데이터베이스 내에 확장 모듈(Extension)을 등록하는 CREATE EXTENSION 명령어는 오직 데이터베이스의 최고 관리자(Superuser)인 'postgres' 계정 권한으로만 실행 가능합니다. 사내 공유 DB나 관리 권한이 엄격히 통제되는 엔터프라이즈 클라우드 환경에서는 일반 개발자가 이 권한을 직접 획득할 수 없어, 초기 확장 기능 활성화 단계가 커다란 조직적·기술적 허들로 작용합니다. (※ 참고: 본 권한은 티베로 DBMS의 SYS/SYSTEM 관리자 권한이 아닌, PostgreSQL 기반의 OpenSQL 슈퍼유저 권한을 의미합니다.)</p>
        
        <h3 class="wp-block-heading" style="font-size: 20px;">3. 문서 구조화와 OCR 기반의 까다로운 전처리</h3>
        <p class="wp-block-paragraph">RAG 시스템의 성능은 '쓰레기가 들어가면 쓰레기가 나온다(Garbage In, Garbage Out)'는 말처럼 입력 데이터의 정제도에 크게 의존합니다. 아티클에 사용된 Tibero 매뉴얼은 표(Table)와 다이어그램이 가득한 기술 문서입니다. 단순 PyPDF로 읽으면 텍스트가 조각나고 표 구조가 깨져 답변 퀄리티가 무너집니다. 이를 극복하려면 PaddleOCR과 OpenDataLoaderPDF의 하이브리드 모드를 정교하게 코드로 결합하여 레이아웃을 보존한 마크다운을 추출해야 하는데, 이 전처리 코드를 조율하는 난이도가 매우 높습니다.</p>
        
        <h3 class="wp-block-heading" style="font-size: 20px;">4. 검색 파이프라인 고도화(Hybrid Search & Re-rank) 튜닝</h3>
        <p class="wp-block-paragraph">단순 벡터 유사도 검색만으로는 질문의 세밀한 키워드 매칭을 놓치기 쉽습니다. 따라서 BM25 키워드 검색과 코사인 거리 벡터 검색을 가중치별로 연산하는 Hybrid Search 쿼리를 작성하고, 그 결과로 추출된 상위 결과 중 질문에 가장 밀접한 내용만 선별하기 위해 CrossEncoder 딥러닝 모델 기반의 Re-rank(재정렬) 파이프라인을 추가해야 합니다. 이 전체 파이프라인(LangChain, psycopg3, sentence_transformers)을 완벽히 통합하고 최적화하는 데는 수준 높은 백엔드 및 AI 엔지니어링 역량이 필요합니다.</p>
    </div>
    """
    
    # article 본문 마지막에 추가
    article_str = str(article) + barrier_html

    # 표지 및 메인 조립
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
            <h1>OpenSQL pgvector를 활용한<br>Tibero 매뉴얼 챗봇 미니 프로젝트 구축기</h1>
            <div class="divider"></div>
            <div class="meta-info">
                <strong>출처</strong>: TmaxTibero 공식 블로그<br>
                <strong>발행일</strong>: 2026년 04월 27일
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

    # =====================================================================
    # 📘 6-2. 일반인 테스트용 우회 대안 HTML 조립 (본문과 대안 꿀팁 및 실습 코드 결합)
    # =====================================================================
    ALT_HTML_PATH = os.path.join(PROJECT_DIR, "alternative.html")
    ALT_PDF_PATH = os.path.join(PROJECT_DIR, "일반인이 테스트.pdf")
    
    # BeautifulSoup을 이용하여 본문 복제 및 섹션별 팁 박스 주입
    alt_soup = BeautifulSoup(str(article), "html.parser")

    # 일반인 우회 대안 스택용 코드 블록 정의
    SUPABASE_EXT_CODE = """
<div class="wp-block-kevinbatdorf-code-block-pro" data-code-block-pro-font-family="Code-Pro-JetBrains-Mono" style="font-size: .75rem; font-family: Code-Pro-JetBrains-Mono,ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace; line-height: 1.25rem;">
<pre class="shiki nord" style="background-color: #2e3440ff; color: #d8dee9ff; padding: 18px; border-radius: 6px;" tabindex="0"><code><span class="line"><span style="color: #d8dee9ff;">-- Supabase SQL Editor에서 실행하여 pgvector 활성화 및 테이블 생성</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">CREATE EXTENSION IF NOT EXISTS</span> <span style="color: #8fbcbb;">vector</span><span style="color: #81a1c1;">;</span></span>
<span class="line"></span>
<span class="line"><span style="color: #d8dee9ff;">-- 1. 벡터 및 문서 데이터를 저장할 테이블 생성</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">CREATE TABLE</span> <span style="color: #d8dee9;">documents</span> <span style="color: #d8dee9ff;">(</span></span>
<span class="line"><span style="color: #d8dee9;">    id</span> <span style="color: #b48ead;">bigserial</span> <span style="color: #81a1c1; font-weight: bold;">PRIMARY KEY</span><span style="color: #d8dee9ff;">,</span></span>
<span class="line"><span style="color: #d8dee9;">    content</span> <span style="color: #b48ead;">text</span><span style="color: #d8dee9ff;">,</span></span>
<span class="line"><span style="color: #d8dee9;">    metadata</span> <span style="color: #b48ead;">jsonb</span><span style="color: #d8dee9ff;">,</span></span>
<span class="line"><span style="color: #d8dee9;">    embedding</span> <span style="color: #8fbcbb;">vector</span><span style="color: #d8dee9ff;">(</span><span style="color: #b48ead;">1536</span><span style="color: #d8dee9ff;">) -- OpenAI 임베딩 차원수 (text-embedding-3-small)</span></span>
<span class="line"><span style="color: #d8dee9ff;">);</span></span>
<span class="line"></span>
<span class="line"><span style="color: #d8dee9ff;">-- 2. 유사도 검색용 RPC 함수 정의</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">CREATE OR REPLACE FUNCTION</span> <span style="color: #88c0d0;">match_documents</span><span style="color: #d8dee9ff;">(</span></span>
<span class="line"><span style="color: #d8dee9;">    query_embedding</span> <span style="color: #8fbcbb;">vector</span><span style="color: #d8dee9ff;">(</span><span style="color: #b48ead;">1536</span><span style="color: #d8dee9ff;">),</span></span>
<span class="line"><span style="color: #d8dee9;">    match_threshold</span> <span style="color: #b48ead;">float</span><span style="color: #d8dee9ff;">,</span></span>
<span class="line"><span style="color: #d8dee9;">    match_count</span> <span style="color: #b48ead;">integer</span></span>
<span class="line"><span style="color: #d8dee9ff;">)</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">RETURNS TABLE</span> <span style="color: #d8dee9ff;">(</span></span>
<span class="line"><span style="color: #d8dee9;">    id</span> <span style="color: #b48ead;">bigserial</span><span style="color: #d8dee9ff;">,</span></span>
<span class="line"><span style="color: #d8dee9;">    content</span> <span style="color: #b48ead;">text</span><span style="color: #d8dee9ff;">,</span></span>
<span class="line"><span style="color: #d8dee9;">    metadata</span> <span style="color: #b48ead;">jsonb</span><span style="color: #d8dee9ff;">,</span></span>
<span class="line"><span style="color: #d8dee9;">    similarity</span> <span style="color: #b48ead;">float</span></span>
<span class="line"><span style="color: #d8dee9ff;">)</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">LANGUAGE</span> <span style="color: #d8dee9;">plpgsql</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">AS</span> <span style="color: #d8dee9ff;">$$</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">BEGIN</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">    RETURN QUERY</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">    SELECT</span></span>
<span class="line"><span style="color: #d8dee9;">        documents.id</span><span style="color: #d8dee9ff;">,</span></span>
<span class="line"><span style="color: #d8dee9;">        documents.content</span><span style="color: #d8dee9ff;">,</span></span>
<span class="line"><span style="color: #d8dee9;">        documents.metadata</span><span style="color: #d8dee9ff;">,</span></span>
<span class="line"><span style="color: #b48ead;">        1</span> <span style="color: #81a1c1;">-</span> <span style="color: #d8dee9ff;">(documents.embedding</span> <span style="color: #81a1c1;">&lt;=&gt;</span> <span style="color: #d8dee9;">query_embedding</span><span style="color: #d8dee9ff;">)</span> <span style="color: #81a1c1; font-weight: bold;">AS</span> <span style="color: #d8dee9;">similarity</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">    FROM</span> <span style="color: #d8dee9;">documents</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">    WHERE</span> <span style="color: #b48ead;">1</span> <span style="color: #81a1c1;">-</span> <span style="color: #d8dee9ff;">(documents.embedding</span> <span style="color: #81a1c1;">&lt;=&gt;</span> <span style="color: #d8dee9;">query_embedding</span><span style="color: #d8dee9ff;">)</span> <span style="color: #81a1c1;">&gt;</span> <span style="color: #d8dee9;">match_threshold</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">    ORDER BY</span> <span style="color: #d8dee9;">documents.embedding</span> <span style="color: #81a1c1;">&lt;=&gt;</span> <span style="color: #d8dee9;">query_embedding</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">    LIMIT</span> <span style="color: #d8dee9;">match_count</span><span style="color: #81a1c1;">;</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">END;</span></span>
<span class="line"><span style="color: #d8dee9ff;">$$;</span></span></code></pre>
</div>
"""

    LLAMAPARSE_CODE = """
<div class="wp-block-kevinbatdorf-code-block-pro" data-code-block-pro-font-family="Code-Pro-JetBrains-Mono" style="font-size: .75rem; font-family: Code-Pro-JetBrains-Mono,ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace; line-height: 1.25rem;">
<pre class="shiki nord" style="background-color: #2e3440ff; color: #d8dee9ff; padding: 18px; border-radius: 6px;" tabindex="0"><code><span class="line"><span style="color: #81a1c1; font-weight: bold;">import</span> <span style="color: #d8dee9;">os</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">from</span> <span style="color: #d8dee9;">llama_parse</span> <span style="color: #81a1c1; font-weight: bold;">import</span> <span style="color: #8fbcbb;">LlamaParse</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">from</span> <span style="color: #d8dee9;">langchain_core.documents</span> <span style="color: #81a1c1; font-weight: bold;">import</span> <span style="color: #8fbcbb;">Document</span></span>
<span class="line"></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">def</span> <span style="color: #88c0d0;">load_pdf_with_llamaparse</span><span style="color: #d8dee9ff;">(</span><span style="color: #d8dee9;">pdf_path</span><span style="color: #d8dee9ff;">: </span><span style="color: #d8dee9;">str</span><span style="color: #d8dee9ff;">) </span><span style="color: #81a1c1;">-&gt;</span> <span style="color: #d8dee9;">list</span><span style="color: #d8dee9ff;">:</span></span>
<span class="line"><span style="color: #d8dee9ff;">    \"\"\"LlamaParse API를 이용하여 PDF를 고품질 마크다운으로 파싱하고 LangChain Document로 변환합니다.\"\"\"</span></span>
<span class="line"><span style="color: #d8dee9;">    parser</span> <span style="color: #81a1c1;">=</span> <span style="color: #88c0d0;">LlamaParse</span><span style="color: #d8dee9ff;">(</span></span>
<span class="line"><span style="color: #d8dee9;">        api_key</span><span style="color: #81a1c1;">=</span><span style="color: #eceff4;">"llx-your-llamaparse-api-key"</span><span style="color: #eceff4;">,  # LlamaCloud API Key 입력</span></span>
<span class="line"><span style="color: #d8dee9;">        result_type</span><span style="color: #81a1c1;">=</span><span style="color: #eceff4;">"markdown"</span><span style="color: #eceff4;">,              # 텍스트 및 표 레이아웃 보존을 위해 마크다운 지정</span></span>
<span class="line"><span style="color: #d8dee9;">        verbose</span><span style="color: #81a1c1;">=</span><span style="color: #d8dee9;">True</span></span>
<span class="line"><span style="color: #d8dee9ff;">    )</span></span>
<span class="line"><span style="color: #d8dee9ff;">    </span></span>
<span class="line"><span style="color: #d8dee9ff;">    # 클라우드 API 호출하여 파싱 수행</span></span>
<span class="line"><span style="color: #d8dee9;">    documents</span> <span style="color: #81a1c1;">=</span> <span style="color: #d8dee9;">parser</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">load_data</span><span style="color: #d8dee9ff;">(</span><span style="color: #d8dee9;">pdf_path</span><span style="color: #d8dee9ff;">)</span></span>
<span class="line"><span style="color: #d8dee9ff;">    </span></span>
<span class="line"><span style="color: #d8dee9ff;">    # LangChain Standard Document 객체로 매핑</span></span>
<span class="line"><span style="color: #d8dee9;">    langchain_docs</span> <span style="color: #81a1c1;">=</span> <span style="color: #d8dee9ff;">[]</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">    for</span> <span style="color: #d8dee9;">i</span><span style="color: #eceff4;">,</span> <span style="color: #d8dee9;">doc</span> <span style="color: #81a1c1; font-weight: bold;">in</span> <span style="color: #88c0d0;">enumerate</span><span style="color: #d8dee9ff;">(</span><span style="color: #d8dee9;">documents</span><span style="color: #d8dee9ff;">):</span></span>
<span class="line"><span style="color: #d8dee9;">        langchain_docs</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">append</span><span style="color: #d8dee9ff;">(</span><span style="color: #88c0d0;">Document</span><span style="color: #d8dee9ff;">(</span></span>
<span class="line"><span style="color: #d8dee9;">            page_content</span><span style="color: #81a1c1;">=</span><span style="color: #d8dee9;">doc</span><span style="color: #eceff4;">.</span><span style="color: #d8dee9;">text</span><span style="color: #eceff4;">,</span></span>
<span class="line"><span style="color: #d8dee9;">            metadata</span><span style="color: #81a1c1;">=</span><span style="color: #d8dee9ff;">{</span><span style="color: #eceff4;">"source"</span><span style="color: #81a1c1;">:</span> <span style="color: #d8dee9;">pdf_path</span><span style="color: #eceff4;">,</span> <span style="color: #eceff4;">"page"</span><span style="color: #81a1c1;">:</span> <span style="color: #d8dee9;">i</span> <span style="color: #81a1c1;">+</span> <span style="color: #b48ead;">1</span><span style="color: #d8dee9ff;">}</span></span>
<span class="line"><span style="color: #d8dee9ff;">        ))</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">    return</span> <span style="color: #d8dee9;">langchain_docs</span></span></code></pre>
</div>
"""

    SUPABASE_INSERT_CODE = """
<div class="wp-block-kevinbatdorf-code-block-pro" data-code-block-pro-font-family="Code-Pro-JetBrains-Mono" style="font-size: .75rem; font-family: Code-Pro-JetBrains-Mono,ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace; line-height: 1.25rem;">
<pre class="shiki nord" style="background-color: #2e3440ff; color: #d8dee9ff; padding: 18px; border-radius: 6px;" tabindex="0"><code><span class="line"><span style="color: #81a1c1; font-weight: bold;">from</span> <span style="color: #d8dee9;">supabase.client</span> <span style="color: #81a1c1; font-weight: bold;">import</span> <span style="color: #8fbcbb;">create_client</span><span style="color: #eceff4;">,</span> <span style="color: #8fbcbb;">Client</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">from</span> <span style="color: #d8dee9;">langchain_community.vectorstores</span> <span style="color: #81a1c1; font-weight: bold;">import</span> <span style="color: #8fbcbb;">SupabaseVectorStore</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">from</span> <span style="color: #d8dee9;">langchain_openai</span> <span style="color: #81a1c1; font-weight: bold;">import</span> <span style="color: #8fbcbb;">OpenAIEmbeddings</span></span>
<span class="line"></span>
<span class="line"><span style="color: #d8dee9ff;"># Supabase 클라우드 접속 정보 설정</span></span>
<span class="line"><span style="color: #d8dee9;">SUPABASE_URL</span> <span style="color: #81a1c1;">=</span> <span style="color: #eceff4;">"https://your-project-ref.supabase.co"</span></span>
<span class="line"><span style="color: #d8dee9;">SUPABASE_KEY</span> <span style="color: #81a1c1;">=</span> <span style="color: #eceff4;">"your-supabase-anon-key"</span></span>
<span class="line"><span style="color: #d8dee9;">supabase_client</span><span style="color: #d8dee9ff;">: Client = </span><span style="color: #88c0d0;">create_client</span><span style="color: #d8dee9ff;">(</span><span style="color: #d8dee9;">SUPABASE_URL</span><span style="color: #eceff4;">,</span> <span style="color: #d8dee9;">SUPABASE_KEY</span><span style="color: #d8dee9ff;">)</span></span>
<span class="line"></span>
<span class="line"><span style="color: #d8dee9ff;"># OpenAI 임베딩 모듈 활성화</span></span>
<span class="line"><span style="color: #d8dee9;">embeddings</span> <span style="color: #81a1c1;">=</span> <span style="color: #88c0d0;">OpenAIEmbeddings</span><span style="color: #d8dee9ff;">(</span></span>
<span class="line"><span style="color: #d8dee9;">    model</span><span style="color: #81a1c1;">=</span><span style="color: #eceff4;">"text-embedding-3-small"</span><span style="color: #eceff4;">,</span></span>
<span class="line"><span style="color: #d8dee9;">    openai_api_key</span><span style="color: #81a1c1;">=</span><span style="color: #eceff4;">"sk-proj-your-api-key"</span></span>
<span class="line"><span style="color: #d8dee9ff;">)</span></span>
<span class="line"></span>
<span class="line"><span style="color: #d8dee9ff;"># LangChain SupabaseVectorStore를 통해 문서를 DB에 적재</span></span>
<span class="line"><span style="color: #d8dee9;">vector_store</span> <span style="color: #81a1c1;">=</span> <span style="color: #d8dee9;">SupabaseVectorStore</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">from_documents</span><span style="color: #d8dee9ff;">(</span></span>
<span class="line"><span style="color: #d8dee9;">    documents</span><span style="color: #81a1c1;">=</span><span style="color: #d8dee9;">langchain_docs</span><span style="color: #eceff4;">,  # LlamaParse로 파싱하고 분할된 Document 청크들</span></span>
<span class="line"><span style="color: #d8dee9;">    embedding</span><span style="color: #81a1c1;">=</span><span style="color: #d8dee9;">embeddings</span><span style="color: #eceff4;">,</span></span>
<span class="line"><span style="color: #d8dee9;">    client</span><span style="color: #81a1c1;">=</span><span style="color: #d8dee9;">supabase_client</span><span style="color: #eceff4;">,</span></span>
<span class="line"><span style="color: #d8dee9;">    table_name</span><span style="color: #81a1c1;">=</span><span style="color: #eceff4;">"documents"</span><span style="color: #eceff4;">,</span></span>
<span class="line"><span style="color: #d8dee9;">    query_name</span><span style="color: #81a1c1;">=</span><span style="color: #eceff4;">"match_documents"</span></span>
<span class="line"><span style="color: #d8dee9ff;">)</span></span></code></pre>
</div>
"""

    SUPABASE_SEARCH_CODE = """
<div class="wp-block-kevinbatdorf-code-block-pro" data-code-block-pro-font-family="Code-Pro-JetBrains-Mono" style="font-size: .75rem; font-family: Code-Pro-JetBrains-Mono,ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace; line-height: 1.25rem;">
<pre class="shiki nord" style="background-color: #2e3440ff; color: #d8dee9ff; padding: 18px; border-radius: 6px;" tabindex="0"><code><span class="line"><span style="color: #d8dee9ff;"># LangChain SupabaseVectorStore를 활용한 간편한 유사도 검색 수행</span></span>
<span class="line"><span style="color: #d8dee9;">query</span> <span style="color: #81a1c1;">=</span> <span style="color: #eceff4;">"사용자 매뉴얼에서 가장 핵심적인 아키텍처나 주요 기능 설정 방법은?"</span></span>
<span class="line"><span style="color: #d8dee9;">matched_docs</span> <span style="color: #81a1c1;">=</span> <span style="color: #d8dee9;">vector_store</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">similarity_search</span><span style="color: #d8dee9ff;">(</span></span>
<span class="line"><span style="color: #d8dee9;">    query</span><span style="color: #eceff4;">, </span></span>
<span class="line"><span style="color: #d8dee9;">    k</span><span style="color: #81a1c1;">=</span><span style="color: #b48ead;">3</span></span>
<span class="line"><span style="color: #d8dee9ff;">)</span></span>
<span class="line"></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">for</span> <span style="color: #d8dee9;">doc</span> <span style="color: #81a1c1; font-weight: bold;">in</span> <span style="color: #d8dee9;">matched_docs</span><span style="color: #d8dee9ff;">:</span></span>
<span class="line"><span style="color: #88c0d0;">    print</span><span style="color: #d8dee9ff;">(</span><span style="color: #eceff4;">f"[페이지: {doc.metadata.get('page')}]"</span><span style="color: #d8dee9ff;">)</span></span>
<span class="line"><span style="color: #88c0d0;">    print</span><span style="color: #d8dee9ff;">(</span><span style="color: #d8dee9;">doc</span><span style="color: #eceff4;">.</span><span style="color: #d8dee9;">page_content</span><span style="color: #d8dee9ff;">)</span></span>
<span class="line"><span style="color: #88c0d0;">    print</span><span style="color: #d8dee9ff;">(</span><span style="color: #eceff4;">"-"</span> <span style="color: #81a1c1;">*</span> <span style="color: #b48ead;">50</span><span style="color: #d8dee9ff;">)</span></span></code></pre>
</div>
"""

    STREAMLIT_OPENAI_CODE = """
<div class="wp-block-kevinbatdorf-code-block-pro" data-code-block-pro-font-family="Code-Pro-JetBrains-Mono" style="font-size: .75rem; font-family: Code-Pro-JetBrains-Mono,ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace; line-height: 1.25rem;">
<pre class="shiki nord" style="background-color: #2e3440ff; color: #d8dee9ff; padding: 18px; border-radius: 6px;" tabindex="0"><code><span class="line"><span style="color: #81a1c1; font-weight: bold;">import</span> <span style="color: #d8dee9;">streamlit</span> <span style="color: #81a1c1; font-weight: bold;">as</span> <span style="color: #d8dee9;">st</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">from</span> <span style="color: #d8dee9;">langchain_openai</span> <span style="color: #81a1c1; font-weight: bold;">import</span> <span style="color: #8fbcbb;">ChatOpenAI</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">from</span> <span style="color: #d8dee9;">langchain_core.messages</span> <span style="color: #81a1c1; font-weight: bold;">import</span> <span style="color: #8fbcbb;">HumanMessage</span><span style="color: #eceff4;">,</span> <span style="color: #8fbcbb;">SystemMessage</span></span>
<span class="line"></span>
<span class="line"><span style="color: #d8dee9;">st</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">title</span><span style="color: #d8dee9ff;">(</span><span style="color: #eceff4;">"🤖 맞춤형 PDF 매뉴얼 AI 챗봇 (클라우드 서비스 통합)"</span><span style="color: #d8dee9ff;">)</span></span>
<span class="line"></span>
<span class="line"><span style="color: #d8dee9ff;"># 세션 상태 초기화</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">if</span> <span style="color: #eceff4;">"messages"</span> <span style="color: #81a1c1; font-weight: bold;">not in</span> <span style="color: #d8dee9;">st</span><span style="color: #eceff4;">.</span><span style="color: #d8dee9;">session_state</span><span style="color: #d8dee9ff;">:</span></span>
<span class="line"><span style="color: #d8dee9;">    st</span><span style="color: #eceff4;">.</span><span style="color: #d8dee9;">session_state</span><span style="color: #eceff4;">.</span><span style="color: #d8dee9;">messages</span> <span style="color: #81a1c1;">=</span> <span style="color: #d8dee9ff;">[]</span></span>
<span class="line"></span>
<span class="line"><span style="color: #d8dee9ff;"># 이전 대화 렌더링</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">for</span> <span style="color: #d8dee9;">message</span> <span style="color: #81a1c1; font-weight: bold;">in</span> <span style="color: #d8dee9;">st</span><span style="color: #eceff4;">.</span><span style="color: #d8dee9;">session_state</span><span style="color: #eceff4;">.</span><span style="color: #d8dee9;">messages</span><span style="color: #d8dee9ff;">:</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">    with</span> <span style="color: #d8dee9;">st</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">chat_message</span><span style="color: #d8dee9ff;">(</span><span style="color: #d8dee9;">message</span><span style="color: #d8dee9ff;">[</span><span style="color: #eceff4;">"role"</span><span style="color: #d8dee9ff;">]):</span></span>
<span class="line"><span style="color: #d8dee9;">        st</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">write</span><span style="color: #d8dee9ff;">(</span><span style="color: #d8dee9;">message</span><span style="color: #d8dee9ff;">[</span><span style="color: #eceff4;">"content"</span><span style="color: #d8dee9ff;">])</span></span>
<span class="line"></span>
<span class="line"><span style="color: #d8dee9ff;"># 사용자 질문 입력 처리</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">if</span> <span style="color: #d8dee9;">user_question</span> <span style="color: #81a1c1; font-weight: bold;">:=</span> <span style="color: #d8dee9;">st</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">chat_input</span><span style="color: #d8dee9ff;">(</span><span style="color: #eceff4;">"매뉴얼에 대해 궁금한 점을 질문해보세요:"</span><span style="color: #d8dee9ff;">):</span></span>
<span class="line"><span style="color: #d8dee9;">    st</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">session_state</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">messages</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">append</span><span style="color: #d8dee9ff;">(</span><span style="color: #eceff4;">{</span><span style="color: #eceff4;">"role"</span><span style="color: #81a1c1;">: </span><span style="color: #eceff4;">"user"</span><span style="color: #eceff4;">,</span> <span style="color: #eceff4;">"content"</span><span style="color: #81a1c1;">: </span><span style="color: #d8dee9;">user_question</span><span style="color: #eceff4;">}</span><span style="color: #d8dee9ff;">)</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">    with</span> <span style="color: #d8dee9;">st</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">chat_message</span><span style="color: #d8dee9ff;">(</span><span style="color: #eceff4;">"user"</span><span style="color: #d8dee9ff;">):</span></span>
<span class="line"><span style="color: #d8dee9;">        st</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">write</span><span style="color: #d8dee9;">(</span><span style="color: #d8dee9;">user_question</span><span style="color: #d8dee9ff;">)</span></span>
<span class="line"></span>
<span class="line"><span style="color: #d8dee9ff;"># 1단계. Supabase Vector Store에서 질문에 관한 유사도 검색 진행</span></span>
<span class="line"><span style="color: #d8dee9;">    matched_docs</span> <span style="color: #81a1c1;">= </span><span style="color: #d8dee9;">vector_store</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">similarity_search</span><span style="color: #d8dee9ff;">(</span><span style="color: #d8dee9;">user_question</span><span style="color: #eceff4;">, </span><span style="color: #d8dee9;">k</span><span style="color: #81a1c1;">= </span><span style="color: #b48ead;">3</span><span style="color: #d8dee9ff;">)</span></span>
<span class="line"><span style="color: #d8dee9;">    context</span> <span style="color: #81a1c1;">= </span><span style="color: #eceff4;">"\\n\\n"</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">join</span><span style="color: #d8dee9ff;">([</span><span style="color: #d8dee9;">doc</span><span style="color: #eceff4;">.</span><span style="color: #d8dee9;">page_content</span> <span style="color: #81a1c1; font-weight: bold;">for</span> <span style="color: #d8dee9;">doc</span> <span style="color: #81a1c1; font-weight: bold;">in</span> <span style="color: #d8dee9;">matched_docs</span><span style="color: #d8dee9ff;">])</span></span>
<span class="line"></span>
<span class="line"><span style="color: #d8dee9ff;"># 2단계. LLM 프롬프트 주입 및 SystemMessage 설정</span></span>
<span class="line"><span style="color: #d8dee9;">    system_prompt</span> <span style="color: #81a1c1;">= </span><span style="color: #8fbcbb;">f</span><span style="color: #eceff4;">"당신은 업로드된 매뉴얼을 안내하는 전문 AI 어시스턴트입니다. 제공된 문서 내용을 바탕으로 질문에 대해 명확하고 친절하게 답변하세요.\\n\\n[참고 문서]\\n</span><span style="color: #eceff4;">{</span><span style="color: #d8dee9;">context</span><span style="color: #eceff4;">}</span><span style="color: #eceff4;">"</span></span>
<span class="line"></span>
<span class="line"><span style="color: #d8dee9ff;"># 3단계. OpenAI GPT-4o-mini 스트리밍 호출</span></span>
<span class="line"><span style="color: #d8dee9;">    llm</span> <span style="color: #81a1c1;">= </span><span style="color: #88c0d0;">ChatOpenAI</span><span style="color: #d8dee9ff;">(</span></span>
<span class="line"><span style="color: #d8dee9;">        model</span><span style="color: #81a1c1;">=</span><span style="color: #eceff4;">"gpt-4o-mini"</span><span style="color: #eceff4;">,</span></span>
<span class="line"><span style="color: #d8dee9;">        openai_api_key</span><span style="color: #81a1c1;">=</span><span style="color: #eceff4;">"sk-proj-..."</span><span style="color: #eceff4;">,</span></span>
<span class="line"><span style="color: #d8dee9;">        streaming</span><span style="color: #81a1c1;">=</span><span style="color: #d8dee9;">True</span></span>
<span class="line"><span style="color: #d8dee9ff;">    )</span></span>
<span class="line"></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">    with</span> <span style="color: #d8dee9;">st</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">chat_message</span><span style="color: #d8dee9ff;">(</span><span style="color: #eceff4;">"assistant"</span><span style="color: #d8dee9ff;">):</span></span>
<span class="line"><span style="color: #d8dee9;">        response_placeholder</span> <span style="color: #81a1c1;">= </span><span style="color: #d8dee9;">st</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">empty</span><span style="color: #d8dee9ff;">()</span></span>
<span class="line"><span style="color: #d8dee9;">        full_response</span> <span style="color: #81a1c1;">= </span><span style="color: #eceff4;">""</span></span>
<span class="line"><span style="color: #81a1c1; font-weight: bold;">        for</span> <span style="color: #d8dee9;">chunk</span> <span style="color: #81a1c1; font-weight: bold;">in</span> <span style="color: #d8dee9;">llm</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">stream</span><span style="color: #d8dee9ff;">([</span></span>
<span class="line"><span style="color: #d8dee9;">            SystemMessage</span><span style="color: #d8dee9ff;">(</span><span style="color: #d8dee9;">content</span><span style="color: #81a1c1;">=</span><span style="color: #d8dee9;">system_prompt</span><span style="color: #d8dee9ff;">),</span></span>
<span class="line"><span style="color: #d8dee9;">            HumanMessage</span><span style="color: #d8dee9ff;">(</span><span style="color: #d8dee9;">content</span><span style="color: #81a1c1;">=</span><span style="color: #d8dee9;">user_question</span><span style="color: #d8dee9ff;">)</span></span>
<span class="line"><span style="color: #d8dee9ff;">        ]):</span></span>
<span class="line"><span style="color: #d8dee9;">            full_response</span> <span style="color: #81a1c1;">+= </span><span style="color: #d8dee9;">chunk</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">content</span></span>
<span class="line"><span style="color: #d8dee9;">            response_placeholder</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">write</span><span style="color: #d8dee9ff;">(</span><span style="color: #d8dee9;">full_response</span><span style="color: #d8dee9ff;">)</span></span>
<span class="line"><span style="color: #d8dee9;">        st</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">session_state</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">messages</span><span style="color: #eceff4;">.</span><span style="color: #88c0d0;">append</span><span style="color: #d8dee9ff;">(</span><span style="color: #eceff4;">{</span><span style="color: #eceff4;">"role"</span><span style="color: #81a1c1;">: </span><span style="color: #eceff4;">"assistant"</span><span style="color: #eceff4;">, </span><span style="color: #eceff4;">"content"</span><span style="color: #81a1c1;">: </span><span style="color: #d8dee9;">full_response</span><span style="color: #eceff4;">}</span><span style="color: #d8dee9ff;">)</span></span></code></pre>
</div>
"""

    # 1. install.sh pgvector 가 포함된 코드 블록 치환
    for div in alt_soup.find_all("div", class_="wp-block-kevinbatdorf-code-block-pro"):
        text = div.get_text()
        if "install.sh pgvector" in text:
            new_code = BeautifulSoup(SUPABASE_EXT_CODE, "html.parser").find("div")
            div.replace_with(new_code)
            break

    # 2. _load_pdf_safe 가 포함된 코드 블록 치환
    for div in alt_soup.find_all("div", class_="wp-block-kevinbatdorf-code-block-pro"):
        text = div.get_text()
        if "_load_pdf_safe" in text:
            new_code = BeautifulSoup(LLAMAPARSE_CODE, "html.parser").find("div")
            div.replace_with(new_code)
            break

    # 3. PGVector.from_documents 가 포함된 코드 블록 치환
    for div in alt_soup.find_all("div", class_="wp-block-kevinbatdorf-code-block-pro"):
        text = div.get_text()
        if "PGVector.from_documents" in text:
            new_code = BeautifulSoup(SUPABASE_INSERT_CODE, "html.parser").find("div")
            div.replace_with(new_code)
            break

    # 4. hnsw_similarity_search 가 포함된 코드 블록 치환
    for div in alt_soup.find_all("div", class_="wp-block-kevinbatdorf-code-block-pro"):
        text = div.get_text()
        if "hnsw_similarity_search" in text:
            new_code = BeautifulSoup(SUPABASE_SEARCH_CODE, "html.parser").find("div")
            div.replace_with(new_code)
            break

    # 5. Streamlit UI 부분 아래에 st.chat_message 코드 블록 추가
    target_p = alt_soup.find(lambda tag: tag.name == "p" and "오픈소스 웹 프레임워크인 Streamlit" in tag.get_text())
    if target_p:
        new_code = BeautifulSoup(STREAMLIT_OPENAI_CODE, "html.parser").find("div")
        target_p.insert_after(new_code)

    def make_tip_box(title, text):
        return f"""
        <div class="alternative-tip-box" style="margin: 2em 0; padding: 18px 22px; background-color: #f0f7ff; border-left: 5px solid #0056B3; border-radius: 0 6px 6px 0; font-size: 13.5px; color: #2d3748; line-height: 1.7; box-shadow: 0 2px 5px rgba(0,0,0,0.02); -webkit-print-color-adjust: exact; print-color-adjust: exact;">
            <strong style="color: #0056B3; font-size: 14px; display: block; margin-bottom: 6px;">💡 일반인을 위한 실습 팁 - {title}</strong>
            <span>{text}</span>
        </div>
        """

    # 팁 1: OpenSQL VectorDB 구축 뒤에 Supabase 팁 삽입
    target1 = alt_soup.find(lambda tag: tag.name in ["h3", "h4"] and "OpenSQL VectorDB 구축" in tag.get_text())
    if target1:
        next_sibling = target1.next_sibling
        while next_sibling:
            if next_sibling.name == "h3":
                break
            if next_sibling.name == "div" and "wp-block-kevinbatdorf-code-block-pro" in next_sibling.get("class", []):
                tip_html = make_tip_box("Supabase 클라우드 데이터베이스 활용", 
                    "로컬 컴퓨터나 VM 환경에 OpenSQL을 빌드하고 패키지를 직접 컴파일하여 설치하는 복잡한 과정 대신, "
                    "개발자들에게 널리 쓰이는 <strong>Supabase</strong> 클라우드 플랫폼에서 무료 계정을 생성해 보세요. "
                    "대시보드의 <code>Database</code> -> <code>Extensions</code> 메뉴로 이동해 <code>vector</code>를 클릭 한 번으로 "
                    "활성화할 수 있어 최고 관리자(postgres) 권한 획득 문제 및 인프라 구축 장벽이 단번에 해결됩니다.")
                next_sibling.insert_after(BeautifulSoup(tip_html, "html.parser"))
                break
            next_sibling = next_sibling.next_sibling

    # 팁 2: 가장 험난한 '전처리(Preprocessing)' 뒤에 LlamaParse 팁 삽입
    target2 = alt_soup.find(lambda tag: tag.name in ["h3", "h4"] and "전처리" in tag.get_text() and "가장 험난한" in tag.get_text())
    if target2:
        next_sibling = target2.next_sibling
        while next_sibling:
            if next_sibling.name == "h3":
                break
            if next_sibling.name == "p":
                tip_html = make_tip_box("LlamaParse & 텍스트/마크다운 단순화 실습", 
                    "로컬 환경에 PaddleOCR 모듈이나 하이브리드 파서를 연동하기 위해 환경 변수와 의존성을 조율하는 것은 "
                    "초보 개발자에게 꽤 큰 장애물입니다. "
                    "대시보드에서 클라우드 기반의 문서 파싱 API인 <strong>LlamaParse</strong>(무료 크레딧 제공)를 이용하면 "
                    "복잡한 표와 다이어그램 구조가 깨지지 않고 깔끔한 마크다운 문서로 파싱하여 다운로드받을 수 있습니다. "
                    "또는 RAG 실습 초기 단계에는 복잡한 PDF 대신 자신이 직접 적은 메모장(.txt)이나 마크다운(.md) 파일들로 학습을 시작해 보세요.")
                next_sibling.insert_after(BeautifulSoup(tip_html, "html.parser"))
                break
            next_sibling = next_sibling.next_sibling

    # 팁 3: OpenSQL 내부를 들여다보다 : ‘VectorDB 처리 과정’ 뒤에 LangChain SupabaseVectorStore 팁 삽입
    target3 = alt_soup.find(lambda tag: tag.name in ["h3", "h4"] and "VectorDB 처리 과정" in tag.get_text())
    if target3:
        next_sibling = target3.next_sibling
        while next_sibling:
            if next_sibling.name == "h3":
                break
            if next_sibling.name == "div" and "wp-block-kevinbatdorf-code-block-pro" in next_sibling.get("class", []):
                tip_html = make_tip_box("LangChain 고수준 래퍼 API 활용", 
                    "psycopg3 커넥션을 열어 SQL 코사인 유사도 거리 연산(&lt;=&gt;) 쿼리를 직접 빌드하여 DB에 삽입하는 복잡한 과정 대신, "
                    "<strong>LangChain의 SupabaseVectorStore</strong> 클래스를 사용해 보세요. "
                    "단 한 줄의 코드 <code>SupabaseVectorStore.from_documents(...)</code>로 문서를 벡터로 임베딩하여 적재하고, "
                    "<code>similarity_search(...)</code>를 호출하는 것만으로 복잡한 SQL 연산 없이 벡터 검색 기능을 완전 자동화하여 구현할 수 있습니다.")
                next_sibling.insert_after(BeautifulSoup(tip_html, "html.parser"))
                break
            next_sibling = next_sibling.next_sibling

    # 팁 4: 파이썬으로 가볍게 그려낸 지능형 챗봇, ‘Streamlit UI 구현’ 뒤에 API 모델 팁 삽입
    target4 = alt_soup.find(lambda tag: tag.name in ["h3", "h4"] and "Streamlit UI 구현" in tag.get_text())
    if target4:
        next_sibling = target4.next_sibling
        while next_sibling:
            if next_sibling.name == "h3":
                break
            if next_sibling.name == "p":
                tip_html = make_tip_box("OpenAI / Gemini 클라우드 API 연동", 
                    "Ollama를 사용하여 고사양 로컬 모델(7B 이상)을 저사양 로컬 컴퓨터에서 동작시키는 경우, "
                    "심각한 지연이나 메모리 부족 오류를 겪게 됩니다. "
                    "대신 <strong>OpenAI API(GPT-4o-mini)</strong>나 <strong>Gemini API(Gemini 1.5 Flash)</strong>를 연동해 보세요. "
                    "무료 크레딧 또는 매우 저렴한 비용으로 1초 이내에 답변하는 고성능 RAG 모델을 연결할 수 있으며, UI는 Streamlit의 "
                    "<code>st.chat_message</code> API를 이용하면 20줄 안팎의 짧은 파이썬 코드로 모바일 지원 대화창을 그릴 수 있습니다.")
                next_sibling.insert_after(BeautifulSoup(tip_html, "html.parser"))
                break
            next_sibling = next_sibling.next_sibling

    alternative_html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>일반인을 위한 RAG 챗봇 구축 실습 가이드</title>
    {PRINT_STYLE}
</head>
<body>
    <div class="book-container">
        <!-- 📘 1. 표지 -->
        <div class="book-cover">
            <div class="divider"></div>
            <h1>일반인도 쉽게 따라하는<br>RAG 챗봇 구축 실습 가이드</h1>
            <div style="font-size: 1.2em; color: #4a5568; margin-top: 10px;">원본 아티클 상세 내용 + 초간단 우회 실습 팁 통합 가이드북</div>
            <div class="divider"></div>
            <div class="meta-info">
                <strong>출처</strong>: TmaxTibero RAG 구축기 아티클 & 일반인 가이드<br>
                <strong>작성일</strong>: 2026년 06월 26일
            </div>
        </div>

        <!-- 📖 2. 본문 컨텐츠 -->
        <div class="article-body">
            {str(alt_soup)}
        </div>
    </div>
</body>
</html>
"""

    with open(ALT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(alternative_html_content)
    print(f"✓ 대안 가이드 HTML 빌드 성공! -> {ALT_HTML_PATH}")

    # 7. Chrome/Edge를 사용하여 PDF 변환 시도
    browser_path = find_browser_path()
    if not browser_path:
        print("\n⚠️ 시스템에서 Google Chrome 또는 Microsoft Edge 브라우저를 찾을 수 없습니다.")
        print("👉 생성된 index.html / alternative.html을 브라우저에서 여신 후 PDF로 저장해주세요.\n")
        sys.exit(0)

    print(f"✓ PDF 변환 엔진 발견: {browser_path}")
    profile_dir = os.path.join(PROJECT_DIR, "chrome_profile")
    
    # 7-1. 원본 RAG 아티클 PDF 빌드
    file_url = "file:///" + OUTPUT_HTML_PATH.replace("\\", "/")
    cmd1 = [
        browser_path, "--headless=new", "--disable-gpu", "--no-sandbox",
        f"--user-data-dir={profile_dir}", f"--print-to-pdf={OUTPUT_PDF_PATH}",
        "--no-pdf-header-footer", file_url
    ]
    
    # 7-2. 일반인 대안 가이드 PDF 빌드
    alt_file_url = "file:///" + ALT_HTML_PATH.replace("\\", "/")
    cmd2 = [
        browser_path, "--headless=new", "--disable-gpu", "--no-sandbox",
        f"--user-data-dir={profile_dir}", f"--print-to-pdf={ALT_PDF_PATH}",
        "--no-pdf-header-footer", alt_file_url
    ]

    try:
        print("   [Render 1/2] RAG 아티클 PDF 렌더링 중...")
        subprocess.run(cmd1, check=True, timeout=40, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"   ✓ RAG 아티클 PDF 생성 완료: {OUTPUT_PDF_PATH}")
        
        print("   [Render 2/2] 일반인 대안 PDF 렌더링 중...")
        subprocess.run(cmd2, check=True, timeout=40, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"   ✓ 일반인 대안 PDF 생성 완료: {ALT_PDF_PATH}")
        
        print("\n✨ 모든 PDF 전자책 생성 성공! ✨")
    except Exception as pe:
        print(f"\n❌ PDF 변환 중 에러 발생: {pe}")
        print("👉 생성된 HTML 파일들은 정상적이므로 수동으로 브라우저를 통해 PDF 저장을 진행하실 수 있습니다.")

    print("=" * 60)

if __name__ == "__main__":
    main()
