import streamlit as st
from chief import ask_agent

st.set_page_config(
    page_title="AbuOthman AI",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AbuOthman AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("اكتب رسالتك...")

if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("يفكر..."):
            answer = ask_agent(prompt)

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )