import requests
from bs4 import BeautifulSoup
import re

url = "https://cognitive-reasoners.epfl.ch/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

res = requests.get(url, headers=headers)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, "lxml")

print("👉 EPFL 원본 페이지 텍스트 & 이미지 추출 중...")

# 1. 이미지 절대경로 수집 및 마이그레이션 확인
# 원본 사이트의 상대경로 이미지를 절대경로로 보정
for img in soup.find_all("img"):
    src = img.get("src")
    if src and not src.startswith("http"):
        img["src"] = "https://cognitive-reasoners.epfl.ch" + ("" if src.startswith("/") else "/") + src

# 2. 메인 텍스트 영역 상세 추출
# Bulma 기반의 section 이나 container 단위로 순회하여 마크다운 형태로 저장
markdown_lines = []

# 제목 및 부제목
title_h1 = soup.find("h1", class_="publication-title")
title = title_h1.text.strip() if title_h1 else "Mixture of Cognitive Reasoners"
subtitle_h2 = soup.find("h2")
subtitle = subtitle_h2.text.strip() if subtitle_h2 else "Modular Reasoning with Brain-Like Specialization"

markdown_lines.append(f"# {title}")
markdown_lines.append(f"## {subtitle}\n")

# 저자 정보
author_div = soup.find("div", class_="publication-authors")
if author_div:
    markdown_lines.append(f"**Authors:** {author_div.text.strip()}\n")

# Abstract 섹션
abstract_sec = soup.find("section", class_="hero") or soup.find("div", class_="container is-max-desktop")
# Bulma 컨테이너들 뒤지기
containers = soup.find_all("div", class_="container")
for idx, container in enumerate(containers):
    # 각 컨테이너 안의 텍스트와 이미지 태그를 순서대로 읽기
    h2_tags = container.find_all(["h2", "h3"])
    p_tags = container.find_all("p")
    img_tags = container.find_all("img")
    
    container_text = container.text.strip()
    if not container_text:
        continue
        
    markdown_lines.append(f"### --- Section {idx} ---")
    
    # 구조적 파싱
    for elem in container.descendants:
        if elem.name in ["h1", "h2", "h3", "h4"]:
            markdown_lines.append(f"\n## {elem.text.strip()}\n")
        elif elem.name == "p":
            text = elem.text.strip()
            if text and not text.startswith("Authors") and not text.startswith("EPFL"):
                markdown_lines.append(f"\n{text}\n")
        elif elem.name == "img":
            img_src = elem.get("src")
            img_alt = elem.get("alt", "Image")
            markdown_lines.append(f"\n![{img_alt}]({img_src})\n")
        elif elem.name == "pre":
            markdown_lines.append(f"\n```\n{elem.text.strip()}\n```\n")

# 파일 저장
with open("raw_epfl_content.md", "w", encoding="utf-8") as f:
    f.write("\n".join(markdown_lines))

print("✓ 추출 완료: raw_epfl_content.md 파일이 생성되었습니다.")
