import os
import sys
import subprocess

def install_and_extract():
    # pypdf 라이브러리 검사 및 설치
    try:
        import pypdf
    except ImportError:
        print("💡 pypdf 라이브러리가 필요합니다. 자동 설치를 시작합니다...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pypdf"], check=True)
            import pypdf
            print("✓ pypdf 설치 완료.")
        except Exception as e:
            print(f"❌ 라이브러리 설치 실패: {e}")
            sys.exit(1)

    pdf_path = "0629/송지현 포트폴리오.260626_1.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ 에러: PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return

    # PDF 텍스트 추출
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for idx, page in enumerate(reader.pages, 1):
        page_text = page.extract_text()
        text += f"\n==================================================\n"
        text += f"📄 PAGE {idx}\n"
        text += f"==================================================\n"
        text += page_text + "\n"
        
    with open("song_portfolio_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("✓ 송지현 학생 포트폴리오의 전체 텍스트 추출 성공 -> song_portfolio_text.txt")

if __name__ == "__main__":
    install_and_extract()
