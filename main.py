import requests
from datetime import date

# 🔧 본인 Discord Webhook URL 입력
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1425269624215310407/FlmDiO8nrayDSJWioXCaH6zs73_0V_pPBwkfiiIVfqtY2noEGW-PXD8G9vLkdiu1hp2A"


def fetch_papers():
    """Hugging Face Daily Papers RSS JSON 가져오기"""
    url = "https://papers.takara.ai/api/feed"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def chunk_message(content, limit=1900):
    """디스코드 2000자 제한을 피하기 위한 메시지 분할"""
    chunks = []
    while len(content) > limit:
        split_idx = content[:limit].rfind("\n\n")
        if split_idx == -1:
            split_idx = limit
        chunks.append(content[:split_idx])
        content = content[split_idx:]
    chunks.append(content)
    return chunks


def summarize_all(papers):
    """전체 논문 요약"""
    lines = []
    for idx, p in enumerate(papers, 1):
        title = p.get("title", "제목 없음")
        authors = ", ".join(p.get("authors", [])) or "저자 정보 없음"
        summary = p.get("summary") or p.get("description", "") or "(요약 없음)"
        link = p.get("url") or p.get("link", "")
        lines.append(f"**{idx}. {title}**\n👥 {authors}\n📝 {summary}\n🔗 {link}\n")
    return "\n".join(lines)


def send_to_discord(message):
    """메시지를 Discord에 전송 (자동 분할 포함)"""
    chunks = chunk_message(message)
    for chunk in chunks:
        payload = {"content": chunk}
        requests.post(DISCORD_WEBHOOK_URL, json=payload)


def main():
    try:
        papers = fetch_papers()
        today = date.today().strftime("%Y-%m-%d")
        header = f"📰 **Hugging Face Daily Papers - {today}**\n총 {len(papers)}편\n\n"
        body = summarize_all(papers)
        send_to_discord(header + body)
        print(f"✅ 전송 완료 ({len(papers)} papers)")
    except Exception as e:
        print("❌ 오류 발생:", e)


if __name__ == "__main__":
    main()
