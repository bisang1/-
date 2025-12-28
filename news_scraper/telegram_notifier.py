#!/usr/bin/env python3
"""
텔레그램 알림 모듈
수집된 뉴스를 텔레그램으로 전송합니다.
"""

import json
import requests
from typing import List, Dict, Optional
from datetime import datetime


class TelegramNotifier:
    """텔레그램 봇을 통한 알림 전송 클래스"""

    def __init__(self, bot_token: str, chat_id: str):
        """
        Args:
            bot_token: 텔레그램 봇 토큰
            chat_id: 메시지를 받을 채팅 ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, text: str, parse_mode: str = 'HTML') -> bool:
        """
        텔레그램으로 메시지를 전송합니다.

        Args:
            text: 전송할 메시지
            parse_mode: 메시지 파싱 모드 (HTML, Markdown 등)

        Returns:
            전송 성공 여부
        """
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': False
            }

            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            result = response.json()
            if result.get('ok'):
                return True
            else:
                print(f"❌ 텔레그램 전송 실패: {result.get('description', 'Unknown error')}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"❌ 텔레그램 API 요청 실패: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ 메시지 전송 중 오류: {str(e)}")
            return False

    def format_news_message(self, news_list: List[Dict], max_news: int = 5, include_summary: bool = True) -> str:
        """
        뉴스 목록을 텔레그램 메시지 형식으로 변환합니다.

        Args:
            news_list: 뉴스 리스트
            max_news: 한 번에 전송할 최대 뉴스 개수
            include_summary: 요약 포함 여부

        Returns:
            포맷된 메시지 문자열
        """
        if not news_list:
            return "📰 오늘 수집된 AI 뉴스가 없습니다."

        # 메시지 헤더
        message = f"🤖 <b>AI 뉴스 브리핑</b>\n"
        message += f"📅 {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}\n"
        message += f"📊 총 {len(news_list)}개의 뉴스\n"
        message += "━━━━━━━━━━━━━━━━━\n\n"

        # 뉴스 목록 (최대 max_news개까지만)
        for i, news in enumerate(news_list[:max_news], 1):
            # 제목과 링크
            title = self._escape_html(news.get('title', '제목 없음'))
            link = news.get('link', '')
            source = self._escape_html(news.get('source', '출처 미상'))

            message += f"{i}. <b>{title}</b>\n"
            message += f"   📌 출처: {source}\n"

            # 요약 포함 (옵션)
            if include_summary and news.get('summary'):
                summary = self._escape_html(news['summary'][:150])
                if len(news['summary']) > 150:
                    summary += "..."
                message += f"   💬 {summary}\n"

            # 링크
            message += f"   🔗 <a href='{link}'>기사 보기</a>\n\n"

        # 더 많은 뉴스가 있을 경우
        if len(news_list) > max_news:
            remaining = len(news_list) - max_news
            message += f"📚 외 {remaining}개의 뉴스가 더 있습니다.\n"

        return message

    def format_category_message(self, news_list: List[Dict]) -> str:
        """
        카테고리별로 뉴스를 분류하여 메시지를 생성합니다.

        Args:
            news_list: 뉴스 리스트

        Returns:
            카테고리별로 포맷된 메시지
        """
        if not news_list:
            return "📰 오늘 수집된 AI 뉴스가 없습니다."

        # 카테고리별로 분류
        categorized = {}
        for news in news_list:
            category = news.get('category', 'unknown')
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(news)

        # 메시지 헤더
        message = f"🤖 <b>AI 뉴스 브리핑</b>\n"
        message += f"📅 {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}\n"
        message += f"📊 총 {len(news_list)}개의 뉴스\n"
        message += "━━━━━━━━━━━━━━━━━\n\n"

        # 카테고리별로 출력
        category_names = {
            'korean': '🇰🇷 한국 뉴스',
            'english': '🌍 글로벌 뉴스',
            'unknown': '📰 기타 뉴스'
        }

        for category, news_items in categorized.items():
            category_name = category_names.get(category, category)
            message += f"<b>{category_name}</b> ({len(news_items)}개)\n\n"

            for i, news in enumerate(news_items[:3], 1):  # 카테고리당 최대 3개
                title = self._escape_html(news.get('title', '제목 없음'))
                link = news.get('link', '')
                source = self._escape_html(news.get('source', '출처 미상'))

                message += f"{i}. {title}\n"
                message += f"   📌 {source} | <a href='{link}'>링크</a>\n\n"

            if len(news_items) > 3:
                message += f"   ... 외 {len(news_items) - 3}개\n\n"

        return message

    def send_news_notification(self, news_list: List[Dict],
                               format_type: str = 'simple',
                               max_news: int = 5,
                               include_summary: bool = True) -> bool:
        """
        뉴스 알림을 전송합니다.

        Args:
            news_list: 뉴스 리스트
            format_type: 메시지 형식 ('simple' 또는 'category')
            max_news: 최대 뉴스 개수
            include_summary: 요약 포함 여부

        Returns:
            전송 성공 여부
        """
        try:
            if format_type == 'category':
                message = self.format_category_message(news_list)
            else:
                message = self.format_news_message(news_list, max_news, include_summary)

            # 텔레그램 메시지 길이 제한 (4096자) 처리
            if len(message) > 4096:
                # 메시지를 분할하여 전송
                parts = self._split_message(message, 4000)
                for part in parts:
                    if not self.send_message(part):
                        return False
                return True
            else:
                return self.send_message(message)

        except Exception as e:
            print(f"❌ 뉴스 알림 전송 중 오류: {str(e)}")
            return False

    def send_summary_stats(self, news_list: List[Dict]) -> bool:
        """
        수집 통계 요약을 전송합니다.

        Args:
            news_list: 뉴스 리스트

        Returns:
            전송 성공 여부
        """
        if not news_list:
            message = "📊 <b>오늘의 AI 뉴스 통계</b>\n\n"
            message += "수집된 뉴스가 없습니다. 😔"
            return self.send_message(message)

        # 소스별 통계
        source_stats = {}
        for news in news_list:
            source = news.get('source', '알 수 없음')
            source_stats[source] = source_stats.get(source, 0) + 1

        # 카테고리별 통계
        category_stats = {}
        for news in news_list:
            category = news.get('category', 'unknown')
            category_stats[category] = category_stats.get(category, 0) + 1

        # 메시지 생성
        message = f"📊 <b>오늘의 AI 뉴스 통계</b>\n"
        message += f"📅 {datetime.now().strftime('%Y년 %m월 %d일')}\n"
        message += "━━━━━━━━━━━━━━━━━\n\n"

        message += f"📰 <b>총 수집 뉴스:</b> {len(news_list)}개\n\n"

        message += "<b>📌 소스별 통계:</b>\n"
        for source, count in sorted(source_stats.items(), key=lambda x: x[1], reverse=True):
            message += f"  • {self._escape_html(source)}: {count}개\n"

        message += "\n<b>🌍 카테고리별 통계:</b>\n"
        category_names = {
            'korean': '🇰🇷 한국',
            'english': '🌍 글로벌',
            'unknown': '📰 기타'
        }
        for category, count in category_stats.items():
            cat_name = category_names.get(category, category)
            message += f"  • {cat_name}: {count}개\n"

        return self.send_message(message)

    def test_connection(self) -> bool:
        """
        텔레그램 봇 연결을 테스트합니다.

        Returns:
            연결 성공 여부
        """
        try:
            url = f"{self.api_url}/getMe"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            result = response.json()
            if result.get('ok'):
                bot_info = result.get('result', {})
                print(f"✅ 텔레그램 봇 연결 성공!")
                print(f"   봇 이름: {bot_info.get('first_name', 'Unknown')}")
                print(f"   봇 사용자명: @{bot_info.get('username', 'Unknown')}")
                return True
            else:
                print(f"❌ 봇 연결 실패: {result.get('description', 'Unknown error')}")
                return False

        except Exception as e:
            print(f"❌ 봇 연결 테스트 실패: {str(e)}")
            return False

    @staticmethod
    def _escape_html(text: str) -> str:
        """
        HTML 특수 문자를 이스케이프합니다.

        Args:
            text: 원본 텍스트

        Returns:
            이스케이프된 텍스트
        """
        if not text:
            return ""

        replacements = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
        }

        for char, escape in replacements.items():
            text = text.replace(char, escape)

        return text

    @staticmethod
    def _split_message(message: str, max_length: int = 4000) -> List[str]:
        """
        긴 메시지를 여러 부분으로 분할합니다.

        Args:
            message: 원본 메시지
            max_length: 최대 길이

        Returns:
            분할된 메시지 리스트
        """
        if len(message) <= max_length:
            return [message]

        parts = []
        current_part = ""

        for line in message.split('\n'):
            if len(current_part) + len(line) + 1 <= max_length:
                current_part += line + '\n'
            else:
                if current_part:
                    parts.append(current_part)
                current_part = line + '\n'

        if current_part:
            parts.append(current_part)

        return parts


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
        print(f"❌ {config_file} 파일을 찾을 수 없습니다.")
        print(f"💡 config.json.example을 참고하여 config.json을 생성하세요.")
        return None
    except json.JSONDecodeError:
        print(f"❌ {config_file} 파일 형식이 잘못되었습니다.")
        return None


def main():
    """테스트 실행 함수"""
    import os

    # 현재 스크립트의 디렉토리로 이동
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # 설정 로드
    config = load_config()
    if not config:
        return

    telegram_config = config.get('telegram', {})

    if not telegram_config.get('enabled', False):
        print("⚠️  텔레그램 알림이 비활성화되어 있습니다.")
        return

    bot_token = telegram_config.get('bot_token', '')
    chat_id = telegram_config.get('chat_id', '')

    if not bot_token or bot_token == 'YOUR_BOT_TOKEN_HERE':
        print("❌ 텔레그램 봇 토큰이 설정되지 않았습니다.")
        print("💡 config.json 파일에서 bot_token을 설정하세요.")
        return

    if not chat_id or chat_id == 'YOUR_CHAT_ID_HERE':
        print("❌ 텔레그램 채팅 ID가 설정되지 않았습니다.")
        print("💡 config.json 파일에서 chat_id를 설정하세요.")
        return

    # 텔레그램 알림 객체 생성
    notifier = TelegramNotifier(bot_token, chat_id)

    # 연결 테스트
    print("\n🔍 텔레그램 봇 연결 테스트 중...\n")
    if notifier.test_connection():
        # 테스트 메시지 전송
        test_news = [
            {
                'source': 'TechCrunch',
                'title': 'AI 기술의 최신 동향',
                'link': 'https://techcrunch.com/ai',
                'summary': '인공지능 기술이 빠르게 발전하고 있습니다.',
                'published': datetime.now().isoformat(),
                'category': 'english'
            }
        ]

        print("\n📤 테스트 메시지 전송 중...\n")
        if notifier.send_news_notification(test_news):
            print("✅ 텔레그램 알림 설정이 완료되었습니다!")
        else:
            print("❌ 테스트 메시지 전송에 실패했습니다.")
    else:
        print("\n❌ 텔레그램 봇 설정을 확인하세요.")


if __name__ == '__main__':
    main()
