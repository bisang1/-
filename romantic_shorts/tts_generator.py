# -*- coding: utf-8 -*-
"""
낭만처방 쇼츠 - TTS 생성 모듈
"""

import asyncio
import edge_tts
import os
import re
import tempfile
import shutil
from config import TTS_VOICES, SPEED_OPTIONS


async def generate_tts_async(text: str, voice_name: str, speed: float, output_path: str) -> str:
    """
    edge-tts를 사용하여 TTS 음성 생성 (비동기)

    Args:
        text: 변환할 텍스트
        voice_name: TTS_VOICES의 키 (예: "남자 청년")
        speed: 배속 (1.0 = 보통)
        output_path: 출력 파일 경로

    Returns:
        str: 생성된 파일 경로
    """
    voice_id = TTS_VOICES.get(voice_name, "ko-KR-InJoonNeural")

    # 배속을 edge-tts rate 형식으로 변환
    # 1.0 = +0%, 1.5 = +50%, 0.75 = -25%
    rate_percent = int((speed - 1.0) * 100)
    if rate_percent >= 0:
        rate = f"+{rate_percent}%"
    else:
        rate = f"{rate_percent}%"

    communicate = edge_tts.Communicate(text, voice_id, rate=rate)
    await communicate.save(output_path)

    return output_path


def generate_tts(text: str, voice_name: str, speed: float, output_path: str) -> str:
    """
    TTS 음성 생성 (동기 래퍼)

    Args:
        text: 변환할 텍스트
        voice_name: 음성 종류
        speed: 배속
        output_path: 출력 파일 경로

    Returns:
        str: 생성된 파일 경로
    """
    # 대본에서 불필요한 부분 제거 (섹션 헤더 등)
    clean_text = clean_script_for_tts(text)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(
            generate_tts_async(clean_text, voice_name, speed, output_path)
        )
        return result
    finally:
        loop.close()


def clean_script_for_tts(text: str) -> str:
    """
    대본 텍스트를 TTS용으로 정리

    Args:
        text: 원본 대본 텍스트

    Returns:
        str: 정리된 텍스트
    """
    # 섹션 헤더 제거 [도입], [전개] 등
    text = re.sub(r'\[.*?\]', '', text)

    # 마크다운 헤더 제거
    text = re.sub(r'^#+\s+.*$', '', text, flags=re.MULTILINE)

    # 구분선 제거
    text = re.sub(r'^-+$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^=+$', '', text, flags=re.MULTILINE)

    # 총 예상 시간 등 메타 정보 제거
    text = re.sub(r'총 예상 시간:.*', '', text)

    # 여러 줄바꿈을 하나로
    text = re.sub(r'\n+', '\n', text)

    # 앞뒤 공백 제거
    text = text.strip()

    return text


def generate_tts_with_speed(text: str, voice_name: str, speed: float, output_dir: str = None) -> str:
    """
    TTS 생성 + 배속 조절 통합 함수

    Args:
        text: 변환할 텍스트
        voice_name: 음성 종류
        speed: 배속
        output_dir: 출력 디렉토리 (None이면 임시 디렉토리)

    Returns:
        str: 최종 파일 경로
    """
    if output_dir is None:
        output_dir = tempfile.gettempdir()

    # 파일명에 사용할 수 없는 문자 제거
    safe_voice_name = voice_name.replace(" ", "_")
    final_path = os.path.join(output_dir, f"romantic_tts_{safe_voice_name}_{speed}x.mp3")

    # TTS 생성 (배속 포함)
    generate_tts(text, voice_name, speed, final_path)

    return final_path


def get_available_voices() -> list:
    """사용 가능한 음성 목록 반환"""
    return list(TTS_VOICES.keys())


def get_speed_options() -> dict:
    """사용 가능한 배속 옵션 반환"""
    return SPEED_OPTIONS
