class PlannerAgent:

    def create_plan(
        self,
        question,
        route
    ):

        if route == "time_series":

            return {
                "chart": "line",
                "aggregation": "monthly"
            }

        elif route == "summary":

            return {
                "chart": "none",
                "aggregation": "summary"
            }

        return {
            "chart": "bar",
            "aggregation": "groupby"
        }