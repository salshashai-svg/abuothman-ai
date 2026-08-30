import os
import time
import tempfile
import streamlit as st

from chief import ask_agent

st.set_page_config(
    page_title="AbuOthman AI",
    page_icon="🤖",
    layout="wide",
)

# ------------------ Session ------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ Sidebar ------------------

with st.sidebar:

    st.title("🤖 AbuOthman AI")

    uploaded_file = st.file_uploader(
        "📎 رفع ملف",
        type=[
            "pdf",
            "docx",
            "txt",
            "csv",
            "xlsx",
            "png",
            "jpg",
            "jpeg",
        ],
    )

    if st.button("🗑️ محادثة جديدة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.metric(
        "عدد الرسائل",
        len(st.session_state.messages),
    )

# ------------------ Save Uploaded File ------------------

saved_file = None

if uploaded_file:

    suffix = os.path.splitext(uploaded_file.name)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as tmp:

        tmp.write(uploaded_file.getbuffer())

        saved_file = tmp.name

    st.sidebar.success(uploaded_file.name)

# ------------------ Header ------------------

st.title("🤖 AbuOthman AI")
st.caption("وكيل ذكي متعدد التخصصات")

# ------------------ History ------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ Input ------------------

prompt = st.chat_input("اكتب رسالتك...")

# ------------------ Conversation ------------------

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

        holder = st.empty()

        with st.spinner("🧠 يفكر..."):

            answer = ask_agent(
                message=prompt,
                uploaded_file=saved_file,
            )

        text = ""

        for word in answer.split():

            text += word + " "

            holder.markdown(text + "▌")

            time.sleep(0.01)

        holder.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )