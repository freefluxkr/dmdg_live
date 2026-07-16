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
BOOK_ID = "080491"
BASE_URL = f"https://thebook.io/{BOOK_ID}"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# 폴더 설정
CACHE_DIR = "html_cache_fastapi"
CHAPTERS_DIR = "html_chapters_fastapi"
OUTPUT_DIR = "FastAPI"

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
# 🕸️ 목차 분석 및 챕터 구조 생성 (1~2장 전용)
# =====================================================================
def parse_table_of_contents():
    """책의 메인 페이지에서 목차를 파싱하여 장(Chapter) 및 페이지 목록을 동적으로 구성합니다.
    0001부터 0154 페이지 범위 내에서 장(h2/h3 대분류)을 추출합니다."""
    print("🌐 목차(TOC) 분석을 위해 책 메인 페이지를 읽는 중...")
    headers = {"User-Agent": USER_AGENT}
    req = urllib.request.Request(BASE_URL, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            html = res.read()
            soup = BeautifulSoup(html, "html.parser")
            
            # 목차 영역 탐색
            toc_list = soup.select_one("ul#toc, .book-toc")
            if not toc_list:
                print("❌ 에러: 목차(TOC) 영역을 찾을 수 없습니다.")
                sys.exit(1)
                
            chapters = []
            current_chapter = None
            chapter_index = 0
            
            # 모든 링크 a 태그 순회
            links = toc_list.find_all("a")
            for link in links:
                href = link.get("href", "")
                text = link.get_text(strip=True)
                
                # URL에서 4자리 페이지 ID 추출 (예: /080491/0002/ -> 0002)
                page_match = re.search(rf"/{BOOK_ID}/(\d{{4}})", href)
                if not page_match:
                    continue
                    
                page_id = page_match.group(1)
                page_num = int(page_id)
                
                # 사용자가 지정한 0001 ~ 0154 범위를 벗어나면 스킵 (1~2장만 해당)
                if page_num < 1 or page_num > 154:
                    continue
                
                # 텍스트가 '1장 ', '2장 ' 등으로 시작하는 경우 새로운 장의 시작으로 판별
                is_new_chapter = re.match(r"^\d+장", text) is not None
                
                if is_new_chapter:
                    if current_chapter:
                        chapters.append(current_chapter)
                        
                    chapter_index += 1
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
            
            # 마지막 장 추가
            if current_chapter and current_chapter not in chapters:
                chapters.append(current_chapter)
                
            print(f"✓ 총 {len(chapters)}개의 장이 식별되었습니다.")
            return chapters
            
    except Exception as e:
        print(f"❌ 목차 분석 실패: {e}")
        sys.exit(1)

# =====================================================================
# 🛠️ 구버전 정보 최신화 함수 (Optional/Union -> Pipe |, uvicorn -> fastapi dev)
# =====================================================================
def clean_html_content(content_html, page_id):
    """HTML 본문에서 낡은 정보들을 최신화하고 정보/주의 박스를 삽입합니다."""
    soup = BeautifulSoup(content_html, "html.parser")
    
    # 1. 텍스트 및 코드 예제 안의 구형 타입 힌트를 최신 파이썬 3.10+ 파이프 연산자(|) 스타일로 변경
    for text_node in soup.find_all(text=True):
        if text_node.parent and text_node.parent.name in ['script', 'style']:
            continue
        original = text_node.string
        if original:
            replaced = original
            
            # Optional[Type] -> Type | None 변경
            replaced = re.sub(r'Optional\[([A-Za-z0-9_\[\]]+)\]', r'\1 | None', replaced)
            
            # Union[Type, None] -> Type | None 변경
            replaced = re.sub(r'Union\[([A-Za-z0-9_\[\]]+),\s*None\]', r'\1 | None', replaced)
            replaced = re.sub(r'Union\[None,\s*([A-Za-z0-9_\[\]]+)\]', r'\1 | None', replaced)
            
            # List[Type] -> list[Type], Dict[Type, Type] -> dict[Type, Type] 소문자화
            replaced = replaced.replace("List[", "list[")
            replaced = replaced.replace("Dict[", "dict[")
            
            # uvicorn 실행 예시 변경
            replaced = replaced.replace("uvicorn main:app --reload", "fastapi dev main.py")
            replaced = replaced.replace("uvicorn main:app", "fastapi dev main.py")
            
            if replaced != original:
                text_node.replace_with(replaced)
                
    # 2. 1장 서버 구동 단계 (page_id 0066 부근)
    # FastAPI CLI 도입 관련 팁 안내 박스 주입
    if page_id in ["0066"]:
        cli_tip_html = """
        <div class="highlight" style="border-left: 4px solid #f0ad4e; background-color: #fcf8e3; padding: 15px; margin: 20px 0; border-radius: 6px; font-family: sans-serif; font-size: 0.95em; color: #333;">
            <strong style="color: #c09853; font-size: 1.1em;">💡 [최신 FastAPI CLI 권장 가이드] fastapi dev 사용</strong><br/>
            FastAPI 0.111.0 버전부터 자체 개발 서버 기동용 CLI 도구인 <code>fastapi dev</code>가 도입되었습니다.<br/>
            기존의 구버전 방식인 <code>uvicorn main:app --reload</code> 대신, 최신 표준이자 개발 디버깅에 최적화된 <code>fastapi dev main.py</code> 명령어로 서버를 기동하는 것이 적극 권장됩니다.<br/>
            (※ 배포용 프로덕션 서버 실행 시에는 <code>fastapi run main.py</code>를 사용합니다.)
        </div>
        """
        cli_tip_soup = BeautifulSoup(cli_tip_html, "html.parser")
        if soup.contents:
            soup.insert(0, cli_tip_soup)
        else:
            soup.append(cli_tip_soup)
            
    # 3. 2장 Pydantic 다루기 단계 (page_id 0114 또는 0115 부근)
    # Pydantic v2 호환성 (schema_extra -> json_schema_extra) 팁 박스 주입
    if page_id in ["0114", "0115"]:
        pydantic_tip_html = """
        <div class="highlight" style="border-left: 4px solid #5bc0de; background-color: #f0f8ff; padding: 15px; margin: 20px 0; border-radius: 6px; font-family: sans-serif; font-size: 0.95em; color: #333;">
            <strong style="color: #31708f; font-size: 1.1em;">💡 [참고] Pydantic v2 호환 설정 (schema_extra ➔ json_schema_extra)</strong><br/>
            FastAPI 최신 버전들은 내부적으로 Pydantic v2를 채택하여 동작합니다.<br/>
            v1에서 Swagger 스키마 예제 지정을 위해 쓰였던 <code>schema_extra</code>는 v2에서 <code>json_schema_extra</code>로 속성명이 격상되었습니다.<br/>
            따라서 모델 구성 시 예시값 데이터는 <code>model_config = { "json_schema_extra": { "examples": [...] } }</code> 형태로 선언해주어야 Swagger 문서상에 올바르게 적용됩니다.
        </div>
        """
        pydantic_tip_soup = BeautifulSoup(pydantic_tip_html, "html.parser")
        if soup.contents:
            soup.insert(0, pydantic_tip_soup)
        else:
            soup.append(pydantic_tip_soup)
            
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
                    
                time.sleep(0.3)  # 서버 매너용 딜레이
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
# 🖋️ 3~7장 교재 콘텐츠 자체 집필 (HTML 포맷)
# =====================================================================
CHAPTERS_DATA_3_TO_7 = {
    "03_3장_기본_CRUD_구현하기.html": """
    <div class="thebook-content">
        <h1>3장. 기본 CRUD 구현하기</h1>
        <p>본 장에서는 웹 애플리케이션 개발의 근간이 되는 <strong>CRUD(Create, Read, Update, Delete)</strong> 개념을 학습하고, FastAPI를 통해 메모리 기반의 할 일(Todo) 관리 API를 설계하고 구현합니다. 모든 코드는 최신 파이썬 3.10+ 스타일 가이드라인을 따릅니다.</p>
        
        <h2>3.1 REST API와 HTTP 메서드</h2>
        <p>REST API(Representational State Transfer API)는 웹의 기존 기술과 HTTP 프로토콜을 그대로 활용하기 위한 아키텍처 스타일입니다. HTTP 메서드는 리소스에 대해 수행할 작업의 종류를 명시합니다.</p>
        <table>
            <thead>
                <tr>
                    <th>HTTP Method</th>
                    <th>CRUD 매핑</th>
                    <th>상태 코드 (성공)</th>
                    <th>역할</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>GET</strong></td>
                    <td>Read (조회)</td>
                    <td>200 OK</td>
                    <td>지정한 리소스나 컬렉션을 조회합니다.</td>
                </tr>
                <tr>
                    <td><strong>POST</strong></td>
                    <td>Create (생성)</td>
                    <td>201 Created</td>
                    <td>새로운 리소스를 생성합니다.</td>
                </tr>
                <tr>
                    <td><strong>PUT</strong></td>
                    <td>Update (전체 수정)</td>
                    <td>200 OK</td>
                    <td>지정한 리소스의 전체를 교체합니다.</td>
                </tr>
                <tr>
                    <td><strong>DELETE</strong></td>
                    <td>Delete (삭제)</td>
                    <td>204 No Content</td>
                    <td>지정한 리소스를 삭제합니다.</td>
                </tr>
            </tbody>
        </table>

        <h2>3.2 GET API: 할 일 목록 조회하기</h2>
        <p>먼저 메모리에 적재된 Todo 데이터 구조를 다룰 Pydantic 데이터 모델을 정의하고 전체 목록을 조회하는 API를 작성합니다.</p>
        <div class="highlight">
            <pre><code># main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 할 일 데이터 모델 정의
class Todo(BaseModel):
    id: int
    title: str
    content: str
    is_done: bool = False

# 임시 인메모리 데이터베이스 데이터
todo_db: list[Todo] = [
    Todo(id=1, title="FastAPI 공부", content="공식 문서 1장 읽어보기", is_done=True),
    Todo(id=2, title="파이썬 실습", content="3장 기본 CRUD 코딩 완성하기", is_done=False)
]

@app.get("/todos", response_model=list[Todo])
def get_all_todos() -> list[Todo]:
    \"\"\"전체 할 일 목록을 반환합니다.\"\"\"
    return todo_db
</code></pre>
        </div>

        <h2>3.3 GET API: 단일 항목 조회 및 예외 처리 (404)</h2>
        <p>전체 목록 조회가 잘 수행된다면, 특정 ID를 가진 단일 할 일을 상세 검색하는 경로를 구성합니다. 만약 존재하지 않는 ID가 유입되면 예외 처리(`HTTPException`)를 명시해 줍니다.</p>
        <div class="highlight">
            <pre><code>from fastapi import HTTPException

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo_by_id(todo_id: int) -> Todo:
    \"\"\"특정 ID를 가진 할 일 항목을 검색합니다.\"\"\"
    for todo in todo_db:
        if todo.id == todo_id:
            return todo
            
    # 존재하지 않는 경우 404 에러와 안내 메시지 반환
    raise HTTPException(status_code=404, detail="해당 ID의 할 일을 찾을 수 없습니다.")
</code></pre>
        </div>

        <h2>3.4 POST API: 새로운 할 일 등록하기</h2>
        <p>사용자로부터 새로운 데이터를 입력받아 등록하는 POST API를 생성합니다. 생성할 때 데이터 구성을 위한 전용 요청 스키마(`TodoRequest`)를 설계하는 것이 깔끔합니다.</p>
        <div class="highlight">
            <pre><code>class TodoRequest(BaseModel):
    title: str
    content: str
    is_done: bool = False

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(request: TodoRequest) -> Todo:
    \"\"\"새로운 할 일을 추가합니다.\"\"\"
    # 자동 ID 할당
    new_id = len(todo_db) + 1 if todo_db else 1
    new_todo = Todo(
        id=new_id,
        title=request.title,
        content=request.content,
        is_done=request.is_done
    )
    todo_db.append(new_todo)
    return new_todo
</code></pre>
        </div>

        <h2>3.5 PUT &amp; DELETE API: 수정 및 삭제</h2>
        <p>기존 할 일 정보를 수정하는 PUT 요청과 특정 항목을 리스트에서 완전히 제거하는 DELETE API를 구성하여 CRUD 세트를 완성합니다.</p>
        <div class="highlight">
            <pre><code>@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, request: TodoRequest) -> Todo:
    \"\"\"기존 할 일의 내용을 수정합니다.\"\"\"
    for todo in todo_db:
        if todo.id == todo_id:
            todo.title = request.title
            todo.content = request.content
            todo.is_done = request.is_done
            return todo
            
    raise HTTPException(status_code=404, detail="수정할 할 일을 찾을 수 없습니다.")

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> None:
    \"\"\"지정된 ID의 할 일을 목록에서 삭제합니다.\"\"\"
    for index, todo in enumerate(todo_db):
        if todo.id == todo_id:
            todo_db.pop(index)
            return
            
    raise HTTPException(status_code=404, detail="삭제할 할 일을 찾을 수 없습니다.")
</code></pre>
        </div>
        <div class="highlight" style="border-left: 4px solid #5bc0de; background-color: #f0f8ff; padding: 15px; margin: 20px 0; border-radius: 6px;">
            <strong>💡 상태코드 204 (No Content) 안내</strong><br/>
            DELETE와 같이 처리가 성공적으로 완수되었고, 클라이언트에 추가로 반환할 결과 데이터(본문)가 아무것도 없을 때 반환하는 공식적인 HTTP 규격 코드입니다. FastAPI에서는 <code>status_code=204</code>와 함께 <code>None</code> 혹은 빈 값을 반환합니다.
        </div>
    </div>
    """,

    "04_4장_데이터베이스_및_ORM_사용하기.html": """
    <div class="thebook-content">
        <h1>4장. 데이터베이스와 ORM 사용하기</h1>
        <p>로컬 메모리 데이터 구조는 애플리케이션 재기동 시 데이터가 초기화된다는 치명적인 한계가 있습니다. 본 장에서는 가볍고 이식성이 뛰어난 관계형 데이터베이스인 <strong>SQLite</strong>를 연동하고, 파이썬 ORM 라이브러리의 업계 표준인 <strong>SQLAlchemy</strong>를 활용해 데이터의 영속성을 처리하는 과정을 상세히 실습합니다.</p>
        
        <h2>4.1 SQLite와 ORM의 이해</h2>
        <p>SQLite는 서버 구동이 필요 없이 단일 파일 형태로 동작하는 가볍고 신속한 관계형 DB 엔진입니다. ORM(Object-Relational Mapping)은 객체 지향 언어의 <strong>객체(클래스)</strong>와 관계형 데이터베이스의 <strong>테이블</strong>을 자동으로 매핑시켜 주어 개발자가 SQL 질의문 없이도 코드로 쿼리를 실행할 수 있게 해줍니다.</p>

        <h2>4.2 SQLAlchemy 커넥션 설정</h2>
        <p>먼저 데이터베이스 연결 및 세션 생성을 관리할 <code>database.py</code> 파일을 생성합니다.</p>
        <div class="highlight">
            <pre><code># database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 로컬 파일 경로 정의 (프로젝트 내 todos.db 생성)
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# SQLite는 멀티스레드 접근 시 기본적으로 커넥션을 제어하므로 check_same_thread 옵션 필요
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 데이터베이스 세션을 가동할 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 모델들이 상속받아 정의할 Base 클래스
Base = declarative_base()
</code></pre>
        </div>

        <h2>4.3 ORM 데이터베이스 모델 설계</h2>
        <p>SQLite 데이터베이스 내 테이블과 1대1 매핑될 파이썬 클래스를 정의합니다. `Base`를 상속합니다.</p>
        <div class="highlight">
            <pre><code># models.py
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    content = Column(String(200))
    is_done = Column(Boolean, default=False)
</code></pre>
        </div>

        <h2>4.4 데이터베이스 세션 주입 및 테이블 자동 생성</h2>
        <p>FastAPI 구동 시 SQLite 테이블을 생성하고, 의존성 주입(`Depends`) 기능을 사용해 API 요청마다 세션을 열고 닫는 과정을 구조화합니다. 최신 파이썬의 파이프(`|`) 타입 힌트를 적극 사용합니다.</p>
        <div class="highlight">
            <pre><code># main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import TodoModel
from pydantic import BaseModel

# 테이블 초기 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🧪 Pydantic 스키마 정의 (데이터 검증용)
class TodoBase(BaseModel):
    title: str
    content: str | None = None
    is_done: bool = False

class TodoResponse(TodoBase):
    id: int

    class Config:
        from_attributes = True  # SQLAlchemy 객체를 Pydantic으로 자동 파싱 (Pydantic v2 표준)

# 🔑 DB 세션을 얻기 위한 의존성 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # API 요청 완료 후 커넥션 풀 반환 및 자동 세션 닫기
</code></pre>
        </div>

        <h2>4.5 DB 연동 CRUD API 완성</h2>
        <p>의존성이 주입된 `db: Session`을 바탕으로 SQLite 테이블에 데이터를 직접 삽입, 조회, 갱신하는 코드를 작성합니다.</p>
        <div class="highlight">
            <pre><code>@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoBase, db: Session = Depends(get_db)) -> TodoModel:
    db_todo = TodoModel(
        title=todo.title,
        content=todo.content,
        is_done=todo.is_done
    )
    db.add(db_todo)
    db.commit()      # 데이터베이스 반영
    db.refresh(db_todo) # 생성된 자동증가 ID 값 등을 로드
    return db_todo

@app.get("/todos", response_model=list[TodoResponse])
def get_todos(db: Session = Depends(get_db)) -> list[TodoModel]:
    return db.query(TodoModel).all()

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)) -> TodoModel:
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다.")
    return db_todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoBase, db: Session = Depends(get_db)) -> TodoModel:
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="수정할 항목이 없습니다.")
    db_todo.title = todo.title
    db_todo.content = todo.content
    db_todo.is_done = todo.is_done
    db.commit()
    db.refresh(db_todo)
    return db_todo
</code></pre>
        </div>
    </div>
    """,

    "05_5장_회원가입_구현하기.html": """
    <div class="thebook-content">
        <h1>5장. 회원가입 구현하기</h1>
        <p>본 장에서는 사용자 인증의 출발점인 회원가입 기능을 구현합니다. 대형 프로젝트 개발을 위한 <strong>APIRouter 기반 라우터 구조화</strong> 기법을 학습하고, 사용자의 비밀번호를 해시 암호화(`bcrypt`)하여 데이터베이스에 안전하게 기록하는 설계를 알아봅니다.</p>
        
        <h2>5.1 비밀번호 단방향 해싱 아키텍처</h2>
        <p>비밀번호는 데이터베이스 유출 사태를 대비해 절대로 평문 상태로 데이터베이스에 보관해서는 안 됩니다. <strong>단방향 해시 함수(One-Way Hash Function)</strong>는 원본 값을 입력값으로 주었을 때 암호화된 메시지 다이제스트를 도출하지만, 그 암호문을 복호화하여 비밀번호를 다시 원상 복구하는 것은 불가능한 구조입니다. 본 실습에서는 대표적인 안전 해싱 규격인 <strong>bcrypt</strong>를 사용합니다.</p>

        <h2>5.2 User 데이터 모델링 및 테이블 정의</h2>
        <p>회원을 관리할 테이블 구조를 정의합니다. 고유한 식별자인 `id`와 중복 가입을 방지할 고유 인덱스가 부여된 `email`, 그리고 해시 처리될 `hashed_password`로 설계합니다.</p>
        <div class="highlight">
            <pre><code># models.py (User 추가 버전)
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
</code></pre>
        </div>

        <h2>5.3 APIRouter를 사용한 라우터 구조화</h2>
        <p>모든 API를 <code>main.py</code> 한 곳에 기재하면 유지보수가 매우 어려워집니다. 기능별로 라우터를 분리해 가독성을 높입니다.</p>
        <div class="highlight">
            <pre><code># routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from pydantic import BaseModel, EmailStr

router = APIRouter(
    prefix="/users",
    tags=["users"] # Swagger UI의 카테고리 태그 분류
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔑 회원가입 데이터 요청/응답 스키마
class UserCreate(BaseModel):
    email: EmailStr # EmailStr 형식을 사용하려면 pydantic[email] 설치 필요
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True
</code></pre>
        </div>

        <h2>5.4 비밀번호 해싱 및 회원가입 API 로직 구현</h2>
        <p>비밀번호 해시 라이브러리인 <code>passlib</code>과 <code>bcrypt</code>를 활용하여 해싱 함수를 정의하고, 이메일 중복 체크를 거쳐 데이터베이스에 신규 유저를 등록하는 API를 완성합니다.</p>
        <div class="highlight">
            <pre><code># security.py
from passlib.context import CryptContext

# bcrypt 알고리즘을 사용한 해시 컨텍스트 초기화
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    \"\"\"평문 비밀번호를 단방향 암호 해싱하여 반환합니다.\"\"\"
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    \"\"\"입력 비밀번호와 DB의 해시 비밀번호가 일치하는지 비교 검증합니다.\"\"\"
    return pwd_context.verify(plain_password, hashed_password)
</code></pre>
        </div>
        <div class="highlight">
            <pre><code># routers/user.py (회원가입 API 추가)
from security import get_password_hash
from models import UserModel

@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(user: UserCreate, db: Session = Depends(get_db)) -> UserModel:
    # 1. 중복된 이메일이 이미 존재하는지 체크
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="이미 사용 중인 이메일 주소입니다."
        )
        
    # 2. 평문 패스워드 해싱
    hashed_pw = get_password_hash(user.password)
    
    # 3. 데이터 저장
    new_user = UserModel(
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
</code></pre>
        </div>

        <h2>5.5 메인 애플리케이션 연결</h2>
        <p>작성한 라우터 객체를 <code>main.py</code>에 포함시켜 라우팅을 등록합니다.</p>
        <div class="highlight">
            <pre><code># main.py
from fastapi import FastAPI
from database import engine, Base
import routers.user as user_router

# 테이블 동적 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI 백엔드 서비스")

# 라우터 연결
app.include_router(user_router.router)
</code></pre>
        </div>
    </div>
    """,

    "06_6장_로그인과_인증_구현하기.html": """
    <div class="thebook-content">
        <h1>6장. 로그인과 인증 구현하기</h1>
        <p>보안과 세션 관리는 웹 백엔드의 핵심 요소입니다. 본 장에서는 현대식 웹/앱 아키텍처의 웹 인증 방식인 <strong>JWT(JSON Web Token)</strong>를 채택하여 Stateless 인증 시스템을 구성하고, OAuth2 규격을 사용해 인증된 사용자 정보에 접근하는 코드를 구성합니다.</p>
        
        <h2>6.1 JWT(JSON Web Token) 방식의 이해</h2>
        <p>JWT는 헤더(Header), 페이로드(Payload), 서명(Signature)의 세 부분으로 구성되며, 점(`.`)으로 연결된 인코딩된 문자열입니다. 
        인증 시 서버가 클라이언트에 발급한 JWT를 전달받으면, 서버는 데이터베이스 조회 없이 자체 Secret Key로 서명의 조작 여부(유효성)만을 빠르게 검증하여 권한을 파악(Stateless)하므로 서버의 자원을 극도로 아낄 수 있습니다.</p>

        <h2>6.2 JWT 토큰 관리 모듈 개발</h2>
        <p>JWT 토큰을 생성하고 만료 시점을 주며 검증할 `jwt_handler.py` 모듈을 작성합니다. `python-jose` 혹은 `PyJWT` 라이브러리를 활용합니다.</p>
        <div class="highlight">
            <pre><code># jwt_handler.py
import jwt
from datetime import datetime, timedelta, timezone

# ⚠️ 운영 배포 시에는 비밀키를 환경 변수로 감춰야 합니다.
SECRET_KEY = "SUPER_SECRET_FASTAPI_KEY_12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    \"\"\"JWT 엑세스 토큰을 생성합니다.\"\"\"
    to_encode = data.copy()
    # UTC 기준 만료 시점 설정
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict | None:
    \"\"\"JWT 토큰의 서명 및 만료 일자를 확인합니다.\"\"\"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None  # 서명이 유효하지 않거나 만료된 토큰
</code></pre>
        </div>

        <h2>6.3 로그인 및 토큰 발급 API 구현</h2>
        <p>이메일과 비밀번호를 검증하여 일치할 경우 JWT Access Token을 발급하는 로그인 API를 구현합니다.</p>
        <div class="highlight">
            <pre><code># routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal
from models import UserModel
from security import verify_password
from jwt_handler import create_access_token
from pydantic import BaseModel

router = APIRouter(tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Token(BaseModel):
    access_token: str
    token_type: str

# 🗝️ OAuth2 표준 요청 폼(OAuth2PasswordRequestForm) 활용 로그인 엔드포인트
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> dict:
    # form_data.username 에 사용자가 입력한 이메일이 매핑되어 들어옴
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 잘못되었습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 토큰에 실을 Payload 데이터 설정
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
</code></pre>
        </div>

        <h2>6.4 OAuth2PasswordBearer를 통한 인증 의존성 구축</h2>
        <p>FastAPI는 클라이언트 요청 헤더 중 `Authorization: Bearer <TOKEN>` 포맷에서 자동으로 토큰 값을 파싱하는 `OAuth2PasswordBearer` 스키마를 탑재하고 있습니다. 이를 사용해 인증된 사용자 객체를 구하는 의존성을 만듭니다.</p>
        <div class="highlight">
            <pre><code>from fastapi.security import OAuth2PasswordBearer
from jwt_handler import verify_token

# 로그인 엔드포인트 주소를 OAuth2PasswordBearer에 등록
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserModel:
    \"\"\"토큰을 파싱해 현재 사용자의 DB 객체를 반환합니다. 인증되지 않은 사용자는 401 차단.\"\"\"
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않거나 만료된 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email: str = payload.get("sub")
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user
</code></pre>
        </div>
        <div class="highlight">
            <pre><code># 사용법 예제: 로그인한 사용자만 할 일(Todo) 목록을 등록할 수 있도록 보호
from models import TodoModel

@router.post("/todos", status_code=201)
def create_todo_for_user(
    title: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user) # 🔐 인증 보호 주입!
):
    print(f"로그인 사용자: {current_user.email}")
    new_todo = TodoModel(title=title, owner_id=current_user.id) # 소유권 연동 예시
    db.add(new_todo)
    db.commit()
    return {"status": "success"}
</code></pre>
        </div>
    </div>
    """,

    "07_7장_FastAPI_고급_기능.html": """
    <div class="thebook-content">
        <h1>7장. FastAPI 고급 기능</h1>
        <p>본 장에서는 실제 웹 서비스를 구축할 때 반드시 활용하게 되는 FastAPI의 고급 컴포넌트들을 학습합니다. 라이프사이클을 제어하는 <strong>Lifespan</strong> 핸들러, 핵심 유연성을 담당하는 <strong>의존성 주입(DI)</strong>, 연산을 백그라운드로 넘겨 응답을 고속화하는 <strong>BackgroundTasks</strong>, 그리고 멀티파트 <strong>파일 처리</strong> 기법을 다룹니다.</p>
        
        <h2>7.1 Lifespan: 서버 실행과 종료 시점 제어</h2>
        <p>FastAPI는 앱이 구동될 때 데이터베이스 커넥션 풀을 미리 초기화하고, 서버가 종료될 때 커넥션을 정상적으로 닫아주는 수명 주기 제어 기능을 지원합니다. 옛날 방식인 `@app.on_event("startup")` 대신 최신 Python 표준인 `contextmanager` 기반의 **Lifespan** 패턴을 권장합니다.</p>
        <div class="highlight">
            <pre><code>from fastapi import FastAPI
from contextlib import asynccontextmanager

# 🧪 데이터베이스 커넥션풀 초기 가상 함수 예시
async def init_db():
    print("🔋 [Lifespan] 데이터베이스 연결 활성화 완료.")

async def shutdown_db():
    print("🔌 [Lifespan] 데이터베이스 세션 풀 안전 차단 완료.")

# 애플리케이션 수명 주기 관리 매니저 정의
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. startup (서버 구동 시작 시 실행)
    await init_db()
    yield # --- 이 지점에서 대기하다가 앱 동작 수행 ---
    # 2. shutdown (서버 종료 시 실행)
    await shutdown_db()

# app 정의에 lifespan 인자 등록
app = FastAPI(lifespan=lifespan)
</code></pre>
        </div>

        <h2>7.2 의존성 주입(Dependency Injection) 심화</h2>
        <p>FastAPI는 <code>Depends</code> 키워드를 활용해 강력한 의존성 주입 체계를 제공합니다. 의존성 주입을 활용하면 코드 중복을 제거할 뿐 아니라 데이터베이스 연결 관리, 보안 검증, 세션 상태 유지를 정교하게 처리할 수 있습니다.</p>
        <div class="highlight">
            <pre><code>from fastapi import Depends

# 공통 쿼리 파라미터 클래스 예제
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items")
def read_items(commons: CommonQueryParams = Depends()):
    # Depends에 주입하고자 하는 클래스를 명시하면 파라미터가 자동으로 매핑 및 전달됩니다.
    return {"q": commons.q, "skip": commons.skip, "limit": commons.limit}
</code></pre>
        </div>

        <h2>7.3 백그라운드 태스크(BackgroundTasks)</h2>
        <p>사용자에게 빠른 응답을 전달해야 하고, 백그라운드에서 오랜 시간이 소요되는 무거운 로직(예: 메일 발송, 분석 파일 생성, 시스템 모니터링 등)을 수행해야 하는 경우, <code>BackgroundTasks</code>를 이용해 비동기로 처리를 지연 실행시킬 수 있습니다.</p>
        <div class="highlight">
            <pre><code>from fastapi import BackgroundTasks

def send_welcome_email(email: str):
    # 실제 메일 서버 발송 로직이 유입되는 부분 (임시 3초 딜레이 가정)
    import time
    time.sleep(3)
    print(f"📧 [Background] {email} 주소로 가입 환영 메일을 발송 완료했습니다.")

@app.post("/register")
def register_user(email: str, background_tasks: BackgroundTasks):
    \"\"\"회원가입 요청 시 즉시 응답을 전송하고 메일 발송은 백그라운드에 위임합니다.\"\"\"
    # 백그라운드 태스크 대기열에 작업 등록
    background_tasks.add_task(send_welcome_email, email)
    return {"message": "가입 승인이 완료되었습니다. 환영 이메일은 곧 발송됩니다."}
</code></pre>
        </div>

        <h2>7.4 파일 업로드 및 다운로드 (Multipart / UploadFile)</h2>
        <p>사용자가 보낸 이미지나 문서 파일을 서버에 저장하고, 저장된 파일을 클라이언트가 안전하게 내려받도록 경로(Response)를 구성하는 방법을 설명합니다.</p>
        <div class="highlight">
            <pre><code>import os
import shutil
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import FileResponse

# 파일이 적재될 임시 폴더
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
def upload_file(file: UploadFile = File(...)) -> dict:
    \"\"\"UploadFile 객체를 통해 파일명과 메타데이터에 쉽게 접근하고 안전하게 저장합니다.\"\"\"
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # 스트림 형태로 파일을 받아서 저장 (대용량 파일에 메모리 과부하가 걸리지 않는 안전한 방식)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"filename": file.filename, "size": file.size, "status": "Uploaded Successfully"}

@app.get("/download/{filename}")
def download_file(filename: str) -> FileResponse:
    \"\"\"서버의 지정된 경로에서 파일을 로드하여 클라이언트 브라우저로 내려보냅니다.\"\"\"
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="지정된 파일을 찾을 수 없습니다.")
        
    return FileResponse(
        path=file_path,
        media_type="application/octet-stream", # 범용 이진 파일 스트림 헤더
        filename=filename # 브라우저가 저장할 기본 파일명 지정
    )
</code></pre>
        </div>
    </div>
    """
}

# =====================================================================
# 🚀 메인 실행 제어기
# =====================================================================
def main():
    print("=" * 60)
    print("🚀 FastAPI 백엔드 개발 입문 PDF 책 빌더 및 최신화 프로세스 시작")
    print("=" * 60)
    
    # 1. 브라우저 엔진 탐색
    browser_path = find_browser_path()
    if not browser_path:
        print("❌ 에러: 시스템에서 Google Chrome 또는 Microsoft Edge를 찾을 수 없습니다.")
        sys.exit(1)
    print(f"🎯 발견된 브라우저 엔진: {browser_path}")
    
    # 2. 목차 분석 (1~2장)
    chapters = parse_table_of_contents()
    
    # 3. 각 장별 페이지 다운로드 및 병합 (1~2장)
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
        
    # 4. 자체 집필 3~7장 HTML 동적 로컬 생성 및 병합 리스트 결합
    print("\n" + "=" * 60)
    print("🖋️ 2단계: 자체 집필 3~7장 교재(최신 가이드 포함) HTML 생성")
    print("=" * 60)
    
    for filename, html_content in CHAPTERS_DATA_3_TO_7.items():
        chapter_html_path = os.path.join(CHAPTERS_DIR, filename)
        
        # 3~7장 파일명에서 장 번호와 제목 추출
        clean_name = os.path.splitext(filename)[0]
        
        full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>{clean_name}</title>
    {PRINT_STYLE}
</head>
<body>
    {html_content}
</body>
</html>
"""
        with open(chapter_html_path, "w", encoding="utf-8") as f:
            f.write(full_html)
            
        merged_chapters.append({
            "name": clean_name,
            "html_path": os.path.abspath(chapter_html_path)
        })
        print(f"   ✓ [자체 집필] {clean_name} 생성 완료 -> {chapter_html_path}")
        
    # merged_chapters 리스트 이름 기준 정렬 (01_, 02_, 03_ 정렬 보장)
    merged_chapters.sort(key=lambda x: x["name"])

    # 5. Chrome Headless를 활용한 PDF 변환 (1~7장 전체)
    print("\n" + "=" * 60)
    print("🖨️ 3단계: 크롬 헤드리스 기반 개별 PDF 변환 시작")
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
            # 윈도우 환경 대응 shell=True
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
