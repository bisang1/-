#!/usr/bin/env python3
"""
바탕화면에 바로가기를 자동으로 생성하는 스크립트
"""

import os
import sys
import platform
from pathlib import Path


def get_desktop_path():
    """사용자 바탕화면 경로 반환"""
    system = platform.system()

    if system == "Windows":
        return Path.home() / "Desktop"
    elif system == "Darwin":  # macOS
        return Path.home() / "Desktop"
    else:  # Linux
        # XDG 표준 경로 시도
        desktop = Path.home() / "Desktop"
        if not desktop.exists():
            desktop = Path.home() / "바탕화면"
        return desktop


def create_windows_shortcut():
    """Windows용 바로가기 생성"""
    try:
        import win32com.client

        desktop = get_desktop_path()
        script_dir = Path(__file__).parent.absolute()

        # 바로가기 경로
        shortcut_path = desktop / "AI 뉴스 수집기.lnk"

        # WScript.Shell 객체 생성
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path))

        # 바로가기 설정
        shortcut.TargetPath = str(script_dir / "run_gui.bat")
        shortcut.WorkingDirectory = str(script_dir)
        shortcut.Description = "AI 뉴스 자동 수집기"
        shortcut.IconLocation = sys.executable  # Python 아이콘 사용

        # 저장
        shortcut.save()

        print(f"✅ 바로가기 생성 완료!")
        print(f"   위치: {shortcut_path}")
        return True

    except ImportError:
        print("⚠️  pywin32 모듈이 필요합니다.")
        print("   설치: pip install pywin32")
        print("")
        print("대신 run_gui.bat 파일을 바탕화면에 복사하세요:")
        print(f"   복사할 파일: {Path(__file__).parent / 'run_gui.bat'}")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False


def create_mac_shortcut():
    """macOS용 Automator 앱 또는 별칭 생성"""
    desktop = get_desktop_path()
    script_dir = Path(__file__).parent.absolute()
    run_script = script_dir / "run_gui.sh"

    # 실행 권한 부여
    os.chmod(run_script, 0o755)

    # 별칭 생성 (AppleScript 사용)
    try:
        import subprocess

        applescript = f'''
        tell application "Finder"
            make new alias file at desktop to POSIX file "{run_script}" with properties {{name:"AI 뉴스 수집기"}}
        end tell
        '''

        subprocess.run(['osascript', '-e', applescript], check=True)
        print(f"✅ 바탕화면에 별칭 생성 완료!")
        print(f"   위치: {desktop / 'AI 뉴스 수집기'}")
        return True

    except Exception as e:
        print(f"⚠️  자동 생성 실패: {e}")
        print(f"\n수동으로 바로가기를 만드세요:")
        print(f"1. {run_script} 파일을 바탕화면으로 드래그")
        print(f"2. Option 키를 누른 상태로 드래그하여 별칭 생성")
        return False


def create_linux_shortcut():
    """Linux용 .desktop 파일 생성"""
    desktop = get_desktop_path()
    script_dir = Path(__file__).parent.absolute()
    run_script = script_dir / "run_gui.sh"

    # 실행 권한 부여
    os.chmod(run_script, 0o755)

    # .desktop 파일 생성
    desktop_file = desktop / "ai-news-scraper.desktop"

    content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=AI 뉴스 수집기
Comment=AI 뉴스 자동 수집 및 텔레그램 알림
Exec={run_script}
Icon=applications-internet
Terminal=false
Categories=Network;News;
"""

    try:
        with open(desktop_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # 실행 권한 부여
        os.chmod(desktop_file, 0o755)

        print(f"✅ 바탕화면 바로가기 생성 완료!")
        print(f"   위치: {desktop_file}")
        print(f"\n※ 바로가기가 보이지 않으면:")
        print(f"   마우스 오른쪽 버튼 → '실행 허용' 선택")
        return True

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🤖 AI 뉴스 수집기 - 바탕화면 바로가기 생성")
    print("=" * 60)
    print()

    system = platform.system()
    print(f"운영체제: {system}")
    print(f"바탕화면 경로: {get_desktop_path()}")
    print()

    if system == "Windows":
        success = create_windows_shortcut()
    elif system == "Darwin":
        success = create_mac_shortcut()
    else:  # Linux
        success = create_linux_shortcut()

    print()
    if success:
        print("🎉 완료! 바탕화면에서 'AI 뉴스 수집기'를 실행하세요.")
    else:
        print("⚠️  바로가기 생성에 실패했습니다.")
        print("   run_gui.bat (Windows) 또는 run_gui.sh (Mac/Linux)를")
        print("   직접 더블클릭하여 실행하세요.")

    print()
    input("계속하려면 Enter를 누르세요...")


if __name__ == '__main__':
    main()
