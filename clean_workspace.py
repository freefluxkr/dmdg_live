import os
import shutil

def main():
    print("=" * 60)
    print("🧹 [Workspace Cleaner] DMDG_LIVE 폴더 자동 정리정돈 시작...")
    print("=" * 60)

    # 1. 분류 타겟 디렉토리 정의 및 생성
    builders_dir = "00_Textbook_Builders"
    caches_dir = "00_HTML_Caches"
    books_dir = "00_Textbooks"
    assets_dir = "01_Assets"
    docs_dir = "02_Documents"
    scripts_dir = "03_Scripts"

    for d in [builders_dir, caches_dir, books_dir, assets_dir, docs_dir, scripts_dir]:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"✓ 폴더 생성: {d}")

    # 2. 현재 디렉토리 파일 목록 수집
    items = os.listdir(".")
    
    moved_files_count = 0
    moved_dirs_count = 0

    for item in items:
        # 이 클리너 스크립트 자신과 핵심 보존 파일은 제외
        if item in ["clean_workspace.py", "index.html", "admin.html", "sw.js", "manifest.json", 
                    "firebase.json", "firebase-config.js", "serviceAccountKey.json", "firebase-adminsdk-api_key.json", "happy_scrapper.py",
                    "js", "css", ".git", ".github", ".gitignore", ".venv", ".env", ".agent", ".agents",
                    "WEEKEND_TODO.md", "HOMEWORK_GUIDE.md", "GEMINI.md", "README.md", "FOLDER_STRUCTURE.md"]:
            continue

        try:
            if os.path.isdir(item):
                # A. HTML 캐시 및 빌드용 임시 챕터 폴더 격리
                if (item.startswith("html_cache") or 
                    item.startswith("html_chapters") or 
                    item.startswith("html_parts") or 
                    item == "pdf_chapters" or 
                    item == "portfolio_feedbacks"):
                    
                    dest = os.path.join(caches_dir, item)
                    # 만약 이미 존재한다면 안전하게 제거 후 이동
                    if os.path.exists(dest):
                        shutil.rmtree(dest)
                    shutil.move(item, caches_dir)
                    moved_dirs_count += 1
                
                # B. 결과물 교재/도서 폴더 격리
                elif item in ["생활코딩_머신러닝_실습편", "생활코딩_머신러닝_실습편_프리미엄", 
                              "생활코딩_머신러닝_싥습편", "모두의 데이터 분석 with 파이썬", 
                              "사장님 몰래 하는 파이썬 업무자동화", "점프_투_파이썬_PDF", 
                              "정조 리더 쉽", "AI 시대의 DBMS 활용 전략", "FastAPI", "Git",
                              "OpenSQL pgvector를 활용한 Tibero 매뉴얼 챗봇 미니 프로젝트 구축기", 
                              "PDF_3주차 Hermes Agent - 성장하는 AI 에이전트 실전 가이드", 
                              "PDF_인공지능생성형 AI 개발 입문", "학생들", "portfolio_feedbacks", 
                              "0629", "0704보강", "2주차 교재 생활코딩 머신러닝 실습편"]:
                    
                    dest = os.path.join(books_dir, item)
                    if os.path.exists(dest):
                        shutil.rmtree(dest)
                    shutil.move(item, books_dir)
                    moved_dirs_count += 1
            else:
                # C. 빌더 파이썬 스크립트 및 윈도우 배치 파일 격리
                if (item.startswith("build_") or 
                    item.startswith("convert_") or 
                    item.endswith(".bat") or 
                    item in ["compile_reports.py", "run_batch.py", "extract_song_portfolio.py", 
                             "scratch_scrape.py", "test_pagination.py", "force_seed_letters.py",
                             "seed.js", "song_portfolio_text.txt", "extract_diag.txt", "verify_report.md",
                             "verify_report.txt", "daily_work_report_20260625.md", "sample_portfolio.md",
                             "raw_epfl_content.md"]):
                    
                    dest = os.path.join(builders_dir, item)
                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.move(item, builders_dir)
                    moved_files_count += 1
                
                # D. 이미지 에셋 격리
                elif item.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
                    dest = os.path.join(assets_dir, item)
                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.move(item, assets_dir)
                    moved_files_count += 1
                
                # E. 문서 및 데이터 격리
                elif item.endswith((".txt", ".csv", ".pdf", ".pptx", ".xlsx", ".docx")):
                    dest = os.path.join(docs_dir, item)
                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.move(item, docs_dir)
                    moved_files_count += 1
                
                # F. 기타 파이썬 스크립트 격리
                elif item.endswith(".py"):
                    dest = os.path.join(scripts_dir, item)
                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.move(item, scripts_dir)
                    moved_files_count += 1
        except Exception as e:
            print(f"⚠️ {item} 이동 실패: {e}")

    print("-" * 60)
    print(f"✨ 정리정돈이 모두 완료되었습니다!")
    print(f"  └ 폴더 격리 완료: {moved_dirs_count}개")
    print(f"  └ 빌더 스크립트 격리 완료: {moved_files_count}개")
    print(f"📂 이제 DMDG_LIVE 폴더가 눈부시게 깨끗해졌습니다!")
    print("=" * 60)

if __name__ == "__main__":
    main()
