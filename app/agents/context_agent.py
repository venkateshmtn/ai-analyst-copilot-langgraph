from app.utils.llm import llm

class ContextAgent:
    def rewrite_question(
            self,
            question,
            context
    ):

            prompt = f"""
```

You are a BI query understanding agent.

Your task:
Rewrite the user's latest question into a COMPLETE standalone analytics question.

Conversation Context:
{context}

Latest User Question:
{question}

RULES:

* Preserve original meaning
* Use previous context when needed
* Expand vague follow-up questions
* Return ONLY rewritten question

EXAMPLES:

Previous:
Show top products

New:
Only profitable ones

Rewrite:
Show top profitable products by revenue

---

Previous:
Show sales trends

New:
Only for California

Rewrite:
Show sales trends for California
"""


            response = llm.invoke(prompt)

            return response.content.strip()

