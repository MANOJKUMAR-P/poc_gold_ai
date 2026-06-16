from graph.workflow import graph

from database.mongo import (
    predictions
)

def run_analysis():

    result = graph.invoke(
        {
            "market_data": {},
            "news_data": "",
            "analysis": "",
            "decision": ""
        }
    )

    predictions.insert_one(
        result
    )

    return result