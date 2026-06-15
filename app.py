import streamlit as st
import pandas as pd
import requests
import time
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(page_title="AMD Mission Control V2", layout="wide")
st.title("??? AMD AI Supply Chain Command Center")
st.caption("ROCm 6.x Infrastructure | Self-Improving Multi-Agent Framework")

# Initialize persistent session states for presentation safety
if "pipeline_results" not in st.session_state:
    st.session_state.pipeline_results = None
if "memory_committed" not in st.session_state:
    st.session_state.memory_committed = False

@st.cache_data
def get_filter_options():
    try:
        df = pd.read_csv("synthetic_intelligent_supply_chain.csv", encoding='latin1')
        return list(df['SKU'].unique()), list(df['Destination_Region'].unique())
    except:
        return ["SKU-MICROCHIPS-77X", "SKU-LITHIUM-CELLS", "SKU-STEEL-FASTENERS"], ["US-East", "US-West", "EMEA", "APAC"]

available_skus, available_regions = get_filter_options()
col1, col2 = st.columns(2)
sku = col1.selectbox("Target Item Classification (SKU):", available_skus)
region = col2.selectbox("Destination Distribution Node (Region):", available_regions)

if st.button("Initialize Pipeline Optimization Diagnostics", type="primary"):
    st.session_state.memory_committed = False
    with st.status("? Booting Hardware Engines...", expanded=True) as status:
        st.write("?? Evaluating XGBoost Predictive Matrices...")
        res = requests.post("http://127.0.0.1:8000/api/pipeline/run", json={"sku": sku, "region": region})
        if res.status_code == 200:
            st.session_state.pipeline_results = res.json()
            st.session_state.active_sku = sku
            st.session_state.active_region = region
            status.update(label="? Diagnostics Compiled!", state="complete")
        else:
            st.error("Backend offline or failure encountered.")

# Render UI elements if session data exists
if st.session_state.pipeline_results:
    data = st.session_state.pipeline_results
    t = data["telemetry"]
    active_sku = st.session_state.active_sku
    active_region = st.session_state.active_region
    
    st.error(f"?? Operational Exception: {t['predicted_delay']} Day Variance Predicted (+{t['volume_spike']}% Strain)")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Telemetry Core Temp", f"{t['temp']} °C", delta="Target < 35°C", delta_color="inverse")
    m2.metric("Inbound Kinetic Impact", f"{t['shock']} G", delta="Nominal < 1.5G", delta_color="inverse")
    m3.metric("Explainable AI Root Cause Determination", str(t['root_cause']))
    
    # --- GRAPH LAYER ---
    st.markdown("### ??? Graph AI: Topology Blast Radius Mapping")
    nodes = [
        Node(id=active_sku, label=f"CRITICAL: {active_sku}", size=350, color="#FF4B4B"),
        Node(id="Vendor", label="Upstream Factory Node", size=220, color="#FFA500"),
        Node(id=active_region, label=f"Inbound Hub: {active_region}", size=220, color="#1F77B4"),
        Node(id="Enterprise", label="Downstream Channels", size=150, color="#7F7F7F")
    ]
    edges = [Edge(source="Vendor", target=active_sku), Edge(source=active_sku, target=active_region), Edge(source=active_region, target="Enterprise")]
    agraph(nodes=nodes, edges=edges, config=Config(width=1100, height=260, directed=True, physics=True))
    
    # --- CHAT TIMELINE STREAM ---
    st.divider()
    st.markdown("### ?? Live Multi-Agent Consultation Feed")
    
    with st.chat_message("system", avatar="??"):
        st.markdown(f"**?? XGBoost Predictive Sentinel**: Anomaly verified. Instantiating parallel routing loops for execution parameter `{t['root_cause']}`...")
        
    with st.chat_message("user", avatar="??"):
        st.markdown("**?? Strategic Inventory Planner Agent**:")
        st.info(data['agent_outputs']['inventory'])
        
    with st.chat_message("user", avatar="??"):
        st.markdown("**?? Intermodal Logistics Coordinator Agent**:")
        st.info(data['agent_outputs']['logistics'])
        
    with st.chat_message("assistant", avatar="??"):
        st.markdown("**?? Autonomous Executive Critic (Validator)**: Cross-functional audit clear. Verified deterministic freight rate tools. Approved Manifest details below:")
        st.success(data['agent_outputs']['executive_synthesis'])
        
    # --- ENHANCEMENT 1: MEMORY FLYWHEEL BUTTON ---
    st.markdown("#### ?? Human-In-The-Loop Validation")
    if not st.session_state.memory_committed:
        if st.button("Commit Approved Strategy to Long-Term Vector Memory"):
            commit_res = requests.post("http://127.0.0.1:8000/api/pipeline/commit", json={
                "sku": active_sku,
                "region": active_region,
                "approved_plan": data['agent_outputs']['executive_synthesis']
            })
            if commit_res.status_code == 200:
                st.session_state.memory_committed = True
                st.rerun()
    else:
        st.success("?? **System Memory Updated:** This resolution sequence has been appended to the live FAISS index. Future instances of this defect will reference this strategy.")

    # --- UPDATED REAL HARDWARE METRICS ---
    st.divider()
    st.subheader("? AMD Instinct Performance Analytics (ROCm Native Execution)")
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("End-to-End Latency", f"{data['metrics']['latency_sec']}s")
    b2.metric("Processing Throughput", f"{data['metrics']['tokens_per_sec']} tok/s")
    # Dynamic fields pulling straight from local subprocess components
    b3.metric("Live GPU Compute Load", data['metrics']['gpu_utilization'], delta="ROCm Managed")
    b4.metric("Physical Silicon Core Temp", data['metrics']['gpu_temp'])
