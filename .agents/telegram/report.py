#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
영숙 비서 - 텔레그램 작업 현황 정기 보고 봇
매 1시간마다 실행 (Windows 작업 스케줄러로 자동 실행)
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ─── 설정 ───────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent  # connect_dmdg/.agent
PROJECT_ROOT = BASE_DIR.parent           # connect_dmdg/

BOT_TOKEN = "8837085399:AAHDcjtBpBF04yiQTOukpmmSoXryRdtnQ0A"
CHAT_ID   = "8294524472"

KST = timezone(timedelta(hours=9))

# 프로젝트 목록 및 설명
PROJECTS = {
    "kvj-app":        "K-Virtual Journey 메타버스 게임",
    "dmdg_voice":     "보이스 서비스",
    "global_service": "글로벌 서비스 웹앱",
    "dmdg_test":      "당목담글 테스트",
    "stitch_test":    "스티치 테스트",
}

# ─── 유틸 ────────────────────────────────────────────────

def send_telegram(text: str):
    """텔레그램 메시지 전송"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id":    CHAT_ID,
        "text":       text,
        "parse_mode": "HTML",
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def get_project_status(proj_dir: Path) -> dict:
    """프로젝트 디렉토리의 최근 수정 파일 및 상태 확인"""
    if not proj_dir.exists():
        return {"status": "⚠️", "detail": "디렉토리 없음"}

    files = list(proj_dir.rglob("*"))
    files = [f for f in files if f.is_file() and ".git" not in str(f)]

    if not files:
        return {"status": "⏳", "detail": "파일 없음"}

    latest = max(files, key=lambda f: f.stat().st_mtime)
    mtime  = datetime.fromtimestamp(latest.stat().st_mtime, tz=KST)
    now    = datetime.now(tz=KST)
    diff   = now - mtime

    if diff.total_seconds() < 3600:
        status = "🔄"
        time_str = f"{int(diff.total_seconds() // 60)}분 전 수정"
    elif diff.total_seconds() < 86400:
        status = "🟡"
        time_str = f"{int(diff.total_seconds() // 3600)}시간 전 수정"
    else:
        status = "⏳"
        time_str = f"{diff.days}일 전 수정"

    return {
        "status":  status,
        "detail":  time_str,
        "file":    latest.name,
        "count":   len(files),
    }


def build_report() -> str:
    """작업 현황 보고 메시지 생성"""
    now = datetime.now(tz=KST)
    time_str = now.strftime("%Y-%m-%d %p %I:%M").replace("AM", "오전").replace("PM", "오후")

    lines = [
        "📋 <b>영숙 비서입니다, 사장님!</b>",
        f"⏰ <b>{time_str}</b> 작업 현황 보고드립니다.",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "📁 <b>프로젝트별 현황</b>",
        "━━━━━━━━━━━━━━━━━━━━",
    ]

    active_count = 0
    issues = []

    for proj_name, proj_desc in PROJECTS.items():
        proj_dir = PROJECT_ROOT / proj_name
        info = get_project_status(proj_dir)

        status  = info["status"]
        detail  = info["detail"]
        file    = info.get("file", "")
        count   = info.get("count", 0)

        line = f"{status} <b>{proj_name}</b> — {detail}"
        if file:
            line += f"\n    └ 최근: {file} ({count}개 파일)"
        lines.append(line)

        if status == "🔄":
            active_count += 1
        if status == "⚠️":
            issues.append(f"• {proj_name}: {detail}")

    # 이슈 섹션
    lines += ["", "━━━━━━━━━━━━━━━━━━━━"]
    if issues:
        lines += ["🚨 <b>이슈 &amp; 병목</b>", "━━━━━━━━━━━━━━━━━━━━"]
        lines += issues
    else:
        lines += ["✅ <b>이슈 없음</b> — 모든 프로젝트 정상"]

    # 에이전트 팀 현황
    lines += [
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "👥 <b>팀 대기 현황</b>",
        "━━━━━━━━━━━━━━━━━━━━",
        "🟢 레오(CEO) · 조박사 · 루나 · 코다리 — 대기 중",
        "🟢 작가김 · 형사박 · 정감독 · 현빈 — 대기 중",
    ]

    # 다음 보고 안내
    next_time = (now + timedelta(hours=1)).strftime("%H:%M")
    lines += [
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        f"💼 다음 보고: <b>{next_time}</b>",
        "제가 챙겨두겠습니다! ✅",
    ]

    return "\n".join(lines)


# ─── 메인 ────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"[{datetime.now(tz=KST).strftime('%H:%M:%S')}] 영숙 비서 보고 시작...")
    try:
        report = build_report()
        result = send_telegram(report)
        if result.get("ok"):
            print("[OK] 텔레그램 전송 성공!")
        else:
            print(f"[FAIL] 전송 실패: {result}")
    except Exception as e:
        print(f"[ERROR] 오류 발생: {e}")
        sys.exit(1)
