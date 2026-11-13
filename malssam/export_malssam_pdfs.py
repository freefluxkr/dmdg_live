"""
export_malssam_pdfs.py
BOOK1(200선) & BOOK2(118선) 마스터 원고를 출판용 CSS 조판 HTML로 변환 후
Headless Chrome으로 고해상도 단행본 PDF 출력
"""

import html
import os
import re
import subprocess
import fitz  # pymupdf
import markdown

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

BOOKS = [
    {
        "md": os.path.join(BASE_DIR, "BOOK1_말쌈_신조어_200선_완전판.md"),
        "html": os.path.join(BASE_DIR, "_tmp_book1_print.html"),
        "pdf": os.path.join(BASE_DIR, "BOOK1_말쌈_신조어_200선_완전판.pdf"),
        "cover_badge": "MALSSAM EDITION · VOL. 01",
        "title": "말쌈: 1990 삐삐에서 2026 릴스까지",
        "subtitle": "대한민국 신조어 · 유행어 · 밈 연대기 200선 (K-상황극 & 다국어 에디션)",
        "accent": "#0284c7",
        "bg_grad": "linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #0284c7 100%)",
    },
    {
        "md": os.path.join(BASE_DIR, "BOOK2_말쌈_K정서_118선_완전판.md"),
        "html": os.path.join(BASE_DIR, "_tmp_book2_print.html"),
        "pdf": os.path.join(BASE_DIR, "BOOK2_말쌈_K정서_118선_완전판.pdf"),
        "cover_badge": "MALSSAM EDITION · VOL. 02",
        "title": "영어엔 없는 한국인의 마음",
        "subtitle": "눈치부터 정(情)까지 번역 불가 K-소울 118선 (크로스컬처 상황극 에디션)",
        "accent": "#d97706",
        "bg_grad": "linear-gradient(135deg, #1c1917 0%, #78350f 60%, #d97706 100%)",
    },
]

CSS_TEMPLATE = """
@page {
  size: A4 portrait;
  margin: 18mm 16mm 18mm 16mm;
  @bottom-center {
    content: counter(page);
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    font-size: 9pt;
    color: #64748b;
  }
}
@page :first {
  margin: 0;
  @bottom-center { content: none; }
}
* { box-sizing: border-box; }
body {
  font-family: 'Malgun Gothic', 'Noto Sans KR', sans-serif;
  color: #1e293b;
  line-height: 1.62;
  font-size: 10pt;
  margin: 0;
  padding: 0;
}
.cover-page {
  width: 210mm;
  height: 297mm;
  padding: 28mm 22mm;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  page-break-after: always;
}
.cover-badge {
  display: inline-block;
  padding: 6px 14px;
  border: 1px solid rgba(255,255,255,0.45);
  border-radius: 999px;
  font-size: 9.5pt;
  font-weight: 700;
  letter-spacing: 0.12em;
  background: rgba(255,255,255,0.12);
}
.cover-title {
  font-size: 30pt;
  font-weight: 900;
  line-height: 1.25;
  margin: 20px 0 14px 0;
  letter-spacing: -0.02em;
}
.cover-subtitle {
  font-size: 13pt;
  line-height: 1.55;
  color: rgba(255,255,255,0.88);
  font-weight: 400;
}
.cover-footer {
  border-top: 1px solid rgba(255,255,255,0.28);
  padding-top: 14px;
  font-size: 9.5pt;
  color: rgba(255,255,255,0.8);
  display: flex;
  justify-content: space-between;
}
.content-body h1 { display: none; }
.content-body h2 {
  font-size: 15pt;
  font-weight: 900;
  color: #0f172a;
  border-bottom: 2.5px solid ACCENT_COLOR;
  padding-bottom: 6px;
  margin: 22px 0 14px 0;
  page-break-before: always;
}
.content-body h2:first-of-type {
  page-break-before: auto;
}
.unit-card {
  border: 1px solid #e2e8f0;
  border-left: 4px solid ACCENT_COLOR;
  border-radius: 8px;
  padding: 12px 14px;
  margin-bottom: 14px;
  background: #ffffff;
  break-inside: avoid;
  page-break-inside: avoid;
}
.unit-card h3 {
  font-size: 12pt;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 6px 0;
}
.unit-card p {
  margin: 5px 0;
}
.unit-card ul {
  margin: 5px 0 6px 0;
  padding-left: 18px;
}
.unit-card li {
  margin-bottom: 3px;
}
code {
  background: #f1f5f9;
  padding: 1px 5px;
  border-radius: 4px;
  font-size: 8.8pt;
  color: #0f172a;
}
blockquote {
  margin: 10px 0 18px 0;
  padding: 10px 14px;
  background: #f8fafc;
  border-left: 3px solid ACCENT_COLOR;
  color: #475569;
  font-size: 9.5pt;
}
hr {
  display: none;
}
"""


def wrap_units_in_cards(body_html: str) -> str:
    """각 <h3> Unit 블록을 break-inside: avoid 카드 div로 감싸 페이지 잘림을 방지합니다."""
    parts = re.split(r"(<h3>.*?)(?=<h3>|<h2>|$)", body_html, flags=re.DOTALL)
    out = []
    for p in parts:
        if p.startswith("<h3>"):
            out.append(f'<div class="unit-card">{p}</div>')
        else:
            out.append(p)
    return "".join(out)


def render_pdf(book: dict):
    with open(book["md"], "r", encoding="utf-8") as f:
        md_text = f.read()

    raw_html = markdown.markdown(md_text, extensions=["extra", "sane_lists"])
    wrapped_html = wrap_units_in_cards(raw_html)
    css = CSS_TEMPLATE.replace("ACCENT_COLOR", book["accent"])

    full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>{html.escape(book['title'])}</title>
<style>{css}</style>
</head>
<body>
  <section class="cover-page" style="background: {book['bg_grad']};">
    <div>
      <span class="cover-badge">{book['cover_badge']}</span>
      <h1 class="cover-title">{html.escape(book['title'])}</h1>
      <p class="cover-subtitle">{html.escape(book['subtitle'])}</p>
    </div>
    <div class="cover-footer">
      <span>DMDG (당목담글) · MALSSAM.COM</span>
      <span>2026 Official Complete Edition</span>
    </div>
  </section>
  <main class="content-body">
    {wrapped_html}
  </main>
</body>
</html>"""

    with open(book["html"], "w", encoding="utf-8") as f:
        f.write(full_html)

    cmd = [
        CHROME_EXE,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={book['pdf']}",
        book["html"],
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(book["html"]):
        os.remove(book["html"])

    doc = fitz.open(book["pdf"])
    pages = len(doc)
    doc.close()
    size_mb = os.path.getsize(book["pdf"]) / (1024 * 1024)
    print(f"PDF READY: {os.path.basename(book['pdf'])} | {pages} pages | {size_mb:.2f} MB")


if __name__ == "__main__":
    for b in BOOKS:
        render_pdf(b)

