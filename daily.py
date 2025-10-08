from utils.arxiv_fetcher import fetch_arxiv_papers
from utils.classify import classify_field
from utils.discord_sender import send_text_to_discord
from datetime import date


def run_daily():
    today = date.today()
    print("📡 Fetching daily papers...")

    papers = fetch_arxiv_papers(max_results=20)
    if not papers:
        print("⚠️ No papers found.")
        return

    for p in papers:
        p["field"] = classify_field(p["title"], p["summary"])

    send_text_to_discord(papers, f"Hugging Face Daily Papers - {today}", mode="daily")
    print("✅ Daily papers sent!")
