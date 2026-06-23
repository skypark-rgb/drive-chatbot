class PromptBuilder:

    def build(self, question: str, search_results, history):

        context = ""

        # for memory of convo
        conversation = ""

        for message in history:

            conversation += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )
        # end for memeory

        for result in search_results:
            payload = result.payload

            context += (
                f"Document: {payload['document_name']}\n"
                f"{payload['text']}\n\n"
            )

        return f"""
You are a helpful assistant.

Use the conversation history and the provided context.

If the answer cannot be determined from the context,
say you don't know.

Conversation History:

{conversation}

Context:

{context}

Current Question:

{question}

Answer:
"""