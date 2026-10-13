import os
import re
import glob

folder = r"C:\Users\tuesv\Downloads\DMDG_LIVE_CODE\20261012-1016"

titles_map = {
    "15406": "Convolutional Neural Network, CNN",
    "15407": "MaxPooling2D()",
    "15408": "Flatten 레이어와 Dense 레이어",
    "15409": "마지막 Dense 층의 activation='softmax'와 'relu' 차이점",
    "15410": "Recurrent Neural Networks (RNN)",
    "15411": "RNN의 단점을 극복한 LSTM",
    "15412": "의사 결정 트리 (Decision Tree)",
    "15413": "Random Forest",
    "15414": "XGBoost (eXtreme Gradient Boosting)",
    "15415": "LightGBM",
    "15416": "과적합(Overfitting)과 드롭아웃(Drop Out)",
    "15417": "과소적합(Underfitting)",
    "15418": "머신러닝에서의 편향(Bias)과 분산(Variance)",
    "15419": "조기 종료 (Early Stopping)",
    "15420": "Keras 콜백(Callback)의 기능들",
    "15421": "트랜스포머 (Transformer)",
    "15422": "GPT와 BERT의 차이점과 작동 방식",
    "15423": "GAN (생성적 적대 신경망)",
    "15424": "파인 튜닝(Fine-Tuning) vs 프롬프트 엔지니어링"
}

# 1. Rename files and update MD content
md_files = glob.glob(os.path.join(folder, "*.md"))
lessons = []

for md_path in md_files:
    filename = os.path.basename(md_path)
    article_id = filename.split('_')[0]
    
    real_title = titles_map.get(article_id, "강의 자료")
    safe_title = re.sub(r'[\\/*?:"<>|]', "", real_title).strip()
    new_base = f"{article_id}_{safe_title}"
    
    new_md_path = os.path.join(folder, new_base + ".md")
    new_html_path = os.path.join(folder, new_base + ".html")
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update MD content title
    content = re.sub(r'^# .*\n', f'# {real_title}\n', content)
    
    if md_path != new_md_path:
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        os.rename(md_path, new_md_path)
    else:
        with open(new_md_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Rename matching html files
    old_html_pattern = os.path.join(folder, f"{article_id}_*.html")
    html_matches = glob.glob(old_html_pattern)
    for html_match in html_matches:
        if html_match != new_html_path:
            os.rename(html_match, new_html_path)
            
    lessons.append({
        'id': article_id,
        'title': real_title,
        'html_file': new_base + ".html",
        'md_file': new_base + ".md"
    })

lessons.sort(key=lambda x: int(x['id']))

# 2. Build Website with explicit buttons
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
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
            background-image: radial-gradient(at 0% 0%, hsla(28,100%,74%,1) 0, transparent 50%), radial-gradient(at 100% 100%, hsla(339,100%,79%,1) 0, transparent 50%);
            min-height: 100vh;
        }}
        .glass {{
            background: rgba(255, 255, 255, 0.55);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.6);
        }}
        .card-hover {{
            transition: all 0.3s ease;
        }}
        .card-hover:hover {{
            transform: translateY(-4px);
            box-shadow: 0 15px 30px rgba(255, 120, 80, 0.12);
            background: rgba(255, 255, 255, 0.85);
        }}
    </style>
</head>
<body class="p-6 md:p-12 text-gray-800">
    <div class="max-w-6xl mx-auto">
        <header class="glass rounded-3xl p-10 mb-12 text-center relative overflow-hidden shadow-sm">
            <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-orange-400 via-pink-400 to-orange-400"></div>
            <h1 class="text-4xl md:text-5xl font-extrabold mb-4 tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-orange-600 to-pink-600">
                삼성AXI 딥러닝 심화 과정
            </h1>
            <p class="text-lg md:text-xl text-gray-600 font-medium">인공지능 핵심 개념부터 최신 모델까지 완벽 마스터</p>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
"""

for i, lesson in enumerate(lessons, 1):
    html_content += f"""
            <div class="glass rounded-2xl p-7 card-hover flex flex-col relative overflow-hidden">
                <div class="flex items-center justify-between mb-5 relative z-10">
                    <span class="inline-flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-orange-100 to-pink-100 text-orange-600 font-extrabold text-sm shadow-sm">
                        {i:02d}
                    </span>
                    <span class="text-xs font-semibold text-gray-500 bg-white/70 px-3 py-1.5 rounded-full shadow-sm">#{lesson['id']}</span>
                </div>
                
                <h2 class="text-lg font-bold leading-snug mb-6 text-gray-800 relative z-10 flex-grow">
                    {lesson['title']}
                </h2>
                
                <div class="mt-auto pt-4 border-t border-gray-200/60 flex items-center justify-between gap-3 relative z-10">
                    <a href="{lesson['html_file']}" target="_blank" class="flex-1 flex items-center justify-center bg-orange-500 hover:bg-orange-600 text-white py-2.5 px-3 rounded-xl font-bold text-sm transition-colors shadow-sm">
                        <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                        HTML 열기
                    </a>
                    <a href="{lesson['md_file']}" target="_blank" class="flex-1 flex items-center justify-center bg-white hover:bg-gray-50 text-gray-700 py-2.5 px-3 rounded-xl font-bold text-sm transition-colors border border-gray-200 shadow-sm">
                        <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                        MD 열기
                    </a>
                </div>
            </div>
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

print(f"웹사이트 수정 완료!")
