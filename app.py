import streamlit as st

# 앱 페이지 설정
st.set_page_config(page_title="속보고(Sokbogo) 콘텐츠 생성기", page_icon="🐱", layout="wide")

# 제목 및 스타일 설정
st.title("🔬 속보고(Sokbogo) 건강 콘텐츠 패키지 생성기")
st.markdown(
    "임상병리사 관점의 건강 정보를 바탕으로, **3D 미니어처 클레이 디오라마 토이 월드** 스타일 콘텐츠를 생성합니다."
)
st.divider()

# 사용자 입력
topic = st.text_input(
    "건강 주제를 입력하세요:",
    placeholder="예: 공복혈당 관리, 철분 부족 신호, 콜레스테롤 검사 해석",
)

if topic:
    character_rule = (
        "Character rule (fixed): A white cat couple only — one cat wearing a pastel blue sweater and hat, "
        "the other wearing a pastel pink sweater and hat."
    )

    # 1. DALL-E 3 이미지 프롬프트
    image_prompt = f"""Create a highly detailed DALL-E 3 prompt for a vertical 9:16 YouTube Shorts cover scene.

Topic: {topic}
{character_rule}
Art style: 3D miniature clay diorama, toy world aesthetics, strong tilt-shift effect, shallow depth of field.

Scene requirements:
- The two white cats are the only main characters and appear as a loving couple exploring a tiny health lab.
- Build a miniature medical set that visually explains the topic through lab tools (microscope, slides, blood tube rack, tiny charts).
- Express clinical-laboratory credibility with clean labels, realistic specimen colors, and educational visual cues.
- Keep the tone cute and warm, but scientifically trustworthy.
- Add tactile clay texture details: fingerprints on clay, matte finish, soft handcrafted edges.
- Lighting: soft studio key light + gentle rim light, high clarity, macro lens look.
- Composition: central characters, readable foreground symbols related to the topic, cinematic bokeh background.
- Quality tags: ultra-detailed, 8k, physically based rendering, toy photography, macro miniature.
"""

    # 2. Kling 2.6 영상 프롬프트
    video_prompt = f"""Kling 2.6 Video Prompt (9:16, 30s)

Topic: {topic}
{character_rule}
Visual style: 3D miniature clay diorama toy world, strong tilt-shift, macro cinematography.

Direction:
- Start with an extreme macro close-up of clay texture (sweater knit, hat seam, tiny medical props).
- Slow dolly-in as the blue-sweater cat points to a tiny test result board; pink-sweater cat reacts and organizes sample tubes.
- Add subtle hand-crafted motion: tiny clay particles, gentle prop vibration, soft cloth friction.
- Transition through 3 short scenes that explain the health topic logically from cause → 검사/지표 → 생활관리 팁.
- Maintain clinical-laboratory authority while preserving a cute couple chemistry.

ASMR/Sound design emphasis:
- Soft tapping on clay desk, micro brush swish, sample tube click, notebook page flip, sweater fabric rustle.
- Crisp close-mic Foley, low ambient hum, no harsh music.

Render notes: ultra-detailed clay material, realistic miniature shadows, stable focus pulls, warm educational mood.
"""

    # 3. 30초 나레이션 (타임코드 제외)
    narration = f"""오늘은 {topic}를 쉽고 정확하게 알려드릴게요.
검사실에서 실제로 중요하게 보는 포인트는 몸의 신호를 숫자로 확인하는 것입니다.
이 주제에서는 원인과 위험 신호를 먼저 이해하고, 필요한 검사 지표를 함께 확인하는 것이 핵심입니다.
수치가 경계 범위에 있다면 생활 습관 교정만으로도 충분히 개선될 수 있습니다.
식사 균형, 수면, 활동량, 그리고 정기 검사를 꾸준히 이어가면 몸은 분명히 달라집니다.
내 수치를 알고 관리하는 습관이 가장 정확한 건강 전략입니다.
속보고와 함께, 오늘도 내 몸의 변화를 똑똑하게 확인해 보세요."""

    # 4. 유튜브 메타데이터
    title = f"{topic}, 검사실 관점으로 30초 핵심 정리 🧪 | 속보고"
    hashtags = "#속보고 #건강정보 #임상병리 #건강검진 #shorts"
    description = f"""{topic}, 어디서부터 관리해야 할지 막막하셨나요?
임상병리 지식을 바탕으로 원인·검사 지표·실천 팁을 30초에 정리했습니다.
귀엽지만 정확한 토이 월드 디오라마로, 건강 정보를 더 쉽게 이해해 보세요.

{hashtags}"""
    pinned_comment = f"오늘 주제는 '{topic}' 입니다. 다음에 다뤄줬으면 하는 건강 주제를 댓글로 남겨주세요! 🐱💕"

    # 결과 출력
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🖼️ 이미지 프롬프트 (DALL-E 3)")
        st.code(image_prompt, language="text")

        st.subheader("🎬 Kling 2.6 영상 프롬프트 (ASMR 강화)")
        st.code(video_prompt, language="text")

    with col2:
        st.subheader("📝 30초 나레이션")
        st.info(narration)

        st.subheader("📈 유튜브 메타데이터")
        st.text_area(
            "제목 / 해시태그 / 영상 설명",
            f"""[제목] {title}
[해시태그] {hashtags}
[영상 설명]
{description}""",
            height=260,
        )

        st.subheader("📌 고정 댓글")
        st.code(pinned_comment)

else:
    st.info("건강 주제를 입력하면 요청하신 규칙 기반 전체 콘텐츠 패키지가 생성됩니다.")
