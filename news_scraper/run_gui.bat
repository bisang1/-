@echo off
REM AI 뉴스 수집기 GUI 실행 스크립트 (Windows)
REM 이 파일을 더블클릭하면 GUI가 실행됩니다

cd /d "%~dp0"
python gui_app.py

if errorlevel 1 (
    echo.
    echo 오류가 발생했습니다!
    echo Python이 설치되어 있는지 확인하세요.
    echo.
    pause
)
