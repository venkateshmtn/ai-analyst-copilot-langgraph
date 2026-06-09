FORBIDDEN_KEYWORDS = [
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE"
]

def validate_sql(sql_query):

    sql_upper = sql_query.upper()

    for keyword in FORBIDDEN_KEYWORDS:

        if keyword in sql_upper:

            raise ValueError(
                f"Unsafe SQL detected: {keyword}"
            )

    return True

def sanitize_sql(sql):
    replacements = {
        "BETWE0N": "BETWEEN",
        "SELEC ": "SELECT ",
        "GROPU BY": "GROUP BY",
        "ODER BY": "ORDER BY"
    }

    for wrong, correct in replacements.items():
        sql = sql.replace(wrong, correct)

    return sql
