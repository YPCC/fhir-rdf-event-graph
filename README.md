# fhir-rdf-event-graph

**End-to-end pipeline**: FHIR patient data (realistic colorectal/synthetic cancer journeys) → RDF (Turtle) with proper blank node handling → **Interactive GraphDB visualization first** + high-quality Python timeline animations/GIFs + exports to Gephi, Protégé, rdfglance, Reactodia, and more.

Python-first, production-ready starter kit. Fast, clean, and designed for healthcare informatics, research, and semantic web demos.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Why This Project?

- **Your exact vision realized**: Read FHIR → FHIR-to-RDF (official spec) → manage blank nodes → visualize as **patient event timeline/graph**.
- **GraphDB-first** interactive exploration (your priority #1).
- Beautiful Python timelines + animated GIF patient journeys (priority #2).
- Export-ready for Gephi (graph layout), Protégé (OWL), rdfglance, Reactodia.
- Realistic **colorectal cancer** synthetic patient examples included.
- Cookie-cutter structure — anyone can clone and run in minutes.

## Installation (Step-by-Step)

### Option 1: Docker Compose (Recommended - Fastest)

```bash
# 1. Clone the repository
git clone https://github.com/YPCC/fhir-rdf-event-graph.git
cd fhir-rdf-event-graph

# 2. Start everything with one command
docker-compose up --build
```

**Access Points:**
- Streamlit Web App: http://localhost:8501
- GraphDB: http://localhost:7200

Click **"Run Full POC"** in the web app.

---

### Option 2: Local Python Installation

```bash
# 1. Clone the repository
git clone https://github.com/YPCC/fhir-rdf-event-graph.git
cd fhir-rdf-event-graph

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. (Optional) Install additional visualization tools
pip install pyvis pyshacl
```

---

### Option 3: GraphDB Setup (for Interactive Exploration)

1. Download **GraphDB Free** from https://graphdb.ontotext.com/
2. Extract and run:
   ```bash
   ./graphdb
   ```
3. Open http://localhost:7200 in your browser
4. Create a new repository (e.g., `patient-events`)
5. Import any `.ttl` file from `data/samples/`

---

### Run the POC

After installation, run:

```bash
python scripts/fetch_convert_poc.py
```

This will automatically:
- Fetch colorectal patient data
- Convert to FHIR RDF
- Generate interactive visualizations
- Create animated GIF
- Export to Gephi

---

### Verify Installation

```bash
# Check if everything works
python -c "from patient_event_graph.converter import convert_fhir_to_rdf; print('✅ Installation successful!')"
```

---

## Documentation

- **Full Project Documentation**: [FHIR_RDF_Patient_Event_Graph_POC_Documentation.md](FHIR_RDF_Patient_Event_Graph_POC_Documentation.md)
- **One-Page Executive Summary**: [FHIR_RDF_Executive_Summary.md](FHIR_RDF_Executive_Summary.md)
- **Demo Video Script**: [docs/demo_video_script.md](docs/demo_video_script.md)
- **Word Document Versions**: Available in the repository root (`*.docx` files)

## Phase 1: POC — Colorectal Patient Event Graph (What You Get Now)

### 1. GraphDB Interactive Exploration (Priority #1)

**Recommended**: Download **GraphDB Free** (desktop or server) from https://graphdb.ontotext.com/

**Steps**:
1. Start GraphDB → Create new repository (e.g. `patient-events`).
2. Go to **Import** → **RDF** → Upload the generated `.ttl` file (or paste from `data/samples/`).
3. Go to **Explore** → **Visual Graph**.
4. Search for the Patient IRI or any resource → expand the graph.
5. Use **SPARQL** tab for timeline queries:

```sparql
PREFIX fhir: <http://hl7.org/fhir/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?event ?date ?type ?label WHERE {
  ?event a fhir:Encounter, fhir:Procedure, fhir:Condition, fhir:MedicationAdministration ;
         fhir:effective ?eff ;
         rdfs:label ?label .
  ?eff fhir:dateTime| fhir:start ?date .
}
ORDER BY ?date
```

**Blank nodes**: They appear as anonymous nodes (normal in FHIR RDF). Hover/expand to see details. For cleaner viz you can run the included skolemization option.

**OWL / RDF Reasoning** (optional, desirable):
- In repository settings enable **OWL reasoning** (RDFS or OWL2-RL).
- Add the FHIR ontology + your custom `timeline:` vocabulary for inference (e.g. infer "hasNextEvent" or temporal relations).

### 2. Python Timeline Visualizations (Priority #2)

- **Interactive Plotly Gantt/Timeline**: Hover, zoom, filter by event type (Condition, Encounter, Procedure, Medication, Observation).
- **Animated GIF Patient Journey**: Watch the colorectal cancer journey unfold chronologically with color-coded events, progress bar, and labels. High-quality output ready for presentations.

Run:
```bash
python scripts/generate_gif.py   # or from the notebook
```

### 3. Other RDF Viewers & Tools

- **Gephi** (graph layouts): Export from GraphDB or use `visualizer.py --export-gephi` → open `.graphml`.
- **Protégé**: Import the Turtle/OWL version for ontology editing + reasoning.
- **rdfglance**: Excellent lightweight RDF graph viewer (recommended in your notes).
- **Reactodia**: Modern web-based interactive RDF explorer.
- Others: OntoSpy, RDF Playground, yEd, etc.

## Project Structure

```
fhir-rdf-event-graph/
├── README.md
├── requirements.txt
├── src/patient_event_graph/
│   ├── converter.py          # FHIR JSON → RDF Turtle + blank node handling
│   ├── visualizer.py         # Plotly + Matplotlib GIF + Gephi export
│   └── fhir_fetcher.py
├── scripts/
│   ├── fetch_convert_poc.py
│   └── generate_gif.py
├── data/samples/
│   └── colorectal_sample.ttl   # Ready-to-use realistic example
├── notebooks/
│   └── 01_poc_colorectal.ipynb
├── docs/
│   └── architecture.md
└── LICENSE (MIT)
```

## Realistic Colorectal Cancer Example Included

We use synthetic but clinically realistic data based on:
- SNOMED CT: `363406005` | Malignant tumor of colon |
- Common colorectal journey: Screening → Diagnosis (Condition) → Colonoscopy (Procedure) → Surgery → Chemotherapy (MedicationAdministration) + follow-up Observations/Encounters.

Full patient bundle can be generated with **Synthea** (highly recommended for more complex journeys):
```bash
# After installing Synthea (Java)
./run_synthea -p 1 --exporter.fhir.export=true "Colorectal Cancer"
```

## How It Works (Technical)

1. **Fetch** — `fhir_fetcher.py` uses `requests` + public HAPI FHIR (`http://hapi.fhir.org/baseR4`) or local Synthea JSON.
2. **Convert** — `converter.py` wraps `fhirtordf` (official FHIR RDF tool) + rdflib post-processing for blank node options (preserve / skolemize).
3. **Visualize** — Events extracted chronologically → Plotly timeline + Matplotlib animation saved as GIF.
4. **Export** — Turtle, GraphML (Gephi), optional OWL.

**Blank Node Handling** (core requirement):
- Default: Preserve (faithful to FHIR spec).
- Option `--skolem`: Replace blanks with stable UUID-based IRIs for easier persistence and some viewers.
- GraphDB and most tools handle both perfectly.

## Next Steps / Roadmap (Phase 2 Ideas)

- Full Dash/Streamlit web app with time slider.
- Bulk processing for 100+ patients.
- Custom `timeline:` ontology + SHACL shapes.
- Docker Compose (GraphDB + app).
- Direct GraphDB Python client integration.
- More cancer types + mCODE alignment.

## Contributing

PRs welcome! Especially:
- Better SPARQL timeline templates
- Additional visualizers
- More realistic Synthea modules

## License

MIT License — free for commercial and research use.

---

**Built with ❤️ for the FHIR + Semantic Web community.**

Questions? Open an issue or reach out. Let's make patient event graphs beautiful and useful!

---

## New Features (v1.2 – Latest)

### 🎥 Professional Demo Video Script
Ready-to-use script in `docs/demo_video_script.md` (4:30–5:30 min video optimized for YouTube/product demos).

### 🧬 mCODE Alignment for Oncology
- Optional flag: `add_mcode_alignment=True` in converter
- Aligns colorectal conditions to `mcode:CancerCondition`
- Included in the sample Synthea patient

### 📦 Included Synthea Colorectal Sample
High-quality realistic patient bundle at:
`data/synthea/colorectal_sample_patient.json`
(Already processed with mCODE alignment in bulk script)

---

## New Features (v1.1 Enhancements)

### 🐳 Docker Compose (GraphDB + Streamlit App)
Run the entire stack with one command:

```bash
docker-compose up --build
```

- **GraphDB** at http://localhost:7200
- **Streamlit Web App** at http://localhost:8501 (interactive POC runner + auto-load to GraphDB)

### 📓 Full Jupyter Notebook
```bash
jupyter notebook notebooks/01_poc_colorectal.ipynb
```

Complete interactive version with all steps + SHACL validation.

### 📦 Bulk Processing (Synthea Colorectal Patients)
```bash
# 1. Generate data with Synthea (Java)
./run_synthea -p 20 --module ColorectalCancer

# 2. Process in bulk
python scripts/bulk_process_synthea.py
```

### 🎥 Improved GIF Animation
- Support for 10+ event types (DiagnosticReport, Immunization, CarePlan, etc.)
- Better visuals, legend, patient context, smoother animation
- Higher quality output

### ✅ Enhanced SHACL Validation
- `shacl/patient_event_shacl.ttl` — Comprehensive rules for Patient, CancerCondition, ClinicalEvents, and Timeline sequencing
- Includes mCODE alignment validation and colorectal-specific rules
- **New validation report script**: `scripts/validate_event_graph.py`

```bash
python scripts/validate_event_graph.py
```

### 🧬 Custom OWL Ontology
- `ontology/patient_timeline.owl` — Timeline ontology with `hasNextEvent`
- `ontology/mcode_alignment.ttl` — mCODE oncology alignment

### 📊 Event Graph Visualization Scripts
- `scripts/visualize_event_graph.py` — Interactive HTML graph using Pyvis
- `scripts/load_to_graphdb.py` — Load TTL into GraphDB + ready-to-use SPARQL queries

```bash
# Visualize locally
python scripts/visualize_event_graph.py

# Load to GraphDB
python scripts/load_to_graphdb.py --graphdb-url http://localhost:7200 --repo patient-events
```

### ✅ FHIR JSON Validation (using project-fhir-lens)
Validate FHIR resources against official HL7 FHIR specifications **before** converting to RDF:

```bash
# Install the validator
pip install git+https://github.com/zpak96/project-fhir-lens.git

# Run validation on our sample data
python scripts/validate_fhir.py
```

This adds an important quality gate in the pipeline.

---

**Next Roadmap**
- Full mCODE alignment
- Neo4j + RDF* support
- LLM-assisted event summarization
- Production deployment on Kubernetes

Thank you for using this project!
