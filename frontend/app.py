import streamlit as st
import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Must be the first Streamlit command
st.set_page_config(
    page_title="Chatbot V2",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import components after page config
from components.sidebar import render_sidebar
from components.inspector import render_inspector
from utils import process_memory_api, improve_prompt_api, chat_api

def main():
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        
    # Render Sidebar
    sidebar_config = render_sidebar()
    
    chat_col, inspector_col = st.columns([7, 3])
    
    with chat_col:
        st.title("💬 Chat")
        
        if not sidebar_config["backend_healthy"]:
            st.warning("⚠️ Cannot connect to the backend API. Please make sure the FastAPI server is running.")
            st.stop()

        # Display chat messages from history on app rerun
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("What is up?"):
            original_prompt = prompt
            
            if sidebar_config.get("use_improver"):
                with st.spinner("Improving prompt..."):
                    improved_data = improve_prompt_api(prompt)
                    if improved_data:
                        prompt = improved_data["improved_prompt"]
                        st.session_state["last_improvement"] = improved_data
                        
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            
            if sidebar_config.get("use_improver") and "last_improvement" in st.session_state:
                with st.expander("Prompt Improvement Metrics", expanded=False):
                    metrics = st.session_state["last_improvement"].get("improvement_metrics", {})
                    st.write(f"**Original:** {st.session_state['last_improvement']['original_prompt']}")
                    st.write(f"**Latency:** {metrics.get('latency_ms', 0)} ms")
                    st.write(f"**Tokens Added:** {metrics.get('tokens_added', 0)}")

            # Add user message to chat history
            st.session_state["messages"].append({"role": "user", "content": prompt})

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                with st.spinner("Generating response..."):
                    chat_data = chat_api(st.session_state["messages"], sidebar_config["model"])
                    if chat_data:
                        response_text = chat_data["response"]["content"]
                        st.markdown(response_text)
                        st.session_state["last_generation_metrics"] = chat_data["metrics"]
                    else:
                        response_text = "Error communicating with backend."
                        st.error(response_text)
                
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
