from dataclasses import dataclass


@dataclass
class ChatResponse:
    answer: str
    citations: list