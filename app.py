import streamlit as st
from chief import ask_agent

st.set_page_config(
    page_title="AbuOthman AI",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AbuOthman AI")
st.caption("مساعدك الذكي متعدد الوكلاء")

# ---------- Sidebar ----------

with st.sidebar:
    st.header("AbuOthman AI")

    if st.button("🗑️ محادثة جديدة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### عدد الرسائل")
    st.info(len(st.session_state.get("messages", [])))

# ---------- Chat Memory ----------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Show History ----------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------- Chat Input ----------

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

        placeholder = st.empty()

        with st.spinner("🧠 الوكيل يفكر..."):

            answer = ask_agent(prompt)

        text = ""

        for word in answer.split():
            text += word + " "
            placeholder.markdown(text + "▌")

        placeholder.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )