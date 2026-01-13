@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo 🌸 낭만처방 쇼츠 생성기를 시작합니다...
echo.
echo 브라우저에서 http://localhost:8501 로 접속하세요.
echo 휴대폰에서 접속: 같은 WiFi 연결 후 http://[컴퓨터IP]:8501
echo.
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
pause
