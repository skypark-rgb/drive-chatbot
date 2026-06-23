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
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=texts,
        )

        return [
            item.embedding
            for item in response.data
        ]
    
    def chat(self, prompt: str):

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )

        return response.output_text