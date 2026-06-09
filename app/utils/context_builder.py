def build_conversation_context(history):
    
    if not history:
        return ""

    context = []

    for item in history[-3:]:
        context.append(
            f"""
```

Previous Question:
{item['question']}

Previous SQL:
{item['sql_query']}
"""
)

        return "\n".join(context)

