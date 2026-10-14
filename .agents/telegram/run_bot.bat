@echo off
chcp 65001 > nul
title 당목담글 Great AI 마스터 팀 텔레그램 봇
echo =====================================================================
echo    🍊 당목담글 Great AI 마스터 팀 텔레그램 양방향 봇을 실행합니다
echo    봇 계정: @aiffall_bot
echo    에이전트: 12인 마스터 전원 + 대기업 HR 7인
echo =====================================================================
echo.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
python bot.py
echo.
pause
