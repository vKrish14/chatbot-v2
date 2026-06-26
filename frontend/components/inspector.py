import streamlit as st
import time

def render_inspector():
    st.markdown('<div class="gradient-title" style="font-size: 2rem;">Diagnostics</div>', unsafe_allow_html=True)
    
    from utils import get_diagnostics_api
    diag_state = get_diagnostics_api()
    
    if not diag_state or not diag_state.get("telemetry"):
        st.info("System idle. Awaiting user interaction to display real-time telemetry.")
        return
        
    telemetry = diag_state.get("telemetry", {})
    pipeline = diag_state.get("pipeline", {})
    retrieval = diag_state.get("retrieval", {})
    prompt_stats = diag_state.get("prompt", {})
    generation = diag_state.get("generation", {})
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Telemetry", "Pipeline", "Retrieval", "Prompt", "Chunks"])
    
    with tab1:
        st.markdown("**Performance Metrics**")
        col1, col2 = st.columns(2)
        col1.metric("Routing Latency", f"{telemetry.get('routing_latency_ms', 0)} ms")
        col2.metric("Retrieval Latency", f"{telemetry.get('vector_retrieval_latency_ms', telemetry.get('web_retrieval_latency_ms', 0))} ms")
        col3, col4 = st.columns(2)
        col3.metric("Prompt Building", f"{telemetry.get('prompt_building_latency_ms', 0)} ms")
        col4.metric("Generation Latency", f"{telemetry.get('generation_latency_ms', 0)} ms")
        st.divider()
        st.metric("Total Tokens", generation.get('total_tokens', 0))
        st.metric("Throughput", f"{generation.get('tokens_per_sec', 0)} T/s")

    with tab2:
        st.markdown("**Execution Pipeline**")
        st.info(f"**Target:** {pipeline.get('query', 'N/A')}")
        st.success(f"**Strategy:** {pipeline.get('pipeline_type', 'chat').upper()}")
        
        st.markdown("""
        <div style="text-align: center; margin-top: 24px; font-family: 'Fira Code', monospace; color: #00c6ff; padding: 16px; border: 1px solid rgba(0,198,255,0.2); border-radius: 8px; background: rgba(0,198,255,0.05);">
            [ INTAKE ] ➔ [ ROUTER ] ➔ [ CONTEXT ] ➔ [ PROMPT ] ➔ [ LLM ]
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("**Context Acquisition**")
        st.metric("Method", retrieval.get('strategy', 'N/A').upper())
        st.metric("Top-K Parameters", retrieval.get('top_k', 0))
        st.metric("Chunks Acquired", retrieval.get('chunks_retrieved', 0))
        if retrieval.get('avg_similarity') is not None:
            st.metric("Mean Similarity", f"{retrieval.get('avg_similarity', 0):.2f}")
        if retrieval.get('threshold') is not None:
            st.metric("Confidence Threshold", f"{retrieval.get('threshold', 0):.2f}")

    with tab4:
        st.markdown("**Prompt Architecture**")
        st.metric("System Tokens", prompt_stats.get('system_prompt_tokens', 0))
        st.metric("Context Tokens", prompt_stats.get('context_tokens', 0))
        st.metric("History Tokens", prompt_stats.get('history_tokens', 0))
        st.metric("Total Input Tokens", prompt_stats.get('final_prompt_tokens', 0))

    with tab5:
        st.markdown("**Acquired Knowledge Chunks**")
        sources = retrieval.get("sources", [])
        if sources:
            st.caption(f"{len(sources)} chunks retrieved successfully.")
            for i, source in enumerate(sources):
                score = source.get('similarity', 0)
                st.markdown(f"""
                <div class="chunk-card">
                    <div class="meta">
                        <strong>Source:</strong> {source.get('document_name', 'Web')}
                        <span style="float:right; color:#00c6ff;">Score: {score:.2f}</span>
                    </div>
                    <div>{source.get('content', '')[:200]}...</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No contextual chunks were retrieved during the last execution.")

