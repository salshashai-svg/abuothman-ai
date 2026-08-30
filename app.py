import os
import tempfile
import time
from pathlib import Path

import streamlit as st
from PIL import Image

from chief import ask_agent, extract_document_content

# Configure page
st.set_page_config(
    page_title="AbuOthman AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern interface
st.markdown(
    """
    <style>
    /* Main container */
    .main {
        padding-top: 1rem;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
    }
    
    .assistant-message {
        background-color: #f5f5f5;
    }
    
    /* Sidebar styling */
    .sidebar-content {
        padding: 1.5rem;
    }
    
    /* File uploader */
    .file-uploader {
        border: 2px dashed #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================== Session State ====================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}

if "current_document" not in st.session_state:
    st.session_state.current_document = None

# ==================== Sidebar ====================

with st.sidebar:
    st.title("🤖 AbuOthman AI")
    st.caption("وكيل ذكي متعدد التخصصات")
    
    st.divider()
    
    # New Chat button
    if st.button("➕ محادثة جديدة", use_container_width=True, key="new_chat_btn"):
        st.session_state.messages = []
        st.session_state.uploaded_files = {}
        st.session_state.current_document = None
        st.rerun()
    
    st.divider()
    
    # File Upload Section
    st.subheader("📎 رفع ملفات")
    
    uploaded_file = st.file_uploader(
        "اختر ملفًا للتحليل",
        type=[
            "pdf",
            "doc",
            "docx",
            "txt",
            "csv",
            "xls",
            "xlsx",
            "png",
            "jpg",
            "jpeg",
        ],
        key="file_uploader",
    )
    
    if uploaded_file is not None:
        # Save and process uploaded file
        suffix = os.path.splitext(uploaded_file.name)[1].lower() or ".txt"
        
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:
            tmp.write(uploaded_file.getbuffer())
            saved_file = tmp.name
        
        file_content = extract_document_content(saved_file)
        
        # Store file info
        st.session_state.uploaded_files[uploaded_file.name] = {
            "path": saved_file,
            "content": file_content,
            "size": len(file_content),
        }
        st.session_state.current_document = uploaded_file.name
        
        # Display success message
        st.success(f"✅ {uploaded_file.name}")
        st.caption(f"الحجم: {len(file_content.strip())} حرف")
        
        # Show file preview for images
        if suffix.lower() in [".png", ".jpg", ".jpeg"]:
            try:
                img = Image.open(saved_file)
                st.image(img, caption=uploaded_file.name, use_column_width=True)
            except Exception:
                pass
    
    st.divider()
    
    # Chat statistics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("الرسائل", len(st.session_state.messages))
    with col2:
        st.metric("الملفات", len(st.session_state.uploaded_files))
    
    st.divider()
    
    # Current document info
    if st.session_state.current_document:
        st.info(f"📄 الملف الحالي: {st.session_state.current_document}")

# ==================== Main Chat Area ====================

# Header
st.title("🤖 AbuOthman AI")
st.caption("مساعدك الذكي في التحليل والمعالجة")

st.divider()

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("اكتب رسالتك هنا... 💬", key="chat_input")

# ==================== Message Processing ====================

if prompt:
    # Add user message to history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process and display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("🧠 جاري المعالجة..."):
            # Prepare message with document context if available
            final_prompt = prompt
            
            if st.session_state.current_document:
                doc_info = st.session_state.uploaded_files.get(st.session_state.current_document)
                if doc_info:
                    final_prompt = (
                        f"{prompt}\n\n"
                        f"FILE_PATH={doc_info['path']}\n"
                        f"FILE_NAME={st.session_state.current_document}\n\n"
                        f"DOCUMENT_CONTENT:\n{doc_info['content']}"
                    )
            
            # Get response from agent
            answer = ask_agent(
                message=final_prompt,
                uploaded_file=st.session_state.current_document,
            )
        
        # Display response with typing animation
        text = ""
        for word in answer.split():
            text += word + " "
            message_placeholder.markdown(text + "▌")
            time.sleep(0.01)
        
        message_placeholder.markdown(answer)
    
    # Add assistant message to history
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )