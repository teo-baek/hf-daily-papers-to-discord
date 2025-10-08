# from utils.arxiv_fetcher import fetch_arxiv_papers
# from utils.classify import classify_field
# from utils.translator import summarize_paper, translate_korean
# from utils.discord_sender import send_text_to_discord
# from utils.chart_maker import make_charts
# from datetime import date
# from utils.insight_maker import generate_llm_insight, select_llm_recommendations
# from collections import Counter


# def generate_insights(papers):
#     fields = [p.get("field", "📘") for p in papers]
#     counts = Counter(fields)
#     total = sum(counts.values())
#     top_field, top_count = counts.most_common(1)[0]

#     return (
#         f"🧭 이번 주 트렌드 요약\n"
#         f"> {top_field} 분야 연구가 가장 활발했으며, "
#         f"전체의 약 {top_count / total * 100:.1f}%를 차지했습니다.\n"
#         f"> 총 {len(papers)}편의 논문이 {len(set(fields))}개 분야에서 발표되었습니다."
#     )


# def select_top_papers(papers, n=5):
#     """요약 길이 기반으로 대표 논문 5개 선별"""
#     scored = sorted(papers, key=lambda p: len(p["summary"]))[:n]
#     return scored


# def run_weekly():
#     today = date.today()
#     print("📊 Generating weekly insight report...")

#     papers = fetch_arxiv_papers(max_results=200, days=7)
#     for p in papers:
#         p["field"] = classify_field(p["title"], p["summary"])

#     insight = generate_insights(papers)
#     charts = make_charts(papers)
#     top_papers = select_top_papers(papers)

#     # Discord 메시지 구성
#     summary_lines = [insight, "\n💎 **추천 논문 TOP 5**"]
#     for i, p in enumerate(top_papers, 1):
#         summary_lines.append(
#             f"{i}. **{p['title']}**\n> {p['summary'][:120]}...\n> 🔗 <{p['link']}>"
#         )
#     summary_message = "\n".join(summary_lines)

#     send_text_to_discord(
#         [],  # 개별 논문 카드 대신 요약만 전송
#         f"Hugging Face Weekly Papers - {today}",
#         charts=charts,
#         mode="weekly",
#     )

#     print(summary_message)
#     print("✅ Weekly insight report sent!")


# if __name__ == "__main__":
#     run_weekly()

from utils.arxiv_fetcher import fetch_arxiv_papers
from utils.classify import classify_field
from utils.translator import summarize_paper, translate_korean
from utils.chart_maker import make_charts
from utils.discord_sender import send_text_to_discord
from utils.insight_maker import generate_llm_insight, select_llm_recommendations
from datetime import date, timedelta


def run_weekly():
    today = date.today()
    start_date = today - timedelta(days=7)
    date_range = f"{start_date} ~ {today}"

    print(f"📊 Generating AI-powered weekly insight report ({date_range})...")

    # 1️⃣ 논문 수집
    papers = fetch_arxiv_papers(max_results=100, days=7)
    for p in papers:
        p["field"] = classify_field(p["title"], p["summary"])
        p["summary_short"] = summarize_paper(p["title"], p["summary"])
        p["summary_ko"] = translate_korean(p["summary_short"])

    # 2️⃣ LLM 기반 인사이트 & 추천 논문
    insight = generate_llm_insight(papers)
    recommendations = select_llm_recommendations(papers)
    charts = make_charts(papers)

    # 3️⃣ Discord 리포트 전송
    report = (
        f"🗓️ **기간:** {date_range}\n\n"
        f"🧭 **이번 주 트렌드 요약 (LLM 기반)**\n{insight}\n\n"
        f"💎 **추천 논문 TOP 5 (LLM 선정)**\n{recommendations}"
    )
    send_text_to_discord(
        [], f"Hugging Face Weekly Papers - {today}", charts=charts, mode="weekly"
    )

    print(report)
    print("✅ Weekly AI insight report sent!")


if __name__ == "__main__":
    run_weekly()
