# -*- coding: utf-8 -*-
"""
낭만처방 쇼츠 생성기 - Streamlit 웹 앱
모바일 최적화 버전
"""

import streamlit as st
import os
import tempfile
from datetime import datetime

from generators import generate_titles, generate_script, generate_midjourney_prompts
from tts_generator import generate_tts_with_speed, get_available_voices, get_speed_options
from config import OPENAI_API_KEY

# 페이지 설정 (모바일 최적화)
st.set_page_config(
    page_title="낭만처방 쇼츠 생성기",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 모바일 최적화 CSS
st.markdown("""
<style>
    /* 모바일 최적화 */
    .stApp {
        max-width: 100%;
    }

    /* 버튼 크기 증가 (터치 친화적) */
    .stButton > button {
        width: 100%;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        border-radius: 10px;
        margin: 0.25rem 0;
    }

    /* 성공 버튼 (초록색) */
    .success-btn > button {
        background-color: #28a745 !important;
        color: white !important;
    }

    /* 위험 버튼 (빨간색) */
    .danger-btn > button {
        background-color: #dc3545 !important;
        color: white !important;
    }

    /* 텍스트 영역 */
    .stTextArea textarea {
        font-size: 1rem;
        line-height: 1.6;
    }

    /* 제목 스타일 */
    h1 {
        font-size: 1.8rem !important;
        text-align: center;
    }

    /* 단계 표시 */
    .step-indicator {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }

    .step-badge {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
    }

    .step-active {
        background-color: #007bff;
        color: white;
    }

    .step-completed {
        background-color: #28a745;
        color: white;
    }

    .step-pending {
        background-color: #e9ecef;
        color: #6c757d;
    }

    /* 모바일 반응형 */
    @media (max-width: 768px) {
        .stButton > button {
            padding: 1rem;
            font-size: 1.1rem;
        }

        h1 {
            font-size: 1.5rem !important;
        }

        .stTextArea textarea {
            font-size: 0.95rem;
        }
    }

    /* 오디오 플레이어 */
    audio {
        width: 100%;
    }

    /* 카드 스타일 */
    .content-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """세션 상태 초기화"""
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'topic' not in st.session_state:
        st.session_state.topic = ""
    if 'generated_titles' not in st.session_state:
        st.session_state.generated_titles = ""
    if 'selected_title' not in st.session_state:
        st.session_state.selected_title = ""
    if 'generated_script' not in st.session_state:
        st.session_state.generated_script = ""
    if 'generated_prompts' not in st.session_state:
        st.session_state.generated_prompts = ""
    if 'tts_file' not in st.session_state:
        st.session_state.tts_file = None
    if 'step1_approved' not in st.session_state:
        st.session_state.step1_approved = False
    if 'step2_approved' not in st.session_state:
        st.session_state.step2_approved = False
    if 'step3_approved' not in st.session_state:
        st.session_state.step3_approved = False


def reset_all():
    """모든 상태 초기화 (새 주제 시작)"""
    st.session_state.current_step = 1
    st.session_state.topic = ""
    st.session_state.generated_titles = ""
    st.session_state.selected_title = ""
    st.session_state.generated_script = ""
    st.session_state.generated_prompts = ""
    st.session_state.tts_file = None
    st.session_state.step1_approved = False
    st.session_state.step2_approved = False
    st.session_state.step3_approved = False


def display_step_indicator():
    """단계 표시기"""
    steps = [
        ("1. 제목", st.session_state.step1_approved, st.session_state.current_step == 1),
        ("2. 대본", st.session_state.step2_approved, st.session_state.current_step == 2),
        ("3. 프롬프트", st.session_state.step3_approved, st.session_state.current_step == 3),
    ]

    cols = st.columns(3)
    for i, (name, completed, active) in enumerate(steps):
        with cols[i]:
            if completed:
                st.success(f"✅ {name}")
            elif active:
                st.info(f"🔵 {name}")
            else:
                st.write(f"⚪ {name}")


def step1_titles():
    """1단계: 제목 생성"""
    st.header("📌 1단계: 제목 생성")

    if st.session_state.step1_approved:
        st.success(f"✅ 선택된 제목: {st.session_state.selected_title}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ 제목 수정", use_container_width=True):
                st.session_state.step1_approved = False
                st.session_state.step2_approved = False
                st.session_state.step3_approved = False
                st.session_state.current_step = 1
                st.rerun()
        with col2:
            if st.button("➡️ 대본 생성으로", use_container_width=True, type="primary"):
                st.session_state.current_step = 2
                st.rerun()
        return

    # 주제 입력
    topic = st.text_input(
        "쇼츠 주제를 입력하세요:",
        value=st.session_state.topic,
        placeholder="예: 퇴근 후 지친 마음을 달래는 방법"
    )
    st.session_state.topic = topic

    # 제목 생성 버튼
    if st.button("🎯 제목 5개 생성", use_container_width=True, type="primary"):
        if not topic:
            st.error("주제를 입력해주세요!")
            return

        with st.spinner("⏳ AI가 제목을 생성하는 중..."):
            result = generate_titles(topic)
            st.session_state.generated_titles = result

    # 생성된 제목 표시
    if st.session_state.generated_titles:
        st.markdown("### 생성된 제목 후보:")
        st.text_area(
            "제목 목록",
            st.session_state.generated_titles,
            height=200,
            label_visibility="collapsed"
        )

        # 제목 선택
        st.markdown("### 사용할 제목을 입력하세요:")
        selected = st.text_input(
            "선택한 제목",
            value=st.session_state.selected_title,
            placeholder="위에서 마음에 드는 제목을 복사해 붙여넣으세요",
            label_visibility="collapsed"
        )
        st.session_state.selected_title = selected

        # 승인 버튼
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 다시 생성", use_container_width=True):
                st.session_state.generated_titles = ""
                st.rerun()
        with col2:
            if st.button("✅ 제목 승인", use_container_width=True, type="primary"):
                if not selected:
                    st.error("제목을 입력해주세요!")
                else:
                    st.session_state.step1_approved = True
                    st.session_state.current_step = 2
                    st.rerun()


def step2_script():
    """2단계: 대본 생성"""
    st.header("📝 2단계: 대본 생성")

    if not st.session_state.step1_approved:
        st.warning("⚠️ 먼저 1단계에서 제목을 선택해주세요.")
        if st.button("⬅️ 1단계로 돌아가기", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
        return

    st.info(f"🎬 제목: {st.session_state.selected_title}")

    if st.session_state.step2_approved:
        st.success("✅ 대본이 승인되었습니다!")
        st.text_area("승인된 대본", st.session_state.generated_script, height=300)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ 대본 수정", use_container_width=True):
                st.session_state.step2_approved = False
                st.session_state.step3_approved = False
                st.rerun()
        with col2:
            if st.button("➡️ 프롬프트 생성으로", use_container_width=True, type="primary"):
                st.session_state.current_step = 3
                st.rerun()
        return

    # 대본 생성 버튼
    if st.button("📝 40초 대본 생성", use_container_width=True, type="primary"):
        with st.spinner("⏳ AI가 대본을 작성하는 중... (약 10-15초)"):
            result = generate_script(st.session_state.selected_title)
            st.session_state.generated_script = result

    # 생성된 대본 표시
    if st.session_state.generated_script:
        st.markdown("### 생성된 대본 (40초 분량):")

        # 편집 가능한 텍스트 영역
        edited_script = st.text_area(
            "대본 편집",
            st.session_state.generated_script,
            height=350,
            label_visibility="collapsed"
        )
        st.session_state.generated_script = edited_script

        # TTS 미리듣기
        st.markdown("### 🔊 TTS 미리듣기")
        col1, col2 = st.columns(2)
        with col1:
            voice_options = get_available_voices()
            selected_voice = st.selectbox("음성 선택", voice_options)
        with col2:
            speed_options = get_speed_options()
            selected_speed = st.selectbox("배속 선택", list(speed_options.keys()), index=1)

        if st.button("🎧 TTS 생성", use_container_width=True):
            with st.spinner("🔊 음성 생성 중..."):
                try:
                    speed_value = speed_options[selected_speed]
                    output_dir = tempfile.gettempdir()
                    audio_path = generate_tts_with_speed(
                        edited_script,
                        selected_voice,
                        speed_value,
                        output_dir
                    )
                    st.session_state.tts_file = audio_path
                except Exception as e:
                    st.error(f"TTS 생성 오류: {str(e)}")

        # 오디오 재생
        if st.session_state.tts_file and os.path.exists(st.session_state.tts_file):
            st.audio(st.session_state.tts_file, format="audio/mp3")

            # 다운로드 버튼
            with open(st.session_state.tts_file, "rb") as f:
                st.download_button(
                    "📥 음성 파일 다운로드",
                    f.read(),
                    file_name=f"낭만처방_TTS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )

        st.markdown("---")

        # 버튼들
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ 이전 단계", use_container_width=True):
                st.session_state.current_step = 1
                st.rerun()
        with col2:
            if st.button("🔄 다시 생성", use_container_width=True):
                st.session_state.generated_script = ""
                st.session_state.tts_file = None
                st.rerun()
        with col3:
            if st.button("✅ 대본 승인", use_container_width=True, type="primary"):
                st.session_state.step2_approved = True
                st.session_state.current_step = 3
                st.rerun()


def step3_prompts():
    """3단계: 미드저니 프롬프트 생성"""
    st.header("🎨 3단계: 미드저니 프롬프트")

    if not st.session_state.step2_approved:
        st.warning("⚠️ 먼저 2단계에서 대본을 승인해주세요.")
        if st.button("⬅️ 2단계로 돌아가기", use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()
        return

    st.info(f"🎬 제목: {st.session_state.selected_title}")

    if st.session_state.step3_approved:
        st.success("✅ 모든 단계가 완료되었습니다!")
        st.text_area("생성된 프롬프트", st.session_state.generated_prompts, height=400)

        st.markdown("---")
        st.markdown("### 🎉 완료! 다음 작업을 선택하세요:")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 프롬프트 복사용 보기", use_container_width=True):
                st.code(st.session_state.generated_prompts)
        with col2:
            if st.button("🗑️ 전체 삭제 & 새 주제 시작", use_container_width=True, type="primary"):
                reset_all()
                st.rerun()

        # 전체 결과 다운로드
        full_result = f"""
{'='*60}
🌸 낭만처방 쇼츠 생성 결과
생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

📌 선택된 제목
{'-'*40}
{st.session_state.selected_title}

📝 대본 (40초 분량)
{'-'*40}
{st.session_state.generated_script}

🎨 미드저니 프롬프트
{'-'*40}
{st.session_state.generated_prompts}
"""
        st.download_button(
            "📥 전체 결과 다운로드",
            full_result,
            file_name=f"낭만처방_쇼츠_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        return

    # 프롬프트 생성 버튼
    if st.button("🎨 미드저니 프롬프트 10개 생성", use_container_width=True, type="primary"):
        with st.spinner("⏳ AI가 프롬프트를 생성하는 중... (약 15-20초)"):
            result = generate_midjourney_prompts(
                st.session_state.generated_script,
                st.session_state.selected_title
            )
            st.session_state.generated_prompts = result

    # 생성된 프롬프트 표시
    if st.session_state.generated_prompts:
        st.markdown("### 생성된 프롬프트 (캐릭터 5 + 배경 5):")
        st.text_area(
            "프롬프트",
            st.session_state.generated_prompts,
            height=400,
            label_visibility="collapsed"
        )

        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ 이전 단계", use_container_width=True):
                st.session_state.current_step = 2
                st.rerun()
        with col2:
            if st.button("🔄 다시 생성", use_container_width=True):
                st.session_state.generated_prompts = ""
                st.rerun()
        with col3:
            if st.button("✅ 완료", use_container_width=True, type="primary"):
                st.session_state.step3_approved = True
                st.rerun()


def main():
    """메인 앱"""
    init_session_state()

    # 헤더
    st.title("🌸 낭만처방 쇼츠 생성기")

    # API 키 체크
    if not OPENAI_API_KEY:
        st.error("⚠️ config.py에 OPENAI_API_KEY를 설정해주세요.")
        st.stop()

    # 단계 표시기
    display_step_indicator()

    st.markdown("---")

    # 새 주제 시작 버튼 (항상 표시)
    with st.sidebar:
        st.markdown("### ⚙️ 설정")
        if st.button("🗑️ 전체 초기화", use_container_width=True):
            reset_all()
            st.rerun()

        st.markdown("---")
        st.markdown("### 📍 현재 진행 상황")
        st.write(f"**주제:** {st.session_state.topic or '(미입력)'}")
        st.write(f"**제목:** {st.session_state.selected_title or '(미선택)'}")
        st.write(f"**대본:** {'✅ 생성됨' if st.session_state.generated_script else '❌'}")
        st.write(f"**프롬프트:** {'✅ 생성됨' if st.session_state.generated_prompts else '❌'}")

    # 단계별 화면 표시
    if st.session_state.current_step == 1:
        step1_titles()
    elif st.session_state.current_step == 2:
        step2_script()
    elif st.session_state.current_step == 3:
        step3_prompts()

    # 푸터
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #888;'>낭만처방 쇼츠 생성기 v2.0 | 모바일 최적화</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
