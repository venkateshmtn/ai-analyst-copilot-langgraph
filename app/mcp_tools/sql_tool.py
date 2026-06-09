import duckdb

class SQLTool:

    def run_query(self, df, query):

        duckdb.register(
            "data_table",
            df
        )

        result = duckdb.sql(query).df()

        return result