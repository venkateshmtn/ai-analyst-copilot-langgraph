from app.agents.planner_agent import PlannerAgent
from app.agents.sql_agent import SQLAgent
from app.agents.insight_agent import InsightAgent

planner = PlannerAgent()
sql_agent = SQLAgent()
insight_agent = InsightAgent()

# =========================
# Planner Node
# =========================

def planner_node(state):

    question = state["question"]

    plan = planner.plan(question)

    return {
        **state,
        "plan": plan
    }

# =========================
# SQL Node
# =========================

def sql_node(state):

    question = state["question"]
    columns = state["columns"]

    sql_query = sql_agent.generate_sql(
        question,
        columns
    )

    return {
        **state,
        "sql_query": sql_query
    }

# =========================
# Insight Node
# =========================

def insight_node(state):

    summary = state["summary"]

    insight = insight_agent.generate_insight(
        summary
    )

    return {
        **state,
        "insight": insight
    }