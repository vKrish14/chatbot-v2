import streamlit as st
import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Must be the first Streamlit command
st.set_page_config(
    page_title="KrishGPT",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import components after page config
from components.sidebar import render_sidebar
from components.inspector import render_inspector
from utils import process_memory_api, improve_prompt_api, chat_stream_api
import utils
import importlib
importlib.reload(utils)
from utils import upload_document_api, get_documents_api, delete_document_api

def main():
    import uuid
    # Initialize session state
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
        
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        
    # Load CSS
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
    # Render Sidebar
    sidebar_config = render_sidebar()
    st.session_state["sidebar_config"] = sidebar_config
    
    chat_col, inspector_col = st.columns([7, 3])
    
    with chat_col:
        st.markdown('<div class="gradient-title">KrishGPT</div>', unsafe_allow_html=True)
        
        if not sidebar_config["backend_healthy"]:
            st.error("Cannot connect to the backend API. Please ensure the server is running.")
            st.stop()

        # --- Document Management UI ---
        from utils import upload_document_api, get_documents_api, delete_document_api
        
        docs = get_documents_api(session_id=st.session_state["session_id"])
        if docs:
            st.markdown("### Knowledge Base")
            cols = st.columns(4)
            for i, doc in enumerate(docs):
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="chunk-card" style="margin-bottom: 0px;">
                        <div style="font-weight: 600; margin-bottom: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{doc.get('filename', 'Unknown')}</div>
                        <div class="meta">Pages: {doc.get('page_count', 0)} | Chunks: {doc.get('chunk_count', 0)}</div>
                        <div style="font-size: 0.8rem; color: {'#00c6ff' if doc.get('embedded') else '#f5a623'}">
                            {'Active' if doc.get('embedded') else 'Pending'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Delete", key=f"del_{doc.get('document_id')}", use_container_width=True):
                        delete_document_api(doc.get('document_id'), session_id=st.session_state["session_id"])
                        st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
                        
        st.divider()
        # --- End Document Management UI ---

        # Display chat messages from history on app rerun
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("Enter your query or attach a document...", accept_file=True, file_type=['pdf', 'docx', 'txt', 'csv']):
            
            # 1. Handle File Upload if present
            if hasattr(prompt, "files") and prompt.files:
                uploaded_file = prompt.files[0]
                with st.chat_message("assistant"):
                    with st.spinner(f"Ingesting {uploaded_file.name} to the vector store..."):
                        upload_document_api(uploaded_file, session_id=st.session_state["session_id"])
                    st.success(f"Successfully ingested {uploaded_file.name}!")
            
            # 2. Handle Text Input
            original_prompt = prompt.text if (hasattr(prompt, "text") and prompt.text) else "Please analyze the uploaded document."
            
            if sidebar_config.get("use_improver"):
                with st.spinner("Optimizing logic..."):
                    improved_data = improve_prompt_api(prompt)
                    if improved_data:
                        prompt = improved_data["improved_prompt"]
                        st.session_state["last_improvement"] = improved_data
                        
            # Display user message in chat message container
            st.chat_message("user").markdown(original_prompt)
            
            if sidebar_config.get("use_improver") and "last_improvement" in st.session_state:
                with st.expander("Prompt Optimization Logs", expanded=False):
                    metrics = st.session_state["last_improvement"].get("improvement_metrics", {})
                    st.write(f"**Original:** {st.session_state['last_improvement']['original_prompt']}")
                    st.write(f"**Latency:** {metrics.get('latency_ms', 0)} ms")
                    st.write(f"**Tokens Added:** {metrics.get('tokens_added', 0)}")

            # Add user message to chat history
            st.session_state["messages"].append({"role": "user", "content": original_prompt})

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                response_text = st.write_stream(chat_stream_api(
                    st.session_state["messages"], 
                    sidebar_config["model"],
                    session_id=st.session_state["session_id"],
                    search_strategy=sidebar_config.get("search_strategy"),
                    top_k=sidebar_config.get("top_k"),
                    similarity_threshold=sidebar_config.get("similarity_threshold")
                ))
                
            # Add assistant response to chat history
            st.session_state["messages"].append({"role": "assistant", "content": response_text})
            
            # Process memory and update stats
            mem_data = process_memory_api(
                st.session_state["messages"], 
                sidebar_config["memory_window"],
                session_id=st.session_state["session_id"]
            )
            if mem_data and "stats" in mem_data:
                st.session_state["memory_stats"] = mem_data["stats"]
                st.rerun()

    with inspector_col:
        render_inspector()

if __name__ == "__main__":
    main()
