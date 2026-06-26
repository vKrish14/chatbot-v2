import streamlit as st

prompt = st.chat_input("Enter your query or attach a document...", accept_file=True, file_type=['pdf', 'docx', 'txt', 'csv'])

if prompt:
    st.write(type(prompt))
    if hasattr(prompt, "files"):
        st.write("Files:", prompt.files)
    if hasattr(prompt, "text"):
        st.write("Text:", prompt.text)
    
    st.write("Prompt object:", prompt)
