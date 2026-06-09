
from app.utils.llm import llm


class ChartAgent:

    def recommend_chart(
        self,
        question,
        columns,
        sample_data
    ):

        prompt = f"""
You are an expert Data Visualization AI Agent.

Your task:
Select the BEST chart type for the analytics query.

AVAILABLE CHARTS:
- bar
- line
- pie
- scatter

USER QUESTION:
{question}

AVAILABLE COLUMNS:
{columns}

SAMPLE DATA:
{sample_data}

RULES:

1. Use:
   - line → trends/time series
   - pie → distributions
   - scatter → correlations
   - bar → comparisons/rankings

2. Return ONLY valid Python dictionary.

FORMAT:
{{
    "chart": "bar",
    "x_axis": "Category",
    "y_axis": "Sales"
}}

3. No markdown
4. No explanations
"""

        response = llm.invoke(prompt)

        result = response.content.strip()

        result = result.replace(
            "```python",
            ""
        ).replace(
            "```",
            ""
        )

        try:

            chart_config = eval(result)

        except:

            chart_config = {
                "chart": "bar",
                "x_axis": columns[0],
                "y_axis": columns[-1]
            }

        return chart_config