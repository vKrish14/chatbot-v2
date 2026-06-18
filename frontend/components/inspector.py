import streamlit as st
import time

def render_inspector():
    st.header("🔍 Inspector")
    
    if "last_generation_metrics" not in st.session_state:
        st.info("No generations yet. Send a message to see metrics.")
        return
        
    metrics = st.session_state["last_generation_metrics"]
    
    tab1, tab2, tab3 = st.tabs(["📊 Metrics", "🧠 Reasoning", "🔄 Pipeline"])
    
    with tab1:
        st.subheader("Performance")
        col1, col2, col3 = st.columns(3)
        col1.metric("Latency", f"{metrics.get('latency_ms', 0)} ms")
        col2.metric("Tokens", metrics.get('total_tokens', 0))
        col3.metric("Tokens/sec", metrics.get('tokens_per_sec', 0))
        
        st.subheader("Context Usage")
        ctx = metrics.get("context_usage", 0)
        st.progress(min(ctx / 100, 1.0), text=f"Context Window Used: {ctx}%")
        
    with tab2:
        st.subheader("LLM Reasoning")
        st.write(metrics.get("reasoning", "No reasoning provided by the model."))
        
    with tab3:
        st.subheader("Execution Pipeline")
        st.code("""
        1. User Input Received
        2. Memory Layer: Truncated context to N messages
        3. Prompt Layer: Improved prompt (if enabled)
        4. LLM Generation: Streamed response
        5. Inspector: Metrics updated
        """, language="text")
        
        # dynamic timeline
        st.write("**Current Execution:**")
        st.success("✅ Memory Processed")
        if st.session_state.get("use_improver"):
            st.success("✅ Prompt Improved")
        else:
            st.info("⏭️ Prompt Improver Skipped")
        st.success(f"✅ LLM Generation completed in {metrics.get('latency_ms', 0)}ms")
