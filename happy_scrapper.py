import os
import re
import urllib.request
import urllib.error
import hashlib
import time
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# ==========================================
# 🍊 1. Firebase Admin SDK 설정
# ==========================================
# Firebase Admin SDK의 비공개 키가 없는 경우에도 안전하게 작동하도록 구성
# 프로젝트 ID가 dmdg-pwa 이므로 로컬 혹은 Firebase Admin 기본 자격 증명을 로드합니다.
try:
    # dmdg-pwa 프로젝트 인증 초기화
    if not firebase_admin._apps:
        # GCP 환경 혹은 로컬 서비스 계정 키 파일 경로 지정 가능
        # 만약 로컬에 키 파일(serviceAccountKey.json)이 없다면 Application Default Credentials 사용
        cred_path = "serviceAccountKey.json"
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            # credentials 없이 초기화할 때 환경 변수를 기준으로 인증을 시도합니다.
            firebase_admin.initialize_app(options={
                'projectId': 'dmdg-pwa'
            })
    db = firestore.client()
except Exception as e:
    print(f"⚠️ Firebase Admin SDK 초기화 실패: {e}")
    print("👉 로컬 실행을 위해 Firebase 콘솔에서 serviceAccountKey.json 파일을 발급받아 스크립트와 동일 폴더에 넣어주세요.")
    db = None

# ==========================================
# 🌿 2. 감정(Emotion) 분류용 키워드 룰
# ==========================================
EMOTION_KEYWORDS = {
    "위로": ["위로", "고생", "눈물", "아픔", "상처", "괜찮아", "슬픔", "토닥", "이해", "지친", "힘들"],
    "설렘": ["설렘", "사랑", "가족", "부모", "기쁨", "미소", "아이", "소풍", "만남", "기대", "새로운"],
    "평온": ["평온", "평화", "바람", "고요", "숲", "명상", "침묵", "쉬어", "자연", "오후", "안정", "차분"]
}

def classify_emotion(content):
    """글 내용에 포함된 키워드로 감정 상태를 단순 추출 분류합니다."""
    scores = {"위로": 0, "설렘": 0, "평온": 0}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in content:
                scores[emotion] += 1
                
    # 점수가 높은 감정을 선택하고 동률이거나 0점이면 기본값 '위로' 부여
    max_emotion = max(scores, key=scores.get)
    if scores[max_emotion] == 0:
        return "위로"
    return max_emotion

# ==========================================
# 🕷️ 3. 행복한가 웹사이트 크롤러
# ==========================================
def fetch_happy_contents():
    """'행복한가' 웹사이트에서 최신 글귀 컨텐츠를 크롤링하여 카테고리별로 정제합니다."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    scraped_items = []
    
    # 크롤링할 카테고리별 주소 맵 (행복한가 편지 카테고리)
    categories = {
        "일상스토리": "https://m-letter.or.kr/happy-contents?category=I6d504u2k1",
        "문화생활정보": "https://m-letter.or.kr/happy-contents?category=q233ZF15bi"
    }
    
    for category_name, url in categories.items():
        print(f"🔗 [{category_name}] 최신 글 추출 중: {url}")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser')
                
                # 행복한가 목록 페이지의 카드 혹은 아티클 래퍼 선택 (일반적인 목록 리스크 구조 적용)
                # m-letter.or.kr 구조에 맞추어 article, card 또는 특정 class를 탐색합니다.
                posts = soup.select('.post-item, .card, article, .board-list tr')
                
                # 만약 클래스명이 매칭되지 않을 경우를 대비하여 일반적인 a 태그를 탐색하는 Fallback 지원
                if not posts:
                    posts = soup.find_all('a', href=re.compile(r'/happy-contents/\d+'))
                
                for post in posts[:5]:  # 각 카테고리별 최신 5개 글 분석
                    # 글의 링크가 있으면 링크로 들어가서 본문 전문 크롤링
                    link = post.get('href') if post.name == 'a' else (post.find('a')['href'] if post.find('a') else None)
                    if not link:
                        continue
                        
                    if not link.startswith('http'):
                        link = "https://m-letter.or.kr" + link
                        
                    # 본문 상세 페이지 요청
                    detail_req = urllib.request.Request(link, headers=headers)
                    with urllib.request.urlopen(detail_req, timeout=10) as detail_res:
                        detail_soup = BeautifulSoup(detail_res.read(), 'html.parser')
                        
                        # 본문 영역 파싱 (일반적인 상세페이지 본문 클래스/ID 탐색)
                        content_area = detail_soup.select_one('.post-content, .article-body, #content_area, .view-content')
                        title_area = detail_soup.select_one('.post-title, .title, h1, .view-title')
                        
                        title = title_area.get_text().strip() if title_area else "따뜻한 마중물 편지"
                        
                        if content_area:
                            # 이미지를 제외한 텍스트 콘텐츠 정제
                            for img in content_area.find_all('img'):
                                img.decompose()
                            content_text = content_area.get_text().strip()
                        else:
                            # Fallback: 본문 태그가 명확하지 않으면 p 태그들을 묶어서 텍스트 추출
                            paragraphs = detail_soup.find_all('p')
                            content_text = "\n".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30])
                        
                        if len(content_text) > 40: # 유효한 글만 적재
                            scraped_items.append({
                                "title": title,
                                "content": content_text,
                                "category": category_name,
                                "link": link
                            })
                            print(f"✅ 성공적으로 가져옴: {title[:20]}...")
                            
            time.sleep(1.5) # 서버 부하 방지를 위한 슬립
        except urllib.error.URLError as ue:
            print(f"❌ [{category_name}] 네트워크 오류: {ue}")
        except Exception as ex:
            print(f"❌ [{category_name}] 데이터 추출 중 에러: {ex}")
            
    return scraped_items

# ==========================================
# 📂 4. 데이터베이스 증분 적재 (중복 제거)
# ==========================================
def seed_new_contents():
    """새로 가져온 데이터 중 데이터베이스에 존재하지 않는 신규 데이터만 필터링하여 Firestore에 적재합니다."""
    if db is None:
        print("❌ Firestore 클라이언트가 유효하지 않아 로컬 데이터 적재를 진행하지 않습니다.")
        return
        
    print("\n🚀 데이터베이스 동기화 및 신규 데이터 필터링을 시작합니다...")
    scraped_data = fetch_happy_contents()
    
    if not scraped_data:
        print("ℹ️ 새로 긁어온 컨텐츠가 없습니다.")
        return
        
    primers_col = db.collection("primers")
    
    # 중복 삽입 방지를 위해 기존 Firestore에 등록된 primers 문서들의 해시값을 확인합니다.
    # 내용의 MD5 해시값 혹은 고유 식별 링크를 기준으로 삼습니다.
    existing_hashes = set()
    try:
        docs = primers_col.stream()
        for doc in docs:
            doc_data = doc.to_dict()
            content = doc_data.get("content", "")
            # 내용의 공백을 제거한 해시값 생성
            content_hash = hashlib.md5(content.replace(" ", "").encode('utf-8')).hexdigest()
            existing_hashes.add(content_hash)
    except Exception as e:
        print(f"⚠️ 기존 데이터 해시화 확인 중 실패(처음 적재 시 정상): {e}")

    new_count = 0
    batch = db.batch()
    
    for item in scraped_data:
        content_hash = hashlib.md5(item["content"].replace(" ", "").encode('utf-8')).hexdigest()
        
        # 이미 데이터베이스에 등록된 동일한 내용이면 건너뜀 (증분 데이터만 삽입)
        if content_hash in existing_hashes:
            continue
            
        # 감정 자동 분류
        detected_emotion = classify_emotion(item["content"])
        
        # Firestore 새 문서 추가
        new_doc_ref = primers_col.document()
        batch.set(new_doc_ref, {
            "title": item["title"],
            "content": item["content"],
            "category": item["category"],
            "emotion": detected_emotion,
            "type": "오늘의 편지",
            "timestamp": firestore.SERVER_TIMESTAMP,
            "source_url": item["link"]
        })
        new_count += 1
        print(f"➕ 신규 추가 대상 결정: [{item['category']}] ({detected_emotion}) - {item['title']}")
        
    if new_count > 0:
        batch.commit()
        print(f"🎉 성공적으로 {new_count}개의 새로운 '행복한가' 편지를 적재 완료했습니다!")
    else:
        print("✨ 데이터베이스가 이미 최신 상태입니다. 추가할 새로운 컨텐츠가 없습니다.")

if __name__ == "__main__":
    seed_new_contents()
