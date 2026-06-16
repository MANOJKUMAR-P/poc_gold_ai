import streamlit as st

from services.analysis_service import (
    run_analysis
)

st.set_page_config(
    page_title="GoldSense AI"
)

st.title(
    "GoldSense AI"
)

st.write(
    "Daily Gold Buy Suggestion"
)

if st.button(
    "Generate Recommendation"
):

    with st.spinner(
        "Analyzing..."
    ):

        result = run_analysis()

    st.subheader(
        "Market Data"
    )

    st.json(
        result["market_data"]
    )

    st.subheader(
        "News Analysis"
    )

    st.write(
        result["analysis"]
    )

    st.subheader(
        "Recommendation"
    )

    st.write(
        result["decision"]
    )