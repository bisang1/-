import streamlit as st

# 앱 페이지 설정
st.set_page_config(page_title="속보고(Sokbogo) 콘텐츠 생성기", page_icon="🫁", layout="wide")

# 제목 및 스타일 설정
st.title("🔬 속보고(Sokbogo) 유튜브 쇼츠 제작 자동화 도구")
st.markdown("임상병리사의 전문성이 담긴 **거대 해부 디오라마** 콘텐츠를 위한 자동 생성기입니다.")
st.divider()

# 사용자 입력
organ = st.text_input("콘텐츠를 제작할 장기/신체 부위를 입력하세요:", placeholder="예: 심장, 폐, 간, 치아")

if organ:
    # 1. 이미지 프롬프트 생성 로직
    image_prompt = f"""Input Variable: {organ}

System Instruction:
Generate a hyper-realistic, scientifically accurate "Anatomical Autopsy" cross-section diorama.
- Layer 1 (Integumentary): Outer protective barrier.
- Layer 2 (Parenchyma): Functional internal tissue.
- Layer 3 (Vascular/Neural): Internal transport network.

Layout: Vertical Anatomical Chart (Top to Bottom) for 9:16 frame.
Details: 1:87 Scale tiny researchers, Magenta MRI lines, holographic UI.
Output: 9:16 Aspect Ratio, Medical Macro Photography, Gray's Anatomy Aesthetic, 8k Resolution."""

    # 2. 영상 프롬프트 생성 로직 (정책 준수형)
    video_prompt = f"""Prompt: [Scene Description] Cinematic 9:16 macro video of a massive "Bio-Engineered Architectural Model" of a {organ}. Camera: Slow vertical crane-down.
[Action] Tiny 1:87 scale technical inspectors performing "Precision Calibration", robotic cranes, magenta data-mapping lines.
[Aesthetics] Translucent pearlescent finish, internal glow, high-key scientific lab lighting.
[Cinematography] 8k resolution, extreme detail, Gray's Anatomy aesthetic."""

    # 3. 쇼츠 대본 및 메타데이터 (이전 대본 구조 반영)
    script = f"""(00:00~00:05) [후킹]
당신의 몸속에 숨겨진 경이로운 비밀, {organ}! 지금 이 안에서 무슨 일이 벌어지고 있을까요?

(00:05~00:15) [본론 1]
놀라지 마세요. 우리 {organ}은(는) 생각보다 훨씬 거대하고 정밀한 시스템입니다.

(00:15~00:25) [본론 2]
수천 명의 보이지 않는 세포들이 당신의 생명을 위해 24시간 쉬지 않고 일하고 있죠. 이 정교한 설계도를 보세요.

(00:25~00:30) [엔딩]
당신의 소중한 {organ}, 오늘 한 번 더 아껴주세요. 속보고였습니다! 구독하고 건강을 지키세요!"""

    # 결과물 출력 (복사 버튼 제공)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🖼️ 이미지 생성 프롬프트 (Midjourney/DALL-E)")
        st.code(image_prompt, language="text")

        st.subheader("🎬 영상 생성 프롬프트 (Sora 2/Veo)")
        st.code(video_prompt, language="text")

    with col2:
        st.subheader("📝 30초 쇼츠 나레이션 대본")
        st.info(script)

        st.subheader("📈 채널 최적화 정보")
        st.text_area(
            "제목/설명/태그",
            f"""[제목] 내 몸속의 거대 도시, {organ}의 신비로운 정체 🔬
[설명] 당신의 {organ} 내부를 초정밀 해부 디오라마로 공개합니다!
#속보고 #인체의신비 #{organ} #건강정보 #shorts""",
        )

        st.subheader("📌 고정 댓글")
        st.code(f"여러분의 {organ}은 오늘 안녕한가요? 궁금한 점은 댓글로 남겨주세요! 👇")

    st.subheader("🏷️ 썸네일 추천 후킹 문구")
    st.warning(f"'{organ} 속의 거대 도시' | '당신만 모르는 {organ}의 비밀' | '절대 무시 금지!'")

else:
    st.info("장기 이름을 입력하면 '속보고' 전용 콘텐츠 팩이 생성됩니다.")
