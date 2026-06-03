# FHIR-RDF Patient Event Graph POC

**Executive Summary** | Colorectal Cancer Patient Timeline Visualization

---

## Problem

Oncology patient data is fragmented across EHRs, labs, and imaging systems. Clinicians and researchers lack an integrated, visual, standards-based way to explore complete patient journeys — especially for complex cancer cases like colorectal cancer.

## Solution

An end-to-end open-source pipeline that converts FHIR patient data into a rich RDF knowledge graph, with native GraphDB visualization, interactive Python timelines, animated GIFs, and mCODE oncology alignment — all deployable in one command via Docker.

## Key Features

- FHIR R4 → RDF (Turtle) conversion with blank node handling  
- Interactive GraphDB Visual Graph explorer  
- Plotly timelines + high-quality animated patient journey GIFs  
- mCODE alignment for oncology  
- SHACL validation  
- One-click Docker Compose (GraphDB + Streamlit)  
- Bulk Synthea processing support

## Technology Stack

| FHIR / Data       | RDF / Graph          | Visualization          | Deployment             |
|-------------------|----------------------|------------------------|------------------------|
| HAPI FHIR, Synthea| GraphDB Free, rdflib | Plotly, Matplotlib, Gephi | Docker Compose, Streamlit |

## Business Value

Delivers a production-ready foundation for oncology data interoperability, clinical decision support, and research. Enables instant visualization of complex cancer patient journeys while maintaining full compliance with HL7 FHIR and mCODE standards.

---

**Ready to transform cancer patient data visualization?**  
Clone the repo and run with Docker in under 2 minutes.

**GitHub:** https://github.com/YPCC/fhir-rdf-event-graph

*May 2026*
