import os
import re
import glob

folder = r"C:\Users\tuesv\Downloads\DMDG_LIVE_CODE\20261012-1016"

# 1. 파일 이름 일괄 정리 (Renaming)
md_files = glob.glob(os.path.join(folder, "*.md"))
lessons = []

for md_path in md_files:
    filename = os.path.basename(md_path)
    article_id = filename.split('_')[0]
    
    with open(md_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
    
    # H1 태그에서 진짜 제목 추출
    if first_line.startswith("# "):
        title = first_line[2:].strip()
    else:
        title = filename.replace('.md', '').split('_', 1)[1]
    
    # "참고 : " 와 같은 불필요한 접두어 제거
    display_title = title
    if display_title.startswith("참고 : "):
        display_title = display_title[7:].strip()
    elif display_title.startswith("참고:"):
        display_title = display_title[5:].strip()
    elif display_title == "참고":
        display_title = "강의 자료"
        
    # 특수문자 제거하여 안전한 파일명 생성
    safe_title = re.sub(r'[\\/*?:"<>|]', "", display_title).strip()
    new_base = f"{article_id}_{safe_title}"
    
    new_md_path = os.path.join(folder, new_base + ".md")
    new_html_path = os.path.join(folder, new_base + ".html")
    old_html_path = os.path.join(folder, filename.replace(".md", ".html"))
    
    if md_path != new_md_path:
        os.rename(md_path, new_md_path)
    if os.path.exists(old_html_path) and old_html_path != new_html_path:
        os.rename(old_html_path, new_html_path)
        
    lessons.append({
        'id': article_id,
        'title': display_title,
        'html_file': new_base + ".html"
    })

# 게시물 번호순으로 정렬
lessons.sort(key=lambda x: int(x['id']))

# 2. 프리미엄 index.html 생성 (Glassmorphism & TailwindCSS)
html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 딥러닝 마스터 클래스</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        body {{
            font-family: 'Pretendard', -apple-system, sans-serif;
            /* 주황/핑크 기반의 은은한 그라데이션 (당목담글 스타일 반영) */
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
            background-image: radial-gradient(at 0% 0%, hsla(28,100%,74%,1) 0, transparent 50%), radial-gradient(at 100% 100%, hsla(339,100%,79%,1) 0, transparent 50%);
            min-height: 100vh;
        }}
        .glass {{
            background: rgba(255, 255, 255, 0.45);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.5);
        }}
        .card-hover {{
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        .card-hover:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(255, 120, 80, 0.15);
            background: rgba(255, 255, 255, 0.8);
        }}
    </style>
</head>
<body class="p-6 md:p-12 text-gray-800">
    
    <div class="max-w-6xl mx-auto">
        <!-- Header -->
        <header class="glass rounded-3xl p-10 mb-12 text-center relative overflow-hidden shadow-lg">
            <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-orange-400 via-pink-400 to-orange-400"></div>
            <h1 class="text-4xl md:text-5xl font-extrabold mb-4 tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-orange-600 to-pink-600">
                삼성AXI 딥러닝 심화 과정
            </h1>
            <p class="text-lg md:text-xl text-gray-700 font-medium">인공지능 핵심 개념부터 최신 모델까지 완벽 마스터</p>
        </header>

        <!-- Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
"""

for i, lesson in enumerate(lessons, 1):
    html_content += f"""
            <a href="{lesson['html_file']}" class="glass rounded-2xl p-7 card-hover flex flex-col group cursor-pointer block text-current no-underline relative overflow-hidden">
                <div class="absolute top-0 right-0 w-20 h-20 bg-orange-400 rounded-full opacity-10 -mr-10 -mt-10 group-hover:scale-150 transition-transform duration-500"></div>
                <div class="flex items-center justify-between mb-5 relative z-10">
                    <span class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-br from-orange-100 to-pink-100 text-orange-600 font-extrabold text-lg shadow-sm group-hover:bg-gradient-to-br group-hover:from-orange-500 group-hover:to-pink-500 group-hover:text-white transition-all duration-300">
                        {i:02d}
                    </span>
                    <span class="text-xs font-semibold text-gray-500 bg-white/70 px-3 py-1.5 rounded-full shadow-sm">#{lesson['id']}</span>
                </div>
                <h2 class="text-xl font-bold leading-snug mb-4 text-gray-800 group-hover:text-orange-700 transition-colors duration-300 relative z-10">
                    {lesson['title']}
                </h2>
                <div class="mt-auto pt-4 border-t border-gray-200/50 flex items-center text-sm font-bold text-orange-500 relative z-10">
                    <span>강의 학습하기</span>
                    <svg class="w-5 h-5 ml-1 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"></path></svg>
                </div>
            </a>
"""

html_content += """
        </div>
        
        <footer class="mt-16 mb-8 text-center text-gray-600 text-sm font-medium">
            <p>© 2026 AI Class Portal. Designed by AI Agent 🍊</p>
        </footer>
    </div>
</body>
</html>
"""

index_path = os.path.join(folder, "index.html")
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"작업 완료! {index_path} 가 생성되었습니다.")
