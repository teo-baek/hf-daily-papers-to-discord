import os
import requests
from dotenv import load_dotenv
from utils.translator import translate_korean


load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# ---------------------------------------
# ✳️ 분야별 색상 맵
# ---------------------------------------
FIELD_COLORS = {
    "🧠": 0x3498DB,  # LLM / NLP - 파랑
    "🖼️": 0xE67E22,  # Vision - 주황
    "🔊": 0x9B59B6,  # Audio - 보라
    "🤖": 0x1ABC9C,  # Robotics - 청록
    "🎮": 0xE74C3C,  # Reinforcement Learning - 빨강
    "🕸️": 0x2ECC71,  # Graph - 초록
    "📘": 0x95A5A6,  # 기타 - 회색
}


def short_summary(text, limit=200):
    text = text.strip().replace("\n", " ")
    if len(text) > limit:
        text = text[:limit].rsplit(".", 1)[0] + "..."
    return text


def send_text_to_discord(
    papers, title="Hugging Face Papers", charts=None, mode="daily"
):
    if not DISCORD_WEBHOOK_URL:
        print("❌ DISCORD_WEBHOOK_URL not set.")
        return

    # 1️⃣ 헤더 메시지
    header = {
        "content": f"📰 **{title}**\n총 {len(papers)}편의 논문 요약입니다.",
    }
    requests.post(DISCORD_WEBHOOK_URL, json=header)

    # 2️⃣ 각 논문을 Embed 카드로 전송
    for i, paper in enumerate(papers, start=1):
        field_icon = paper.get("field", "📘")
        color = FIELD_COLORS.get(field_icon, FIELD_COLORS["📘"])
        eng_summary = short_summary(paper["summary"])
        try:
            kr_summary = translate_korean(eng_summary)
        except Exception:
            kr_summary = "(번역 실패)"

        embed = {
            "title": f"{paper.get('field', '📘')} {paper['title']}",
            "url": paper["link"],
            "description": f"📄 {eng_summary}",
            "color": color,  # 초록색
            "fields": [
                {"name": "👥 Authors", "value": paper["authors"], "inline": False},
                {"name": "🇰🇷 Summary (Korean)", "value": kr_summary, "inline": False},
            ],
            "footer": {"text": f"논문 업데이트: {paper.get('updated', 'N/A')}"},
        }

        resp = requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed]})
        if resp.status_code not in (200, 204):
            print(f"⚠️ Embed 전송 실패 ({resp.status_code}): {resp.text[:200]}")
        else:
            print(f"✅ [{i}/{len(papers)}] {paper['title'][:40]}...")

    # 주간 / 월간 그래프 Embed 카드로 전송
    if charts and mode in ("weekly", "monthly"):
        for name, buf in charts.items():
            embed = {
                "title": "📊 Field Distribution",
                "description": f"{mode.capitalize()} paper distribution by category",
                "color": 0x7289DA,  # Discord 블루톤
                "image": {"url": f"attachment://{name}"},
            }

            files = {"file": (name, buf, "image/png")}
            resp = requests.post(
                DISCORD_WEBHOOK_URL, json={"embeds": [embed]}, files=files
            )

            if resp.status_code not in (200, 204):
                print(
                    f"⚠️ 그래프 Embed 전송 실패 ({resp.status_code}): {resp.text[:200]}"
                )
            else:
                print(f"📊 그래프 Embed 전송 완료: {name}")
