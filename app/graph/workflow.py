from langgraph.graph import (
    StateGraph,
    END
)

from graph.state import GoldState

from agents.market_agent import (
    market_agent
)

from agents.news_agent import (
    news_agent
)

from agents.analysis_agent import (
    analysis_agent
)

from agents.decision_agent import (
    decision_agent
)

workflow = StateGraph(
    GoldState
)

workflow.add_node(
    "market",
    market_agent
)

workflow.add_node(
    "news",
    news_agent
)

workflow.add_node(
    "analysis",
    analysis_agent
)

workflow.add_node(
    "decision",
    decision_agent
)

workflow.set_entry_point(
    "market"
)

workflow.add_edge(
    "market",
    "news"
)

workflow.add_edge(
    "news",
    "analysis"
)

workflow.add_edge(
    "analysis",
    "decision"
)

workflow.add_edge(
    "decision",
    END
)

graph = workflow.compile()