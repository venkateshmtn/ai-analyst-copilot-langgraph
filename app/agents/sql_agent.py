from app.utils.llm import llm
from app.utils.execution_logger import ExecutionLogger


class SQLAgent:

    def generate_sql(
        self,
        question,
        columns,
        schema=None,
        context=None,
        intent=None
    ):

        ExecutionLogger.log(
            "SQLAgent",
            f"Generating SQL for question: {question}"
        )

        ExecutionLogger.log(
            "SQLAgent",
            f"Intent Received: {intent}"
        )

        # =====================================
        # INTENT-BASED SHORTCUTS
        # =====================================

        if intent:

            entity = str(
                intent.get("entity", "")
            ).lower()

            operation = str(
                intent.get("operation", "")
            ).lower()

            if (
                entity == "customer"
                and operation == "top_n"
            ):

                return """
SELECT
    "Customer Name",
    SUM("Sales") AS Revenue
FROM data_table
GROUP BY "Customer Name"
ORDER BY Revenue DESC
LIMIT 10
""".strip()

            if (
                entity == "product"
                and operation == "top_n"
            ):

                return """
SELECT
    "Product Name",
    SUM("Sales") AS Revenue
FROM data_table
GROUP BY "Product Name"
ORDER BY Revenue DESC
LIMIT 10
""".strip()

        # =====================================
        # QUESTION FALLBACKS
        # =====================================

        question_lower = question.lower()

        if (
            "customer" in question_lower
            or "customers" in question_lower
        ):

            return """
SELECT
    "Customer Name",
    SUM("Sales") AS Revenue
FROM data_table
GROUP BY "Customer Name"
ORDER BY Revenue DESC
LIMIT 10
""".strip()

        if (
            "product" in question_lower
            or "products" in question_lower
        ):

            return """
SELECT
    "Product Name",
    SUM("Sales") AS Revenue
FROM data_table
GROUP BY "Product Name"
ORDER BY Revenue DESC
LIMIT 10
""".strip()
        
        
        # =====================================
        # SALES TREND
        # =====================================

        if (
            "trend" in question_lower
            or "monthly" in question_lower
            or "over time" in question_lower
        ):
            
            return """
SELECT
    DATE_TRUNC(
        'month',
        STRPTIME("Order Date", '%m/%d/%Y')
    ) AS Month,
    SUM("Sales") AS Revenue
FROM data_table
GROUP BY Month
ORDER BY Month
""".strip()

        # =====================================
        # LLM SQL GENERATION
        # =====================================

        prompt = f"""
You are an expert DuckDB SQL generator.

Table:
data_table

Columns:
{columns}

Intent:
{intent}

Schema:
{schema}

Context:
{context}

Question:
{question}

Rules:
1. Use ONLY provided columns.
2. Use ONLY data_table.
3. Never invent columns.
4. Never invent tables.
5. Never use JOIN.
6. Return ONLY SQL.
7. No markdown.
8. No explanation.
"""

        response = llm.invoke(prompt)

        sql_query = (
            response.content
            .replace("```sql", "")
            .replace("```", "")
            .strip()
        )

        sql_query = sql_query.replace(
            "sales_table",
            "data_table"
        )

        sql_query = sql_query.replace(
            "STRFTIME(",
            "STRPTIME("
        )

        if (
            '"Product ID"' in sql_query
            and '"Product Name"' in columns
        ):
            sql_query = sql_query.replace(
                '"Product ID"',
                '"Product Name"'
            )

        if (
            '"Customer ID"' in sql_query
            and '"Customer Name"' in columns
        ):
            sql_query = sql_query.replace(
                '"Customer ID"',
                '"Customer Name"'
            )

        ExecutionLogger.log(
            "SQLAgent",
            f"Generated SQL:\n{sql_query}"
        )

        return sql_query