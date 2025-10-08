import matplotlib.pyplot as plt
import os
from collections import Counter
from datetime import date


def make_charts(papers):
    os.makedirs("charts", exist_ok=True)
    fields = [p.get("field", "General") for p in papers]
    counts = Counter(fields)

    # 분야별 비율
    plt.figure(figsize=(6, 4))
    plt.bar(counts.keys(), counts.values())
    plt.title("Field Distribution")
    plt.savefig("charts/fields.png", bbox_inches="tight")
    plt.close()

    return ["charts/fields.png"]


def make_monthly_charts(papers):
    # 확장용: 월간 데이터 기반 그래프
    return make_charts(papers)
