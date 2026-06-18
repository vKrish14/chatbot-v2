import streamlit as st
from utils import check_backend_health

def render_sidebar():
    with st.sidebar:
        st.title("🤖 Chatbot V2")
        
        # Backend Status
        is_healthy = check_backend_health()
        if is_healthy:
            st.success("Backend: Connected ✅", icon="🟢")
        else:
            st.error("Backend: Disconnected ❌", icon="🔴")
            
        st.divider()
        
        # Model Configuration
        st.header("Settings")
        model = st.selectbox(
            "Select Model",
            [
                "google/gemma-4-31b-it:free",
                "qwen/qwen3-coder:free",
                "openai/gpt-oss-20b:free",
                "nvidia/nemotron-3-super-120b-a12b:free",
                "openai/gpt-4o-mini",
            ]
        )
        st.session_state["model"] = model
        
        # Memory Settings
        st.subheader("Memory")
        memory_window = st.slider("Context Window (messages)", min_value=2, max_value=20, value=10)
        st.session_state["memory_window"] = memory_window
        
        if "memory_stats" in st.session_state and st.session_state["memory_stats"]:
            stats = st.session_state["memory_stats"]
            st.caption("Memory Stats:")
            st.text(f"Total Messages: {stats.get('total_messages', 0)}")
            st.text(f"Retained: {stats.get('retained_messages', 0)}")
            st.text(f"Est. Tokens: {stats.get('estimated_tokens', 0)}")
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state["messages"] = []
            st.session_state.pop("last_improvement", None)
            st.rerun()
            
        # Prompt Settings
        st.subheader("Prompt Engineering")
        use_improver = st.toggle("Enable Prompt Improver", value=False)
            
        return {
            "model": model,
            "memory_window": memory_window,
            "backend_healthy": is_healthy,
            "use_improver": use_improver
        }
