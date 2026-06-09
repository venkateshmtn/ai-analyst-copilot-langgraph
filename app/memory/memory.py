class MemoryManager:

    def __init__(self):

        self.history = []

    # =========================
    # Save Conversation
    # =========================

    def save(self, question, sql_query):

        self.history.append({
            "question": question,
            "sql_query": sql_query
        })

    # =========================
    # Get Memory
    # =========================

    def get_history(self):

        return self.history

    # =========================
    # Clear Memory
    # =========================

    def clear(self):

        self.history = []