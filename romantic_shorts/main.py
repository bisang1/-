# -*- coding: utf-8 -*-
"""
낭만처방 쇼츠 생성기 - 메인 GUI 애플리케이션
YouTube Shorts 제작을 위한 제목, 대본, 미드저니 프롬프트 생성 도구
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from datetime import datetime

from generators import generate_titles, generate_script, generate_midjourney_prompts
from config import OPENAI_API_KEY


class RomanticShortsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 낭만처방 쇼츠 생성기")
        self.root.geometry("900x700")
        self.root.configure(bg="#FFF8F0")

        # 상태 변수
        self.current_step = 1
        self.generated_titles = ""
        self.selected_title = ""
        self.generated_script = ""
        self.generated_prompts = ""

        self.setup_ui()
        self.check_api_key()

    def check_api_key(self):
        """API 키 확인"""
        if not OPENAI_API_KEY:
            messagebox.showwarning(
                "API 키 필요",
                "config.py 파일에 OPENAI_API_KEY를 설정해주세요."
            )

    def setup_ui(self):
        """UI 구성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 스타일 설정
        style = ttk.Style()
        style.configure("Title.TLabel", font=("맑은 고딕", 18, "bold"))
        style.configure("Step.TLabel", font=("맑은 고딕", 12, "bold"))
        style.configure("Action.TButton", font=("맑은 고딕", 11))

        # 제목
        title_label = ttk.Label(
            main_frame,
            text="🌸 낭만처방 쇼츠 생성기",
            style="Title.TLabel"
        )
        title_label.pack(pady=(0, 20))

        # 진행 상황 표시
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=(0, 20))

        self.step_labels = []
        steps = ["1. 제목 생성", "2. 대본 생성", "3. 프롬프트 생성"]
        for i, step in enumerate(steps):
            label = ttk.Label(self.progress_frame, text=step, font=("맑은 고딕", 10))
            label.pack(side=tk.LEFT, padx=20)
            self.step_labels.append(label)

        self.update_step_display()

        # 노트북 (탭)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Step 1: 제목 생성
        self.step1_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.step1_frame, text="1단계: 제목 생성")
        self.setup_step1()

        # Step 2: 대본 생성
        self.step2_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.step2_frame, text="2단계: 대본 생성")
        self.setup_step2()

        # Step 3: 프롬프트 생성
        self.step3_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.step3_frame, text="3단계: 프롬프트 생성")
        self.setup_step3()

        # 저장 버튼
        save_frame = ttk.Frame(main_frame)
        save_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            save_frame,
            text="📁 전체 결과 저장",
            command=self.save_all_results,
            style="Action.TButton"
        ).pack(side=tk.RIGHT)

    def update_step_display(self):
        """단계 표시 업데이트"""
        for i, label in enumerate(self.step_labels):
            if i + 1 < self.current_step:
                label.configure(foreground="green")
            elif i + 1 == self.current_step:
                label.configure(foreground="blue")
            else:
                label.configure(foreground="gray")

    def setup_step1(self):
        """Step 1: 제목 생성 UI"""
        # 주제 입력
        input_frame = ttk.Frame(self.step1_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_frame, text="쇼츠 주제:", font=("맑은 고딕", 11)).pack(side=tk.LEFT)
        self.topic_entry = ttk.Entry(input_frame, width=50, font=("맑은 고딕", 11))
        self.topic_entry.pack(side=tk.LEFT, padx=10)
        self.topic_entry.insert(0, "예: 퇴근 후 지친 마음을 달래는 방법")

        ttk.Button(
            input_frame,
            text="🎯 제목 생성",
            command=self.on_generate_titles,
            style="Action.TButton"
        ).pack(side=tk.LEFT)

        # 결과 표시
        ttk.Label(
            self.step1_frame,
            text="생성된 제목 (하나를 선택하세요):",
            font=("맑은 고딕", 10, "bold")
        ).pack(anchor=tk.W, pady=(10, 5))

        self.titles_text = scrolledtext.ScrolledText(
            self.step1_frame,
            height=10,
            font=("맑은 고딕", 11),
            wrap=tk.WORD
        )
        self.titles_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 제목 선택 및 승인
        select_frame = ttk.Frame(self.step1_frame)
        select_frame.pack(fill=tk.X)

        ttk.Label(select_frame, text="선택한 제목:", font=("맑은 고딕", 11)).pack(side=tk.LEFT)
        self.selected_title_entry = ttk.Entry(select_frame, width=50, font=("맑은 고딕", 11))
        self.selected_title_entry.pack(side=tk.LEFT, padx=10)

        self.approve_btn1 = ttk.Button(
            select_frame,
            text="✅ 승인 → 다음 단계",
            command=self.approve_step1,
            style="Action.TButton"
        )
        self.approve_btn1.pack(side=tk.LEFT)

    def setup_step2(self):
        """Step 2: 대본 생성 UI"""
        # 선택된 제목 표시
        title_frame = ttk.Frame(self.step2_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(title_frame, text="선택된 제목:", font=("맑은 고딕", 11)).pack(side=tk.LEFT)
        self.step2_title_label = ttk.Label(
            title_frame,
            text="(1단계에서 제목을 선택하세요)",
            font=("맑은 고딕", 11, "italic")
        )
        self.step2_title_label.pack(side=tk.LEFT, padx=10)

        ttk.Button(
            title_frame,
            text="📝 대본 생성",
            command=self.on_generate_script,
            style="Action.TButton"
        ).pack(side=tk.RIGHT)

        # 대본 결과
        ttk.Label(
            self.step2_frame,
            text="생성된 대본 (40초 분량):",
            font=("맑은 고딕", 10, "bold")
        ).pack(anchor=tk.W, pady=(10, 5))

        self.script_text = scrolledtext.ScrolledText(
            self.step2_frame,
            height=15,
            font=("맑은 고딕", 11),
            wrap=tk.WORD
        )
        self.script_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 승인 버튼
        self.approve_btn2 = ttk.Button(
            self.step2_frame,
            text="✅ 승인 → 다음 단계",
            command=self.approve_step2,
            style="Action.TButton"
        )
        self.approve_btn2.pack(anchor=tk.E)

    def setup_step3(self):
        """Step 3: 미드저니 프롬프트 생성 UI"""
        # 생성 버튼
        btn_frame = ttk.Frame(self.step3_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            btn_frame,
            text="🎨 미드저니 프롬프트 생성",
            command=self.on_generate_prompts,
            style="Action.TButton"
        ).pack(side=tk.LEFT)

        ttk.Button(
            btn_frame,
            text="📋 클립보드에 복사",
            command=self.copy_prompts,
            style="Action.TButton"
        ).pack(side=tk.RIGHT)

        # 프롬프트 결과
        ttk.Label(
            self.step3_frame,
            text="미드저니 프롬프트 (캐릭터 5개 + 배경 5개):",
            font=("맑은 고딕", 10, "bold")
        ).pack(anchor=tk.W, pady=(10, 5))

        self.prompts_text = scrolledtext.ScrolledText(
            self.step3_frame,
            height=18,
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        self.prompts_text.pack(fill=tk.BOTH, expand=True)

    def on_generate_titles(self):
        """제목 생성 버튼 클릭"""
        topic = self.topic_entry.get().strip()
        if not topic or topic.startswith("예:"):
            messagebox.showwarning("입력 필요", "쇼츠 주제를 입력해주세요.")
            return

        self.titles_text.delete(1.0, tk.END)
        self.titles_text.insert(tk.END, "⏳ 제목 생성 중...")

        def generate():
            result = generate_titles(topic)
            self.root.after(0, lambda: self.display_titles(result))

        threading.Thread(target=generate, daemon=True).start()

    def display_titles(self, result):
        """생성된 제목 표시"""
        self.titles_text.delete(1.0, tk.END)
        self.titles_text.insert(tk.END, result)
        self.generated_titles = result

    def approve_step1(self):
        """1단계 승인"""
        title = self.selected_title_entry.get().strip()
        if not title:
            messagebox.showwarning("선택 필요", "사용할 제목을 입력해주세요.")
            return

        self.selected_title = title
        self.current_step = 2
        self.update_step_display()
        self.step2_title_label.configure(text=title)
        self.notebook.select(1)  # 2단계 탭으로 이동
        messagebox.showinfo("승인 완료", f"제목이 선택되었습니다:\n\n{title}")

    def on_generate_script(self):
        """대본 생성 버튼 클릭"""
        if not self.selected_title:
            messagebox.showwarning("순서 오류", "먼저 1단계에서 제목을 선택해주세요.")
            self.notebook.select(0)
            return

        self.script_text.delete(1.0, tk.END)
        self.script_text.insert(tk.END, "⏳ 대본 생성 중... (약 10-15초 소요)")

        def generate():
            result = generate_script(self.selected_title)
            self.root.after(0, lambda: self.display_script(result))

        threading.Thread(target=generate, daemon=True).start()

    def display_script(self, result):
        """생성된 대본 표시"""
        self.script_text.delete(1.0, tk.END)
        self.script_text.insert(tk.END, result)
        self.generated_script = result

    def approve_step2(self):
        """2단계 승인"""
        if not self.generated_script or "오류" in self.generated_script:
            messagebox.showwarning("생성 필요", "먼저 대본을 생성해주세요.")
            return

        self.current_step = 3
        self.update_step_display()
        self.notebook.select(2)  # 3단계 탭으로 이동
        messagebox.showinfo("승인 완료", "대본이 승인되었습니다. 이제 미드저니 프롬프트를 생성하세요.")

    def on_generate_prompts(self):
        """미드저니 프롬프트 생성 버튼 클릭"""
        if not self.generated_script:
            messagebox.showwarning("순서 오류", "먼저 2단계에서 대본을 생성하고 승인해주세요.")
            return

        self.prompts_text.delete(1.0, tk.END)
        self.prompts_text.insert(tk.END, "⏳ 미드저니 프롬프트 생성 중... (약 15-20초 소요)")

        def generate():
            result = generate_midjourney_prompts(self.generated_script, self.selected_title)
            self.root.after(0, lambda: self.display_prompts(result))

        threading.Thread(target=generate, daemon=True).start()

    def display_prompts(self, result):
        """생성된 프롬프트 표시"""
        self.prompts_text.delete(1.0, tk.END)
        self.prompts_text.insert(tk.END, result)
        self.generated_prompts = result

    def copy_prompts(self):
        """프롬프트 클립보드 복사"""
        content = self.prompts_text.get(1.0, tk.END)
        if content.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("복사 완료", "프롬프트가 클립보드에 복사되었습니다.")

    def save_all_results(self):
        """전체 결과 저장"""
        if not self.selected_title:
            messagebox.showwarning("저장 불가", "생성된 콘텐츠가 없습니다.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")],
            initialfilename=f"낭만처방_쇼츠_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("🌸 낭만처방 쇼츠 생성 결과\n")
                f.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")

                f.write("📌 선택된 제목\n")
                f.write("-" * 40 + "\n")
                f.write(f"{self.selected_title}\n\n")

                if self.generated_titles:
                    f.write("📋 생성된 제목 후보들\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"{self.generated_titles}\n\n")

                if self.generated_script:
                    f.write("📝 대본 (40초 분량)\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"{self.generated_script}\n\n")

                if self.generated_prompts:
                    f.write("🎨 미드저니 프롬프트\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"{self.generated_prompts}\n")

            messagebox.showinfo("저장 완료", f"결과가 저장되었습니다:\n{filename}")


def main():
    root = tk.Tk()
    app = RomanticShortsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
