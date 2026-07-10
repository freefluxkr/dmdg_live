import os
import sys
import subprocess
import shutil

# =====================================================================
# 📦 1. 라이브러리 자동 의존성 확인 및 설치
# =====================================================================
def check_dependencies():
    """스크립트 구동에 필요한 외부 라이브러리 존재 여부를 확인하고 없으면 자동 설치합니다."""
    required = ["Pillow", "numpy"]
    missing = []
    for lib in required:
        try:
            if lib == "Pillow":
                import PIL
            elif lib == "numpy":
                import numpy
            else:
                __import__(lib)
        except ImportError:
            missing.append(lib)

    if missing:
        print(f"💡 [Dependency] {missing} 라이브러리가 필요합니다. 자동 설치를 시작합니다...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing, check=True)
            print("✓ 필요한 라이브러리 설치 완료.")
        except Exception as e:
            print(f"❌ 라이브러리 설치 실패: {e}")
            sys.exit(1)

check_dependencies()
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# =====================================================================
# 📐 2. 300 DPI 기준 175mm x 235mm 물리 규격을 픽셀(Pixel)로 계산
# =====================================================================
DPI = 300
MM_TO_INCH = 25.4

def mm_to_px(mm):
    return int((mm / MM_TO_INCH) * DPI)

# 175mm x 235mm 페이지 크기 계산
PAGE_W = mm_to_px(175)  # 약 2066 픽셀
PAGE_H = mm_to_px(235)  # 약 2775 픽셀

# 여백을 제외한 실제 이미지가 안착할 내부 가용 영역 (헤더 제외)
MAX_CONTENT_W = PAGE_W - 200 # 좌우 100px 마진
MAX_CONTENT_H = PAGE_H - 470 # 상단 350px, 하단 120px 여백

# =====================================================================
# 🎨 3. 프리미엄 네이비 커버 생성 함수 (맑은 고딕 볼드 폰트 활용)
# =====================================================================
def create_premium_cover(subtitle_text):
    """지정한 타이틀을 가진 고해상도 프리미엄 네이비 표지 이미지를 동적 생성합니다."""
    canvas = Image.new("RGB", (PAGE_W, PAGE_H), "#0f172a")
    draw = ImageDraw.Draw(canvas)
    
    font_path = r"C:\Windows\Fonts\malgunbd.ttf"
    if not os.path.exists(font_path):
        font_path = r"C:\Windows\Fonts\malgun.ttf" # Fallback
        
    try:
        font_title = ImageFont.truetype(font_path, 110)
        font_subtitle = ImageFont.truetype(font_path, 65)
        font_part = ImageFont.truetype(font_path, 85)
    except Exception:
        font_title = font_subtitle = font_part = ImageFont.load_default()
        
    # 타이틀
    draw.text((150, 450), "생활코딩 머신러닝 실습편", fill="#ffffff", font=font_title)
    
    # 부 타이틀
    draw.text((150, 620), subtitle_text, fill="#38bdf8", font=font_part)
    
    # 데코 라인
    draw.line([(150, 780), (PAGE_W - 150, 780)], fill="#38bdf8", width=12)
    
    # 서브타이틀
    draw.text((150, 860), "with 파이썬 텐서플로", fill="#94a3b8", font=font_subtitle)
    
    return canvas

# =====================================================================
# 🧹 4. NumPy 기반 고속 워터마크 제거 필터 함수
# =====================================================================
def remove_watermark(pil_img):
    """이미지 내의 연한 회색 워터마크 및 하단 6% (19/320p)류의 페이지 찌꺼기를 순수 흰색으로 지워줍니다."""
    data = np.array(pil_img)
    r, g, b = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    
    # 임계치를 200으로 설정하여 연한 회색 텍스트 및 잔여 워터마크까지 제거 대상에 포함
    gray_mask = (r > 200) & (r < 255) & (g > 200) & (g < 255) & (b > 200) & (b < 255)
    
    # R-G-B 편차가 적은 무채색 회색 조건 (노란색/파란색 등 원본 그림 채널 보호)
    deviation_mask = (np.abs(r.astype(int) - g.astype(int)) < 15) & \
                     (np.abs(g.astype(int) - b.astype(int)) < 15) & \
                     (np.abs(r.astype(int) - b.astype(int)) < 15)
                     
    watermark_pixels = gray_mask & deviation_mask
    data[watermark_pixels] = [255, 255, 255]
    
    return Image.fromarray(data)

# =====================================================================
# ✂️ 5. 스마트 상하좌우 바운딩 박스 콘텐츠 크롭 함수
# =====================================================================
def crop_content_bounding_box(pil_img):
    """스크린샷 이미지의 상하좌우를 스캔하여 흉물스러운 흰색 여백을 깎아내고 알맹이만 추출합니다."""
    data = np.array(pil_img)
    height, width, _ = data.shape
    
    # 1. R, G, B가 모두 250 이상인 영역은 여백(흰색)으로 판단
    white_mask = (data[:, :, 0] >= 250) & (data[:, :, 1] >= 250) & (data[:, :, 2] >= 250)
    content_mask = ~white_mask
    
    # 2. 콘텐츠가 나타나는 Bounding Box 좌표 검출
    coords = np.argwhere(content_mask)
    if coords.size == 0:
        return pil_img # 검출 실패 시 원본 유지
        
    top_y = coords[:, 0].min()
    bottom_y = coords[:, 0].max()
    left_x = coords[:, 1].min()
    right_x = coords[:, 1].max()
    
    # 3. 💡 하단 페이지 정보 찌꺼기 문자(예: 8% (24/320p)) 우회용 스마트 검출
    # 아래에서 위로 검색하여 본문 본체 카드와 페이지 번호 텍스트 사이에 존재하는 넓은 흰색 공백 행을 탐색
    non_white_ratio = np.sum(content_mask, axis=1) / width
    for y in range(bottom_y - 10, int(height * 0.55), -1):
        # 행의 콘텐츠 비율이 3% 미만(거의 흰색 공백선)을 만났다면
        if non_white_ratio[y] < 0.03:
            # 이 공백선 위쪽에서 진짜 콘텐츠가 다시 시작되는 y좌표를 찾음
            found_edge = False
            for y_check in range(y, int(height * 0.5), -1):
                if non_white_ratio[y_check] > 0.05:
                    bottom_y = y_check
                    found_edge = True
                    break
            if found_edge:
                break
                
    # 4. 여백 버퍼 보정 (텍스트 글자가 잘리지 않도록 사방 12픽셀 안전지대 확보)
    top_y = max(0, top_y - 12)
    bottom_y = min(height - 1, bottom_y + 12)
    left_x = max(0, left_x - 12)
    right_x = min(width - 1, right_x + 12)
    
    # 비정상 영역 크롭 방지 안전장치
    if (right_x - left_x) < width * 0.25 or (bottom_y - top_y) < height * 0.25:
        return pil_img
        
    return pil_img.crop((left_x, top_y, right_x, bottom_y))

# =====================================================================
# ✂️ 6. 개별 이미지 처리 함수 (상하좌우 크롭 + 프리미엄 캔버스 프레임 합성)
# =====================================================================
def process_single_image(src_path, part_title):
    """이미지를 열어 워터마크 제거 및 상하좌우 여백을 크롭 후, 상단 네이비 헤더 액자 프레임에 안착시킵니다."""
    with Image.open(src_path) as raw_img:
        if raw_img.mode != 'RGB':
            raw_img = raw_img.convert('RGB')
        
        # 1. 🧹 교보문고 워터마크 소거
        clean_img = remove_watermark(raw_img)
        
        # 2. ✂️ 스마트 상하좌우 바운딩 박스 크롭 (흰색 좌우 날개 여백까지 완벽 제거)
        cropped_img = crop_content_bounding_box(clean_img)
        
        # 3. 프리미엄 딥 네이비 페이지 배경 생성
        canvas = Image.new("RGB", (PAGE_W, PAGE_H), "#0f172a")
        draw = ImageDraw.Draw(canvas)
        
        # 4. 폰트 로드 및 상단 타이틀 카드 텍스트 렌더링
        font_path = r"C:\Windows\Fonts\malgunbd.ttf"
        if not os.path.exists(font_path):
            font_path = r"C:\Windows\Fonts\malgun.ttf" # Fallback
            
        try:
            font_meta = ImageFont.truetype(font_path, 45)
            font_header = ImageFont.truetype(font_path, 60)
        except Exception:
            font_meta = font_header = ImageFont.load_default()
            
        # 상단 메타텍스트 및 구분 장식라인 그리기
        draw.text((120, 120), "생활코딩 머신러닝 실습편", fill="#64748b", font=font_meta)
        draw.text((120, 190), part_title, fill="#38bdf8", font=font_header)
        draw.line([(120, 280), (PAGE_W - 120, 280)], fill="#38bdf8", width=6)
        
        # 5. 크롭된 슬라이드 카드 이미지 비율 유지 리사이징
        width, height = cropped_img.size
        ratio = min(MAX_CONTENT_W / width, MAX_CONTENT_H / height)
        new_w = int(width * ratio)
        new_h = int(height * ratio)
        
        resized_img = cropped_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # 6. 본문 카드 중앙 정렬 및 안착 (테두리에 슬레이트 컬러의 얇은 프레임 액자선 추가)
        paste_x = (PAGE_W - new_w) // 2
        paste_y = 350 + (MAX_CONTENT_H - new_h) // 2
        
        # 얇은 액자 선 그리기
        draw.rectangle(
            [(paste_x - 3, paste_y - 3), (paste_x + new_w + 3, paste_y + new_h + 3)], 
            outline="#334155", 
            width=3
        )
        canvas.paste(resized_img, (paste_x, paste_y))
        
        return canvas

# =====================================================================
# 🚀 7. 메인 분할 변환 프로세스
# =====================================================================
def main():
    img_dir = "2주차 교재 생활코딩 머신러닝 실습편"

    print("=" * 60)
    print("💡 이미지 PDF 병합기: 스마트 Bounding-Box 크롭 + 프리미엄 네이비 카드 빌더 가동")
    print("=" * 60)

    if not os.path.exists(img_dir):
        fallback_dir = "생활코딩 머신러닝 실습편"
        if os.path.exists(fallback_dir):
            img_dir = fallback_dir
        else:
            print(f"❌ 에러: '{img_dir}' 폴더를 찾을 수 없습니다.")
            sys.exit(1)

    print(f"🎯 소스 이미지 디렉토리: {os.path.abspath(img_dir)}")

    # 1. 이미지 파일 수집 및 정렬
    valid_extensions = (".jpg", ".jpeg", ".png")
    image_files = [
        f for f in os.listdir(img_dir)
        if f.lower().endswith(valid_extensions) and not f.endswith(".pdf")
    ]
    image_files.sort()

    if not image_files:
        print("❌ 에러: 폴더 내에 변환할 이미지 파일이 없습니다.")
        sys.exit(1)

    # 2. 1부(08시 대 촬영)와 2부(09시 대 촬영) 파일 리스트 분할
    part1_files = [f for f in image_files if "20260629_08" in f]
    part2_files = [f for f in image_files if "20260629_09" in f]

    print(f"✓ 감지된 총 이미지 파일: {len(image_files)}장")
    print(f"  └ 1부 (Tensorflow 101): {len(part1_files)}장")
    print(f"  └ 2부 (Tensorflow 102): {len(part2_files)}장")
    print("-" * 60)

    # 3. PDF 인코딩 및 빌드 기능 정의
    def build_part_pdf(files, part_title, cover_subtitle, output_filename):
        if not files:
            print(f"⚠️ {part_title}에 매칭되는 이미지가 없어 빌드를 스킵합니다.")
            return

        print(f"👉 {part_title} 스마트 Bounding-Box 크롭 및 액자 합성 시작 ({output_filename})...")
        pages = []
        
        # A. 프리미엄 네이비 표지 생성 및 삽입
        cover_page = create_premium_cover(cover_subtitle)
        pages.append(cover_page)
        
        total = len(files)
        for idx, filename in enumerate(files, 1):
            src_path = os.path.join(img_dir, filename)
            try:
                # 💡 액자 프레임에 입힐 헤더용 텍스트 전달
                canvas = process_single_image(src_path, cover_subtitle)
                pages.append(canvas)
            except Exception as e:
                print(f"   ⚠️ {filename} 처리 에러: {e}")

            if idx % 30 == 0 or idx == total:
                print(f"   [{idx}/{total}] 스마트 크롭 및 레이아웃 합성 완료...")

        if pages:
            pdf_path = os.path.join(img_dir, output_filename)
            try:
                pages[0].save(
                    pdf_path,
                    save_all=True,
                    append_images=pages[1:],
                    dpi=(DPI, DPI),
                    quality=95
                )
                print(f"✨ {part_title} 빌드 완료! -> {pdf_path}")
            except Exception as e:
                print(f"❌ {part_title} PDF 저장 실패: {e}")
        print("-" * 60)

    # 1. 1부 빌드 (스마트 크롭 + 프리미엄 네이비 프레임)
    build_part_pdf(part1_files, "1부 (Tensorflow 101)", "1부: Tensorflow 101 (딥러닝 기초)", "생활코딩_머신러닝_실습편_1부.pdf")

    # 2. 2부 빌드 (스마트 크롭 + 프리미엄 네이비 프레임)
    build_part_pdf(part2_files, "2부 (Tensorflow 102)", "2부: Tensorflow 102 (이미지 분류 CNN)", "생활코딩_머신러닝_실습편_2부.pdf")

    # 스크립트 복사 백업
    try:
        this_script = sys.argv[0]
        if os.path.exists(this_script) and os.path.basename(this_script) == "make_image_pdf.py":
            shutil.copy(this_script, os.path.join(img_dir, "make_image_pdf.py"))
            print(f"✓ 스크립트 백업 완료: make_image_pdf.py -> {img_dir}/")
    except Exception:
        pass

    print("\n🎉 스마트 크롭 및 네이비 디자인이 적용된 파트별 분리 PDF 변환이 완료되었습니다!")
    print(f"📂 출력 폴더: {os.path.abspath(img_dir)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
