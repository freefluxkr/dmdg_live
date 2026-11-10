import time
import requests

TOKEN = "a85dcdacf7b3a2a9966ae3bef8fd4e5af3aecd5b"
HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "Mozilla/5.0",
}

EXAM_BANNER_22015 = """<div style="background:linear-gradient(135deg,#091930 0%,#0f172a 100%);border:2px solid #f59e0b;border-radius:12px;padding:18px 22px;margin:18px 0;color:#f8fafc;">
  <div style="font-size:16px;font-weight:800;color:#fcd34d;margin-bottom:8px;">🎓 [공식 역량 평가 &amp; 직무 추천] 자율주행 빅데이터 레이크하우스 객관식 30문항 실전 시험</div>
  <p style="font-size:13.5px;color:#e2e8f0;margin:0 0 12px 0;line-height:1.6;">
    Ch 01 ~ Ch 15 전 과정을 총망라하는 <b>실전 변별력 객관식 30문항</b>을 응시하고, 즉시 자동 채점 및 <b>DMDG A.C.E.S 6대 육각형 직무 추천 평가지표(레이더 차트 · 1~3순위 추천 직무 · SHAP 강점 분석)</b> 성적표를 받아보세요!
  </p>
  <a href="https://dmdg-live.com/exam_smartcar_lakehouse.html" target="_blank" style="display:inline-block;background:linear-gradient(135deg,#f59e0b,#38bdf8);color:#040914;font-weight:800;font-size:13.5px;padding:9px 18px;border-radius:8px;text-decoration:none;">
    📝 심화 1: 30문항 공인 시험 응시 &amp; 직무 추천 받기 ➔
  </a>
</div>
"""

EXAM_BANNER_22036 = """<div style="background:linear-gradient(135deg,#082026 0%,#0f172a 100%);border:2px solid #f59e0b;border-radius:12px;padding:18px 22px;margin:18px 0;color:#f8fafc;">
  <div style="font-size:16px;font-weight:800;color:#fcd34d;margin-bottom:8px;">🎓 [공식 역량 평가 &amp; 직무 추천] 리눅스 · FastMCP · GraphRAG 객관식 30문항 실전 시험</div>
  <p style="font-size:13.5px;color:#e2e8f0;margin:0 0 12px 0;line-height:1.6;">
    제1부 ~ 제5부 전 과정을 총망라하는 <b>실전 변별력 객관식 30문항</b>을 응시하고, 즉시 자동 채점 및 <b>DMDG A.C.E.S 6대 육각형 직무 추천 평가지표(레이더 차트 · 1~3순위 추천 직무 · SHAP 강점 분석)</b> 성적표를 받아보세요!
  </p>
  <a href="https://dmdg-live.com/exam_graphrag_mcp.html" target="_blank" style="display:inline-block;background:linear-gradient(135deg,#f59e0b,#10b981);color:#040914;font-weight:800;font-size:13.5px;padding:9px 18px;border-radius:8px;text-decoration:none;">
    📝 심화 2: 30문항 공인 시험 응시 &amp; 직무 추천 받기 ➔
  </a>
</div>
"""

EXAM_BANNER_22037 = """<div style="background:linear-gradient(135deg,#1d1035 0%,#0f172a 100%);border:2px solid #f59e0b;border-radius:12px;padding:18px 22px;margin:18px 0;color:#f8fafc;">
  <div style="font-size:16px;font-weight:800;color:#fcd34d;margin-bottom:8px;">🎓 [공식 역량 평가 &amp; 직무 추천] 지속 메모리 &amp; 모델 정렬 객관식 30문항 실전 시험</div>
  <p style="font-size:13.5px;color:#e2e8f0;margin:0 0 12px 0;line-height:1.6;">
    제1부 ~ 제5부 전 과정을 총망라하는 <b>실전 변별력 객관식 30문항</b>을 응시하고, 즉시 자동 채점 및 <b>DMDG A.C.E.S 6대 육각형 직무 추천 평가지표(레이더 차트 · 1~3순위 추천 직무 · SHAP 강점 분석)</b> 성적표를 받아보세요!
  </p>
  <a href="https://dmdg-live.com/exam_continual_memory.html" target="_blank" style="display:inline-block;background:linear-gradient(135deg,#f59e0b,#a855f7);color:#040914;font-weight:800;font-size:13.5px;padding:9px 18px;border-radius:8px;text-decoration:none;">
    📝 심화 3: 30문항 공인 시험 응시 &amp; 직무 추천 받기 ➔
  </a>
</div>
"""


def inject_exam_banner(book_id: int, page_id: int, banner_html: str, exam_key: str):
    url = f"https://wikidocs.net/napi/pages/{page_id}/"
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()
    content = data.get("content", "")
    if exam_key in content:
        print(f"ℹ️ Page {page_id} 이미 시험 배너 포함됨")
        return

    new_content = content + "\n\n---\n\n" + banner_html
    payload = {
        "id": page_id,
        "book_id": book_id,
        "subject": data["subject"],
        "content": new_content,
        "parent_id": data.get("parent_id"),
        "seq": data.get("seq", 0),
        "open_yn": "Y",
    }
    resp = requests.put(url, headers=HEADERS, json=payload, timeout=30)
    resp.raise_for_status()
    print(f"✅ [Book {book_id}] Page {page_id} ({data['subject']}) 시험 배너 연동 완료")
    time.sleep(1.2)


def main():
    # Book 22015: 도서 소개(475998), Ch 14(481095), Ch 15(476018)
    for pid in [475998, 481095, 476018]:
        inject_exam_banner(22015, pid, EXAM_BANNER_22015, "exam_smartcar_lakehouse.html")

    # Book 22036: 도서 개요(478082), Ch 19(478149), Ch 20(478150)
    for pid in [478082, 478149, 478150]:
        inject_exam_banner(22036, pid, EXAM_BANNER_22036, "exam_graphrag_mcp.html")

    # Book 22037: 도서 개요(478124), Ch 19(478169), Ch 20(478170)
    for pid in [478124, 478169, 478170]:
        inject_exam_banner(22037, pid, EXAM_BANNER_22037, "exam_continual_memory.html")

    print("\n🎉 3권 전 도서 객관식 30문항 시험 & 직무추천 연동 완료!")


if __name__ == "__main__":
    main()

