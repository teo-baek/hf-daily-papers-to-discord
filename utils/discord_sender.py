import os
import requests
from dotenv import load_dotenv
from utils.translator import translate_korean

load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def chunk_message(content, limit=1900):
    """디스코드 2000자 제한 대응"""
    chunks = []
    while len(content) > limit:
        split_idx = content[:limit].rfind("\n\n")
        if split_idx == -1:
            split_idx = limit
        chunks.append(content[:split_idx])
        content = content[split_idx:]
    chunks.append(content)
    return chunks


def format_paper_entry(paper):
    """논문 정보 Markdown 포맷 변환"""
    kr_summary = translate_korean(paper["summary"][:250]) or "(번역 없음)"
    field_icon = get_field_icon(paper.get("field", "General"))

    entry = (
        f"# {field_icon} {paper['title']}\n"
        f"> 👥 {paper['authors']}\n"
        f"> 📄 {paper['summary']}\n"
        f"> 📄 {kr_summary}\n"
        f"> 🔗 <{paper['link']}>\n"
    )
    return entry


def get_field_icon(field):
    icons = {
        "LLM": "🧠",
        "Vision": "🖼️",
        "Audio": "🔊",
        "Robotics": "🤖",
        "RL": "🎮",
        "Graph": "🕸️",
        "General": "📘",
    }
    return icons.get(field, "📘")


def send_text_to_discord(
    papers, title="Hugging Face Papers", charts=None, mode="daily"
):
    """텍스트 기반 Discord 전송 (공용)"""
    if not DISCORD_WEBHOOK_URL:
        print("❌ DISCORD_WEBHOOK_URL not set.")
        return

    header = f"📰 **{title}**\n총 {len(papers)}편의 논문 요약입니다.\n\n"
    body = "\n\n".join(format_paper_entry(p) for p in papers)
    full_message = header + body

    for chunk in chunk_message(full_message):
        resp = requests.post(DISCORD_WEBHOOK_URL, json={"content": chunk})
        if resp.status_code not in (200, 204):
            print(f"⚠️ Discord 전송 실패 ({resp.status_code}): {resp.text[:200]}")
        else:
            print(f"✅ Discord 전송 완료 ({len(chunk)}자)")

    # 주간 / 월간에는 그래프도 첨부
    if charts and mode in ("weekly", "monthly"):
        for name, buf in charts.items():
            resp = requests.post(
                DISCORD_WEBHOOK_URL, files={"file": (name, buf, "image/png")}
            )
            print(f"📊 그래프 전송 완료: {name} ({resp.status_code})")
