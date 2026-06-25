import streamlit as st
import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Must be the first Streamlit command
st.set_page_config(
    page_title="KrishGPT",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import components after page config
from components.sidebar import render_sidebar
from components.inspector import render_inspector
from utils import process_memory_api, improve_prompt_api, chat_stream_api

def main():
    # Initialize session state
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
        st.markdown('<div class="gradient-title">✦ KrishGPT</div>', unsafe_allow_html=True)
        
        if not sidebar_config["backend_healthy"]:
            st.warning("⚠️ Cannot connect to the backend API. Please make sure the FastAPI server is running.")
            st.stop()

        # --- Document Management UI ---
        from utils import upload_document_api, get_documents_api, delete_document_api
        
        docs = get_documents_api()
        if docs:
            st.markdown("### 📚 Knowledge Base")
            cols = st.columns(4)
            for i, doc in enumerate(docs):
                with cols[i % 4]:
                    st.markdown(f"""
                    <div style='padding: 10px; border: 1px solid #333; border-radius: 8px; margin-bottom: 10px;'>
                        <strong>📄 {doc.get('filename', 'Unknown')}</strong><br/>
                        <small>Pages: {doc.get('page_count', 0)} | Chunks: {doc.get('chunk_count', 0)}</small><br/>
                        <small style="color: {'#00ff00' if doc.get('embedded') else '#ffaa00'}">
                            {'✓ Embedded' if doc.get('embedded') else '⌛ Pending'}
                        </small>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Delete", key=f"del_{doc.get('document_id')}", use_container_width=True):
                        delete_document_api(doc.get('document_id'))
                        st.rerun()
                        
        with st.expander("➕ Upload New Document"):
            uploaded_file = st.file_uploader("Upload PDF, DOCX, TXT, CSV", type=['pdf', 'docx', 'txt', 'csv'])
            if uploaded_file and st.button("Process Document"):
                with st.spinner("Ingesting and vectorizing..."):
                    upload_document_api(uploaded_file)
                st.rerun()
        
        st.divider()
        # --- End Document Management UI ---

        # Display chat messages from history on app rerun
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("What's on your mind ?"):
            original_prompt = prompt
            
            if sidebar_config.get("use_improver"):
                with st.spinner("Optimizing logic..."):
                    improved_data = improve_prompt_api(prompt)
                    if improved_data:
                        prompt = improved_data["improved_prompt"]
                        st.session_state["last_improvement"] = improved_data
                        
            # Display user message in chat message container
            st.chat_message("user").markdown(original_prompt)
            
            if sidebar_config.get("use_improver") and "last_improvement" in st.session_state:
                with st.expander("⟡ Prompt Optimization", expanded=False):
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
                    search_strategy=sidebar_config.get("search_strategy"),
                    top_k=sidebar_config.get("top_k"),
                    similarity_threshold=sidebar_config.get("similarity_threshold")
                ))
                
            # Add assistant response to chat history
            st.session_state["messages"].append({"role": "assistant", "content": response_text})
            
            # Process memory and update stats
            mem_data = process_memory_api(
                st.session_state["messages"], 
                sidebar_config["memory_window"]
            )
            if mem_data and "stats" in mem_data:
                st.session_state["memory_stats"] = mem_data["stats"]
                st.rerun()

    with inspector_col:
        render_inspector()

if __name__ == "__main__":
    main()
