
import plotly.express as px


class ChartTool:

    def create_chart(
        self,
        chart_type,
        df,
        x_col,
        y_col
    ):

        chart_type = chart_type.lower()

        # =====================================
        # LINE CHART
        # =====================================

        if chart_type == "line":

            fig = px.line(
                df,
                x=x_col,
                y=y_col,
                markers=True,
                title=f"{y_col} Trend"
            )

        # =====================================
        # PIE CHART
        # =====================================

        elif chart_type == "pie":

            fig = px.pie(
                df,
                names=x_col,
                values=y_col,
                title=f"{y_col} Distribution"
            )

        # =====================================
        # SCATTER CHART
        # =====================================

        elif chart_type == "scatter":

            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                title=f"{y_col} vs {x_col}"
            )

        # =====================================
        # BAR CHART
        # =====================================

        else:

            fig = px.bar(
                df,
                x=x_col,
                y=y_col,
                text=y_col,
                title=f"{y_col} by {x_col}"
            )

        fig.update_layout(
            height=550
        )

        return fig

