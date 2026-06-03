#!/usr/bin/env python3
"""
End-to-End POC Script: FHIR → RDF → GraphDB-ready + Python Visualizations
Colorectal cancer patient journey focus.
"""

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

import json
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent / "data" / "samples"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    print("=" * 60)
    print("FHIR → RDF Patient Event Graph POC")
    print("Colorectal Cancer Journey — GraphDB + Python Viz")
    print("=" * 60)

    # 1. Fetch realistic data (colorectal focus)
    print("\n[1/5] Fetching patient data (colorectal / cancer journey)...")
    bundle = fetch_patient_bundle(condition_code="363406005")  # Malignant tumor of colon

    # Save raw JSON for reference
    json_path = OUTPUT_DIR / "patient_bundle.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2)
    print(f"    Saved raw bundle → {json_path}")

    # 2. Convert to RDF (with blank node handling options)
    print("\n[2/5] Converting to FHIR RDF Turtle (blank nodes preserved)...")
    ttl_path = OUTPUT_DIR / "patient_events.ttl"
    turtle = convert_fhir_to_rdf(
        bundle,
        output_path=ttl_path,
        skolemize_blanks=False,      # Change to True for some viewers
        add_timeline_links=True
    )
    print(f"    RDF saved → {ttl_path} ({len(turtle.splitlines())} lines)")

    # Also create a skolemized version for comparison
    skolem_ttl = OUTPUT_DIR / "patient_events_skolem.ttl"
    convert_fhir_to_rdf(bundle, output_path=skolem_ttl, skolemize_blanks=True)

    # 3. Extract events & create visualizations
    print("\n[3/5] Extracting events and building visualizations...")
    df = extract_events_from_rdf(ttl_path)
    print(f"    Found {len(df)} chronological events")

    # Plotly interactive timeline
    fig = create_plotly_timeline(df)
    html_path = OUTPUT_DIR / "timeline_interactive.html"
    fig.write_html(html_path)
    print(f"    Interactive Plotly saved → {html_path}")

    # Animated GIF
    gif_path = OUTPUT_DIR / "patient_journey.gif"
    create_animated_gif(df, gif_path, fps=1.5)

    # Gephi export
    graphml_path = OUTPUT_DIR / "patient_events.graphml"
    export_to_gephi(df, graphml_path)

    # 4. Final instructions
    print("\n[4/5] GraphDB Instructions (copy-paste ready):")
    print("    1. Download GraphDB Free: https://graphdb.ontotext.com/")
    print("    2. Create repository → Import the .ttl file")
    print("    3. Visual Graph → search for Patient or Condition resources")
    print("    4. Try the SPARQL timeline query from the README")

    print("\n[5/5] Done! Open these files:")
    print(f"    • {html_path}          (interactive timeline)")
    print(f"    • {gif_path}           (animated patient journey)")
    print(f"    • {ttl_path}           (load into GraphDB / rdfglance / Reactodia)")
    print(f"    • {graphml_path}       (open in Gephi)")

    print("\n" + "=" * 60)
    print("Next: Load patient_events.ttl into GraphDB for the best interactive experience.")
    print("=" * 60)


if __name__ == "__main__":
    main()
