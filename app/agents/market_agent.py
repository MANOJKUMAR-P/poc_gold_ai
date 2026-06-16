import yfinance as yf

def market_agent(state):

    gold = yf.Ticker("GC=F")
    dxy = yf.Ticker("DX-Y.NYB")

    gold_hist = gold.history(period="5d")
    dxy_hist = dxy.history(period="5d")

    gold_change = (
        (
            gold_hist["Close"].iloc[-1]
            -
            gold_hist["Close"].iloc[-2]
        )
        /
        gold_hist["Close"].iloc[-2]
    ) * 100

    dxy_change = (
        (
            dxy_hist["Close"].iloc[-1]
            -
            dxy_hist["Close"].iloc[-2]
        )
        /
        dxy_hist["Close"].iloc[-2]
    ) * 100

    state["market_data"] = {
        "gold_change": round(
            float(gold_change), 2
        ),
        "dxy_change": round(
            float(dxy_change), 2
        )
    }

    return state