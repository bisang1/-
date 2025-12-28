# AI 뉴스 자동 수집기

매일 최신 AI 뉴스를 자동으로 수집하는 Python 스크립트입니다.

## 기능

- 여러 뉴스 소스에서 AI 관련 최신 뉴스 자동 수집
- RSS 피드 및 웹 스크래핑 지원
- 최근 24시간 이내 뉴스만 필터링
- JSON 형식으로 데이터 저장
- 텔레그램 알림 및 블로그 포스팅용으로 활용 가능

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

```bash
python scraper.py
```

또는 실행 권한 부여 후:

```bash
chmod +x scraper.py
./scraper.py
```

## 파일 구조

```
news_scraper/
├── scraper.py              # 메인 스크립트
├── sources.json            # 뉴스 소스 설정
├── collected_news.json     # 수집된 뉴스 (자동 생성)
├── requirements.txt        # 필수 패키지 목록
└── README.md              # 이 파일
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

## 다음 단계

- [ ] 텔레그램 봇 연동 (2단계)
- [ ] 네이버 블로그 자동 포스팅 (3단계)
- [ ] 카테고리별 필터링
- [ ] 키워드 기반 뉴스 수집

## 문제 해결

### 403 Forbidden 오류

일부 사이트는 봇 접근을 차단할 수 있습니다. `scraper.py`의 User-Agent를 변경하거나, 해당 소스를 비활성화하세요.

### 날짜 파싱 오류

특정 날짜 형식이 인식되지 않을 수 있습니다. `python-dateutil` 라이브러리가 대부분의 형식을 지원하지만, 필요시 수동 파싱 로직을 추가하세요.

## 라이선스

MIT License
