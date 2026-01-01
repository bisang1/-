# -*- coding: utf-8 -*-
"""
낭만처방 쇼츠 - TTS 생성 모듈
"""

import asyncio
import edge_tts
from pydub import AudioSegment
import os
import tempfile
from config import TTS_VOICES, SPEED_OPTIONS


async def generate_tts_async(text: str, voice_name: str, output_path: str) -> str:
    """
    edge-tts를 사용하여 TTS 음성 생성 (비동기)

    Args:
        text: 변환할 텍스트
        voice_name: TTS_VOICES의 키 (예: "남자 청년")
        output_path: 출력 파일 경로

    Returns:
        str: 생성된 파일 경로
    """
    voice_id = TTS_VOICES.get(voice_name, "ko-KR-InJoonNeural")

    communicate = edge_tts.Communicate(text, voice_id)
    await communicate.save(output_path)

    return output_path


def generate_tts(text: str, voice_name: str, output_path: str) -> str:
    """
    TTS 음성 생성 (동기 래퍼)

    Args:
        text: 변환할 텍스트
        voice_name: 음성 종류
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
            generate_tts_async(clean_text, voice_name, output_path)
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
    import re

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


def change_audio_speed(input_path: str, output_path: str, speed: float) -> str:
    """
    오디오 파일의 배속 변경

    Args:
        input_path: 입력 파일 경로
        output_path: 출력 파일 경로
        speed: 배속 (1.0 = 원본 속도)

    Returns:
        str: 출력 파일 경로
    """
    if speed == 1.0:
        # 배속 변경 없음 - 파일 복사만
        if input_path != output_path:
            import shutil
            shutil.copy(input_path, output_path)
        return output_path

    # 오디오 로드
    audio = AudioSegment.from_mp3(input_path)

    # 배속 변경 (샘플레이트 조절 방식)
    # speed > 1: 빠르게, speed < 1: 느리게
    new_sample_rate = int(audio.frame_rate * speed)

    # 샘플레이트 변경으로 속도 조절
    speed_changed = audio._spawn(audio.raw_data, overrides={
        "frame_rate": new_sample_rate
    })

    # 원래 샘플레이트로 복원 (피치 유지하면서 속도만 변경)
    final_audio = speed_changed.set_frame_rate(audio.frame_rate)

    # 저장
    final_audio.export(output_path, format="mp3")

    return output_path


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

    # 임시 파일로 TTS 생성
    temp_path = os.path.join(output_dir, "tts_temp.mp3")
    final_path = os.path.join(output_dir, f"낭만처방_tts_{voice_name}_{speed}x.mp3")

    # TTS 생성
    generate_tts(text, voice_name, temp_path)

    # 배속 조절
    change_audio_speed(temp_path, final_path, speed)

    # 임시 파일 삭제
    if os.path.exists(temp_path) and temp_path != final_path:
        os.remove(temp_path)

    return final_path


def get_available_voices() -> list:
    """사용 가능한 음성 목록 반환"""
    return list(TTS_VOICES.keys())


def get_speed_options() -> dict:
    """사용 가능한 배속 옵션 반환"""
    return SPEED_OPTIONS
