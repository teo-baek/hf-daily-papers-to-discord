import io
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib import font_manager, rc
import os

# ✅ 폰트 설정 (이모지 지원)
font_path = "C:/Windows/Fonts/seguiemj.ttf"  # Windows용 이모지 폰트
if os.path.exists(font_path):
    font_manager.fontManager.addfont(font_path)
    rc("font", family="Segoe UI Emoji")

FIELD_COLORS = {
    "🧠": "#3498DB",  # 파랑
    "🖼️": "#E67E22",  # 주황
    "🔊": "#9B59B6",  # 보라
    "🤖": "#1ABC9C",  # 청록
    "🎮": "#E74C3C",  # 빨강
    "🕸️": "#2ECC71",  # 초록
    "📘": "#95A5A6",  # 회색
}


def make_charts(papers):
    """분야별 통계 그래프를 이미지 버퍼로 반환"""
    fields = [p.get("field", "📘") for p in papers]
    counts = Counter(fields)

    colors = [FIELD_COLORS.get(f, "#95A5A6") for f in counts.keys()]

    plt.figure(figsize=(6, 4))
    plt.bar(counts.keys(), counts.values(), color=colors)
    plt.title("Field Distribution")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return {"fields.png": buf}


def make_monthly_charts(papers):
    """월간 차트 (현재는 동일하지만 확장 가능)"""
    return make_charts(papers)
