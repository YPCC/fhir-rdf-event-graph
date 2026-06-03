"""
Streamlit Web App for FHIR-RDF Patient Event Graph POC
Runs inside Docker with GraphDB integration
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from patient_event_graph.fhir_fetcher import fetch_patient_bundle
from patient_event_graph.converter import convert_fhir_to_rdf
from patient_event_graph.visualizer import (
    extract_events_from_rdf,
    create_plotly_timeline,
    create_animated_gif,
    export_to_gephi
)
import requests
import tempfile

st.set_page_config(
    page_title="FHIR-RDF Patient Event Graph POC",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 FHIR → RDF Patient Event Graph POC")
st.markdown("**Colorectal Cancer Journey** | GraphDB + Python Visualizations")

# Sidebar
st.sidebar.header("Configuration")
patient_id = st.sidebar.text_input("Patient ID (optional)", "")
use_skolem = st.sidebar.checkbox("Skolemize blank nodes", value=False)
load_to_graphdb = st.sidebar.checkbox("Auto-load to GraphDB", value=True)

GRAPHDB_URL = "http://graphdb:7200"  # Docker internal URL

def load_to_graphdb(ttl_path: Path, repo_name: str = "patient-events"):
    """Load TTL into GraphDB via REST API"""
    try:
        # Create repository if not exists
        repo_config = f"""
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix rep: <http://www.openrdf.org/config/repository#> .
        @prefix sr: <http://www.openrdf.org/config/repository/sail#> .
        @prefix sail: <http://www.openrdf.org/config/sail#> .
        
        [] a rep:Repository ;
           rep:repositoryID "{repo_name}" ;
           rdfs:label "Patient Events Repository" ;
           rep:repositoryImpl [
             rep:repositoryType "graphdb:SailRepository" ;
             sr:sailImpl [
               sail:sailType "graphdb:Sail" ;
             ]
           ] .
        """
        
        # Check if repo exists
        resp = requests.get(f"{GRAPHDB_URL}/rest/repositories/{repo_name}")
        if resp.status_code != 200:
            requests.post(
                f"{GRAPHDB_URL}/rest/repositories",
                data=repo_config,
                headers={"Content-Type": "application/x-turtle"}
            )
        
        # Upload data
        with open(ttl_path, "rb") as f:
            resp = requests.post(
                f"{GRAPHDB_URL}/rest/repositories/{repo_name}/statements",
                data=f.read(),
                headers={"Content-Type": "application/x-turtle"}
            )
        return resp.status_code == 204
    except Exception as e:
        st.error(f"GraphDB upload failed: {e}")
        return False

# Main action
if st.button("🚀 Run Full POC (Colorectal Patient)", type="primary"):
    with st.spinner("Running end-to-end POC..."):
        # 1. Fetch
        st.info("Step 1: Fetching colorectal patient data...")
        bundle = fetch_patient_bundle(patient_id if patient_id else None)
        
        # 2. Convert
        st.info("Step 2: Converting to RDF...")
        ttl_path = Path("/app/output/patient_events.ttl")
        convert_fhir_to_rdf(bundle, output_path=ttl_path, skolemize_blanks=use_skolem)
        
        # 3. Visualize
        st.info("Step 3: Generating visualizations...")
        df = extract_events_from_rdf(ttl_path)
        
        # Plotly
        fig = create_plotly_timeline(df)
        st.plotly_chart(fig, use_container_width=True)
        
        # GIF
        gif_path = Path("/app/output/patient_journey.gif")
        create_animated_gif(df, gif_path)
        st.image(str(gif_path), caption="Animated Patient Journey GIF")
        
        # Gephi
        graphml_path = Path("/app/output/patient_events.graphml")
        export_to_gephi(df, graphml_path)
        
        # 4. Load to GraphDB
        if load_to_graphdb:
            st.info("Step 4: Loading into GraphDB...")
            success = load_to_graphdb(ttl_path)
            if success:
                st.success("✅ Loaded into GraphDB! Open http://localhost:7200")
        
        st.success("✅ POC completed successfully!")
        st.balloons()

# Additional sections
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Quick Stats")
    if Path("/app/output/patient_events.ttl").exists():
        df = extract_events_from_rdf(Path("/app/output/patient_events.ttl"))
        st.metric("Total Events", len(df))
        st.dataframe(df[["date", "type", "label"]])

with col2:
    st.subheader("🔗 Quick Links")
    st.markdown("""
    - [GraphDB Workbench](http://localhost:7200)
    - [Download Latest TTL](/app/output/patient_events.ttl)
    - [View Animated GIF](/app/output/patient_journey.gif)
    """)

st.caption("Running in Docker | GraphDB + Streamlit")
