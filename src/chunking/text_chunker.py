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
                    file_id=document.file_id,
                    document_name=document.name,
                    chunk_index=chunk_index,
                    text=chunk_text,
                )
            )

            chunk_index += 1

            start += self.chunk_size - self.overlap

        return chunks

    def chunk_documents(self, documents):
        all_chunks = []

        for document in documents:
            all_chunks.extend(self.chunk_document(document))

        return all_chunks