import requests

from config import NEWS_API_KEY

def news_agent(state):

    url = (
        "https://newsapi.org/v2/everything?"
        "q=gold OR inflation OR federal reserve"
        f"&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)

    articles = response.json().get(
        "articles",
        []
    )

    news = []

    for article in articles[:5]:

        news.append(
            article.get(
                "title",
                ""
            )
        )

    state["news_data"] = "\n".join(news)

    return state