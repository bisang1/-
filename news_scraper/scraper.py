#!/usr/bin/env python3
"""
AI 뉴스 자동 수집 스크립트
최신 AI 관련 뉴스를 여러 소스에서 수집하여 JSON 파일로 저장합니다.
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
import re


class NewsCollector:
    """뉴스 수집 및 처리를 담당하는 클래스"""

    def __init__(self, sources_file: str = 'sources.json'):
        """
        Args:
            sources_file: 뉴스 소스 설정 파일 경로
        """
        self.sources_file = sources_file
        self.sources = self._load_sources()
        self.collected_news = []

    def _load_sources(self) -> List[Dict]:
        """뉴스 소스 설정 파일을 읽어옵니다."""
        try:
            with open(self.sources_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('sources', [])
        except FileNotFoundError:
            print(f"❌ {self.sources_file} 파일을 찾을 수 없습니다.")
            return []
        except json.JSONDecodeError:
            print(f"❌ {self.sources_file} 파일 형식이 잘못되었습니다.")
            return []

    def is_recent(self, pub_date: datetime, hours: int = 24) -> bool:
        """
        발행일이 최근 N시간 이내인지 확인합니다.

        Args:
            pub_date: 발행일시
            hours: 기준 시간 (기본값: 24시간)

        Returns:
            최근 뉴스 여부
        """
        now = datetime.now()
        # pub_date가 timezone-aware일 경우를 대비해 처리
        if pub_date.tzinfo is not None:
            from datetime import timezone
            now = datetime.now(timezone.utc)

        cutoff_time = now - timedelta(hours=hours)
        return pub_date >= cutoff_time

    def collect_from_rss(self, source: Dict) -> List[Dict]:
        """
        RSS 피드에서 뉴스를 수집합니다.

        Args:
            source: 뉴스 소스 정보

        Returns:
            수집된 뉴스 리스트
        """
        news_list = []

        try:
            print(f"📡 RSS 수집 중: {source['name']}...")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(source['url'], headers=headers, timeout=10)
            response.raise_for_status()

            # RSS XML 파싱
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')

            for item in items:
                try:
                    # 제목 추출
                    title_tag = item.find('title')
                    if not title_tag:
                        continue
                    title = title_tag.get_text(strip=True)

                    # 링크 추출
                    link_tag = item.find('link')
                    if not link_tag:
                        continue
                    link = link_tag.get_text(strip=True)

                    # 발행일 파싱
                    pub_date = None
                    pub_date_tag = item.find('pubDate') or item.find('published') or item.find('dc:date')
                    if pub_date_tag:
                        try:
                            pub_date = date_parser.parse(pub_date_tag.get_text(strip=True))
                        except:
                            pass

                    # 최근 24시간 이내 뉴스만 수집
                    if pub_date and not self.is_recent(pub_date):
                        continue

                    # 요약 추출
                    summary = ''
                    desc_tag = item.find('description') or item.find('summary') or item.find('content:encoded')
                    if desc_tag:
                        # HTML 태그 제거
                        desc_soup = BeautifulSoup(desc_tag.get_text(), 'html.parser')
                        summary = desc_soup.get_text(strip=True)[:200]  # 200자까지만

                    news_item = {
                        'source': source['name'],
                        'title': title,
                        'link': link,
                        'summary': summary,
                        'published': pub_date.isoformat() if pub_date else datetime.now().isoformat(),
                        'category': source.get('category', 'unknown')
                    }

                    news_list.append(news_item)

                except Exception as e:
                    print(f"  ⚠️ 항목 처리 중 오류: {str(e)}")
                    continue

            print(f"  ✅ {len(news_list)}개의 뉴스 수집 완료")

        except Exception as e:
            print(f"  ❌ RSS 수집 실패: {str(e)}")

        return news_list

    def collect_from_scraping(self, source: Dict) -> List[Dict]:
        """
        웹 스크래핑으로 뉴스를 수집합니다.

        Args:
            source: 뉴스 소스 정보

        Returns:
            수집된 뉴스 리스트
        """
        news_list = []

        try:
            print(f"🌐 웹 스크래핑 중: {source['name']}...")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(source['url'], headers=headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')
            selectors = source.get('selectors', {})

            # 기사 목록 추출
            articles = soup.select(selectors.get('article', 'article'))

            for article in articles[:10]:  # 최대 10개까지만
                try:
                    # 제목 추출
                    title_elem = article.select_one(selectors.get('title', 'h2'))
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)

                    # 링크 추출
                    link_elem = article.select_one(selectors.get('link', 'a'))
                    if not link_elem:
                        continue
                    link = link_elem.get('href', '')

                    # 상대 경로를 절대 경로로 변환
                    if link.startswith('/'):
                        from urllib.parse import urljoin
                        link = urljoin(source['url'], link)

                    # 날짜 추출 (선택적)
                    date_elem = article.select_one(selectors.get('date', '.date'))
                    pub_date = datetime.now()
                    if date_elem:
                        try:
                            pub_date = date_parser.parse(date_elem.get_text(strip=True))
                        except:
                            pass

                    news_item = {
                        'source': source['name'],
                        'title': title,
                        'link': link,
                        'summary': '',
                        'published': pub_date.isoformat(),
                        'category': source.get('category', 'unknown')
                    }

                    news_list.append(news_item)

                except Exception as e:
                    print(f"  ⚠️ 항목 처리 중 오류: {str(e)}")
                    continue

            print(f"  ✅ {len(news_list)}개의 뉴스 수집 완료")

        except Exception as e:
            print(f"  ❌ 웹 스크래핑 실패: {str(e)}")

        return news_list

    def collect_all(self) -> List[Dict]:
        """
        모든 소스에서 뉴스를 수집합니다.

        Returns:
            수집된 전체 뉴스 리스트
        """
        print(f"\n🚀 뉴스 수집을 시작합니다...\n")

        for source in self.sources:
            if source.get('type') == 'rss':
                news = self.collect_from_rss(source)
                self.collected_news.extend(news)
            elif source.get('type') == 'scraping':
                news = self.collect_from_scraping(source)
                self.collected_news.extend(news)
            print()

        # 발행일 기준으로 정렬 (최신순)
        self.collected_news.sort(
            key=lambda x: x.get('published', ''),
            reverse=True
        )

        return self.collected_news

    def save_to_json(self, output_file: str = 'collected_news.json'):
        """
        수집된 뉴스를 JSON 파일로 저장합니다.

        Args:
            output_file: 출력 파일 경로
        """
        try:
            data = {
                'collected_at': datetime.now().isoformat(),
                'total_count': len(self.collected_news),
                'news': self.collected_news
            }

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"💾 {output_file}에 저장 완료!")
            print(f"📊 총 {len(self.collected_news)}개의 뉴스를 수집했습니다.\n")

        except Exception as e:
            print(f"❌ 파일 저장 실패: {str(e)}")

    def print_summary(self):
        """수집 결과 요약을 출력합니다."""
        if not self.collected_news:
            print("수집된 뉴스가 없습니다.")
            return

        print("=" * 60)
        print("📰 수집된 뉴스 요약")
        print("=" * 60)

        # 소스별 통계
        source_stats = {}
        for news in self.collected_news:
            source = news['source']
            source_stats[source] = source_stats.get(source, 0) + 1

        for source, count in source_stats.items():
            print(f"  • {source}: {count}개")

        print("\n" + "=" * 60)
        print("최신 뉴스 5개:")
        print("=" * 60)

        for i, news in enumerate(self.collected_news[:5], 1):
            print(f"\n{i}. [{news['source']}] {news['title']}")
            print(f"   🔗 {news['link']}")
            if news['summary']:
                print(f"   📝 {news['summary'][:100]}...")

        print("\n" + "=" * 60 + "\n")


def load_config(config_file: str = 'config.json') -> Optional[Dict]:
    """
    설정 파일을 로드합니다.

    Args:
        config_file: 설정 파일 경로

    Returns:
        설정 딕셔너리 또는 None
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  {config_file} 파일을 찾을 수 없습니다. (텔레그램 알림 비활성화)")
        return None
    except json.JSONDecodeError:
        print(f"❌ {config_file} 파일 형식이 잘못되었습니다.")
        return None


def main():
    """메인 실행 함수"""
    # 현재 스크립트의 디렉토리로 이동
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # 설정 로드
    config = load_config()

    # 뉴스 수집기 초기화
    collector = NewsCollector()

    # 뉴스 수집
    collector.collect_all()

    # 결과 요약 출력
    collector.print_summary()

    # JSON 파일로 저장
    collector.save_to_json()

    # 텔레그램 알림 전송
    if config and config.get('telegram', {}).get('enabled', False):
        try:
            from telegram_notifier import TelegramNotifier

            telegram_config = config['telegram']
            bot_token = telegram_config.get('bot_token', '')
            chat_id = telegram_config.get('chat_id', '')

            if bot_token and chat_id and bot_token != 'YOUR_BOT_TOKEN_HERE':
                print("📱 텔레그램 알림 전송 중...\n")

                notifier = TelegramNotifier(bot_token, chat_id)

                notification_config = config.get('notification', {})
                max_news = notification_config.get('max_news_per_message', 5)
                include_summary = notification_config.get('include_summary', True)

                # 뉴스 알림 전송
                if notifier.send_news_notification(
                    collector.collected_news,
                    format_type='category',
                    max_news=max_news,
                    include_summary=include_summary
                ):
                    print("✅ 텔레그램 알림 전송 완료!\n")
                else:
                    print("❌ 텔레그램 알림 전송 실패\n")
            else:
                print("⚠️  텔레그램 봇 정보가 설정되지 않았습니다.\n")

        except ImportError:
            print("❌ telegram_notifier 모듈을 찾을 수 없습니다.\n")
        except Exception as e:
            print(f"❌ 텔레그램 알림 중 오류: {str(e)}\n")


if __name__ == '__main__':
    main()
