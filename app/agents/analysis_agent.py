from langchain_groq import ChatGroq

from config import GROQ_API_KEY

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=GROQ_API_KEY
)

def analysis_agent(state):

    prompt = f"""
Analyze the following
gold market news.

News:

{state['news_data']}

Return:

Bullish
Bearish
Neutral

Short explanation.
"""

    response = llm.invoke(
        prompt
    )

    state["analysis"] = (
        response.content
    )

    return state