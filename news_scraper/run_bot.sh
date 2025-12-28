#!/bin/bash
# AI 뉴스 수집기 텔레그램 봇 서버 실행 (Mac/Linux)
# PC에서 이 파일을 실행하면 봇 서버가 시작됩니다

# 스크립트가 있는 디렉토리로 이동
cd "$(dirname "$0")"

echo "========================================"
echo "  AI 뉴스 수집기 - 텔레그램 봇 서버"
echo "========================================"
echo ""
echo "봇 서버를 시작합니다..."
echo "휴대폰 텔레그램에서 봇과 대화하세요!"
echo ""
echo "종료하려면 Ctrl+C를 누르세요."
echo "========================================"
echo ""

python3 telegram_bot.py

if [ $? -ne 0 ]; then
    echo ""
    echo "오류가 발생했습니다!"
    echo "config.json 파일과 봇 토큰을 확인하세요."
    echo ""
    read -p "계속하려면 Enter를 누르세요..."
fi
