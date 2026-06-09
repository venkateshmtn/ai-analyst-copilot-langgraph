from app.utils.llm import llm


class RouterAgent:

    def route(self, question):

        question_lower = question.lower()

        # =====================================
        # FAST RULE-BASED ROUTING
        # =====================================

        sql_keywords = [
            "top",
            "sales",
            "revenue",
            "profit",
            "customer",
            "customers",
            "product",
            "products",
            "trend",
            "compare",
            "category",
            "region",
            "state",
            "city",
            "quantity"
        ]

        insight_keywords = [
            "insight",
            "summary",
            "summarize",
            "observation",
            "pattern",
            "explain"
        ]

        visualization_keywords = [
            "chart",
            "graph",
            "plot",
            "dashboard",
            "visualize"
        ]

        if any(word in question_lower for word in visualization_keywords):
            return {"task": "visualization"}

        if any(word in question_lower for word in insight_keywords):
            return {"task": "insight"}

        if any(word in question_lower for word in sql_keywords):
            return {"task": "sql"}

        # =====================================
        # LLM FALLBACK
        # =====================================

        prompt = f"""
Classify this analytics question.

Possible outputs:
sql
insight
visualization

Question:
{question}

Return only one word.
"""

        try:

            response = llm.invoke(prompt)

            task = response.content.strip().lower()

            if task not in [
                "sql",
                "insight",
                "visualization"
            ]:
                task = "sql"

            return {
                "task": task
            }

        except Exception:

            return {
                "task": "sql"
            }