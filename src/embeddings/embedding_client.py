from openai import OpenAI


class EmbeddingClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

        