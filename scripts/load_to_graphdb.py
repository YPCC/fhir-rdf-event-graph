#!/usr/bin/env python3
"""
Script to load FHIR RDF TTL file into local GraphDB and provide SPARQL queries
for visualizing the Patient Event Graph.

Usage:
    python scripts/load_to_graphdb.py --graphdb-url http://localhost:7200 --repo patient-events
"""

import argparse
import requests
from pathlib import Path
import sys

TTL_FILE = Path(__file__).parent.parent / "data" / "samples" / "colorectal_patient_event_graph.ttl"


def create_repository(graphdb_url: str, repo_id: str):
    """Create a new GraphDB repository if it doesn't exist."""
    repo_config = f"""
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix rep: <http://www.openrdf.org/config/repository#> .
    @prefix sr: <http://www.openrdf.org/config/repository/sail#> .
    @prefix sail: <http://www.openrdf.org/config/sail#> .

    [] a rep:Repository ;
       rep:repositoryID "{repo_id}" ;
       rdfs:label "Patient Event Graph Repository" ;
       rep:repositoryImpl [
         rep:repositoryType "graphdb:SailRepository" ;
         sr:sailImpl [
           sail:sailType "graphdb:Sail" ;
         ]
       ] .
    """

    url = f"{graphdb_url}/rest/repositories"
    headers = {"Content-Type": "application/x-turtle"}

    response = requests.post(url, data=repo_config, headers=headers)

    if response.status_code in [201, 409]:  # 409 = already exists
        print(f"✅ Repository '{repo_id}' is ready")
        return True
    else:
        print(f"❌ Failed to create repository: {response.text}")
        return False


def upload_ttl(graphdb_url: str, repo_id: str, ttl_path: Path):
    """Upload TTL file to GraphDB repository."""
    if not ttl_path.exists():
        print(f"❌ File not found: {ttl_path}")
        return False

    url = f"{graphdb_url}/rest/repositories/{repo_id}/statements"
    headers = {"Content-Type": "application/x-turtle"}

    with open(ttl_path, "rb") as f:
        response = requests.post(url, data=f.read(), headers=headers)

    if response.status_code == 204:
        print(f"✅ Successfully uploaded {ttl_path.name} to repository '{repo_id}'")
        return True
    else:
        print(f"❌ Upload failed: {response.text}")
        return False


def print_sparql_queries(repo_id: str):
    """Print useful SPARQL queries for the event graph."""
    print("\n" + "=" * 70)
    print("SPARQL QUERIES FOR PATIENT EVENT GRAPH")
    print("=" * 70)

    print("\n1. VIEW ALL EVENTS IN CHRONOLOGICAL ORDER")
    print("-" * 70)
    print(f"""
PREFIX fhir: <http://hl7.org/fhir/>
PREFIX timeline: <http://example.org/timeline/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?event ?label ?date WHERE {{
  ?event a ?type ;
         fhir:effective ?eff ;
         rdfs:label ?label .
  ?eff fhir:dateTime| fhir:start ?date .
  FILTER(?type IN (fhir:Condition, fhir:Encounter, fhir:Procedure, 
                   fhir:MedicationAdministration, fhir:Observation))
}}
ORDER BY ?date
""")

    print("\n2. CONSTRUCT THE FULL EVENT GRAPH (for visualization)")
    print("-" * 70)
    print(f"""
PREFIX fhir: <http://hl7.org/fhir/>
PREFIX timeline: <http://example.org/timeline/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

CONSTRUCT {{
  ?event a ?type ;
         rdfs:label ?label ;
         timeline:hasNextEvent ?nextEvent .
  ?event fhir:effective ?eff .
}}
WHERE {{
  ?event a ?type ;
         rdfs:label ?label .
  OPTIONAL {{ ?event timeline:hasNextEvent ?nextEvent . }}
  OPTIONAL {{ ?event fhir:effective ?eff . }}
  FILTER(?type IN (fhir:Condition, fhir:Encounter, fhir:Procedure, 
                   fhir:MedicationAdministration, fhir:Observation))
}}
""")

    print("\n3. FIND THE COMPLETE PATIENT JOURNEY PATH")
    print("-" * 70)
    print(f"""
PREFIX fhir: <http://hl7.org/fhir/>
PREFIX timeline: <http://example.org/timeline/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?step ?label ?nextLabel WHERE {{
  ?step rdfs:label ?label .
  OPTIONAL {{
    ?step timeline:hasNextEvent ?next .
    ?next rdfs:label ?nextLabel .
  }}
}}
ORDER BY ?label
""")

    print("\n4. COUNT EVENTS BY TYPE")
    print("-" * 70)
    print(f"""
PREFIX fhir: <http://hl7.org/fhir/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?type (COUNT(?event) AS ?count) WHERE {{
  ?event a ?type ;
         rdfs:label ?label .
  FILTER(?type IN (fhir:Condition, fhir:Encounter, fhir:Procedure, 
                   fhir:MedicationAdministration, fhir:Observation))
}}
GROUP BY ?type
ORDER BY DESC(?count)
""")

    print("\n" + "=" * 70)
    print("HOW TO USE IN GRAPHDB:")
    print("1. Open http://localhost:7200")
    print(f"2. Select repository: {repo_id}")
    print("3. Go to 'SPARQL' tab")
    print("4. Paste any query above and click 'Execute'")
    print("5. For visualization: Go to 'Explore' → 'Visual Graph'")
    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Load FHIR RDF sample into GraphDB")
    parser.add_argument("--graphdb-url", default="http://localhost:7200",
                        help="GraphDB server URL (default: http://localhost:7200)")
    parser.add_argument("--repo", default="patient-events",
                        help="Repository ID (default: patient-events)")
    parser.add_argument("--ttl-file", default=str(TTL_FILE),
                        help="Path to TTL file")

    args = parser.parse_args()

    print("=" * 70)
    print("FHIR RDF Patient Event Graph → GraphDB Loader")
    print("=" * 70)

    ttl_path = Path(args.ttl_file)

    # Step 1: Create repository
    if not create_repository(args.graphdb_url, args.repo):
        sys.exit(1)

    # Step 2: Upload TTL
    if not upload_ttl(args.graphdb_url, args.repo, ttl_path):
        sys.exit(1)

    # Step 3: Print useful SPARQL queries
    print_sparql_queries(args.repo)

    print("\n✅ Done! Open GraphDB and explore the event graph.")


if __name__ == "__main__":
    main()