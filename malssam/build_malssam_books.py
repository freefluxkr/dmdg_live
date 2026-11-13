"""
build_malssam_books.py
말쌈(MALSSAM) words_db.json (318단어) 기반
제1권(신조어·밈 200선) & 제2권(번역불가 K-정서 118선)
전체 원고 + 리얼 K-상황극 + 다국어 연동 시드 자동 생성 파이프라인
"""

import json
import os
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "words_db.json")
OUT_BOOK1 = os.path.join(BASE_DIR, "BOOK1_말쌈_신조어_200선_완전판.md")
OUT_BOOK2 = os.path.join(BASE_DIR, "BOOK2_말쌈_K정서_118선_완전판.md")
OUT_SEED = os.path.join(BASE_DIR, "malssam_books_multilingual_seed.json")


def toxicity_badge(level: int) -> str:
    if level == 0:
        return "🟢 순한맛 (비속어 없음)"
    if level == 1:
        return "🟡 보통 (일상 구어체)"
    return "🔴 주의 (순화 권장 표현)"


def parse_example_lines(examples: list) -> tuple[str, str]:
    """기존 예문 A/B 대사를 깔끔히 분리합니다."""
    if not examples:
        return ("", "")
    raw = str(examples[0]).strip()
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    a_line = ""
    b_line = ""
    for ln in lines:
        cleaned = re.sub(r"^[ABab]\s*:\s*", "", ln).strip()
        if ln.upper().startswith("A:") and not a_line:
            a_line = cleaned
        elif ln.upper().startswith("B:") and not b_line:
            b_line = cleaned
        elif not a_line:
            a_line = cleaned
        elif not b_line:
            b_line = cleaned
    return (a_line, b_line)


def build_book1_roleplay(w: dict, idx: int) -> list[dict]:
    """제1권(신조어) 상황극 대본(4턴)을 시대·성격에 맞게 구성합니다."""
    word = w["word"]
    era = w.get("era", "shorts")
    std = w.get("standard_korean_mapping") or "자연스러운 표준 한국어 표현"
    a_line, b_line = parse_example_lines(w.get("examples", []))

    if era == "latte":
        cast_a, cast_b, cast_c = "데미스 (팀장 · X세대)", "알렉스 (외국인 인턴)", "제니퍼 (수석 · MZ세대)"
        setting = "오후 3시 DMDG 오피스 라운지, 팀장님이 레트로 감성에 젖어 대화를 건넨다."
    elif era == "smartphone":
        cast_a, cast_b, cast_c = "크레이그 (시니어)", "알렉스 (외국인 인턴)", "제니퍼 (수석)"
        setting = "점심시간 후 메신저 단톡방과 사무실 자리 사이에서 벌어진 유쾌한 해프닝."
    else:
        cast_a, cast_b, cast_c = "제니퍼 (수석 · 밈 마스터)", "알렉스 (외국인 인턴)", "데미스 (팀장)"
        setting = "트렌드 회의 직전, 쇼츠·릴스 이야기가 오가는 활기찬 사무실."

    if not a_line:
        a_line = f"오늘 회의 끝나고 잠깐 '{word}' 얘기 좀 해볼까요?"
    if not b_line:
        b_line = f"하하, '{word}'라는 말 딱 요즘 분위기에 어울리네요!"

    script = [
        {"speaker": cast_a, "line": f"*(자연스럽게 운을 떼며)* \"{a_line}\""},
        {"speaker": cast_b, "line": f"*(고개를 갸웃하며 메모장을 꺼낸다)* \"잠깐만요! 방금 말씀하신 **'{word}'**가 정확히 무슨 뜻이에요? 교과서엔 없던데요?\""},
        {"speaker": cast_c, "line": f"*(웃으며 통역을 자처한다)* \"{b_line} 쉽게 말해 한국어로 **'{std}'** 같은 느낌이에요!\""},
        {"speaker": cast_b, "line": f"*(무릎을 탁 치며)* \"아하! 이제 맥락이 딱 잡히네요. 오늘 한국인 친구한테 바로 써먹어 봐야겠어요!\""},
    ]
    return script


def build_book2_roleplay(w: dict, idx: int) -> list[dict]:
    """제2권(K-정서) 크로스컬처 상황극 대본(4턴)을 영역별로 구성합니다."""
    word = w["word"]
    sub = w.get("sub_category", "emotion")
    short_def = w.get("short_def", "")
    a_line, b_line = parse_example_lines(w.get("examples", []))

    if sub == "emotion":
        cast_a, cast_b, cast_c = "알렉스 (외국인 동료)", "제니퍼 (수석)", "데미스 (팀장)"
        setting = "비 오는 날 저녁, 따뜻한 차를 마시며 나누는 한국인의 속마음 대화."
    elif sub == "relationship":
        cast_a, cast_b, cast_c = "소피아 (디자이너)", "지훈 (한국인 선배)", "크레이그 (시니어)"
        setting = "함께 프로젝트를 마치고 골목 맛집에 모인 저녁 식사 자리."
    elif sub == "behavior":
        cast_a, cast_b, cast_c = "마크 (교환학생)", "수빈 (한국인 친구)", "크레이그 (시니어)"
        setting = "서울 도심 카페와 거리를 걸으며 마주친 한국인의 일상 리듬."
    else:
        cast_a, cast_b, cast_c = "켄지 (프로듀서)", "서연 (한국인 동료)", "데미스 (팀장)"
        setting = "한국의 회식·모임 문화 속에서 자연스럽게 피어난 문화 교류 에피소드."

    if not a_line:
        a_line = f"한국 사람들은 왜 이런 순간마다 '{word}'라는 말을 자주 쓰나요?"
    if not b_line:
        b_line = f"그건 단순한 단어 하나가 아니라 '{word}'에 담긴 시간과 마음의 결 때문이에요."

    short_tip = short_def.split(".")[0].strip() if short_def else word
    script = [
        {"speaker": cast_a, "line": f"*(진지한 호기심을 담아)* \"{a_line}\""},
        {"speaker": cast_b, "line": f"*(따뜻하게 미소 지으며)* \"{b_line}\""},
        {"speaker": cast_c, "line": f"*(고개를 끄덕이며 거든다)* \"외국어 한 단어로 직역하면 뉘앙스가 다 날아가죠. 핵심은 **{short_tip}**이라는 점이에요.\""},
        {"speaker": cast_a, "line": f"*(감탄하며)* \"단어 하나에 한국인의 삶과 정서가 통째로 들어 있네요. 오늘 **'{word}'**의 진짜 온도를 배웠습니다.\""},
    ]
    return script


def format_lang_bridge(w: dict) -> list[str]:
    langs = [
        ("EN", "en"),
        ("JA", "ja"),
        ("VI", "vi"),
        ("ES", "es"),
        ("ID", "id_lang"),
    ]
    lines = []
    for label, key in langs:
        obj = w.get(key)
        if isinstance(obj, dict):
            slang = obj.get("slang", "").strip()
            desc = obj.get("desc", "").strip()
            if slang or desc:
                lines.append(f"- **{label}**: `{slang}` — {desc}")
    return lines


def generate():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)

    words = db.get("words", [])
    book1_words = [w for w in words if w.get("era") in ("latte", "smartphone", "shorts")]
    book2_words = [w for w in words if w.get("era") == "soul"]

    seed_export = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_words": len(words),
        "book1_count": len(book1_words),
        "book2_count": len(book2_words),
        "book1_units": [],
        "book2_units": [],
    }

    # ==========================
    # 1. 제1권 마스터 원고 생성
    # ==========================
    era_sections = [
        ("latte", "Part 1. 📟 라떼는 말이야 (1990s~2000s 삐삐 · PC통신 · 싸이월드)"),
        ("smartphone", "Part 2. 📱 손안의 혁명 (2010s 스마트폰 · 카카오톡 국민 유행어)"),
        ("shorts", "Part 3. ⚡ 1초 도파민 시대 (2020s~2026 쇼츠 · 릴스 · 틱톡 밈)"),
    ]

    b1_lines = [
        "# 📖 [제1권 완전판] 말쌈: 1990 삐삐에서 2026 릴스까지, 대한민국 신조어 연대기 200",
        "",
        f"> **자동 생성 및 윤문 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M')} · **수록 어휘**: 총 {len(book1_words)}선 (리얼 K-상황극 {len(book1_words)}편 + 다국어 브릿지 포함)",
        "",
        "---",
        "",
    ]

    unit_num = 1
    for era_id, era_title in era_sections:
        subset = [w for w in book1_words if w.get("era") == era_id]
        b1_lines.append(f"## {era_title} ({len(subset)}선)")
        b1_lines.append("")
        for w in subset:
            roman = w.get("romanization") or w.get("pronunciation", "").strip("[]")
            pos = w.get("part_of_speech", "신조어")
            tox = toxicity_badge(int(w.get("toxicity_level", 0)))
            std = w.get("standard_korean_mapping") or "-"
            short_def = w.get("short_def", "")
            origin = w.get("origin", "")
            script = build_book1_roleplay(w, unit_num)
            langs = format_lang_bridge(w)

            b1_lines.append(f"### Unit {unit_num:03d}. {w['word']} ({roman})")
            b1_lines.append(f"- **품사 / 시대**: `{pos}` · `{w.get('era_period', '')}` | **순화 지수**: {tox}")
            b1_lines.append(f"- **표준어 매핑**: *{std}*")
            b1_lines.append("")
            b1_lines.append(f"**💡 뜻과 유래**: {short_def} {origin}".strip())
            b1_lines.append("")
            b1_lines.append("**🎬 리얼 K-상황극**")
            for turn in script:
                b1_lines.append(f"- **{turn['speaker']}**: {turn['line']}")
            b1_lines.append("")
            if langs:
                b1_lines.append("**🌐 다국어 시스템 확장 슬롯**")
                b1_lines.extend(langs)
                b1_lines.append("")
            b1_lines.append("---")
            b1_lines.append("")

            seed_export["book1_units"].append({
                "unit": unit_num,
                "id": w.get("id"),
                "word": w["word"],
                "romanization": roman,
                "era": era_id,
                "standard_korean_mapping": std,
                "short_def": short_def,
                "origin": origin,
                "roleplay_ko": script,
            })
            unit_num += 1

    with open(OUT_BOOK1, "w", encoding="utf-8") as f:
        f.write("\n".join(b1_lines))

    # ==========================
    # 2. 제2권 마스터 원고 생성
    # ==========================
    sub_sections = [
        ("emotion", "Part 1. 💭 마음의 결 — 심리 · 감정 어휘"),
        ("relationship", "Part 2. 🤝 우리라는 울타리 — 관계 · 유대 어휘"),
        ("behavior", "Part 3. 🏃 몸에 밴 리듬 — 습관 · 행동 어휘"),
        ("culture", "Part 4. 🎎 삶의 무늬 — 사회 · 문화 어휘"),
    ]

    b2_lines = [
        "# 💎 [제2권 완전판] 영어엔 없는 한국인의 마음: 눈치부터 정(情)까지 K-소울 118",
        "",
        f"> **자동 생성 및 윤문 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M')} · **수록 어휘**: 총 {len(book2_words)}선 (크로스컬처 상황극 {len(book2_words)}편 + 다국어 브릿지 포함)",
        "",
        "---",
        "",
    ]

    unit_num = 1
    for sub_id, sub_title in sub_sections:
        subset = [w for w in book2_words if w.get("sub_category") == sub_id]
        b2_lines.append(f"## {sub_title} ({len(subset)}선)")
        b2_lines.append("")
        for w in subset:
            roman = w.get("romanization") or w.get("pronunciation", "").strip("[]")
            pos = w.get("part_of_speech", "고유 정서")
            short_def = w.get("short_def", "")
            origin = w.get("origin", "")
            std = w.get("standard_korean_mapping") or "-"
            script = build_book2_roleplay(w, unit_num)
            langs = format_lang_bridge(w)

            b2_lines.append(f"### Unit {unit_num:03d}. {w['word']} ({roman})")
            b2_lines.append(f"- **영역 / 품사**: `{sub_id.upper()}` · `{pos}` | **핵심 개념**: *{std}*")
            b2_lines.append("")
            b2_lines.append(f"**🔍 번역 불가의 이유 & 유래**: {short_def} {origin}".strip())
            b2_lines.append("")
            b2_lines.append("**🎬 크로스컬처 K-상황극**")
            for turn in script:
                b2_lines.append(f"- **{turn['speaker']}**: {turn['line']}")
            b2_lines.append("")
            if langs:
                b2_lines.append("**🌐 다국어 시스템 확장 슬롯**")
                b2_lines.extend(langs)
                b2_lines.append("")
            b2_lines.append("---")
            b2_lines.append("")

            seed_export["book2_units"].append({
                "unit": unit_num,
                "id": w.get("id"),
                "word": w["word"],
                "romanization": roman,
                "sub_category": sub_id,
                "short_def": short_def,
                "origin": origin,
                "roleplay_ko": script,
            })
            unit_num += 1

    with open(OUT_BOOK2, "w", encoding="utf-8") as f:
        f.write("\n".join(b2_lines))

    with open(OUT_SEED, "w", encoding="utf-8") as f:
        json.dump(seed_export, f, ensure_ascii=False, indent=2)

    print(f"SUCCESS: Book1={len(book1_words)} units, Book2={len(book2_words)} units, Total={len(book1_words)+len(book2_words)}")


if __name__ == "__main__":
    generate()

