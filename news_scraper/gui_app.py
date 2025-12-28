#!/usr/bin/env python3
"""
AI 뉴스 수집기 - GUI 버전
바탕화면에서 쉽게 실행할 수 있는 그래픽 인터페이스
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import json
import os
from datetime import datetime
from scraper import NewsCollector, load_config
from telegram_notifier import TelegramNotifier


class NewsScraperGUI:
    """뉴스 수집기 GUI 애플리케이션"""

    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI 뉴스 자동 수집기")
        self.root.geometry("900x700")

        # 아이콘 설정 시도 (선택사항)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # 스타일 설정
        self.setup_styles()

        # 메인 프레임
        self.create_widgets()

        # 설정 로드
        self.config = load_config()
        self.update_config_status()

        # 현재 디렉토리를 스크립트 위치로 변경
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

    def setup_styles(self):
        """스타일 설정"""
        style = ttk.Style()
        style.theme_use('clam')

        # 버튼 스타일
        style.configure('Start.TButton',
                       font=('Arial', 12, 'bold'),
                       foreground='white',
                       background='#4CAF50')

        style.configure('Config.TButton',
                       font=('Arial', 10),
                       foreground='white',
                       background='#2196F3')

    def create_widgets(self):
        """GUI 위젯 생성"""

        # 헤더
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🤖 AI 뉴스 자동 수집기",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)

        # 상태 표시 프레임
        status_frame = tk.Frame(self.root, bg="#ecf0f1")
        status_frame.pack(fill=tk.X, padx=10, pady=10)

        # 텔레그램 설정 상태
        tk.Label(
            status_frame,
            text="📱 텔레그램:",
            font=("Arial", 10, "bold"),
            bg="#ecf0f1"
        ).pack(side=tk.LEFT, padx=5)

        self.telegram_status_label = tk.Label(
            status_frame,
            text="❌ 미설정",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="red"
        )
        self.telegram_status_label.pack(side=tk.LEFT, padx=5)

        # 설정 버튼
        config_btn = ttk.Button(
            status_frame,
            text="⚙️ 설정",
            style='Config.TButton',
            command=self.open_config
        )
        config_btn.pack(side=tk.RIGHT, padx=5)

        # 컨트롤 프레임
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        # 실행 버튼
        self.start_button = ttk.Button(
            control_frame,
            text="▶️  뉴스 수집 시작",
            style='Start.TButton',
            command=self.start_scraping
        )
        self.start_button.pack(side=tk.LEFT, padx=5, ipadx=20, ipady=10)

        # 텔레그램 테스트 버튼
        self.test_telegram_btn = ttk.Button(
            control_frame,
            text="📤 텔레그램 테스트",
            command=self.test_telegram
        )
        self.test_telegram_btn.pack(side=tk.LEFT, padx=5, ipady=10)

        # 수집된 뉴스 보기 버튼
        view_btn = ttk.Button(
            control_frame,
            text="📄 수집 결과 보기",
            command=self.view_collected_news
        )
        view_btn.pack(side=tk.LEFT, padx=5, ipady=10)

        # 진행 상태 표시
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)

        self.progress_label = tk.Label(
            progress_frame,
            text="대기 중...",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        self.progress_label.pack(side=tk.LEFT)

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=200
        )
        self.progress_bar.pack(side=tk.RIGHT, padx=5)

        # 로그 출력 영역
        log_frame = tk.LabelFrame(
            self.root,
            text="📋 실행 로그",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#f8f9fa",
            fg="#2c3e50",
            height=20
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # 하단 정보
        footer_frame = tk.Frame(self.root, bg="#ecf0f1")
        footer_frame.pack(fill=tk.X, pady=5)

        footer_label = tk.Label(
            footer_frame,
            text="AI News Scraper v2.0 | 개발: Claude & User",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        footer_label.pack()

    def update_config_status(self):
        """설정 상태 업데이트"""
        if self.config and self.config.get('telegram', {}).get('enabled', False):
            bot_token = self.config['telegram'].get('bot_token', '')
            if bot_token and bot_token != 'YOUR_BOT_TOKEN_HERE':
                self.telegram_status_label.config(text="✅ 연결됨", fg="green")
            else:
                self.telegram_status_label.config(text="⚠️ 토큰 필요", fg="orange")
        else:
            self.telegram_status_label.config(text="❌ 미설정", fg="red")

    def log(self, message, level="INFO"):
        """로그 메시지 출력"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        # 레벨별 아이콘
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "WARNING": "⚠️"
        }
        icon = icons.get(level, "📝")

        log_message = f"[{timestamp}] {icon} {message}\n"

        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update()

    def start_scraping(self):
        """뉴스 수집 시작"""
        self.start_button.config(state=tk.DISABLED)
        self.progress_label.config(text="수집 중...", fg="#3498db")
        self.progress_bar.start(10)

        self.log_text.delete(1.0, tk.END)
        self.log("🚀 뉴스 수집을 시작합니다...", "INFO")

        # 별도 스레드에서 실행
        thread = threading.Thread(target=self.run_scraping, daemon=True)
        thread.start()

    def run_scraping(self):
        """뉴스 수집 실행 (백그라운드)"""
        try:
            # 뉴스 수집기 초기화
            collector = NewsCollector()

            # 각 소스에서 수집
            for source in collector.sources:
                self.log(f"📡 {source['name']}에서 수집 중...", "INFO")

                if source.get('type') == 'rss':
                    news = collector.collect_from_rss(source)
                elif source.get('type') == 'scraping':
                    news = collector.collect_from_scraping(source)
                else:
                    news = []

                collector.collected_news.extend(news)
                self.log(f"   {len(news)}개의 뉴스 수집 완료", "SUCCESS")

            # 정렬
            collector.collected_news.sort(
                key=lambda x: x.get('published', ''),
                reverse=True
            )

            # JSON 저장
            collector.save_to_json()
            total = len(collector.collected_news)
            self.log(f"💾 총 {total}개의 뉴스를 collected_news.json에 저장했습니다.", "SUCCESS")

            # 텔레그램 알림
            if self.config and self.config.get('telegram', {}).get('enabled', False):
                self.send_telegram_notification(collector.collected_news)

            self.log("✨ 모든 작업이 완료되었습니다!", "SUCCESS")
            messagebox.showinfo("완료", f"총 {total}개의 뉴스를 수집했습니다!")

        except Exception as e:
            self.log(f"오류 발생: {str(e)}", "ERROR")
            messagebox.showerror("오류", f"뉴스 수집 중 오류가 발생했습니다:\n{str(e)}")

        finally:
            self.progress_bar.stop()
            self.progress_label.config(text="완료", fg="#27ae60")
            self.start_button.config(state=tk.NORMAL)

    def send_telegram_notification(self, news_list):
        """텔레그램 알림 전송"""
        try:
            self.log("📱 텔레그램 알림 전송 중...", "INFO")

            telegram_config = self.config['telegram']
            bot_token = telegram_config.get('bot_token', '')
            chat_id = telegram_config.get('chat_id', '')

            if bot_token and chat_id and bot_token != 'YOUR_BOT_TOKEN_HERE':
                notifier = TelegramNotifier(bot_token, chat_id)

                notification_config = self.config.get('notification', {})
                max_news = notification_config.get('max_news_per_message', 5)
                include_summary = notification_config.get('include_summary', True)

                if notifier.send_news_notification(
                    news_list,
                    format_type='category',
                    max_news=max_news,
                    include_summary=include_summary
                ):
                    self.log("✅ 텔레그램 알림 전송 완료!", "SUCCESS")
                else:
                    self.log("텔레그램 알림 전송 실패", "WARNING")
            else:
                self.log("텔레그램 설정이 올바르지 않습니다.", "WARNING")

        except Exception as e:
            self.log(f"텔레그램 알림 오류: {str(e)}", "ERROR")

    def test_telegram(self):
        """텔레그램 연결 테스트"""
        if not self.config or not self.config.get('telegram', {}).get('enabled', False):
            messagebox.showwarning("설정 필요", "텔레그램 설정이 필요합니다.\n설정 버튼을 클릭하여 config.json을 생성하세요.")
            return

        self.log("🔍 텔레그램 봇 연결 테스트 중...", "INFO")

        try:
            telegram_config = self.config['telegram']
            bot_token = telegram_config.get('bot_token', '')
            chat_id = telegram_config.get('chat_id', '')

            if not bot_token or bot_token == 'YOUR_BOT_TOKEN_HERE':
                messagebox.showerror("오류", "봇 토큰이 설정되지 않았습니다.")
                return

            notifier = TelegramNotifier(bot_token, chat_id)

            if notifier.test_connection():
                test_news = [{
                    'source': 'GUI 테스트',
                    'title': '텔레그램 봇 연결 테스트',
                    'link': 'https://github.com',
                    'summary': 'AI 뉴스 수집기 GUI에서 전송한 테스트 메시지입니다.',
                    'published': datetime.now().isoformat(),
                    'category': 'test'
                }]

                notifier.send_news_notification(test_news)
                self.log("✅ 텔레그램 봇 연결 성공!", "SUCCESS")
                messagebox.showinfo("성공", "텔레그램 봇 연결에 성공했습니다!\n메시지를 확인해보세요.")
            else:
                self.log("❌ 텔레그램 봇 연결 실패", "ERROR")
                messagebox.showerror("실패", "텔레그램 봇 연결에 실패했습니다.\n설정을 확인해주세요.")

        except Exception as e:
            self.log(f"오류: {str(e)}", "ERROR")
            messagebox.showerror("오류", f"텔레그램 테스트 중 오류 발생:\n{str(e)}")

    def open_config(self):
        """설정 파일 열기"""
        config_file = "config.json"
        example_file = "config.json.example"

        # config.json이 없으면 example에서 복사
        if not os.path.exists(config_file) and os.path.exists(example_file):
            import shutil
            shutil.copy(example_file, config_file)
            messagebox.showinfo(
                "설정 파일 생성",
                f"{config_file} 파일이 생성되었습니다.\n\n"
                "텍스트 에디터로 열어서 다음 정보를 입력하세요:\n"
                "1. bot_token: 텔레그램 봇 토큰\n"
                "2. chat_id: 텔레그램 채팅 ID\n\n"
                "저장 후 '설정' 버튼을 다시 클릭하세요."
            )

        # OS에 맞는 에디터로 열기
        try:
            if os.name == 'nt':  # Windows
                os.startfile(config_file)
            elif os.name == 'posix':  # Mac/Linux
                import subprocess
                subprocess.call(['open' if os.uname().sysname == 'Darwin' else 'xdg-open', config_file])
        except Exception as e:
            messagebox.showerror("오류", f"파일을 열 수 없습니다:\n{str(e)}\n\n수동으로 {config_file}을 편집하세요.")

        # 설정 다시 로드
        self.config = load_config()
        self.update_config_status()

    def view_collected_news(self):
        """수집된 뉴스 보기"""
        news_file = "collected_news.json"

        if not os.path.exists(news_file):
            messagebox.showwarning("파일 없음", "아직 수집된 뉴스가 없습니다.\n'뉴스 수집 시작' 버튼을 클릭하세요.")
            return

        try:
            with open(news_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 새 창 생성
            view_window = tk.Toplevel(self.root)
            view_window.title("📰 수집된 뉴스")
            view_window.geometry("800x600")

            # 헤더
            header = tk.Label(
                view_window,
                text=f"📊 총 {data.get('total_count', 0)}개의 뉴스 | 수집 시간: {data.get('collected_at', '')}",
                font=("Arial", 12, "bold"),
                bg="#3498db",
                fg="white",
                pady=10
            )
            header.pack(fill=tk.X)

            # 뉴스 목록
            news_text = scrolledtext.ScrolledText(
                view_window,
                wrap=tk.WORD,
                font=("Consolas", 10),
                bg="#f8f9fa"
            )
            news_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # 뉴스 표시
            for i, news in enumerate(data.get('news', []), 1):
                news_text.insert(tk.END, f"\n{i}. ", "number")
                news_text.insert(tk.END, f"[{news['source']}] ", "source")
                news_text.insert(tk.END, f"{news['title']}\n", "title")
                news_text.insert(tk.END, f"   🔗 {news['link']}\n", "link")
                if news.get('summary'):
                    news_text.insert(tk.END, f"   📝 {news['summary'][:150]}...\n", "summary")
                news_text.insert(tk.END, f"   📅 {news['published']}\n\n", "date")

            # 텍스트 태그 설정
            news_text.tag_config("number", foreground="#e74c3c", font=("Arial", 10, "bold"))
            news_text.tag_config("source", foreground="#9b59b6", font=("Arial", 10, "bold"))
            news_text.tag_config("title", foreground="#2c3e50", font=("Arial", 11, "bold"))
            news_text.tag_config("link", foreground="#3498db")
            news_text.tag_config("summary", foreground="#7f8c8d")
            news_text.tag_config("date", foreground="#95a5a6", font=("Arial", 9))

            news_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("오류", f"뉴스 파일을 읽는 중 오류 발생:\n{str(e)}")


def main():
    """GUI 애플리케이션 실행"""
    root = tk.Tk()
    app = NewsScraperGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
