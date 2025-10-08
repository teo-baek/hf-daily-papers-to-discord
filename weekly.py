from utils.arxiv_fetcher import fetch_arxiv_papers
from utils.classify import classify_field
from utils.discord_sender import send_text_to_discord
from utils.chart_maker import make_charts
from datetime import date


def run_weekly():
    today = date.today()
    print("📊 Generating weekly report...")

    papers = fetch_arxiv_papers(max_results=120, days=7)
    for p in papers:
        p["field"] = classify_field(p["title"], p["summary"])

    charts = make_charts(papers)
    send_text_to_discord(
        papers,
        f"Hugging Face Weekly Papers - {today} ({len(papers)}편)",
        charts=charts,
        mode="weekly",
    )

    print("✅ Weekly report sent!")
