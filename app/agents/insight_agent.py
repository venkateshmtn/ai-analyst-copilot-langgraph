import pandas as pd

class InsightAgent:

    def generate_insight(self, result_df):

        if result_df is None or result_df.empty:
            return "No data available."

        try:

            insights = []
            columns = result_df.columns.tolist()

            # =====================================
            # TOP CUSTOMERS
            # =====================================

            if (
                "Customer Name" in columns
                and "Revenue" in columns
            ):

                for idx, row in result_df.head(5).iterrows():

                    insights.append(
                        f"• {row['Customer Name']} ranked #{idx + 1} with revenue of ${row['Revenue']:,.2f}"
                    )

                return "\n\n".join(insights)

            # =====================================
            # TOP PRODUCTS
            # =====================================

            if (
                "Product Name" in columns
                and "Revenue" in columns
            ):

                for idx, row in result_df.head(5).iterrows():

                    insights.append(
                        f"• {row['Product Name']} ranked #{idx + 1} with revenue of ${row['Revenue']:,.2f}"
                    )

                return "\n\n".join(insights)

            # =====================================
            # MONTHLY SALES TREND
            # =====================================

            if (
                "Month" in columns
                and "Revenue" in columns
            ):
                
                highest = result_df.loc[
                    result_df["Revenue"].idxmax()
                ]

                lowest = result_df.loc[
                    result_df["Revenue"].idxmin()
                ]

                avg_revenue = result_df["Revenue"].mean()

                highest_month = pd.to_datetime(
                    highest["Month"]
                ).strftime("%b %Y")

                lowest_month = pd.to_datetime(
                    lowest["Month"]
                ).strftime("%b %Y")

                insights.append(
                    f"• Highest monthly revenue was recorded in {highest_month} at ${highest['Revenue']:,.2f}"
                )

                insights.append(
                    f"• Lowest monthly revenue was recorded in {lowest_month} at ${lowest['Revenue']:,.2f}"
                )

                insights.append(
                    f"• Average monthly revenue was ${avg_revenue:,.2f}"
                )

                insights.append(
                    f"• Revenue data covers {len(result_df)} monthly periods."
                )

                return "\n\n".join(insights)

            # =====================================
            # PROFIT ANALYSIS
            # =====================================

            if "Profit" in columns:

                dimension_col = columns[0]

                for _, row in result_df.head(5).iterrows():

                    insights.append(
                        f"• {row[dimension_col]} recorded profit of ${row['Profit']:,.2f}"
                    )

                return "\n\n".join(insights)

            # =====================================
            # SALES ANALYSIS
            # =====================================

            if "Sales" in columns:

                dimension_col = columns[0]

                for _, row in result_df.head(5).iterrows():

                    insights.append(
                        f"• {row[dimension_col]} recorded sales of ${row['Sales']:,.2f}"
                    )

                return "\n\n".join(insights)

            # =====================================
            # REVENUE ANALYSIS
            # =====================================

            if "Revenue" in columns:

                dimension_col = columns[0]

                for _, row in result_df.head(5).iterrows():

                    insights.append(
                        f"• {row[dimension_col]} recorded revenue of ${row['Revenue']:,.2f}"
                    )

                return "\n\n".join(insights)

            # =====================================
            # GENERIC FALLBACK
            # =====================================

            for _, row in result_df.head(5).iterrows():

                values = [str(v) for v in row.tolist()]

                insights.append(
                    "• " + " | ".join(values)
                )

            return "\n\n".join(insights)

        except Exception as e:

            return f"Insight generation failed: {str(e)}"