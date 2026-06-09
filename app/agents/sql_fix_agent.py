from app.utils.llm import llm


class SQLFixAgent:

    def fix_sql(
        self,
        question,
        failed_sql,
        error_message,
        columns
    ):

        prompt = f"""
You are an expert DuckDB SQL fixer.

User Question:
{question}

Failed SQL:
{failed_sql}

SQL Error:
{error_message}

Available Columns:
{columns}

Rules:

* Return ONLY SQL
* Use DuckDB syntax
* Preserve original intent
* NEVER generate invalid SQL keywords
* If using STRPTIME(), dates MUST use YYYY-MM-DD format
* Always use valid BETWEEN syntax
* Never invent columns
* Always wrap columns with spaces using double quotes


Correct SQL:
"""

        response = llm.invoke(prompt)

        fixed_sql = response.content.strip()

        fixed_sql = fixed_sql.replace(
            "```sql",
            ""
        ).replace(
            "```",
            ""
        )

        return fixed_sql.strip()