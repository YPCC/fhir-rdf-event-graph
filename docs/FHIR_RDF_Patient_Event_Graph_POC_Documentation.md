# FHIR-RDF Patient Event Graph POC

**Project Documentation**

**Colorectal Cancer Patient Timeline Visualization**

---

## 1. Problem Statement

In oncology and chronic disease management, patient data is fragmented across multiple systems (EHRs, labs, imaging, pharmacy). Clinicians and researchers struggle to visualize the complete patient journey in a meaningful, chronological, and interconnected way.

**Key Challenges:**
- Raw FHIR data is difficult to explore interactively at scale
- No standardized way to represent temporal event graphs for cancer patients
- Blank nodes and complex nested structures in FHIR RDF make visualization challenging
- Lack of integrated tools combining GraphDB exploration with Python-based timeline animations
- Limited support for oncology-specific standards like mCODE in open-source tooling

---

## 2. Approach

We built an end-to-end pipeline that transforms FHIR patient data into a rich, queryable, and visualizable RDF knowledge graph with a strong focus on colorectal cancer journeys.

### 2.1 Core Pipeline

- **Data Ingestion**: Fetch realistic colorectal patient bundles from public HAPI FHIR servers or Synthea synthetic data
- **FHIR → RDF Conversion**: Use official HL7 FHIR RDF specification with proper handling of blank nodes (preserve or skolemize)
- **Graph Enrichment**: Add temporal sequencing (`hasNextEvent`) and optional mCODE oncology alignment
- **Visualization Layer**: Interactive Plotly timelines + high-quality animated GIF patient journeys
- **Storage & Exploration**: Native support for GraphDB (Free) with Visual Graph explorer and SPARQL

### 2.2 Key Innovations

- Blank node management strategy (preserve vs skolemize)
- Lightweight timeline ontology with `hasNextEvent` relationships
- mCODE alignment for oncology interoperability
- One-command Docker Compose stack (GraphDB + Streamlit web app)

---

## 3. Technology Stack

### 3.1 Core Technologies

| Component          | Technology                          |
|--------------------|-------------------------------------|
| FHIR Data          | HL7 FHIR R4, HAPI FHIR Server, Synthea |
| RDF Layer          | rdflib, fhirtordf, Turtle serialization |
| Graph Database     | GraphDB Free (Ontotext)             |
| Visualization      | Plotly, Matplotlib, NetworkX, Gephi |
| Web Interface      | Streamlit                           |
| Validation & Ontology | PySHACL, OWL, mCODE IG           |

### 3.2 Supporting Tools

- Docker & Docker Compose (one-command deployment)
- Jupyter Notebook (full interactive version)
- Python 3.11+ with pandas, requests, imageio
- GitHub-ready project structure with MIT license

---

## 4. Project Value

This POC delivers a **production-ready foundation** for healthcare organizations and researchers who need to transform FHIR data into actionable, visual, and standards-compliant patient event graphs — with particular strength in oncology use cases.

---

**Built for the FHIR + Semantic Web + Oncology community.**

*Last updated: May 2026*
