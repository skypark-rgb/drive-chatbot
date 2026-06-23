class PromptBuilder:

    def build(self, question: str, search_results):

        context = ""

        for result in search_results:
            payload = result.payload

            context += (
                f"Document: {payload['document_name']}\n"
                f"{payload['text']}\n\n"
            )

        return f"""
You are a helpful assistant.

Answer the user's question using ONLY the provided context.

If the answer is not contained in the context, say you don't know.

Context:

{context}

Question:

{question}

Answer:
"""