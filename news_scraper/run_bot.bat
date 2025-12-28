@echo off
REM AI 뉴스 수집기 텔레그램 봇 서버 실행 (Windows)
REM PC에서 이 파일을 실행하면 봇 서버가 시작됩니다

cd /d "%~dp0"

echo ========================================
echo   AI 뉴스 수집기 - 텔레그램 봇 서버
echo ========================================
echo.
echo 봇 서버를 시작합니다...
echo 휴대폰 텔레그램에서 봇과 대화하세요!
echo.
echo 종료하려면 Ctrl+C를 누르세요.
echo ========================================
echo.

python telegram_bot.py

if errorlevel 1 (
    echo.
    echo 오류가 발생했습니다!
    echo config.json 파일과 봇 토큰을 확인하세요.
    echo.
    pause
)
