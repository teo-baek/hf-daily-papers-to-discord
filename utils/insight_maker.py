import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_llm_insight(papers):
    """LLM이 주간/월간 트렌드 인사이트 생성"""
    titles = "\n".join([f"- {p['title']}" for p in papers[:50]])  # 상위 50개만 참고
    prompt = f"""
    You are an AI research analyst. Based on the following list of recent AI papers, 
    summarize the key trends and topics emerging in the past period (1-2 paragraphs). 
    List provided:
    {titles}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()


def select_llm_recommendations(papers):
    """LLM이 추천 논문 TOP5 선정"""
    paper_list = "\n".join(
        [
            f"{i+1}. {p['title']} - {p['summary'][:200]}"
            for i, p in enumerate(papers[:30])
        ]
    )
    prompt = f"""
    You are an expert AI reviewer. From the following papers, choose the 5 that are the most impactful or novel.
    Provide the output as a numbered list (1-5) with 1-sentence explanation each.
    Papers:
    {paper_list}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ 추천 논문 생성 실패: {e}")
        return "추천 논문 생성 실패"
