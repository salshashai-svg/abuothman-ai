🤖",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("🤖 AbuOthman AI")

    uploaded_file = st.file_uploader(
        "📎 رفع ملف",
        type=["pdf", "docx", "txt", "xlsx", "csv", "png", "jpg", "jpeg"],
    )

    if st.button("🗑️ محادثة جديدة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.metric("عدد الرسائل", len(st.session_state.messages))

st.title("🤖 AbuOthman AI")
st.caption("وكيل ذكي متعدد التخصصات")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("اكتب رسالتك...")

if uploaded_file:
    st.success(f"تم رفع الملف: {uploaded_file.name}")

if prompt:

    if uploaded_file:
        prompt += f"\n\nالمستخدم أرفق ملفًا اسمه: {uploaded_file.name}"

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        with st.spinner("🧠 يفكر..."):
            answer = ask_agent(prompt)

        text = ""

        for word in answer.split():
            text += word + " "
            placeholder.markdown(text + "▌")
            time.sleep(0.01)

        placeholder.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )import time
import streamlit as st
from chief import ask_agent

st.set_page_config(
    page_title="AbuOthman AI",
    page_icon="