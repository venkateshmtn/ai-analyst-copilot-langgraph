from app.utils.llm import llm

response = llm.invoke("Explain sales analysis")

print(response.content)