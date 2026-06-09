class ValidationAgent:

    def validate(self, sql_query):

        dangerous = [
            "DROP",
            "DELETE",
            "UPDATE",
            "INSERT"
        ]

        sql_upper = sql_query.upper()

        for keyword in dangerous:

            if keyword in sql_upper:
                return False

        return True