from utils.arxiv_fetcher import fetch_arxiv_papers
from utils.classify import classify_field
from utils.discord_sender import send_text_to_discord
from utils.chart_maker import make_monthly_charts
from datetime import date


def run_monthly():
    today = date.today()
    print("🧠 Generating monthly summary...")

    papers = fetch_arxiv_papers(max_results=300, days=30)
    for p in papers:
        p["field"] = classify_field(p["title"], p["summary"])

    charts = make_monthly_charts(papers)
    send_text_to_discord(
        papers,
        f"Hugging Face Monthly Papers - {today} ({len(papers)}편)",
        charts=charts,
        mode="monthly",
    )

    print("✅ Monthly summary sent!")
