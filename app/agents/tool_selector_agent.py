
from app.utils.llm import llm


class ToolSelectorAgent:

    def select_tool(
        self,
        question
    ):

        prompt = f"""
You are a Tool Selection Agent.

Available tools:

1. sql_tool
- querying data
- aggregations
- filtering
- trends
- rankings

2. chart_tool
- charts
- graphs
- visualizations

3. stats_tool
- averages
- distributions
- statistics
- correlations

4. forecast_tool
- predictions
- forecasting
- future trends

USER QUESTION:
{question}

Return ONLY one tool name.

Allowed outputs:
sql_tool
chart_tool
stats_tool
forecast_tool
"""

        response = llm.invoke(prompt)

        tool = response.content.strip().lower()

        allowed = [
            "sql_tool",
            "chart_tool",
            "stats_tool",
            "forecast_tool"
        ]

        if tool not in allowed:
            tool = "sql_tool"

        return {
            "tool": tool
        }

