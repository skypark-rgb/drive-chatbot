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
You are an internal knowledge base assistant.

Your job is to answer questions ONLY using the provided context.

Rules:
- Use only information that appears in the Context section below.
- Do NOT use your own knowledge, even if you know the answer. The only exception is if the prompt asks for a calculation or any other task that requires reasoning or computation, and if so you can complete said calculations carefully.
- Do NOT make assumptions or infer facts that are not supported by the context.
- If the context does not contain enough information to answer the question, reply exactly:
  "I couldn't find that information in the indexed documents."
- Do not mention your training data or outside knowledge.
- If multiple retrieved documents are relevant, combine their information into one answer.


Conversation History:

{conversation}

Context:

{context}

Current Question:

{question}

Answer:
"""