from openai import OpenAI


class EmbeddingClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

        self.model = "text-embedding-3-small"

    def embed_text(self, text: str):

        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding
    

    def embed_texts(self, texts: list[str]):
        all_embeddings = []

        batch_size = 100

        for start_index in range(0, len(texts), batch_size):
            batch = texts[start_index:start_index + batch_size]

            response = self.client.embeddings.create(
                model=self.model,
                input=batch,
            )

            batch_embeddings = [
                item.embedding
                for item in response.data
            ]

            all_embeddings.extend(batch_embeddings)

            print(
                f"✓ Embedded {min(start_index + batch_size, len(texts))} "
                f"of {len(texts)} chunks"
            )

        return all_embeddings


    def chat(self, prompt: str):

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )

        return response.output_text