import sys
import os
import re

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import streamlit as st
import pandas as pd
import plotly.express as px

from app.agents.cleaning_agent import CleaningAgent
from app.agents.insight_agent import InsightAgent
from app.agents.sql_fix_agent import SQLFixAgent
from app.agents.chart_agent import ChartAgent

from app.graph.workflow import app_graph

from app.mcp_tools.sql_tool import SQLTool

from app.memory.memory import MemoryManager

from app.utils.sql_validator import (
    validate_sql,
    sanitize_sql
)

from app.utils.context_builder import (
    build_conversation_context
)

from app.utils.execution_logger import ExecutionLogger


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Data Analyst Copilot",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Data Analyst Copilot")


# =========================================
# LOGGER
# =========================================

logger = ExecutionLogger()


# =========================================
# CACHE DATA
# =========================================

@st.cache_data
def load_data(file):

    return pd.read_csv(
        file,
        encoding="latin1"
    )


# =========================================
# SQL AUTO FIXER
# =========================================

def auto_fix_sql(sql_query, df):

    logger.log(
        "AUTO FIX SQL",
        "Starting SQL auto-fix process"
    )

    # =====================================
    # REMOVE COMMENTS
    # =====================================

    sql_query = re.sub(
        r"--.*",
        "",
        sql_query
    )

    # =====================================
    # FIX STRFTIME → STRPTIME
    # =====================================

    sql_query = sql_query.replace(
        "STRFTIME(",
        "STRPTIME("
    )

    # =====================================
    # FIX ORDER DATE FORMAT
    # =====================================

    sql_query = sql_query.replace(
        "%Y-%m-%d",
        "%m/%d/%Y"
    )

    # =====================================
    # FIX INVALID TABLES
    # =====================================

    invalid_tables = [
        "sales_table",
        "products",
        "regions",
        "electronics_products"
    ]

    for table in invalid_tables:

        sql_query = sql_query.replace(
            table,
            "data_table"
        )

    # =====================================
    # REMOVE JOINS
    # =====================================

    sql_query = re.sub(
        r"JOIN .*? ON .*?(?=WHERE|GROUP BY|ORDER BY|LIMIT)",
        "",
        sql_query,
        flags=re.IGNORECASE | re.DOTALL
    )

    # =====================================
    # FIX PRODUCT ID
    # =====================================

    if (
        '"Product ID"' in sql_query
        and '"Product Name"' in df.columns
    ):

        sql_query = sql_query.replace(
            '"Product ID"',
            '"Product Name"'
        )

    # =====================================
    # FIX CUSTOMER ID
    # =====================================

    if (
        '"Customer ID"' in sql_query
        and '"Customer Name"' in df.columns
    ):

        sql_query = sql_query.replace(
            '"Customer ID"',
            '"Customer Name"'
        )

    # =====================================
    # FIX INVALID YEARS
    # =====================================

    if "Order Date" in df.columns:

        try:

            dates = pd.to_datetime(
                df["Order Date"],
                errors="coerce"
            )

            max_year = int(
                dates.dt.year.max()
            )

            sql_query = re.sub(
                r"2023|2024|2025",
                str(max_year),
                sql_query
            )

        except:
            pass

    logger.log(
        "AUTO FIX SQL",
        f"Final Clean SQL:\n{sql_query}"
    )

    return sql_query.strip()


# =========================================
# SIDEBAR
# =========================================

st.sidebar.title("🤖 AI Analyst Copilot")

st.sidebar.info(
    """
AI-powered analytics system using:

- LangGraph
- MCP Tools
- SQL Agent
- Critic Agent
- Visualization Agent
- Insight Agent
- Memory System
- Execution Logger
"""
)

st.sidebar.success(
    "✅ System Status: Running"
)

# =========================================
# MEMORY
# =========================================

memory = MemoryManager()

# =========================================
# EXAMPLE QUESTIONS
# =========================================

st.markdown("""
### Example Questions

- Show top products
- Find sales trends
- Top customers by revenue
- Show profit by category
""")

# =========================================
# FILE UPLOADER
# =========================================

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# =========================================
# MAIN APP
# =========================================

if uploaded_file:

    logger.log(
        "STREAMLIT",
        "CSV File Uploaded"
    )

    # =====================================
    # LOAD DATA
    # =====================================

    df = load_data(uploaded_file)

    cleaner = CleaningAgent()

    df = cleaner.clean(df)

    logger.log(
        "DATA CLEANING",
        f"Dataset Loaded with {len(df)} rows"
    )

    # =====================================
    # KPIs
    # =====================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Rows",
            len(df)
        )

    with col2:

        if "Sales" in df.columns:

            st.metric(
                "Total Sales",
                f"${df['Sales'].sum():,.0f}"
            )

    with col3:

        if "Profit" in df.columns:

            st.metric(
                "Total Profit",
                f"${df['Profit'].sum():,.0f}"
            )

    # =====================================
    # TABS
    # =====================================

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dataset",
        "🤖 Analytics",
        "🧠 Conversation History",
        "📜 Execution Logs"
    ])

    # =====================================
    # DATASET TAB
    # =====================================

    with tab1:

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(20),
            use_container_width=True,
            height=450
        )

    # =====================================
    # ANALYTICS TAB
    # =====================================

    with tab2:

        if "messages" not in st.session_state:

            st.session_state.messages = []

        # =================================
        # DISPLAY CHAT
        # =================================

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):

                st.markdown(
                    message["content"]
                )

        # =================================
        # USER QUESTION
        # =================================

        question = st.chat_input(
            "Ask question about dataset"
        )

        if question:

            logger.log(
                "USER QUESTION",
                question
            )

            st.session_state.messages.append({

                "role": "user",
                "content": question

            })

            with st.chat_message("user"):

                st.markdown(question)

            with st.spinner(
                "Running AI Workflow..."
            ):

                # =============================
                # CONTEXT
                # =============================

                schema_context = ", ".join(
                    df.columns.tolist()
                )

                conversation_context = (
                    build_conversation_context(
                        memory.get_history()
                    )
                )

                state = {

                    "question": question,

                    "columns": df.columns.tolist(),

                    "schema": schema_context,

                    "context": conversation_context

                }

                logger.log(
                    "WORKFLOW",
                    "Invoking LangGraph Workflow"
                )

                # =============================
                # LANGGRAPH
                # =============================

                try:

                    result = app_graph.invoke(
                        state
                    )

                    generated_sql = result.get(
                        "sql_query",
                        ""
                    )

                    logger.log(
                        "LANGGRAPH",
                        f"Generated SQL:\n{generated_sql}"
                    )

                except Exception as e:
                    
                    logger.log(
                        "LANGGRAPH ERROR",
                        str(e)
                    )

                    st.error(
                        f"Workflow Error: {e}"
                    )

                    raise

                # =============================
                # CLEAN SQL
                # =============================

                sql_query = sanitize_sql(
                    generated_sql
                )

                sql_query = auto_fix_sql(
                    sql_query,
                    df
                )

                # =============================
                # SHOW SQL
                # =============================

                st.subheader(
                    "Generated SQL"
                )

                st.code(
                    sql_query,
                    language="sql"
                )

                # =============================
                # SAVE MEMORY
                # =============================

                memory.save(
                    question,
                    sql_query
                )

                logger.log(
                    "MEMORY",
                    "Conversation Saved"
                )

                # =============================
                # EXECUTE SQL
                # =============================

                sql_tool = SQLTool()

                try:

                    validate_sql(
                        sql_query
                    )

                    logger.log(
                        "SQL EXECUTION",
                        "Executing SQL Query"
                    )

                    result_df = sql_tool.run_query(
                        df,
                        sql_query
                    )

                    logger.log(
                        "SQL EXECUTION",
                        f"Rows Returned: {len(result_df)}"
                    )

                except Exception as e:

                    logger.log(
                        "SQL ERROR",
                        str(e)
                    )

                    st.warning(
                        "⚠️ SQL Error Detected. Attempting Auto Fix..."
                    )

                    fixer = SQLFixAgent()

                    fixed_sql = fixer.fix_sql(

                        question,
                        sql_query,
                        str(e),
                        df.columns.tolist()

                    )

                    fixed_sql = auto_fix_sql(
                        fixed_sql,
                        df
                    )

                    st.subheader(
                        "Auto Fixed SQL"
                    )

                    st.code(
                        fixed_sql,
                        language="sql"
                    )

                    try:

                        result_df = sql_tool.run_query(
                            df,
                            fixed_sql
                        )

                        logger.log(
                            "SQL AUTO FIX",
                            "SQL Fix Successful"
                        )

                        st.success(
                            "✅ SQL Auto Fix Successful"
                        )

                    except Exception as final_error:

                        logger.log(
                            "FINAL SQL ERROR",
                            str(final_error)
                        )

                        st.error(
                            f"❌ Fixed SQL Failed: {final_error}"
                        )

                        st.stop()

                # =============================
                # EMPTY RESULT
                # =============================

                if result_df.empty:

                    logger.log(
                        "RESULT",
                        "No results found"
                    )

                    st.warning(
                        "No results found."
                    )

                    st.stop()

                # =============================
                # QUERY RESULTS
                # =============================

                st.subheader(
                    "Query Results"
                )

                st.dataframe(
                    result_df,
                    use_container_width=True
                )

                # =============================
                # VISUALIZATION
                # =============================

                st.subheader(
                    "Visualization"
                )

                numeric_cols = result_df.select_dtypes(
                    include="number"
                ).columns.tolist()

                non_numeric_cols = result_df.select_dtypes(
                    exclude="number"
                ).columns.tolist()

                if len(numeric_cols) > 0:

                    chart_agent = ChartAgent()

                    chart_config = chart_agent.recommend_chart(
                        question,
                        result_df.columns.tolist(),
                        result_df.head(5).to_string()
                    )

                    logger.log(
                        "CHART AGENT",
                        f"Chart Config: {chart_config}"
                    )

                    chart_type = chart_config.get(
                        "chart",
                        "bar"
                    )

                    x_col = chart_config.get(
                        "x_axis",
                        non_numeric_cols[0]
                        if non_numeric_cols
                        else result_df.columns[0]
                    )

                    y_col = chart_config.get(
                        "y_axis",
                        numeric_cols[0]
                    )

                    if chart_type == "line":
                         chart_df = result_df
                    
                    else:
                        chart_df = result_df.head(10)

                    if chart_type == "line":

                        fig = px.line(
                            chart_df,
                            x=x_col,
                            y=y_col,
                            markers=True
                        )

                    elif chart_type == "pie":

                        fig = px.pie(
                            chart_df,
                            names=x_col,
                            values=y_col
                        )

                    elif chart_type == "scatter":

                        fig = px.scatter(
                            chart_df,
                            x=x_col,
                            y=y_col
                        )

                    else:

                        fig = px.bar(
                            chart_df,
                            x=x_col,
                            y=y_col,
                            text=y_col
                        )

                    fig.update_layout(
                        height=550
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                # =============================
                # AI INSIGHTS
                # =============================

                try:

                    insight_agent = InsightAgent()
                    
                    insights = insight_agent.generate_insight(result_df)

                    logger.log(
                        "INSIGHT AGENT",
                        "Insights Generated Successfully"
                    )

                except Exception as e:
                    
                    logger.log(
                         "INSIGHT ERROR",
                         str(e)
                        
                    )

                    insights = f"Insight Error: {str(e)}"


                st.subheader("AI Insights")

                # Force each bullet onto a new line
                if insights:

                    insights = insights.replace("• ", "\n• ")

                    st.markdown(
                        insights,
                        unsafe_allow_html=False
                    )
                else:
                    
                    st.info("No insights generated.")

                st.session_state.messages.append({

                    "role": "assistant",

                    "content": insights

                })

    # =====================================
    # MEMORY TAB
    # =====================================

    with tab3:

        st.subheader(
            "Conversation History"
        )

        history = memory.get_history()

        if history:

            for item in history:

                st.markdown(
                    "### Question"
                )

                st.info(
                    item["question"]
                )

                st.markdown(
                    "### SQL Query"
                )

                st.code(
                    item["sql_query"],
                    language="sql"
                )

                st.divider()

        else:

            st.info(
                "No conversation history yet."
            )

    # =====================================
    # EXECUTION LOG TAB
    # =====================================

    with tab4:

        st.subheader(
            "Execution Logs"
        )

        logs = logger.read_logs()

        if logs:

            st.text_area(
                "Logs",
                logs,
                height=500
            )

        else:

            st.info(
                "No logs available."
            )

        if st.button("Clear Logs"):

            logger.clear_logs()

            st.success(
                "Logs Cleared Successfully"
            )

            st.rerun()