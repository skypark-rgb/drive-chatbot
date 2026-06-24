
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).parent / "src")
)



import streamlit as st

from chatbot.chatbot_factory import create_chatbot

chat = create_chatbot()

st.title("DriveChatbot")



question = st.chat_input(
    "Ask questions about your Google Drive documents!"
)


## Recurring chat loop/history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and "citations" in message
            and message["citations"]
        ):

            st.markdown("**Sources:**")

            grouped = {}

            for citation in message["citations"]:

                grouped.setdefault(
                    citation.document_name,
                    set()
                ).add(citation.chunk_index)

            for document_name, chunks in grouped.items():

                chunk_list = ", ".join(
                    str(chunk)
                    for chunk in sorted(chunks)
                )

                st.markdown(
                    f"- **{document_name}** "
                    f"(chunks: {chunk_list})"
                )

### end recurring chat loop/history






if question:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(question)

    # Ask chatbot
    response = chat.ask(question)

    answer = response.answer

    # Display assistant message
    with st.chat_message("assistant"):

        st.markdown(answer)

        if response.citations:

            st.markdown("**Sources:**")
       
       
            ### grouped citations by document name and chunk index
            grouped = {}

            for citation in response.citations:

                grouped.setdefault(
                    citation.document_name,
                    set()
                ).add(citation.chunk_index)

            for document_name, chunks in grouped.items():

                chunk_list = ", ".join(
                    str(chunk)
                    for chunk in sorted(chunks)
                )

                st.markdown(
                    f"- **{document_name}** "
                    f"(chunks: {chunk_list})"
                )

    # Save assistant message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "citations": response.citations,
        }
    )