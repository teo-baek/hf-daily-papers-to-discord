import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# 🔑 환경 변수에서 OpenAI API 키 불러오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("⚠️ Warning: OPENAI_API_KEY not found. Translation will be skipped.")
    client = None
else:
    client = OpenAI(api_key=OPENAI_API_KEY)


def translate_korean(text: str, mode: str = "casual") -> str:
    """
    OpenAI 모델을 사용한 자연스러운 한국어 번역.
    mode:
        - "casual": 일반 독자용 (쉬운 표현, 기본값)
        - "tech": 기술적 / 연구자용 (전문 용어 유지)
        - "kids": 청소년도 이해할 수 있는 쉬운 문장
    """

    if not text or text.strip() == "":
        return ""

    if not client:
        # API 키 없을 때는 원문 그대로 반환
        return text

    # --- 번역 스타일 선택 ---
    if mode == "tech":
        style = (
            "Translate the following English text into precise and professional Korean, "
            "keeping technical terms accurate and natural for AI researchers."
        )
    elif mode == "kids":
        style = (
            "Translate and simplify the following text into short, friendly Korean that a middle school student could easily understand. "
            "Avoid jargon and use simple words."
        )
    else:  # casual (default)
        style = (
            "Translate the following English academic summary into natural, smooth Korean "
            "that is easy for anyone to understand, even non-technical readers. "
            "Avoid heavy jargon and math symbols."
        )

    prompt = f"{style}\n\nEnglish text:\n{text.strip()}\n\nKorean translation:"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a skilled Korean translator and science communicator.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=400,
        )

        translation = response.choices[0].message.content.strip()

        # 🧹 후처리 — 너무 긴 문장, HTML 엔티티 등 제거
        translation = translation.replace("&quot;", '"').replace("&amp;", "&")
        translation = translation.replace("번역:", "").strip()

        return translation

    except Exception as e:
        print(f"❌ Translation error: {e}")
        return text
