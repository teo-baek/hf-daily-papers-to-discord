# def classify_field(title, summary):
#     text = (title + " " + summary).lower()
#     if any(k in text for k in ["language model", "llm", "gpt", "bert", "nlp"]):
#         return "🧠"
#     elif any(k in text for k in ["image", "vision", "diffusion", "object detection"]):
#         return "🖼️"
#     elif any(k in text for k in ["audio", "speech", "sound", "voice"]):
#         return "🔊"
#     elif any(k in text for k in ["robot", "motion", "navigation"]):
#         return "🤖"
#     elif any(k in text for k in ["reinforcement", "policy", "agent"]):
#         return "🎮"
#     elif any(k in text for k in ["graph", "gnn", "network"]):
#         return "🕸️"
#     else:
#         return "📘"

import re
import os
from openai import OpenAI
from dotenv import load_dotenv

# ----------------------------
# 🔧 환경설정
# ----------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


# ----------------------------
# 🧩 1️⃣ 정규식 기반 분류
# ----------------------------
def classify_by_regex(title: str, summary: str) -> str:
    """논문 제목 + 요약을 기반으로 분야를 정규식으로 분류"""
    text = (title + " " + summary).lower()

    patterns = {
        "🧠": [
            r"\b(llm|language model|bert|gpt|transformer|reasoning|chatbot|text generation)\b"
        ],
        "🖼️": [
            r"\b(image|vision|diffusion|segmentation|detection|text-to-image|inpainting|clip|gan)\b"
        ],
        "🔊": [r"\b(audio|speech|voice|sound|music|asr|speaker recognition)\b"],
        "🤖": [
            r"\b(robot|navigation|manipulation|grasp|locomotion|control|autonomous)\b"
        ],
        "🎮": [r"\b(reinforcement|agent|policy|rl|q-learning|actor-critic)\b"],
        "🕸️": [r"\b(graph|gnn|node|link prediction|graph neural network)\b"],
        "⚙️": [
            r"\b(multimodal|alignment|embedding|representation|token|cross-modal|fusion)\b"
        ],
    }

    for icon, regexes in patterns.items():
        if any(re.search(r, text) for r in regexes):
            return icon

    return "📘"  # 기본값 (미분류)


# ----------------------------
# 🤖 2️⃣ LLM 기반 보조 분류
# ----------------------------
def classify_by_llm(title: str, summary: str) -> str:
    """LLM을 이용한 분야 분류 (OpenAI API 사용)"""
    if not client:
        return "📘"

    prompt = f"""
    You are an expert AI researcher. Classify the following paper into one of these categories:
    [LLM, Vision, Audio, Robotics, RL, Graph, Multimodal, Other]

    Title: {title}
    Abstract: {summary}

    Return ONLY the category name (e.g., 'LLM').
    """

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt.strip()}],
            temperature=0.0,
            max_tokens=10,
        )
        label = res.choices[0].message.content.strip().lower()
    except Exception as e:
        print(f"⚠️ LLM 분류 실패: {e}")
        return "📘"

    mapping = {
        "llm": "🧠",
        "vision": "🖼️",
        "audio": "🔊",
        "robotics": "🤖",
        "rl": "🎮",
        "graph": "🕸️",
        "multimodal": "⚙️",
        "other": "📘",
    }

    # 키워드 일부 일치 허용 (e.g., 'large language model' → llm)
    for key, icon in mapping.items():
        if key in label:
            return icon

    return "📘"


# ----------------------------
# 🧠 3️⃣ 하이브리드 분류기 (통합)
# ----------------------------
def classify_field(title: str, summary: str) -> str:
    """정규식 + LLM 하이브리드 논문 분야 분류"""
    # 1️⃣ 1차: 정규식 기반 분류 시도
    field = classify_by_regex(title, summary)

    # 2️⃣ 2차: 미분류 시 LLM으로 보완
    if field == "📘" and client:
        print(f"🤔 정규식으로 분류 실패 → LLM 분류 시도 중: {title[:60]}...")
        field = classify_by_llm(title, summary)

    return field
