import requests, feedparser
from datetime import date, timedelta

ARXIV_CATEGORIES = ["cs.AI", "cs.CL", "cs.CV", "cs.LG", "stat.ML", "eess.AS"]


def fetch_arxiv_papers(max_results=20, days=7):
    query = "+OR+".join([f"cat:{c}" for c in ARXIV_CATEGORIES])
    url = f"http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    feed = feedparser.parse(requests.get(url, timeout=20).text)
    cutoff = date.today() - timedelta(days=days)

    papers = []
    for e in feed.entries:
        updated = e.updated.split("T")[0]
        if date.fromisoformat(updated) < cutoff:
            continue
        papers.append(
            {
                "title": e.title.strip(),
                "summary": e.summary.strip().replace("\n", " "),
                "link": e.link,
                "authors": ", ".join(a.name for a in e.authors),
                "updated": updated,
            }
        )
    return papers
