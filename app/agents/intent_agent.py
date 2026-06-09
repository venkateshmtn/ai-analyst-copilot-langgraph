from app.utils.llm import llm
from app.utils.execution_logger import ExecutionLogger

import json

logger = ExecutionLogger()


class IntentAgent:

    def extract_intent(
        self,
        question,
        columns
    ):

        logger.log(
            "INTENT AGENT",
            f"Extracting intent for: {question}"
        )

        q = question.lower()

        # =====================================
        # CUSTOMER DETECTION
        # =====================================

        if "customer" in q or "customers" in q:

            intent = {
                "entity": "customer",
                "metric": "Sales",
                "operation": "top_n",
                "limit": 10
            }

            logger.log(
                "INTENT AGENT",
                f"Intent Extracted: {intent}"
            )

            return intent

        # =====================================
        # PRODUCT DETECTION
        # =====================================

        if "product" in q or "products" in q:

            intent = {
                "entity": "product",
                "metric": "Sales",
                "operation": "top_n",
                "limit": 10
            }

            logger.log(
                "INTENT AGENT",
                f"Intent Extracted: {intent}"
            )

            return intent

        # =====================================
        # CATEGORY DETECTION
        # =====================================

        if "category" in q:

            intent = {
                "entity": "category",
                "metric": "Sales",
                "operation": "aggregation"
            }

            logger.log(
                "INTENT AGENT",
                f"Intent Extracted: {intent}"
            )

            return intent

        # =====================================
        # TREND DETECTION
        # =====================================

        if (
            "trend" in q
            or "over time" in q
            or "monthly" in q
            or "month" in q
        ):

            intent = {
                "entity": "date",
                "dimension": "Order Date",
                "metric": "Sales",
                "operation": "trend"
            }

            logger.log(
                "INTENT AGENT",
                f"Intent Extracted: {intent}"
            )

            return intent

        # =====================================
        # LLM FALLBACK
        # =====================================

        prompt = f"""
Return ONLY JSON.

Available Columns:
{columns}

Question:
{question}

Example:

{{
    "entity":"customer",
    "metric":"Sales",
    "operation":"top_n",
    "limit":10
}}
"""

        try:

            response = llm.invoke(prompt)

            content = (
                response.content
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            intent = json.loads(content)

            logger.log(
                "INTENT AGENT",
                f"Intent Extracted: {intent}"
            )

            return intent

        except Exception as e:

            logger.log(
                "INTENT AGENT ERROR",
                str(e)
            )

            return {
                "entity": "product",
                "metric": "Sales",
                "operation": "top_n",
                "limit": 10
            }