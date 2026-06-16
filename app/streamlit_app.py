import streamlit as st
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import json
from services.analysis_service import run_analysis

# Page config should be set before other Streamlit calls
st.set_page_config(page_title="GoldSense AI", layout="wide")

def get_gold_prices(ticker: str = "GC=F"):
    end = datetime.utcnow()
    start = end - timedelta(days=7)
    try:
        df = yf.download(ticker, start=start, end=end, progress=False, interval="1d")
    except Exception:
        return None
    if df is None or df.empty:
        return None
    prices = df['Close'].dropna()
    if len(prices) < 2:
        return None

    # yfinance may return a Series or a DataFrame (if multiple tickers);
    # handle both cases robustly.
    if isinstance(prices, pd.DataFrame):
        # take the last column (most recent ticker column)
        latest_row = prices.iloc[-1]
        prev_row = prices.iloc[-2]
        latest_price = float(latest_row.iloc[-1])
        prev_price = float(prev_row.iloc[-1])
    else:
        latest_price = float(prices.iloc[-1])
        prev_price = float(prices.iloc[-2])

    latest_date = prices.index[-1]
    return {
        'latest_date': latest_date,
        'latest_price': latest_price,
        'prev_price': prev_price,
    }

CSS = """
<style>
body {background-color: #0f1724;}
.card {background: linear-gradient(180deg, #0b1220 0%, #0f1724 100%); padding:16px; border-radius:10px;}
.decision-buy {border-left: 6px solid #16a34a; padding-left:12px}
.decision-sell {border-left: 6px solid #ef4444; padding-left:12px}
.decision-neutral {border-left: 6px solid #f59e0b; padding-left:12px}
.header-title {color: #f8fafc; font-size:28px; font-weight:700}
.header-sub {color:#94a3b8}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

with st.container():
    col1, _ = st.columns([3,1])
    with col1:
        st.markdown('<div class="header-title">GoldSense AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="header-sub">Daily Gold Buy Suggestion</div>', unsafe_allow_html=True)

with st.spinner("Fetching latest gold prices..."):
    data = get_gold_prices("GC=F")

if not data:
    st.error("Could not fetch gold prices. Ensure `yfinance` is installed and you have network access.")
else:
    latest = data['latest_price']
    prev = data['prev_price']
    change = latest - prev
    pct = (change / prev) * 100 if prev != 0 else 0.0

    left, right = st.columns([2, 1])
    with left:
        st.metric(label="Gold Price (USD/oz)", value=f"${latest:,.2f}", delta=f"{pct:.2f}%")
        st.write(f"**Previous close:** ${prev:,.2f}  ")
        st.write(f"**Change:** ${change:,.2f} ({pct:.2f}%)")

    def render_decision_card(dec: dict) -> str:
        status = dec.get("decision", "N/A").upper()
        conf = dec.get("confidence", 0.0)
        reason = dec.get("reason", "")
        cls = "decision-neutral"
        if status == "BUY":
            cls = "decision-buy"
        elif status == "SELL":
            cls = "decision-sell"

        html = (
            f"<div class=\"card {cls}\">"
            f"<h3 style=\"color:#f8fafc;margin:0\">Decision: {status}</h3>"
            f"<div style=\"color:#cbd5e1;margin-top:6px\"><strong>Confidence:</strong> {conf*100:.0f}%</div>"
            f"<hr style=\"border-color:#1f2937;margin:8px 0\">"
            f"<div style=\"color:#e2e8f0\"><strong>Reason</strong></div>"
            f"<div style=\"color:#cbd5e1;margin-top:6px\">{reason}</div>"
            f"</div>"
        )
        return html

    # right column will display agent decision after analysis runs

with st.spinner("Analyzing..."):
    result = run_analysis()

# Market Data JSON display removed per user request

def _normalize_decision(raw):
    """Return a dict with keys: decision, confidence (float), reason."""
    def _extract_json_substring(s: str):
        # remove common markdown fences and the leading 'JSON' label
        s_clean = s.replace('```', '')
        s_clean = s_clean.replace('`', '')
        s_clean = s_clean.replace('\r\n', '\n')
        # drop any leading non-brace text
        idx = s_clean.find('{')
        if idx == -1:
            return None
        # find matching closing brace by counting
        depth = 0
        start = idx
        for i in range(start, len(s_clean)):
            if s_clean[i] == '{':
                depth += 1
            elif s_clean[i] == '}':
                depth -= 1
                if depth == 0:
                    return s_clean[start:i+1]
        return None

    # If it's already a dict, use it
    if isinstance(raw, dict):
        src = raw
    else:
        src = None
        # try direct JSON load
        try:
            src = json.loads(raw)
        except Exception:
            # try extracting a JSON substring
            try:
                s = str(raw)
                json_sub = _extract_json_substring(s)
                if json_sub:
                    src = json.loads(json_sub)
            except Exception:
                src = None

    if not isinstance(src, dict):
        # fallback: treat raw as plain text decision/reason
        text = str(raw).strip()
        # strip surrounding markdown fences
        if text.startswith('```') and text.endswith('```'):
            text = text.strip('`\n ')
        return {"decision": text, "confidence": 0.0, "reason": text}

    out = {"decision": None, "confidence": 0.0, "reason": ""}
    for k, v in src.items():
        lk = str(k).strip().lower()
        if lk in ("decision", "dec"):
            out["decision"] = v
        elif lk in ("confidence", "conf", "%confidence"):
            try:
                out["confidence"] = float(v)
            except Exception:
                try:
                    out["confidence"] = float(str(v).strip().strip('%')) / 100.0
                except Exception:
                    out["confidence"] = 0.0
        elif lk in ("reason", "explanation", "why"):
            out["reason"] = v

    # normalize confidence to 0-1
    try:
        if out["confidence"] is None:
            out["confidence"] = 0.0
        elif out["confidence"] > 1:
            out["confidence"] = out["confidence"] / 100.0
    except Exception:
        out["confidence"] = 0.0

    if out["decision"] is not None:
        out["decision"] = str(out["decision"]).upper()

    # sanitize reason: strip backticks and excessive whitespace
    if out["reason"] is None:
        out["reason"] = ""
    else:
        out["reason"] = str(out["reason"]).strip().strip('`\n ')

    return out


# Attempt to parse and normalize the agent's decision
dec_raw = result.get("decision", "")
dec_obj = _normalize_decision(dec_raw)

st.subheader("Decision")
st.markdown(render_decision_card(dec_obj), unsafe_allow_html=True)

# end of UI

