import re


class SQLReviewAgent:

    def review_sql(
        self,
        question,
        sql_query,
        columns
    ):

        question_lower = question.lower()

        # ====================================
        # REMOVE MARKDOWN
        # ====================================

        sql_query = (
            sql_query
            .replace("```sql", "")
            .replace("```", "")
            .strip()
        )

        # ====================================
        # REMOVE COMMENTS
        # ====================================

        sql_query = re.sub(
            r'--.*',
            '',
            sql_query
        )

        # ====================================
        # FIX DATE FUNCTIONS
        # ====================================

        sql_query = sql_query.replace(
            "STRFTIME(",
            "STRPTIME("
        )

        sql_query = sql_query.replace(
            "%Y-%m-%d",
            "%m/%d/%Y"
        )

        # ====================================
        # FIX CUSTOMER QUERIES
        # ====================================

        if (
            "customer" in question_lower
            and '"Product Name"' in sql_query
            and '"Customer Name"' in columns
        ):

            sql_query = sql_query.replace(
                '"Product Name"',
                '"Customer Name"'
            )

        # ====================================
        # FIX PRODUCT QUERIES
        # ====================================

        if (
            "product" in question_lower
            and '"Customer Name"' in sql_query
            and '"Product Name"' in columns
        ):

            sql_query = sql_query.replace(
                '"Customer Name"',
                '"Product Name"'
            )

        # ====================================
        # FIX IDS
        # ====================================

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

        return sql_query.strip()