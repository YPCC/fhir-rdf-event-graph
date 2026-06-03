#!/usr/bin/env python3
"""
Bulk Processing Script for Synthea Colorectal Cancer Patients
Generates multiple realistic patient journeys and converts them to RDF.
"""

import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from patient_event_graph.converter import convert_fhir_to_rdf
from patient_event_graph.visualizer import extract_events_from_rdf
import pandas as pd
from tqdm import tqdm

DATA_DIR = Path(__file__).parent.parent / "data" / "synthea"
OUTPUT_DIR = Path(__file__).parent.parent / "output" / "bulk"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def process_synthea_patients(patient_dir: Path, max_patients: int = 10):
    """Process multiple Synthea FHIR bundles."""
    json_files = list(patient_dir.glob("*.json"))[:max_patients]
    
    all_events = []
    
    for json_file in tqdm(json_files, desc="Processing Synthea patients"):
        with open(json_file, "r", encoding="utf-8") as f:
            bundle = json.load(f)
        
        # Convert to RDF
        ttl_path = OUTPUT_DIR / f"{json_file.stem}.ttl"
        convert_fhir_to_rdf(bundle, output_path=ttl_path, skolemize_blanks=True)
        
        # Extract events for summary
        df = extract_events_from_rdf(ttl_path)
        df["patient"] = json_file.stem
        all_events.append(df)
    
    # Create summary
    summary_df = pd.concat(all_events, ignore_index=True)
    summary_path = OUTPUT_DIR / "bulk_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    
    print(f"\n✅ Processed {len(json_files)} patients")
    print(f"📊 Summary saved to {summary_path}")
    print(f"📁 RDF files saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    print("""
    === Bulk Synthea Colorectal Processing ===
    
    Includes a realistic sample colorectal patient (with mCODE alignment).
    For more patients, generate with Synthea and place JSONs in data/synthea/
    """)
    
    synthea_dir = Path(__file__).parent.parent / "data" / "synthea"
    
    # Always process the included high-quality colorectal sample
    sample_file = synthea_dir / "colorectal_sample_patient.json"
    if sample_file.exists():
        print("Processing included colorectal sample with mCODE alignment...")
        with open(sample_file) as f:
            bundle = json.load(f)
        ttl_path = OUTPUT_DIR / "colorectal_sample_patient.ttl"
        convert_fhir_to_rdf(bundle, output_path=ttl_path, skolemize_blanks=True, add_mcode_alignment=True)
        print(f"✅ Sample processed → {ttl_path}")
    
    # Process any additional Synthea files
    other_files = [f for f in synthea_dir.glob("*.json") if f.name != "colorectal_sample_patient.json"]
    if other_files:
        process_synthea_patients(synthea_dir, max_patients=10)
    else:
        print("✅ Sample colorectal patient ready (with mCODE). Add more Synthea files for bulk.")
