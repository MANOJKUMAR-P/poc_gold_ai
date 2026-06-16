from langchain_groq import ChatGroq

from config import GROQ_API_KEY

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=GROQ_API_KEY
)

def decision_agent(state):

    prompt = f"""
You are a professional
gold analyst.

Market Data:

{state['market_data']}

Analysis:

{state['analysis']}

Generate:

BUY
WAIT
HOLD

Return JSON:

decision
confidence
reason
"""

    response = llm.invoke(
        prompt
    )

    state["decision"] = (
        response.content
    )

    return state