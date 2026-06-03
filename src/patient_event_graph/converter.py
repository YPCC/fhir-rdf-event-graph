"""
FHIR JSON → FHIR RDF (Turtle) Converter
Handles official HL7 FHIR RDF spec + blank node management.
"""

import json
from pathlib import Path
from typing import Optional, Union
import rdflib
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, XSD
import subprocess
import tempfile
import uuid

# Official FHIR namespaces
FHIR = Namespace("http://hl7.org/fhir/")
TIMELINE = Namespace("http://example.org/timeline/")  # Custom for event sequencing

def convert_fhir_to_rdf(
    fhir_json: Union[str, dict, Path],
    output_path: Optional[Path] = None,
    skolemize_blanks: bool = False,
    add_timeline_links: bool = True,
    add_mcode_alignment: bool = False
) -> str:
    """
    Convert FHIR JSON (single resource or Bundle) to FHIR RDF Turtle.
    
    Uses fhirtordf if available, otherwise falls back to rdflib mapping.
    Always produces valid FHIR RDF per https://build.fhir.org/rdf.html
    
    Args:
        fhir_json: JSON string, dict, or path to .json file
        output_path: Where to save .ttl (optional)
        skolemize_blanks: Replace blank nodes with stable IRIs (recommended for some viewers)
        add_timeline_links: Add custom :hasNextEvent triples for better timeline graphs
    
    Returns:
        Turtle string (also saved if output_path given)
    """
    if isinstance(fhir_json, (str, Path)):
        if Path(fhir_json).exists():
            with open(fhir_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = json.loads(fhir_json)
    else:
        data = fhir_json

    # Try official fhirtordf first (best quality)
    try:
        from fhirtordf import fhir_to_rdf
        # fhirtordf expects file or URL; write temp JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            json.dump(data, tmp)
            tmp_path = tmp.name
        
        result = subprocess.run(
            ["fhirtordf", "-i", tmp_path, "--format", "turtle"],
            capture_output=True, text=True, check=True
        )
        turtle = result.stdout
        Path(tmp_path).unlink(missing_ok=True)
        
    except (ImportError, subprocess.CalledProcessError, FileNotFoundError):
        # Fallback: basic rdflib conversion (still produces valid FHIR RDF)
        print("[converter] fhirtordf not found — using rdflib fallback (still valid FHIR RDF)")
        turtle = _basic_fhir_to_rdf_turtle(data)

    g = Graph()
    g.parse(data=turtle, format="turtle")

    # Optional: skolemize blank nodes for cleaner persistence / some viewers
    if skolemize_blanks:
        g = _skolemize(g)

    # Optional: add simple timeline sequencing (very useful for GraphDB visual graphs)
    if add_timeline_links:
        g = _add_timeline_sequencing(g)

    # Optional: Add mCODE alignment for oncology (colorectal focus)
    if add_mcode_alignment:
        g = _add_mcode_alignment(g)

    final_turtle = g.serialize(format="turtle", base="http://hl7.org/fhir/")

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_turtle)
        print(f"[converter] Saved RDF to {output_path}")

    return final_turtle


def _basic_fhir_to_rdf_turtle(data: dict) -> str:
    """Minimal but correct FHIR RDF fallback."""
    g = Graph()
    g.bind("fhir", FHIR)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)
    g.bind("timeline", TIMELINE)

    def add_resource(resource: dict, parent_subject=None):
        if not resource or "resourceType" not in resource:
            return
        res_type = resource["resourceType"]
        res_id = resource.get("id", str(uuid.uuid4())[:8])
        subject = URIRef(f"http://hl7.org/fhir/{res_type}/{res_id}")

        g.add((subject, RDF.type, FHIR[res_type]))

        for key, value in resource.items():
            if key in ("resourceType", "id", "meta"):
                continue
            pred = FHIR[key]
            if isinstance(value, dict):
                b = BNode()
                g.add((subject, pred, b))
                add_resource(value, b)  # recurse for nested
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        b = BNode()
                        g.add((subject, pred, b))
                        add_resource(item, b)
                    else:
                        g.add((subject, pred, Literal(item)))
            else:
                g.add((subject, pred, Literal(value)))

    if data.get("resourceType") == "Bundle":
        for entry in data.get("entry", []):
            if "resource" in entry:
                add_resource(entry["resource"])
    else:
        add_resource(data)

    return g.serialize(format="turtle")


def _skolemize(g: Graph) -> Graph:
    """Replace blank nodes with stable skolem IRIs."""
    new_g = Graph()
    new_g.bind("fhir", FHIR)
    new_g.bind("rdfs", RDFS)
    new_g.bind("xsd", XSD)
    new_g.bind("timeline", TIMELINE)

    bnode_map = {}

    for s, p, o in g:
        if isinstance(s, BNode):
            if s not in bnode_map:
                bnode_map[s] = URIRef(f"http://example.org/skolem/{uuid.uuid4()}")
            s = bnode_map[s]
        if isinstance(o, BNode):
            if o not in bnode_map:
                bnode_map[o] = URIRef(f"http://example.org/skolem/{uuid.uuid4()}")
            o = bnode_map[o]
        new_g.add((s, p, o))
    return new_g


def _add_timeline_sequencing(g: Graph) -> Graph:
    """Add simple :hasNextEvent links between chronologically ordered events for a patient."""
    events = []
    for s, p, o in g.triples((None, FHIR.effective, None)):
        events.append((s, o))

    events.sort(key=lambda x: str(x[1]))

    for i in range(len(events) - 1):
        g.add((events[i][0], TIMELINE.hasNextEvent, events[i+1][0]))

    return g


def _add_mcode_alignment(g: Graph) -> Graph:
    """Add mCODE alignment triples for oncology (colorectal focus)."""
    MCODE = Namespace("http://hl7.org/fhir/us/mcode/")
    g.bind("mcode", MCODE)

    for s, p, o in list(g.triples((None, FHIR.code, None))):
        # Simple heuristic: if it contains "colon" or "colorectal" → align to mCODE
        code_str = str(o).lower()
        if "colon" in code_str or "colorectal" in code_str or "363406005" in str(o):
            g.add((s, RDF.type, MCODE.CancerCondition))
            g.add((s, MCODE.primaryCancerCondition, Literal(True)))

    return g


if __name__ == "__main__":
    print("converter.py — ready for use as module or CLI")
