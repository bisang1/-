# -*- coding: utf-8 -*-
"""
낭만처방 쇼츠 - 설정 파일
"""

# OpenAI API 설정
OPENAI_API_KEY = ""  # 여기에 API 키 입력

# 미드저니 캐릭터 일관성 URL
CHARACTER_REFERENCE_URL = "https://cdn.midjourney.com/35a36161-bd6d-4992-93c3-56a9e511a2c8/0_0.png"

# 쇼츠 설정
SHORTS_DURATION_SECONDS = 40
WORDS_PER_SECOND = 2.5  # 한국어 평균 발화 속도
TARGET_WORD_COUNT = int(SHORTS_DURATION_SECONDS * WORDS_PER_SECOND)  # 약 100단어

# 미드저니 프롬프트 설정
MIDJOURNEY_STYLE_PREFIX = "Studio Ghibli style"
CHARACTER_PROMPT_COUNT = 5
BACKGROUND_PROMPT_COUNT = 5

# TTS 음성 설정 (edge-tts 사용)
TTS_VOICES = {
    "남자 청년": "ko-KR-InJoonNeural",
    "남자 중년": "ko-KR-HyunsuNeural",
    "남자 노년": "ko-KR-GookMinNeural",
    "여자 청년": "ko-KR-SunHiNeural",
    "여자 중년": "ko-KR-JiMinNeural",
    "여자 노년": "ko-KR-SoonBokNeural",
}

# 배속 설정
SPEED_OPTIONS = {
    "0.75x (느리게)": 0.75,
    "1.0x (보통)": 1.0,
    "1.25x (조금 빠르게)": 1.25,
    "1.5x (빠르게)": 1.5,
    "2.0x (매우 빠르게)": 2.0,
}
