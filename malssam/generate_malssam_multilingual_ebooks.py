"""
generate_malssam_multilingual_ebooks.py
malssam/words_db.json (318단어) + malssam/global/ 다국어 체계(ko, en, ja, es, fr, id) 연동
1) malssam/global/books/ 에 6개국어 파생 마크다운(12종) 동시 생성
2) data/novels/malssam_slang_200.{json,js} & malssam_ksoul_118.{json,js} 생성
3) data/novels_index.json 에 DMDG 서재(eBook & Audio) 정식 등재
"""

import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(BASE_DIR, "words_db.json")
GLOBAL_BOOKS_DIR = os.path.join(BASE_DIR, "global", "books")
NOVELS_DIR = os.path.join(ROOT_DIR, "data", "novels")
INDEX_PATH = os.path.join(ROOT_DIR, "data", "novels_index.json")

LANGS = ["ko", "en", "ja", "es", "fr", "id"]

LANG_LABELS = {
    "ko": {
        "meaning": "뜻과 유래",
        "std": "표준어 매핑",
        "roleplay": "실전 K-상황극",
        "ex_lead": "실제 대화",
    },
    "en": {
        "meaning": "Meaning & Origin",
        "std": "Standard Korean",
        "roleplay": "K-Culture Roleplay",
        "ex_lead": "Dialogue",
    },
    "ja": {
        "meaning": "意味と由来",
        "std": "標準語マッピング",
        "roleplay": "実戦K-状況劇",
        "ex_lead": "会話例",
    },
    "es": {
        "meaning": "Significado y Origen",
        "std": "Coreano Estándar",
        "roleplay": "Dramatización K-Culture",
        "ex_lead": "Diálogo",
    },
    "fr": {
        "meaning": "Sens et Origine",
        "std": "Coréen Standard",
        "roleplay": "Jeu de Rôle K-Culture",
        "ex_lead": "Dialogue",
    },
    "id": {
        "meaning": "Arti & Asal-Usul",
        "std": "Bahasa Korea Standar",
        "roleplay": "Simulasi Situasi K-Culture",
        "ex_lead": "Dialog",
    },
}


def clean_ex(raw_ex: str) -> str:
    if not raw_ex:
        return ""
    return " / ".join([ln.strip() for ln in str(raw_ex).splitlines() if ln.strip()])


def format_word_block(w: dict, lang: str, idx: int) -> str:
    word = w["word"]
    roman = w.get("romanization") or w.get("pronunciation", "").strip("[]")
    lbl = LANG_LABELS[lang]

    if lang == "ko":
        short_def = w.get("short_def", "")
        origin = w.get("origin", "")
        std = w.get("standard_korean_mapping") or "-"
        ex = clean_ex(w.get("examples", [""])[0] if w.get("examples") else "")
        return (
            f"### {idx:03d}. {word} ({roman})\n"
            f"- **{lbl['std']}**: {std}\n"
            f"- **{lbl['meaning']}**: {short_def} {origin}\n"
            f"- **{lbl['roleplay']}**: {ex}\n"
        )

    db_key = "id_lang" if lang == "id" else ("en" if lang == "fr" else lang)
    loc = w.get(db_key) if isinstance(w.get(db_key), dict) else w.get("en", {})
    slang = loc.get("slang", word)
    desc = loc.get("desc", w.get("short_def", ""))
    ex = clean_ex(loc.get("ex") or loc.get("example") or (w.get("examples", [""])[0] if w.get("examples") else ""))

    if lang == "fr":
        return (
            f"### {idx:03d}. {word} ({roman}) — {slang}\n"
            f"- **{lbl['meaning']}**: {desc}\n"
            f"- **{lbl['roleplay']}**: {ex}\n"
        )

    return (
        f"### {idx:03d}. {word} ({roman}) — {slang}\n"
        f"- **{lbl['meaning']}**: {desc}\n"
        f"- **{lbl['roleplay']}**: {ex}\n"
    )


def build_chapters(words_subset: list, groups: list, book_type: str) -> list:
    chapters = []
    for ch_idx, (group_key, part_name, titles_dict) in enumerate(groups, start=1):
        field = "era" if book_type == "book1" else "sub_category"
        items = [w for w in words_subset if w.get(field) == group_key]
        content_by_lang = {}
        for lang in LANGS:
            blocks = [format_word_block(w, lang, i + 1) for i, w in enumerate(items)]
            content_by_lang[lang] = "\n\n".join(blocks)
        chapters.append({
            "ch": ch_idx,
            "part": part_name,
            "title": titles_dict,
            "content": content_by_lang,
        })
    return chapters


def export_global_markdowns(book_id: str, title_map: dict, chapters: list):
    os.makedirs(GLOBAL_BOOKS_DIR, exist_ok=True)
    for lang in LANGS:
        md_path = os.path.join(GLOBAL_BOOKS_DIR, f"{book_id}_{lang}.md")
        lines = [f"# {title_map[lang]}", ""]
        for ch in chapters:
            lines.append(f"## {ch['title'][lang]}")
            lines.append("")
            lines.append(ch["content"][lang])
            lines.append("")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def save_novel_files(novel_id: str, var_name: str, payload: dict):
    os.makedirs(NOVELS_DIR, exist_ok=True)
    json_path = os.path.join(NOVELS_DIR, f"{novel_id}.json")
    js_path = os.path.join(NOVELS_DIR, f"{novel_id}.js")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(f"window.{var_name} = ")
        json.dump(payload, f, ensure_ascii=False)
        f.write(";\n")


def main():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        words = json.load(f).get("words", [])

    book1_words = [w for w in words if w.get("era") in ("latte", "smartphone", "shorts")]
    book2_words = [w for w in words if w.get("era") == "soul"]

    b1_groups = [
        (
            "latte",
            "Part 1 · 1990s~2000s",
            {
                "ko": "Part 1. 라떼 추억: 1990s~2000s 삐삐·PC통신·싸이월드 (27선)",
                "en": "Part 1. Retro Nostalgia: 1990s~2000s Pager & PC Telecom Slang (27)",
                "ja": "Part 1. レトロ思い出：1990〜2000年代ポケベル・PC通信流行語 (27選)",
                "es": "Parte 1. Nostalgia Retro: Jerga Coreana de los 90 y 2000 (27)",
                "fr": "Partie 1. Nostalgie Rétro : Argot Coréen des Années 90-2000 (27)",
                "id": "Bagian 1. Nostalgia Retro: Bahasa Gaul Korea Era 90an-2000an (27)",
            },
        ),
        (
            "smartphone",
            "Part 2 · 2010s",
            {
                "ko": "Part 2. 국민 유행어: 2010s 스마트폰·카카오톡 시대 (31선)",
                "en": "Part 2. Smartphone Era: 2010s National KakaoTalk Slang (31)",
                "ja": "Part 2. 国民的流行語：2010年代スマホ・カカオトーク時代 (31選)",
                "es": "Parte 2. Era Smartphone: Modismos Populares de los 2010 (31)",
                "fr": "Partie 2. Ère Smartphone : Expressions Populaires des Années 2010 (31)",
                "id": "Bagian 2. Era Smartphone: Bahasa Gaul Populer Tahun 2010-an (31)",
            },
        ),
        (
            "shorts",
            "Part 3 · 2020s~2026",
            {
                "ko": "Part 3. 1초 도파민: 2020s~2026 쇼츠·릴스·틱톡 1020 밈 (142선)",
                "en": "Part 3. Shorts & Reels Era: 2020s~2026 Gen-Z Memes (142)",
                "ja": "Part 3. ショート動画時代：2020〜2026年 1020世代ミーム (142選)",
                "es": "Parte 3. Era Reels y TikTok: Memes Gen-Z 2020-2026 (142)",
                "fr": "Partie 3. Ère Reels & TikTok : Mèmes Gen-Z 2020-2026 (142)",
                "id": "Bagian 3. Era Shorts & Reels: Meme Gen-Z 2020-2026 (142)",
            },
        ),
    ]

    b2_groups = [
        (
            "emotion",
            "Part 1 · 심리·감정",
            {
                "ko": "Part 1. 마음의 결: 심리 · 감정 K-정서 (36선)",
                "en": "Part 1. Textures of Mind: Untranslatable K-Emotions (36)",
                "ja": "Part 1. 心の機微：翻訳不能な韓国の心理・感情 (36選)",
                "es": "Parte 1. Texturas de la Mente: Emociones K-Soul (36)",
                "fr": "Partie 1. Nuances de l'Esprit : Émotions Coréennes Intraduisibles (36)",
                "id": "Bagian 1. Nuansa Batin: Emosi Korea yang Tak Terjemahkan (36)",
            },
        ),
        (
            "relationship",
            "Part 2 · 관계·유대",
            {
                "ko": "Part 2. 우리라는 울타리: 관계 · 유대 K-정서 (25선)",
                "en": "Part 2. Bonds of 'Uri': Korean Relationships & Jeong (25)",
                "ja": "Part 2. 「ウリ（私たち）」の絆：関係・情の表現 (25選)",
                "es": "Parte 2. Lazos de 'Uri': Relaciones y Afecto Coreano (25)",
                "fr": "Partie 2. Liens de 'Uri' : Relations et Affection Coréenne (25)",
                "id": "Bagian 2. Ikatan 'Uri': Hubungan & Kehangatan Korea (25)",
            },
        ),
        (
            "behavior",
            "Part 3 · 습관·행동",
            {
                "ko": "Part 3. 몸에 밴 리듬: 습관 · 행동 K-정서 (25선)",
                "en": "Part 3. Rhythms of Life: Korean Habits & Behaviors (25)",
                "ja": "Part 3. 生活のリズム：韓国特有の習慣・行動 (25選)",
                "es": "Parte 3. Ritmos de Vida: Hábitos y Conductas Coreanas (25)",
                "fr": "Partie 3. Rythmes de Vie : Habitudes Coréennes (25)",
                "id": "Bagian 3. Ritme Hidup: Kebiasaan & Perilaku Khas Korea (25)",
            },
        ),
        (
            "culture",
            "Part 4 · 사회·문화",
            {
                "ko": "Part 4. 삶의 무늬: 사회 · 문화 K-정서 (32선)",
                "en": "Part 4. Tapestry of Society: Korean Culture & Traditions (32)",
                "ja": "Part 4. 暮らしの模様：韓国の社会・文化表現 (32選)",
                "es": "Parte 4. Tapiz Social: Cultura y Tradiciones Coreanas (32)",
                "fr": "Partie 4. Tapisserie Sociale : Culture et Traditions Coréennes (32)",
                "id": "Bagian 4. Corak Sosial: Budaya & Tradisi Masyarakat Korea (32)",
            },
        ),
    ]

    b1_title = {
        "ko": "말쌈: 대한민국 신조어 연대기 200선",
        "en": "MALSSAM: 200 Korean Slang & Memes (1990–2026)",
        "ja": "マルッサム：韓国語新造語・ミーム年代記 200選",
        "es": "MALSSAM: 200 Modismos y Memes Coreanos",
        "fr": "MALSSAM : 200 Argots et Mèmes Coréens",
        "id": "MALSSAM: 200 Bahasa Gaul & Meme Korea",
    }
    b1_sub = {
        "ko": "1990 삐삐에서 2026 릴스까지, K-상황극으로 배우는 살아있는 한국어",
        "en": "From 1990s Pagers to 2026 Reels — Living Korean with Roleplays",
        "ja": "1990年ポケベルから2026年リールまで、状況劇で学ぶ韓国語",
        "es": "De los años 90 a 2026: Coreano vivo con dramatizaciones",
        "fr": "Des années 90 à 2026 : Le coréen vivant par le jeu de rôle",
        "id": "Dari Era 90-an hingga Reels 2026 dengan Simulasi Dialog",
    }

    b2_title = {
        "ko": "영어엔 없는 한국인의 마음: K-소울 118선",
        "en": "Untranslatable Korean Soul: 118 Words from Nunchi to Jeong",
        "ja": "英語にはない韓国人の心：ヌンチから情まで K-ソウル 118選",
        "es": "El Alma Coreana Intraducible: 118 Palabras de Nunchi a Jeong",
        "fr": "L'Âme Coréenne Intraduisible : 118 Mots de Nunchi à Jeong",
        "id": "Jiwa Korea yang Tak Terjemahkan: 118 Kata K-Soul",
    }
    b2_sub = {
        "ko": "눈치부터 정(情)까지, 직역할 수 없는 한국인의 정서와 크로스컬처 상황극",
        "en": "Deep Korean emotional & cultural expressions with cross-cultural roleplays",
        "ja": "直訳できない韓国人の情緒をクロスカルチャー状況劇で読み解く",
        "es": "Expresiones emocionales y culturales coreanas imposibles de traducir",
        "fr": "Expressions émotionnelles et culturelles coréennes uniques",
        "id": "Ekspresi emosional dan budaya Korea yang penuh makna",
    }

    b1_chapters = build_chapters(book1_words, b1_groups, "book1")
    b2_chapters = build_chapters(book2_words, b2_groups, "book2")

    export_global_markdowns("book1_slang_200", b1_title, b1_chapters)
    export_global_markdowns("book2_ksoul_118", b2_title, b2_chapters)

    b1_chars = sum(len(ch["content"]["ko"]) for ch in b1_chapters)
    b2_chars = sum(len(ch["content"]["ko"]) for ch in b2_chapters)

    b1_payload = {
        "id": "malssam_slang_200",
        "title": b1_title,
        "subtitle": b1_sub,
        "author": "DMDG × MALSSAM",
        "badge": "말쌈 신조어 단행본 200선",
        "category": "K-Language · 신조어",
        "cover_gradient": "linear-gradient(135deg, #0f172a 0%, #0284c7 100%)",
        "cover_accent": "#38bdf8",
        "charCount": b1_chars,
        "readingTime": max(15, b1_chars // 700),
        "total_chapters": len(b1_chapters),
        "description": b1_sub["ko"],
        "chapters": b1_chapters,
    }

    b2_payload = {
        "id": "malssam_ksoul_118",
        "title": b2_title,
        "subtitle": b2_sub,
        "author": "DMDG × MALSSAM",
        "badge": "말쌈 K-정서 단행본 118선",
        "category": "K-Soul · 인문교양",
        "cover_gradient": "linear-gradient(135deg, #1c1917 0%, #d97706 100%)",
        "cover_accent": "#fbbf24",
        "charCount": b2_chars,
        "readingTime": max(12, b2_chars // 700),
        "total_chapters": len(b2_chapters),
        "description": b2_sub["ko"],
        "chapters": b2_chapters,
    }

    save_novel_files("malssam_slang_200", "NOVEL_MALSSAM_SLANG_200_DATA", b1_payload)
    save_novel_files("malssam_ksoul_118", "NOVEL_MALSSAM_KSOUL_118_DATA", b2_payload)

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index_list = json.load(f)

    # 기존 동일 id 제거 후 추가 (멱등성 보장)
    index_list = [item for item in index_list if item.get("id") not in ("malssam_slang_200", "malssam_ksoul_118")]
    index_list.extend([
        {
            "id": "malssam_slang_200",
            "title": b1_title,
            "subtitle": b1_sub,
            "author": "DMDG × MALSSAM",
            "badge": "말쌈 신조어 200선",
            "category": "K-Language · 신조어",
            "color": "#0284c7",
            "synopsis": b1_sub,
            "charCount": b1_chars,
            "readingTime": b1_payload["readingTime"],
            "chapterCount": len(b1_chapters),
            "htmlUrl": "novel_malssam_slang_200.html",
            "jsonUrl": "data/novels/malssam_slang_200.json",
            "languages": LANGS,
        },
        {
            "id": "malssam_ksoul_118",
            "title": b2_title,
            "subtitle": b2_sub,
            "author": "DMDG × MALSSAM",
            "badge": "말쌈 K-정서 118선",
            "category": "K-Soul · 인문교양",
            "color": "#d97706",
            "synopsis": b2_sub,
            "charCount": b2_chars,
            "readingTime": b2_payload["readingTime"],
            "chapterCount": len(b2_chapters),
            "htmlUrl": "novel_malssam_ksoul_118.html",
            "jsonUrl": "data/novels/malssam_ksoul_118.json",
            "languages": LANGS,
        },
    ])

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index_list, f, ensure_ascii=False, indent=2)

    print(f"MULTILINGUAL & LIBRARY SYNC DONE: total_books_in_index={len(index_list)}")


if __name__ == "__main__":
    main()

