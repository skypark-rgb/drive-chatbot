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

        search_results = self.retriever.retrieve(question)

        prompt = self.prompt_builder.build(
            question=question,
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
    