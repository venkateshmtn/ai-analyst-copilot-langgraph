class ExecutionAgent:

    def execute(
        self,
        sql_tool,
        df,
        sql_query
    ):

        return sql_tool.run_query(
            df,
            sql_query
        )