import streamlit as st
from utils import check_backend_health

def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="gradient-title" style="font-size: 1.5rem;">✦ KrishGPT</div>', unsafe_allow_html=True)
        
        # Backend Status
        is_healthy = check_backend_health()
        if is_healthy:
            st.success("API Status: Active", icon="⚡")
        else:
            st.error("API Status: Offline", icon="⚠️")
            
        st.divider()
        
        # Model Configuration
        st.markdown("### ⌘ Settings")
        model = st.selectbox(
            "Neural Engine",
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
        st.markdown("### 🧠 Memory Architecture")
        memory_window = st.slider("Context Window", min_value=2, max_value=20, value=10)
        st.session_state["memory_window"] = memory_window
        
        if "memory_stats" in st.session_state and st.session_state["memory_stats"]:
            stats = st.session_state["memory_stats"]
            st.caption(f"✦ Retained: {stats.get('retained_messages', 0)} / {stats.get('total_messages', 0)}")
            st.caption(f"⚡ Tokens: {stats.get('estimated_tokens', 0)}")
        
        if st.button("🗑️ Purge Context", use_container_width=True):
            st.session_state["messages"] = []
            st.session_state.pop("last_improvement", None)
            st.rerun()
            
        # Prompt Settings
        st.divider()
        st.markdown("### ⚙️ Optimization Layer")
        use_improver = st.toggle("Enable Prompt Improver", value=False)
        
        st.divider()
        st.markdown("### 🔍 Retrieval Control")
        search_strategy = st.selectbox("Search Strategy", ["similarity", "mmr", "hybrid"], index=0)
        top_k = st.slider("Top-K Chunks", min_value=1, max_value=10, value=4)
        similarity_threshold = st.slider("Similarity Threshold", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
            
        return {
            "model": model,
            "memory_window": memory_window,
            "backend_healthy": is_healthy,
            "use_improver": use_improver,
            "search_strategy": search_strategy,
            "top_k": top_k,
            "similarity_threshold": similarity_threshold
        }
