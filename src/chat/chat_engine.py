from chat.prompt_builder import PromptBuilder
from chat.chat_response import ChatResponse
from chat.citation import Citation


class ChatEngine:

    def __init__(self, retriever, embedding_client):
        self.retriever = retriever
        self.embedding_client = embedding_client
        self.prompt_builder = PromptBuilder()

    def ask(self, question: str):

        search_results = self.retriever.retrieve(question)

        ###### temp debugging part
        print()
        print("Retrieved chunks:")

        for result in search_results:
            print(
                result.payload["document_name"],
                result.payload["chunk_index"],
                round(result.score, 3)
            )
        ###### end temp deubugging


        prompt = self.prompt_builder.build(
            question,
            search_results,
        )

        answer = self.embedding_client.chat(prompt)





        citations = []

        seen = set()

        for result in search_results:

            key = (
                result.payload["document_name"],
                result.payload["chunk_index"],
            )

            if key in seen:
                continue

            seen.add(key)

            citations.append(
                Citation(
                    document_name=result.payload["document_name"],
                    chunk_index=result.payload["chunk_index"],
                )
            )



        return ChatResponse(answer=answer, citations=citations)
    