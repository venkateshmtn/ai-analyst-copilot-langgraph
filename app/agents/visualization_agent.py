

class VisualizationAgent:

    def suggest_chart(self, question):

        question = question.lower()

        if "trend" in question:
            return "line"

        return "bar"