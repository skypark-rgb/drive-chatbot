import tiktoken

from models.text_chunk import TextChunk


class TextChunker:
    def __init__(self,
                 chunk_size=300,
                 overlap=50):

        self.chunk_size = chunk_size
        self.overlap = overlap

        self.encoding = tiktoken.get_encoding("cl100k_base")

    def chunk_document(self, document):

        tokens = self.encoding.encode(document.text)

        chunks = []

        start = 0
        chunk_index = 0

        while start < len(tokens):

            end = start + self.chunk_size

            chunk_tokens = tokens[start:end]

            chunk_text = self.encoding.decode(chunk_tokens)

            chunks.append(
                TextChunk(
                    document_id=document.id,
                    chunk_index=chunk_index,
                    text=chunk_text,
                )
            )

            chunk_index += 1

            start += self.chunk_size - self.overlap

        return chunks