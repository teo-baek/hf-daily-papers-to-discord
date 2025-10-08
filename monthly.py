#

from utils.arxiv_fetcher import fetch_arxiv_papers
from utils.classify import classify_field
from utils.translator import summarize_paper, translate_korean
from utils.chart_maker import make_monthly_charts
from utils.discord_sender import send_text_to_discord
from utils.insight_maker import generate_llm_insight, select_llm_recommendations
from datetime import date, timedelta


def run_monthly():
    today = date.today()
    start_date = today - timedelta(days=30)
    date_range = f"{start_date} ~ {today}"
    print(f"🧠 Generating AI-powered monthly insight report ({date_range})...")

    papers = fetch_arxiv_papers(max_results=200, days=30)
    for p in papers:
        p["field"] = classify_field(p["title"], p["summary"])
        p["summary_short"] = summarize_paper(p["title"], p["summary"])
        p["summary_ko"] = translate_korean(p["summary_short"])

    insight = generate_llm_insight(papers)
    recommendations = select_llm_recommendations(papers)
    charts = make_monthly_charts(papers)

    report = (
        f"🗓️ **기간:** {date_range}\n\n"
        f"📆 **이달의 트렌드 요약 (LLM 분석)**\n{insight}\n\n"
        f"💎 **이달의 추천 논문 TOP 5 (LLM 선정)**\n{recommendations}"
    )
    send_text_to_discord(
        [], f"Hugging Face Monthly Papers - {today}", charts=charts, mode="monthly"
    )

    print(report)
    print("✅ Monthly AI insight report sent!")


if __name__ == "__main__":
    run_monthly()
