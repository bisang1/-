# AI 뉴스 자동 수집기

매일 최신 AI 뉴스를 자동으로 수집하는 Python 스크립트입니다.

## 기능

- 여러 뉴스 소스에서 AI 관련 최신 뉴스 자동 수집
- RSS 피드 및 웹 스크래핑 지원
- 최근 24시간 이내 뉴스만 필터링
- JSON 형식으로 데이터 저장
- **텔레그램 자동 알림 전송** ✨ (2단계 완료)
- **사용하기 쉬운 GUI 버전** 🖥️ (NEW!)
- 블로그 포스팅용으로 활용 가능

## 뉴스 소스

1. **AI타임스** - 한국 AI 전문 미디어
2. **전자신문 AI섹션** - 한국 IT 전문 미디어
3. **TechCrunch AI** - 글로벌 테크 뉴스
4. **OpenAI Blog** - OpenAI 공식 블로그

## 설치 방법

### 1. 필수 패키지 설치

```bash
cd news_scraper
pip install -r requirements.txt
```

또는 개별 설치:

```bash
pip install requests beautifulsoup4 python-dateutil lxml
```

### 2. 실행

**방법 1: GUI 버전 (추천)** 🖥️

Windows:
```bash
run_gui.bat 더블클릭
```

Mac/Linux:
```bash
./run_gui.sh
```

**방법 2: 커맨드라인 버전**

```bash
python scraper.py
```

## 🖥️ GUI 버전 사용하기 (초보자 추천!)

### 바탕화면에 바로가기 만들기

```bash
python create_desktop_shortcut.py
```

실행하면 바탕화면에 "AI 뉴스 수집기" 아이콘이 생성됩니다!

### GUI 기능

1. **뉴스 수집 시작** - 버튼 한 번 클릭으로 모든 소스에서 뉴스 수집
2. **텔레그램 테스트** - 텔레그램 봇 연결 확인
3. **수집 결과 보기** - 수집된 뉴스를 예쁘게 표시
4. **설정** - config.json 파일을 자동으로 생성/편집
5. **실시간 로그** - 수집 과정을 실시간으로 확인

### GUI 스크린샷

```
┌────────────────────────────────────┐
│  🤖 AI 뉴스 자동 수집기            │
├────────────────────────────────────┤
│ 📱 텔레그램: ✅ 연결됨    [⚙️ 설정] │
├────────────────────────────────────┤
│ [▶️ 뉴스 수집 시작] [📤 텔레그램 테스트] │
├────────────────────────────────────┤
│ 📋 실행 로그                       │
│ ┌────────────────────────────────┐ │
│ │ [09:00:15] ℹ️ 뉴스 수집 시작... │ │
│ │ [09:00:20] ✅ 15개 뉴스 수집   │ │
│ │ [09:00:25] ✅ 텔레그램 전송 완료│ │
│ └────────────────────────────────┘ │
└────────────────────────────────────┘
```

## 파일 구조

```
news_scraper/
├── gui_app.py                  # 🖥️ GUI 메인 프로그램 (NEW!)
├── run_gui.bat                 # Windows 실행 파일 (NEW!)
├── run_gui.sh                  # Mac/Linux 실행 파일 (NEW!)
├── create_desktop_shortcut.py  # 바탕화면 바로가기 생성 (NEW!)
├── scraper.py                  # 커맨드라인 스크립트
├── telegram_notifier.py        # 텔레그램 알림 모듈
├── sources.json                # 뉴스 소스 설정
├── config.json.example         # 설정 파일 예제
├── config.json                 # 설정 파일 (직접 생성)
├── collected_news.json         # 수집된 뉴스 (자동 생성)
├── requirements.txt            # 필수 패키지 목록
└── README.md                   # 이 파일
```

## 출력 형식

수집된 뉴스는 `collected_news.json`에 다음 형식으로 저장됩니다:

```json
{
  "collected_at": "2025-12-28T08:05:00",
  "total_count": 10,
  "news": [
    {
      "source": "TechCrunch AI",
      "title": "Latest AI Development...",
      "link": "https://...",
      "summary": "요약 내용...",
      "published": "2025-12-28T07:00:00",
      "category": "english"
    }
  ]
}
```

## 뉴스 소스 추가/수정

`sources.json` 파일을 편집하여 뉴스 소스를 추가하거나 수정할 수 있습니다.

### RSS 피드 추가 예시

```json
{
  "name": "뉴스 소스 이름",
  "type": "rss",
  "url": "https://example.com/rss.xml",
  "category": "korean"
}
```

### 웹 스크래핑 추가 예시

```json
{
  "name": "뉴스 소스 이름",
  "type": "scraping",
  "url": "https://example.com/news",
  "category": "korean",
  "selectors": {
    "article": "article.news-item",
    "title": "h2.title",
    "link": "a",
    "date": ".publish-date"
  }
}
```

## 텔레그램 알림 설정 📱

### 1. 텔레그램 봇 생성

1. 텔레그램에서 [@BotFather](https://t.me/botfather) 검색
2. `/newbot` 명령어로 새 봇 생성
3. 봇 이름과 사용자명 설정
4. **봇 토큰** 받기 (예: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. 채팅 ID 확인

1. 생성한 봇과 대화 시작 (아무 메시지나 전송)
2. 브라우저에서 다음 URL 접속:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
3. 응답에서 `"chat":{"id":12345678}` 형태로 **채팅 ID** 확인

### 3. 설정 파일 생성

`config.json.example`을 복사하여 `config.json` 파일을 생성하고 정보를 입력합니다:

```bash
cp config.json.example config.json
```

`config.json` 편집:

```json
{
  "telegram": {
    "bot_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    "chat_id": "12345678",
    "enabled": true
  },
  "scraper": {
    "hours_range": 24,
    "max_news_per_source": 10,
    "summary_length": 200
  },
  "notification": {
    "send_immediately": true,
    "max_news_per_message": 5,
    "include_summary": true
  }
}
```

### 4. 텔레그램 알림 테스트

```bash
python telegram_notifier.py
```

성공 시 텔레그램으로 테스트 메시지가 전송됩니다!

### 5. 스크립트 실행

이제 `scraper.py`를 실행하면 뉴스 수집 후 자동으로 텔레그램 알림이 전송됩니다:

```bash
python scraper.py
```

### 알림 형식

텔레그램으로 전송되는 메시지 예시:

```
🤖 AI 뉴스 브리핑
📅 2025년 12월 28일 09:00
📊 총 15개의 뉴스
━━━━━━━━━━━━━━━━━

🇰🇷 한국 뉴스 (8개)

1. AI 기술 발전의 새로운 전환점
   📌 AI타임스 | 링크

2. 챗GPT 활용 사례 급증
   📌 전자신문 | 링크

   ... 외 6개

🌍 글로벌 뉴스 (7개)

1. OpenAI announces new features
   📌 OpenAI Blog | 링크

   ... 외 6개
```

## 고급 설정

### 수집 시간 범위 변경

`scraper.py`의 `is_recent()` 함수에서 기본값을 변경:

```python
def is_recent(self, pub_date: datetime, hours: int = 24):  # 24시간 → 원하는 시간으로 변경
```

### 요약 길이 조정

RSS 수집 함수에서 요약 길이 변경:

```python
summary = desc_soup.get_text(strip=True)[:200]  # 200자 → 원하는 길이로 변경
```

## 자동화 설정

### Linux/Mac - cron 사용

매일 오전 9시에 자동 실행:

```bash
crontab -e
```

다음 줄 추가:

```
0 9 * * * cd /path/to/news_scraper && python scraper.py
```

### Windows - 작업 스케줄러

1. 작업 스케줄러 열기
2. 기본 작업 만들기
3. 트리거: 매일 오전 9시
4. 동작: 프로그램 시작 → `python.exe`
5. 인수: `C:\path\to\news_scraper\scraper.py`

## 개발 로드맵

- [x] ~~뉴스 자동 수집 (1단계)~~ ✅
- [x] ~~텔레그램 봇 연동 (2단계)~~ ✅
- [ ] 네이버 블로그 자동 포스팅 (3단계)
- [ ] 카테고리별 필터링 강화
- [ ] 키워드 기반 뉴스 수집
- [ ] AI 요약 기능 (GPT API 연동)

## 문제 해결

### 403 Forbidden 오류

일부 사이트는 봇 접근을 차단할 수 있습니다. `scraper.py`의 User-Agent를 변경하거나, 해당 소스를 비활성화하세요.

### 날짜 파싱 오류

특정 날짜 형식이 인식되지 않을 수 있습니다. `python-dateutil` 라이브러리가 대부분의 형식을 지원하지만, 필요시 수동 파싱 로직을 추가하세요.

## 라이선스

MIT License
