# POC Notebook: Colorectal Patient Event Graph (FHIR → RDF → Viz)

This notebook mirrors `scripts/fetch_convert_poc.py` for interactive exploration.

## 1. Setup
```python
!pip install -r ../requirements.txt
```

## 2. Run Full Pipeline
```python
from scripts.fetch_convert_poc import main
main()
```

## 3. Explore the RDF in Python
```python
from rdflib import Graph
g = Graph()
g.parse("../output/patient_events.ttl", format="turtle")
print(f"Triples: {len(g)}")
# Run custom SPARQL...
```

## 4. Load into GraphDB (Recommended)
See README.md for detailed steps. The Visual Graph explorer will show the full patient journey as an interactive connected graph.

## 5. View the Animated GIF
Open `../output/patient_journey.gif` — it shows the colorectal cancer journey unfolding over time.

**Tip**: For larger real Synthea datasets, increase `_count` or run locally with Synthea Java generator.
