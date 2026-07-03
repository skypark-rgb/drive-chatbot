from chat.prompt_builder import PromptBuilder
from chat.chat_response import ChatResponse
from chat.citation import Citation


class ChatEngine:

    def __init__(self, retriever, embedding_client):
        self.retriever = retriever
        self.embedding_client = embedding_client
        self.prompt_builder = PromptBuilder()

        # For remembering convos
        self.history = []

    def ask(self, question: str):

        standalone_question = self.rewrite_question(question)

        print()
        print("Original question:", question)
        print("Standalone question:", standalone_question)
        print()

        search_results = self.retriever.retrieve(standalone_question)

        prompt = self.prompt_builder.build(
            question=standalone_question,
            search_results=search_results,
            history=self.history,
        )

        answer = self.embedding_client.chat(prompt)

        # not totally sure where to put this
        self.history.append(
            {
                "role": "user",
                "content": question,
            }
        )

        self.history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )
        # end not sure where to put this


        citations = []

        seen = set()

        for result in search_results:

            key = (
                result.payload["file_id"],
                result.payload["chunk_index"],
            )

            if key in seen:
                continue

            seen.add(key)

            citations.append(
                Citation(
                    file_id=result.payload["file_id"],
                    document_name=result.payload["document_name"],
                    chunk_index=result.payload["chunk_index"],
                    text=result.payload["text"],
                )
            )



        return ChatResponse(answer=answer, citations=citations)

    def rewrite_question(self, question: str) -> str:
        if not self.history:
            return question

        history_text = ""

        for message in self.history[-6:]:
            history_text += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        prompt = f"""
    You rewrite follow-up questions for a retrieval system.

    Use the conversation history to replace pronouns and vague references.

    Important:
    - "his", "he", "him", "that person", or "the person" should refer to the main person discussed in the previous question/answer.
    - Return only the rewritten standalone question.
    - Do not answer the question.
    - Do not explain.

    Conversation History:
    {history_text}

    Current Question:
    {question}

    Rewritten standalone question:
    """

        rewritten_question = self.embedding_client.chat(prompt).strip()

        if not rewritten_question:
            return question

        return rewritten_question
    