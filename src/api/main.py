import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)


from fastapi import FastAPI
from pydantic import BaseModel

from chatbot.chatbot_factory import create_chatbot


app = FastAPI(
    title="DriveChatbot API",
    version="0.1.0",
)

chat = create_chatbot()


class AskRequest(BaseModel):
    question: str


class CitationResponse(BaseModel):
    file_id: str
    document_name: str
    chunk_index: int
    text: str


class AskResponse(BaseModel):
    answer: str
    citations: list[CitationResponse]


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    response = chat.ask(request.question)

    return AskResponse(
        answer=response.answer,
        citations=[
            CitationResponse(
                file_id=citation.file_id,
                document_name=citation.document_name,
                chunk_index=citation.chunk_index,
                text=citation.text,
            )
            for citation in response.citations
        ],
    )