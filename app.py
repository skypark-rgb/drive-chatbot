# import streamlit as st

# st.title("DriveChatbot")

# question = st.text_input(
#     "Ask a question about your documents"
# )

# if question:
#     st.write("You asked:")
#     st.write(question)
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).parent / "src")
)



import streamlit as st

from chatbot.chatbot_factory import create_chatbot

chat = create_chatbot()

st.title("DriveChatbot")

question = st.text_input(
    "Ask a question"
)

if question:

    response = chat.ask(question)

    st.write(response.answer)

    st.subheader("Sources")

    for citation in response.citations:
        st.write(
            f"{citation.document_name} "
            f"(chunk {citation.chunk_index})"
        )