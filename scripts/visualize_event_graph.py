#!/usr/bin/env python3
"""
Script to load FHIR RDF TTL file and visualize the Patient Event Graph
"""

from pathlib import Path
import sys
from rdflib import Graph, Namespace
import networkx as nx
from pyvis.network import Network
import webbrowser

# Paths
TTL_FILE = Path(__file__).parent.parent / "data" / "samples" / "colorectal_patient_event_graph.ttl"
OUTPUT_HTML = Path(__file__).parent.parent / "output" / "patient_event_graph.html"

def load_and_visualize(ttl_path: Path, output_html: Path):
    print(f"Loading TTL file: {ttl_path}")
    
    g = Graph()
    g.parse(ttl_path, format="turtle")
    
    print(f"Loaded {len(g)} triples")
    
    # Create NetworkX graph
    G = nx.DiGraph()
    
    # Add nodes and edges
    for s, p, o in g:
        s_str = str(s).split("/")[-1] if "/" in str(s) else str(s)
        o_str = str(o).split("/")[-1] if "/" in str(o) else str(o)
        
        # Add node with label
        if s not in G:
            G.add_node(s, label=s_str, title=str(s))
        if o not in G and not str(o).startswith("http://www.w3.org"):
            G.add_node(o, label=o_str, title=str(o))
        
        # Add edge for hasNextEvent (main timeline relationship)
        if "hasNextEvent" in str(p):
            G.add_edge(s, o, label="hasNextEvent", color="#e74c3c", width=3)
        elif str(p).endswith("subject") or "subject" in str(p):
            G.add_edge(s, o, label="subject", color="#3498db")
        else:
            # Add other relationships lightly
            G.add_edge(s, o, label=str(p).split("/")[-1], color="#95a5a6", width=1)
    
    print(f"Graph has {len(G.nodes)} nodes and {len(G.edges)} edges")
    
    # Create interactive visualization with Pyvis
    net = Network(height="800px", width="100%", directed=True, notebook=False, bgcolor="#ffffff", font_color="#2c3e50")
    
    # Add nodes with colors based on type
    for node in G.nodes:
        node_data = G.nodes[node]
        label = node_data.get("label", str(node)[:30])
        
        # Color coding
        if "Patient" in str(node):
            color = "#2ecc71"  # Green
        elif "Condition" in str(node):
            color = "#e74c3c"  # Red
        elif "Procedure" in str(node):
            color = "#9b59b6"  # Purple
        elif "Encounter" in str(node):
            color = "#3498db"  # Blue
        elif "Medication" in str(node):
            color = "#f39c12"  # Orange
        elif "Observation" in str(node):
            color = "#1abc9c"  # Teal
        else:
            color = "#95a5a6"  # Gray
        
        net.add_node(str(node), label=label, title=str(node), color=color, size=25)
    
    # Add edges
    for u, v, data in G.edges(data=True):
        label = data.get("label", "")
        color = data.get("color", "#7f8c8d")
        width = data.get("width", 2)
        net.add_edge(str(u), str(v), label=label, color=color, width=width)
    
    # Set physics for better layout
    net.set_options("""
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 150,
          "springConstant": 0.08
        },
        "maxVelocity": 50,
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": {"iterations": 150}
      }
    }
    """)
    
    # Save HTML
    output_html.parent.mkdir(parents=True, exist_ok=True)
    net.save_graph(str(output_html))
    
    print(f"\n✅ Interactive event graph saved to: {output_html}")
    print("Opening in browser...")
    
    # Open in browser
    webbrowser.open(f"file://{output_html.absolute()}")
    
    return output_html

if __name__ == "__main__":
    print("=" * 60)
    print("FHIR RDF Patient Event Graph Visualizer")
    print("=" * 60)
    
    if not TTL_FILE.exists():
        print(f"Error: File not found: {TTL_FILE}")
        sys.exit(1)
    
    load_and_visualize(TTL_FILE, OUTPUT_HTML)
    print("\nDone! Close the browser tab when finished.")