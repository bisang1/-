#!/usr/bin/env python3
"""
AI 뉴스 수집기 - 텔레그램 봇 서버
휴대폰에서 명령어로 뉴스를 수집하고 확인할 수 있습니다.
"""

import json
import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from scraper import NewsCollector, load_config


# 로깅 설정
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class NewsBotServer:
    """텔레그램 봇 서버"""

    def __init__(self, bot_token: str):
        """
        Args:
            bot_token: 텔레그램 봇 토큰
        """
        self.bot_token = bot_token
        self.application = None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /start 명령어 핸들러
        """
        welcome_message = """
🤖 **AI 뉴스 수집기 봇**에 오신 것을 환영합니다!

📱 **사용 가능한 명령어:**

/collect - 최신 AI 뉴스 수집 시작
/latest - 최신 뉴스 5개 보기
/today - 오늘 수집된 모든 뉴스
/stats - 수집 통계 확인
/help - 도움말 보기

💡 휴대폰 어디서든 명령어를 입력하여 뉴스를 확인하세요!
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /help 명령어 핸들러
        """
        help_message = """
📖 **AI 뉴스 수집기 사용 가이드**

**명령어 설명:**

📡 `/collect`
→ AI 뉴스를 수집합니다
→ 4개 소스에서 최근 24시간 뉴스를 가져옵니다
→ 수집 완료 후 자동으로 브리핑을 전송합니다

📰 `/latest`
→ 최신 뉴스 5개를 보여줍니다
→ 빠르게 최신 소식을 확인할 때 사용하세요

📊 `/today`
→ 오늘 수집된 모든 뉴스를 보여줍니다
→ 카테고리별로 정리되어 표시됩니다

📈 `/stats`
→ 수집 통계를 보여줍니다
→ 소스별, 카테고리별 뉴스 개수를 확인할 수 있습니다

**뉴스 소스:**
• AI타임스 (한국)
• 전자신문 AI섹션 (한국)
• TechCrunch AI (글로벌)
• OpenAI Blog (글로벌)

💡 **팁:** 매일 아침 `/collect` 명령어를 입력하여 최신 AI 뉴스를 받아보세요!
        """
        await update.message.reply_text(help_message, parse_mode='Markdown')

    async def collect_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /collect 명령어 핸들러 - 뉴스 수집
        """
        await update.message.reply_text("🚀 뉴스 수집을 시작합니다...\n잠시만 기다려주세요!")

        try:
            # 뉴스 수집기 초기화
            collector = NewsCollector()

            # 뉴스 수집
            collector.collect_all()

            # JSON 저장
            collector.save_to_json()

            total = len(collector.collected_news)

            if total == 0:
                await update.message.reply_text(
                    "😔 수집된 뉴스가 없습니다.\n나중에 다시 시도해주세요."
                )
                return

            # 성공 메시지
            await update.message.reply_text(
                f"✅ **{total}개의 뉴스를 수집했습니다!**\n\n"
                f"📱 뉴스 브리핑을 전송합니다...",
                parse_mode='Markdown'
            )

            # 뉴스 브리핑 전송
            await self.send_news_briefing(update, collector.collected_news)

        except Exception as e:
            logger.error(f"뉴스 수집 중 오류: {e}")
            await update.message.reply_text(
                f"❌ 뉴스 수집 중 오류가 발생했습니다:\n{str(e)}"
            )

    async def latest_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /latest 명령어 핸들러 - 최신 뉴스 5개
        """
        try:
            news_data = self.load_collected_news()

            if not news_data or news_data['total_count'] == 0:
                await update.message.reply_text(
                    "📭 수집된 뉴스가 없습니다.\n"
                    "/collect 명령어로 뉴스를 수집해주세요!"
                )
                return

            news_list = news_data['news'][:5]
            message = self.format_news_list(news_list, "📰 최신 뉴스 5개")

            await update.message.reply_text(message, parse_mode='HTML', disable_web_page_preview=True)

        except Exception as e:
            logger.error(f"최신 뉴스 조회 중 오류: {e}")
            await update.message.reply_text(f"❌ 오류가 발생했습니다: {str(e)}")

    async def today_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /today 명령어 핸들러 - 오늘 수집된 모든 뉴스
        """
        try:
            news_data = self.load_collected_news()

            if not news_data or news_data['total_count'] == 0:
                await update.message.reply_text(
                    "📭 수집된 뉴스가 없습니다.\n"
                    "/collect 명령어로 뉴스를 수집해주세요!"
                )
                return

            # 카테고리별로 분류
            await self.send_news_briefing(update, news_data['news'])

        except Exception as e:
            logger.error(f"오늘 뉴스 조회 중 오류: {e}")
            await update.message.reply_text(f"❌ 오류가 발생했습니다: {str(e)}")

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /stats 명령어 핸들러 - 수집 통계
        """
        try:
            news_data = self.load_collected_news()

            if not news_data or news_data['total_count'] == 0:
                await update.message.reply_text(
                    "📭 수집된 뉴스가 없습니다.\n"
                    "/collect 명령어로 뉴스를 수집해주세요!"
                )
                return

            news_list = news_data['news']

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
            collected_at = news_data.get('collected_at', '')
            if collected_at:
                collected_time = datetime.fromisoformat(collected_at).strftime('%Y년 %m월 %d일 %H:%M')
            else:
                collected_time = '알 수 없음'

            message = f"📊 <b>AI 뉴스 수집 통계</b>\n"
            message += f"📅 수집 시간: {collected_time}\n"
            message += "━━━━━━━━━━━━━━━━━\n\n"

            message += f"📰 <b>총 수집 뉴스:</b> {news_data['total_count']}개\n\n"

            message += "<b>📌 소스별 통계:</b>\n"
            for source, count in sorted(source_stats.items(), key=lambda x: x[1], reverse=True):
                message += f"  • {source}: {count}개\n"

            message += "\n<b>🌍 카테고리별 통계:</b>\n"
            category_names = {
                'korean': '🇰🇷 한국',
                'english': '🌍 글로벌',
                'unknown': '📰 기타'
            }
            for category, count in category_stats.items():
                cat_name = category_names.get(category, category)
                message += f"  • {cat_name}: {count}개\n"

            await update.message.reply_text(message, parse_mode='HTML')

        except Exception as e:
            logger.error(f"통계 조회 중 오류: {e}")
            await update.message.reply_text(f"❌ 오류가 발생했습니다: {str(e)}")

    async def send_news_briefing(self, update: Update, news_list: list):
        """
        뉴스 브리핑을 카테고리별로 전송
        """
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

        for category in ['korean', 'english', 'unknown']:
            if category not in categorized:
                continue

            news_items = categorized[category]
            category_name = category_names.get(category, category)
            message += f"<b>{category_name}</b> ({len(news_items)}개)\n\n"

            for i, news in enumerate(news_items[:3], 1):  # 카테고리당 최대 3개
                title = news.get('title', '제목 없음')
                link = news.get('link', '')
                source = news.get('source', '출처 미상')

                message += f"{i}. {title}\n"
                message += f"   📌 {source} | <a href='{link}'>링크</a>\n\n"

            if len(news_items) > 3:
                message += f"   ... 외 {len(news_items) - 3}개\n\n"

        # 메시지 길이 제한 처리 (4096자)
        if len(message) > 4000:
            # 메시지를 분할하여 전송
            parts = self.split_message(message)
            for part in parts:
                await update.message.reply_text(part, parse_mode='HTML', disable_web_page_preview=True)
        else:
            await update.message.reply_text(message, parse_mode='HTML', disable_web_page_preview=True)

    def format_news_list(self, news_list: list, title: str) -> str:
        """
        뉴스 목록을 HTML 형식으로 포맷팅
        """
        message = f"<b>{title}</b>\n━━━━━━━━━━━━━━━━━\n\n"

        for i, news in enumerate(news_list, 1):
            title = news.get('title', '제목 없음')
            link = news.get('link', '')
            source = news.get('source', '출처 미상')
            summary = news.get('summary', '')

            message += f"{i}. <b>{title}</b>\n"
            message += f"   📌 {source}\n"
            if summary:
                message += f"   💬 {summary[:100]}...\n"
            message += f"   🔗 <a href='{link}'>기사 보기</a>\n\n"

        return message

    def split_message(self, message: str, max_length: int = 4000) -> list:
        """
        긴 메시지를 여러 부분으로 분할
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

    def load_collected_news(self) -> dict:
        """
        수집된 뉴스 JSON 파일 로드
        """
        try:
            with open('collected_news.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'total_count': 0, 'news': []}
        except json.JSONDecodeError:
            return {'total_count': 0, 'news': []}

    def run(self):
        """
        봇 서버 실행
        """
        # 현재 디렉토리를 스크립트 위치로 변경
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

        # Application 생성
        self.application = Application.builder().token(self.bot_token).build()

        # 명령어 핸들러 등록
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("collect", self.collect_command))
        self.application.add_handler(CommandHandler("latest", self.latest_command))
        self.application.add_handler(CommandHandler("today", self.today_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))

        # 봇 실행
        logger.info("🤖 텔레그램 봇 서버를 시작합니다...")
        logger.info("📱 휴대폰에서 봇과 대화를 시작하세요!")
        logger.info("⏹️  종료하려면 Ctrl+C를 누르세요")

        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """메인 실행 함수"""
    # 설정 로드
    config = load_config()

    if not config:
        print("❌ config.json 파일을 찾을 수 없습니다.")
        print("💡 config.json.example을 참고하여 config.json을 생성하세요.")
        return

    telegram_config = config.get('telegram', {})
    bot_token = telegram_config.get('bot_token', '')

    if not bot_token or bot_token == 'YOUR_BOT_TOKEN_HERE':
        print("❌ 텔레그램 봇 토큰이 설정되지 않았습니다.")
        print("💡 config.json 파일에서 bot_token을 설정하세요.")
        return

    # 봇 서버 시작
    bot = NewsBotServer(bot_token)
    bot.run()


if __name__ == '__main__':
    main()
