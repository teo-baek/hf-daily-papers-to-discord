import requests
from datetime import date

# 🔧 Discord Webhook URL — 본인 것으로 교체 (이미 연결된 걸 그대로 사용 가능)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1425269624215310407/FlmDiO8nrayDSJWioXCaH6zs73_0V_pPBwkfiiIVfqtY2noEGW-PXD8G9vLkdiu1hp2A"


def fetch_papers():
    """Hugging Face Daily Papers JSON 데이터 가져오기"""
    url = "https://huggingface.co/papers/api/feed"
    print(f"📡 Fetching data from: {url}")
    resp = requests.get(url)
    resp.raise_for_status()

    # 응답이 JSON인지 확인
    try:
        data = resp.json()
        print(f"✅ 데이터 수신 완료 ({len(data)}개 논문)")
        return data
    except ValueError:
        print("❌ API 응답이 JSON이 아닙니다. 응답 내용 일부:")
        print(resp.text[:300])
        return []


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
        resp = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        try:
            resp.raise_for_status()
            print(f"📨 전송됨 ({len(chunk)}자)")
        except requests.exceptions.HTTPError as e:
            print(f"❌ Discord 전송 실패: {e} ({resp.status_code})")
            print("응답 내용:", resp.text[:200])


def main():
    try:
        papers = fetch_papers()
        if not papers:
            print("⚠️ 가져온 논문 데이터가 없습니다. (API 응답 확인 필요)")
            return

        today = date.today().strftime("%Y-%m-%d")
        header = f"📰 **Hugging Face Daily Papers - {today}**\n총 {len(papers)}편\n\n"
        body = summarize_all(papers)
        send_to_discord(header + body)
        print(f"✅ 전송 완료 ({len(papers)} papers)")
    except Exception as e:
        print("❌ 오류 발생:", e)


if __name__ == "__main__":
    main()
