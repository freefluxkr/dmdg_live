import os
from PIL import Image, ImageDraw, ImageFont

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """Pillow 버전 호환성을 위한 둥근 사각형 그리기 헬퍼 함수"""
    try:
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)
    except AttributeError:
        # 구버전 Pillow 대비 Fallback
        draw.rectangle(xy, fill=fill, outline=outline, width=width)

def create_manual_pdf():
    # 고해상도 A4 규격 (가로 2480 x 세로 3508)
    PAGE_W, PAGE_H = 2480, 3508
    canvas = Image.new("RGB", (PAGE_W, PAGE_H), "#F8FAFC") # 깔끔한 쿨톤 화이트
    draw = ImageDraw.Draw(canvas)
    
    # 폰트 로드
    font_path = r"C:\Windows\Fonts\malgunbd.ttf"
    regular_font_path = r"C:\Windows\Fonts\malgun.ttf"
    if not os.path.exists(font_path):
        font_path = regular_font_path = r"C:\Windows\Fonts\arial.ttf"
        
    try:
        font_title = ImageFont.truetype(font_path, 110)
        font_h1 = ImageFont.truetype(font_path, 85)
        font_body = ImageFont.truetype(regular_font_path, 60)
        font_bold = ImageFont.truetype(font_path, 65)
        font_code = ImageFont.truetype(font_path, 55)
    except Exception:
        font_title = font_h1 = font_body = font_bold = font_code = ImageFont.load_default()

    # ==========================================
    # 상단 헤더 영역 (다크 네이비 테마)
    # ==========================================
    draw.rectangle([(0, 0), (PAGE_W, 450)], fill="#0F172A")
    draw.text((PAGE_W//2, 225), "마법의 가상 데이터 만들기 설명서", fill="#FFFFFF", font=font_title, anchor="mm")
    draw.line([(PAGE_W//2 - 600, 320), (PAGE_W//2 + 600, 320)], fill="#38BDF8", width=8)

    y_pos = 650
    left_margin = 250

    # ==========================================
    # 1. 소개 섹션
    # ==========================================
    draw.text((left_margin, y_pos), "1. 이 코드는 뭐하는 건가요?", fill="#0369A1", font=font_h1)
    y_pos += 130
    draw.text((left_margin + 50, y_pos), "• 5,000명의 가상 친구들이 집에 대해 어떻게 생각하는지", fill="#334155", font=font_body)
    y_pos += 90
    draw.text((left_margin + 50, y_pos), "  점수를 매겨주는 마법 지팡이입니다!", fill="#334155", font=font_body)
    y_pos += 250

    # ==========================================
    # 2. 가중치 설명 섹션
    # ==========================================
    draw.text((left_margin, y_pos), "2. '가중치'가 뭔가요?", fill="#0369A1", font=font_h1)
    y_pos += 130
    draw.text((left_margin + 50, y_pos), "• 가중치는 요리할 때 넣는 '조미료'와 같아요.", fill="#334155", font=font_body)
    y_pos += 90
    draw.text((left_margin + 50, y_pos), "• '집 크기' 가중치를 올리면 집 크기가 만족도에 훨씬 중요해집니다.", fill="#334155", font=font_body)
    y_pos += 250

    # ==========================================
    # 3. 코드 수정 가이드 섹션 (박스 UI)
    # ==========================================
    draw.text((left_margin, y_pos), "3. 내 맘대로 숫자를 바꿔보자!", fill="#0369A1", font=font_h1)
    y_pos += 150
    
    # 박스 1: 숫자 조미료
    box1_top = y_pos
    box1_bottom = y_pos + 450
    draw_rounded_rect(draw, [(left_margin, box1_top), (PAGE_W - left_margin, box1_bottom)], radius=30, fill="#F1F5F9", outline="#CBD5E1", width=4)
    
    draw.text((left_margin + 60, box1_top + 60), "[ CUSTOM_WEIGHTS ] : 숫자 조미료", fill="#0F172A", font=font_bold)
    draw.text((left_margin + 100, box1_top + 180), "'Area_Size':  0.15   -> 집이 크면 기분이 좋아져요! (+0.15)", fill="#1D4ED8", font=font_code)
    draw.text((left_margin + 100, box1_top + 280), "'Noise_Level': -0.15 -> 시끄러우면 기분이 나빠져요! (-0.15)", fill="#B91C1C", font=font_code)
    
    y_pos = box1_bottom + 100
    
    # 설명 텍스트
    draw.text((left_margin + 50, y_pos), "• 숫자를 크게 만들면 그 항목이 전체 만족도에 큰 영향을 미칩니다.", fill="#475569", font=font_body)
    y_pos += 100
    draw.text((left_margin + 50, y_pos), "• 소음처럼 나쁜 요소에는 꼭 마이너스(-) 기호를 붙여주세요.", fill="#475569", font=font_body)
    y_pos += 250

    # ==========================================
    # 4. 하단 주의사항 섹션 (강조 박스)
    # ==========================================
    warn_box_top = y_pos
    warn_box_bottom = y_pos + 350
    draw_rounded_rect(draw, [(left_margin, warn_box_top), (PAGE_W - left_margin, warn_box_bottom)], radius=30, fill="#ECFEFF", outline="#06B6D4", width=5)
    
    draw.text((left_margin + 60, warn_box_top + 80), "💡 꼭 기억하세요!", fill="#0891B2", font=font_bold)
    draw.text((left_margin + 60, warn_box_top + 200), "파이썬 코드에서 숫자를 재미있게 바꾼 다음에는,", fill="#0F172A", font=font_body)
    draw.text((left_margin + 60, warn_box_top + 280), "반드시 파일을 저장(Ctrl+S)하고 다시 실행해야 적용됩니다!", fill="#0F172A", font=font_bold)
    
    # ==========================================
    # 5. 저장
    # ==========================================
    save_path = r"C:\Users\user\Downloads\DMDG_LIVE\life\매뉴얼_초딩용.pdf"
    canvas.save(save_path, "PDF", resolution=300.0)
    print(f"고화질 프리미엄 PDF 생성 완료: {save_path}")

if __name__ == "__main__":
    create_manual_pdf()
