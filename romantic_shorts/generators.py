# -*- coding: utf-8 -*-
"""
낭만처방 쇼츠 - AI 생성 모듈
"""

import openai
from config import (
    get_openai_api_key, CHARACTER_REFERENCE_URL, TARGET_WORD_COUNT,
    MIDJOURNEY_STYLE_PREFIX, CHARACTER_PROMPT_COUNT, BACKGROUND_PROMPT_COUNT
)
from word_library import get_word_library_prompt


def init_openai():
    """OpenAI API 초기화"""
    openai.api_key = get_openai_api_key()


def generate_titles(topic: str) -> list:
    """
    주제를 기반으로 쇼츠 최적화 제목 5개 생성

    Args:
        topic: 쇼츠 주제

    Returns:
        list: 최적화된 제목 5개
    """
    init_openai()

    prompt = f"""당신은 YouTube Shorts 전문 콘텐츠 기획자입니다.
"낭만처방"이라는 채널의 쇼츠 제목을 만들어주세요.

채널 컨셉: 현대인의 지친 일상에 80년대 감성의 낭만과 위로를 전달하는 힐링 채널

주제: {topic}

다음 조건을 반드시 지켜주세요:
1. YouTube Shorts 알고리즘에 최적화된 제목 5개 생성
2. 각 제목은 30자 이내
3. 호기심을 자극하고 클릭을 유도하는 문구
4. 감성적이고 공감을 이끌어내는 톤
5. 숫자나 감정 단어 활용 권장

형식:
1. [제목1]
2. [제목2]
3. [제목3]
4. [제목4]
5. [제목5]
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류 발생: {str(e)}"


def generate_script(title: str) -> str:
    """
    선택된 제목을 기반으로 40초 분량의 대본 생성

    Args:
        title: 선택된 쇼츠 제목

    Returns:
        str: 40초 분량 대본
    """
    init_openai()

    word_library = get_word_library_prompt()

    prompt = f"""당신은 "낭만처방" 채널의 전문 대본 작가입니다.
YouTube Shorts용 40초 분량의 감성 대본을 작성해주세요.

제목: {title}

{word_library}

### 대본 작성 규칙:
1. 총 분량: 약 {TARGET_WORD_COUNT}단어 (40초 분량)
2. 위의 필수 단어 라이브러리에서 적절히 단어를 활용할 것
3. 구조:
   - 도입 (5초): 현재의 지친 상태 묘사 (부정 형용사/동사 활용)
   - 전개 (20초): 과거의 낭만적 순간 회상 (80년대 감성)
   - 전환 (10초): 깨달음과 위로의 메시지
   - 마무리 (5초): 희망적 메시지로 끝맺음

4. 톤: 따뜻하고 감성적인 내레이션 스타일
5. 비유 표현을 자연스럽게 1-2개 포함
6. 짧은 문장, 운율감 있게 작성

### 출력 형식:
[도입]
(대본 내용)

[전개]
(대본 내용)

[전환]
(대본 내용)

[마무리]
(대본 내용)

---
총 예상 시간: 00초
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류 발생: {str(e)}"


def generate_midjourney_prompts(script: str, title: str) -> str:
    """
    대본을 기반으로 미드저니 프롬프트 10개 생성

    Args:
        script: 생성된 대본
        title: 쇼츠 제목

    Returns:
        str: 미드저니 프롬프트 10개 (캐릭터 5 + 배경 5)
    """
    init_openai()

    prompt = f"""당신은 Studio Ghibli 스타일 전문 미드저니 프롬프트 엔지니어입니다.
아래 대본을 기반으로 미드저니 이미지 프롬프트를 생성해주세요.

### 쇼츠 제목:
{title}

### 대본:
{script}

### 절대 규칙:
1. 총 10개 생성 (캐릭터 5개 + 배경 5개)
2. 모든 프롬프트는 반드시 "{MIDJOURNEY_STYLE_PREFIX}"로 시작
3. 지브리 감성이 강하게 나오도록 상세 묘사 필수
4. 영어로 작성

### 캐릭터 프롬프트 규칙:
- 캐릭터 일관성을 위해 모든 캐릭터 프롬프트 끝에 다음 추가:
  --cref {CHARACTER_REFERENCE_URL} --cw 100
- 20-30대 한국인 캐릭터
- 감정과 상황이 잘 드러나도록 묘사

### 배경 프롬프트 규칙:
- 80년대 한국 감성 또는 지브리 자연 풍경
- 따뜻하고 노스탤지어 느낌
- 황혼, 골목길, 들판 등 감성적 장소

### 출력 형식:

## 🎭 캐릭터 프롬프트 (5개)

1. [장면 설명]
```
(프롬프트)
```

2. [장면 설명]
```
(프롬프트)
```

(3, 4, 5번 동일 형식)

## 🌄 배경 프롬프트 (5개)

1. [장면 설명]
```
(프롬프트)
```

(2, 3, 4, 5번 동일 형식)
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류 발생: {str(e)}"
