from graph.workflow import graph


def run_analysis():

    result = graph.invoke(
        {
            "market_data": {},
            "news_data": "",
            "analysis": "",
            "decision": ""
        }
    )

    return result