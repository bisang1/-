#!/bin/bash
# AI 뉴스 수집기 GUI 실행 스크립트 (Mac/Linux)
# 이 파일을 더블클릭하거나 터미널에서 실행하세요

# 스크립트가 있는 디렉토리로 이동
cd "$(dirname "$0")"

# GUI 실행
python3 gui_app.py

# 오류 발생 시 메시지 표시
if [ $? -ne 0 ]; then
    echo ""
    echo "오류가 발생했습니다!"
    echo "Python 3가 설치되어 있는지 확인하세요."
    echo ""
    read -p "계속하려면 Enter를 누르세요..."
fi
