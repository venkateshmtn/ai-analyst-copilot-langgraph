from app.utils.execution_logger import ExecutionLogger


logger = ExecutionLogger()


class CriticAgent:

    def review_sql(
        self,
        question,
        sql_query,
        columns
    ):

        logger.log(
            "CRITIC AGENT",
            f"Reviewing SQL:\n{sql_query}"
        )

        # =====================================
        # REMOVE MARKDOWN
        # =====================================

        sql_query = (
            sql_query
            .replace("```sql", "")
            .replace("```", "")
            .strip()
        )

        # =====================================
        # FIX DATE FUNCTIONS
        # =====================================

        sql_query = sql_query.replace(
            "STRFTIME(",
            "STRPTIME("
        )

        # =====================================
        # FIX COLUMN NAMES
        # =====================================

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

        # =====================================
        # FIX TABLE NAME
        # =====================================

        sql_query = sql_query.replace(
            "sales_table",
            "data_table"
        )

        # =====================================
        # REMOVE INVALID JOINS
        # =====================================

        forbidden_words = [
            " JOIN ",
            " LEFT JOIN ",
            " RIGHT JOIN ",
            " INNER JOIN ",
            " OUTER JOIN "
        ]

        upper_sql = sql_query.upper()

        for word in forbidden_words:

            if word in upper_sql:

                logger.log(
                    "CRITIC AGENT",
                    "JOIN detected, preserving intent"
                )

                q = question.lower()

                if "customer" in q:

                    return """
SELECT
    "Customer Name",
    SUM("Sales") AS Revenue
FROM data_table
GROUP BY "Customer Name"
ORDER BY Revenue DESC
LIMIT 10
""".strip()

                elif "product" in q:

                    return """
SELECT
    "Product Name",
    SUM("Sales") AS Revenue
FROM data_table
GROUP BY "Product Name"
ORDER BY Revenue DESC
LIMIT 10
""".strip()

        logger.log(
            "CRITIC AGENT",
            f"Final SQL:\n{sql_query}"
        )

        return sql_query.strip()