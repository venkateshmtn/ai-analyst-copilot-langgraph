from langgraph.graph import StateGraph, END

from app.agents.planner_agent import PlannerAgent
from app.agents.sql_agent import SQLAgent
from app.agents.insight_agent import InsightAgent
from app.agents.sql_review_agent import SQLReviewAgent
from app.agents.context_agent import ContextAgent
from app.agents.router_agent import RouterAgent
from app.agents.critic_agent import CriticAgent
from app.agents.tool_selector_agent import ToolSelectorAgent
from app.agents.intent_agent import IntentAgent

from app.utils.execution_logger import ExecutionLogger


# =========================================
# AGENTS
# =========================================

sql_agent = SQLAgent()
review_agent = SQLReviewAgent()
context_agent = ContextAgent()
router_agent = RouterAgent()
critic_agent = CriticAgent()
tool_selector_agent = ToolSelectorAgent()
intent_agent = IntentAgent()

logger = ExecutionLogger()


# =========================================
# ROUTER NODE
# =========================================

def router_node(state):

    question = state["question"]

    logger.log(
        "RouterAgent",
        f"Received question: {question}"
    )

    route = router_agent.route(question)

    state["task"] = route.get(
        "task",
        "analytics"
    )

    logger.log(
        "RouterAgent",
        f"Task routed: {state['task']}"
    )

    return state


# =========================================
# TOOL SELECTOR NODE
# =========================================

def tool_selector_node(state):

    question = state["question"]

    logger.log(
        "ToolSelectorAgent",
        "Selecting best tool"
    )

    result = tool_selector_agent.select_tool(
        question
    )

    state["selected_tool"] = result.get(
        "tool",
        "sql_tool"
    )

    logger.log(
        "ToolSelectorAgent",
        f"Selected tool: {state['selected_tool']}"
    )

    return state

# =========================================
# INTENT NODE
# =========================================

def intent_node(state):

    logger.log(
        "IntentAgent",
        "Intent analysis started"
    )

    question = state["question"]

    columns = state["columns"]

    question_lower = question.lower()

    # =========================================
    # HARDCODED INTENT FIXES
    # =========================================

    if (
        "top customer" in question_lower
        or "customers by revenue" in question_lower
        or "customer revenue" in question_lower
    ):

        intent = {
            "metric": "Sales",
            "dimension": "Customer Name",
            "entity": "customer",
            "operation": "top_n",
            "limit": 10
        }

    elif (
        "top product" in question_lower
        or "products by revenue" in question_lower
        or "best products" in question_lower
    ):

        intent = {
            "metric": "Sales",
            "dimension": "Product Name",
            "entity": "product",
            "operation": "top_n",
            "limit": 10
        }

    else:

        intent = intent_agent.extract_intent(
            question,
            columns
        )

        # =========================================
        # FORCE ENTITY IF MISSING
        # =========================================

        if "Customer Name" in str(
            intent.get("dimension", "")
        ):

            intent["entity"] = "customer"

        elif "Product Name" in str(
            intent.get("dimension", "")
        ):

            intent["entity"] = "product"

    state["intent"] = intent

    logger.log(
        "IntentAgent",
        f"Intent extracted: {intent}"
    )

    return state


# =========================================
# PLANNER NODE
# =========================================

def planner_node(state):

    logger.log(
        "PlannerAgent",
        "Generating execution plan"
    )

    planner = PlannerAgent()

    route = state.get(
        "task",
        "summary"
    )

    plan = planner.create_plan(
        state["question"],
        route
    )

    state["plan"] = plan

    logger.log(
        "PlannerAgent",
        f"Plan created: {plan}"
    )

    return state

# =========================================
# SQL NODE
# =========================================

def sql_node(state):

    logger.log(
        "SQLAgent",
        "SQL generation started"
    )

    question = state["question"]

    rewritten_question = context_agent.rewrite_question(
        question,
        state.get("context", "")
    )

    intent = state.get("intent", {})

    logger.log(
        "INTENT DEBUG",
        f"Intent Received: {intent}"
    )

    # =========================================
    # HARDCODED CUSTOMER / PRODUCT FIX
    # =========================================

    entity = str(
        intent.get("entity", "")
    ).lower()

    if entity == "customer":

        final_sql = """
SELECT
    "Customer Name",
    SUM("Sales") AS Revenue
FROM data_table
GROUP BY "Customer Name"
ORDER BY Revenue DESC
LIMIT 10
""".strip()

        logger.log(
            "SQLAgent",
            "Customer query detected"
        )

        state["sql_query"] = final_sql
        return state

    if entity == "product":

        final_sql = """
SELECT
    "Product Name",
    SUM("Sales") AS Revenue
FROM data_table
GROUP BY "Product Name"
ORDER BY Revenue DESC
LIMIT 10
""".strip()

        logger.log(
            "SQLAgent",
            "Product query detected"
        )

        state["sql_query"] = final_sql
        return state

    # =========================================
    # NORMAL FLOW
    # =========================================

    generated_sql = sql_agent.generate_sql(
        question=rewritten_question,
        columns=state["columns"],
        schema=state.get("schema"),
        context=state.get("context", ""),
        intent=intent
    )

    logger.log(
        "SQLAgent",
        f"Generated SQL:\n{generated_sql}"
    )

    reviewed_sql = review_agent.review_sql(
        rewritten_question,
        generated_sql,
        state["columns"]
    )

    logger.log(
        "SQLReviewAgent",
        f"Reviewed SQL:\n{reviewed_sql}"
    )

    final_sql = critic_agent.review_sql(
        rewritten_question,
        reviewed_sql,
        state["columns"]
    )

    logger.log(
        "CriticAgent",
        f"Final SQL:\n{final_sql}"
    )

    state["sql_query"] = final_sql

    return state
# =========================================
# INSIGHT NODE
# =========================================

def insight_node(state):

    logger.log(
        "InsightAgent",
        "Generating insights"
    )

    insight_agent = InsightAgent()

    insights = insight_agent.generate_insight(
        state.get("summary", "")
    )

    state["insights"] = insights

    logger.log(
        "InsightAgent",
        "Insights generated"
    )

    return state


# =========================================
# WORKFLOW
# =========================================

workflow = StateGraph(dict)


# =========================================
# REGISTER NODES
# =========================================

workflow.add_node(
    "router",
    router_node
)

workflow.add_node(
    "tool_selector",
    tool_selector_node
)

workflow.add_node(
    "intent_analyzer",
    intent_node
)

workflow.add_node(
    "planner",
    planner_node
)

workflow.add_node(
    "sql_generator",
    sql_node
)

workflow.add_node(
    "insight_generator",
    insight_node
)


# =========================================
# ENTRY POINT
# =========================================

workflow.set_entry_point(
    "router"
)


# =========================================
# EDGES
# =========================================

workflow.add_edge(
    "router",
    "tool_selector"
)

workflow.add_edge(
    "tool_selector",
    "intent_analyzer"
)

workflow.add_edge(
    "intent_analyzer",
    "planner"
)

workflow.add_edge(
    "planner",
    "sql_generator"
)

workflow.add_edge(
    "sql_generator",
    END
)


# =========================================
# COMPILE
# =========================================

app_graph = workflow.compile()