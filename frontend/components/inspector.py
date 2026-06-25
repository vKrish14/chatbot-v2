import streamlit as st
import time

def render_inspector():
    st.markdown('<div class="gradient-title" style="font-size: 2rem;">🔍 Diagnostics</div>', unsafe_allow_html=True)
    
    from utils import get_diagnostics_api
    diag_state = get_diagnostics_api()
    
    if not diag_state or not diag_state.get("telemetry"):
        st.info("Initiate a generation to capture real-time telemetry.")
        return
        
    telemetry = diag_state.get("telemetry", {})
    pipeline = diag_state.get("pipeline", {})
    retrieval = diag_state.get("retrieval", {})
    prompt_stats = diag_state.get("prompt", {})
    generation = diag_state.get("generation", {})
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["⚡ Telemetry", "🔄 Pipeline", "🔍 Retrieval", "📝 Prompt", "🧩 Chunks", "📚 Sources"])
    
    with tab1:
        st.markdown("**Real-Time Telemetry**")
        col1, col2 = st.columns(2)
        col1.metric("Pipeline Latency", f"{telemetry.get('routing_latency_ms', 0)} ms", help="Routing")
        col2.metric("Retrieval Latency", f"{telemetry.get('vector_retrieval_latency_ms', telemetry.get('web_retrieval_latency_ms', 0))} ms")
        col3, col4 = st.columns(2)
        col3.metric("Prompt Latency", f"{telemetry.get('prompt_building_latency_ms', 0)} ms")
        col4.metric("Generation Latency", f"{telemetry.get('generation_latency_ms', 0)} ms")
        st.divider()
        st.metric("Total Tokens Generated", generation.get('total_tokens', 0))
        st.metric("Throughput", f"{generation.get('tokens_per_sec', 0)} T/s")

    with tab2:
        st.markdown("**Pipeline Routing**")
        st.info(f"**Query:** {pipeline.get('query', 'N/A')}")
        st.success(f"**Selected Pipeline:** {pipeline.get('pipeline_type', 'chat').upper()}")
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px; font-family: monospace; color: #00f2fe;">
            [ Query Intake ] ➔ [ Router ] ➔ [ Context ] ➔ [ Builder ] ➔ [ LLM ]
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("**Retrieval Architecture**")
        st.metric("Strategy", retrieval.get('strategy', 'N/A').upper())
        st.metric("Target Top-K", retrieval.get('top_k', 0))
        st.metric("Chunks Retrieved", retrieval.get('chunks_retrieved', 0))
        if retrieval.get('avg_similarity') is not None:
            st.metric("Avg Similarity", f"{retrieval.get('avg_similarity', 0):.2f}")
        if retrieval.get('threshold') is not None:
            st.metric("Similarity Threshold", f"{retrieval.get('threshold', 0):.2f}")

    with tab4:
        st.markdown("**Prompt Construction**")
        st.metric("System Tokens", prompt_stats.get('system_prompt_tokens', 0))
        st.metric("Context Tokens", prompt_stats.get('context_tokens', 0))
        st.metric("History Tokens", prompt_stats.get('history_tokens', 0))
        st.metric("Final Prompt Tokens", prompt_stats.get('final_prompt_tokens', 0))

    with tab5:
        st.markdown("**Retrieved Chunks**")
        # Since chunks and sources are inside the conversation context, we can't get them directly from diagnostics state 
        # unless we pass them. For now we will show the number from retrieval stats.
        st.info(f"{retrieval.get('chunks_retrieved', 0)} chunks were retrieved in the last run.")
        if retrieval.get('strategy') == 'web_search':
            st.caption("Chunks originated from web search.")
        else:
            st.caption("Chunks originated from vector store.")

    with tab6:
        st.markdown("**Sources Used**")
        st.info("Check chat response for inline citations.")
        st.caption("Note: Inline citations contain exact document and page references based on the context.")
