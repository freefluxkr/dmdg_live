import os
import sys
import re
import subprocess

# =====================================================================
# 📦 1. 라이브러리 자동 의존성 확인 및 설치
# =====================================================================
def check_dependencies():
    """스크립트 구동에 필요한 외부 라이브러리 존재 여부를 확인하고 없으면 자동 설치합니다."""
    try:
        import markdown
    except ImportError:
        print("💡 [Dependency] 'markdown' 라이브러리가 없습니다. 자동 설치를 시작합니다...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "markdown"], check=True)
            print("✓ 'markdown' 설치 완료.")
        except Exception as e:
            print(f"❌ 라이브러리 설치 실패: {e}")
            print("👉 수동 설치 명령어: pip install markdown")
            sys.exit(1)

check_dependencies()
import markdown

# =====================================================================
# 🔍 2. 브라우저 엔진 경로 검색 (Chrome 또는 Edge)
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
# 🎨 3. 프리미엄 CSS 스타일링이 적용된 HTML 템플릿 생성
# =====================================================================
def md_to_styled_html(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 마크다운을 HTML로 변환
    html_body = markdown.markdown(md_content, extensions=['tables'])

    # 대기업 리포트 수준의 프리미엄 CSS 테마
    styled_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>약점 분석 및 보완 계획서</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.8/dist/web/static/pretendard-dynamic-subset.css');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');

        body {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
            color: #2c3e50;
            background-color: #ffffff;
            margin: 0;
            padding: 2.5rem 2rem;
            line-height: 1.8;
            -webkit-print-color-adjust: exact;
        }}

        h1 {{
            font-family: 'Pretendard', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            color: #1e3a8a;
            border-bottom: 3px solid #1e3a8a;
            padding-bottom: 0.75rem;
            margin-bottom: 2rem;
            text-align: center;
        }}

        h2 {{
            font-size: 1.35rem;
            font-weight: 700;
            color: #1e40af;
            border-left: 5px solid #2563eb;
            padding-left: 0.75rem;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
        }}

        h3 {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #1e3a8a;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
        }}

        p, li {{
            font-size: 0.95rem;
            color: #334155;
        }}

        ul {{
            padding-left: 1.25rem;
            margin-bottom: 1rem;
        }}

        li {{
            margin-bottom: 0.5rem;
        }}

        /* Table Design */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.85rem;
            background: #ffffff;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }}

        th {{
            background-color: #f1f5f9;
            color: #1e293b;
            font-weight: 700;
            padding: 12px 10px;
            border-bottom: 2px solid #e2e8f0;
            text-align: left;
        }}

        td {{
            padding: 12px 10px;
            border-bottom: 1px solid #e2e8f0;
            color: #475569;
            line-height: 1.5;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        /* Recruiter Recommendation Badges styling (if match) */
        span.rating {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            background: #eff6ff;
            color: #1e40af;
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid #bfdbfe;
        }}

        /* Warning/Caution Box Styles (Replacing Markdown blockquotes or headers) */
        li strong {{
            color: #0f172a;
        }}

        /* Page break controls for print */
        @media print {{
            body {{
                padding: 1.5cm;
            }}
            h2 {{
                page-break-before: always;
            }}
            h2:first-of-type {{
                page-break-before: avoid;
            }}
            table, ul {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""
    return styled_html

# =====================================================================
# 🚀 4. 메인 변환 로직
# =====================================================================
def main():
    target_folder = "0629"
    files_to_convert = [
        "어창선_약점보완계획.md",
        "한정현_약점보완계획.md",
        "현다은_약점보완계획.md",
        "송지현_약점보완계획.md"
    ]

    print("=" * 60)
    print("🚀 마크다운 -> 디자인 PDF 일괄 변환기 가동")
    print("=" * 60)

    # 브라우저 경로 확인
    browser_path = find_browser_path()
    if not browser_path:
        print("❌ 에러: 시스템에서 Google Chrome 또는 Microsoft Edge를 찾을 수 없습니다.")
        print("👉 브라우저 설치 상태를 확인하시거나 마크다운 뷰어 프로그램을 사용해 인쇄해 주세요.")
        sys.exit(1)

    print(f"🎯 발견된 브라우저 엔진: {browser_path}")

    # 임시 HTML 저장용 폴더
    html_cache = "html_cache_feedbacks"
    os.makedirs(html_cache, exist_ok=True)

    for filename in files_to_convert:
        md_path = os.path.join(target_folder, filename)
        if not os.path.exists(md_path):
            print(f"⚠️ 경고: '{md_path}' 파일이 존재하지 않아 건너뜁니다.")
            continue

        print(f"\n👉 {filename} PDF 변환 시작...")
        
        # HTML 변환 및 임시 저장
        html_content = md_to_styled_html(md_path)
        base_name = os.path.splitext(filename)[0]
        temp_html_path = os.path.abspath(os.path.join(html_cache, f"temp_{base_name}.html"))
        
        with open(temp_html_path, 'w', encoding='utf-8') as hf:
            hf.write(html_content)

        # PDF 변환 경로 설정
        pdf_path = os.path.abspath(os.path.join(target_folder, f"{base_name}.pdf"))
        file_url = "file:///" + temp_html_path.replace("\\", "/")
        profile_dir = os.path.abspath(os.path.join(html_cache, f"profile_print_{base_name}"))

        # Chrome Headless PDF 인쇄 명령어 구성
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
            print(f"   ✨ PDF 생성 성공! -> {pdf_path}")
        except Exception as e:
            print(f"   ❌ PDF 변환 중 에러 발생: {e}")

    print("\n" + "=" * 60)
    print(f"🎉 모든 작업이 완료되었습니다! {target_folder}/ 폴더를 확인해 주세요.")
    print("=" * 60)

if __name__ == "__main__":
    main()
