# 🎥 Demo Video Script: FHIR-RDF Patient Event Graph POC

**Video Title:**  
**"From FHIR to Interactive Patient Timeline in 5 Minutes – Colorectal Cancer Demo"**

**Target Length:** 4:30 – 5:30 minutes  
**Style:** Professional, clean, fast-paced (like a product demo)  
**Music:** Subtle tech/medical background (royalty-free)

---

## **00:00 – 00:20 | Hook & Problem Statement**

**Visuals:**  
- Screen recording of a complex patient chart  
- Text overlay: *"Managing cancer patient data is messy..."*

**Narration (Voiceover):**
> "In oncology, patient journeys involve dozens of events across systems.  
> Today, I'll show you how we turn raw FHIR data into a beautiful, interactive, standards-based patient event graph in under 5 minutes."

---

## **00:20 – 01:10 | Project Overview**

**Visuals:**  
- GitHub repo homepage  
- Zoom into README highlights

**Narration:**
> "This is the open-source `fhir-rdf-event-graph` project.  
> It takes FHIR patient data — specifically colorectal cancer journeys — converts it to RDF, loads it into **GraphDB**, and generates stunning visualizations."

**Show on screen:**
- Docker Compose logo
- GraphDB Visual Graph
- Animated GIF
- Plotly timeline

---

## **01:10 – 02:30 | Live Demo – One-Command Setup**

**Visuals:** Terminal + browser side-by-side

**Narration:**
> "Let's start with the easiest way — Docker Compose."

```bash
docker-compose up --build
```

**On screen:**
- Terminal output
- Streamlit app loading at http://localhost:8501
- Click "Run Full POC"

**Show:**
- Colorectal patient data being fetched
- RDF conversion happening
- GraphDB auto-load
- Interactive Plotly timeline appearing
- Beautiful animated GIF playing

**Voiceover:**
> "With one command, we get a full colorectal cancer patient journey:  
> diagnosis → colonoscopy → surgery → chemotherapy.  
> All converted to FHIR RDF and loaded into GraphDB automatically."

---

## **02:30 – 03:30 | GraphDB Deep Dive**

**Visuals:** Switch to GraphDB at http://localhost:7200

**Narration:**
> "Now let's explore the data in **GraphDB** — the heart of this solution."

**Actions:**
1. Open Visual Graph
2. Search for Patient or Condition
3. Expand nodes to show full event graph
4. Run the timeline SPARQL query (pre-loaded)
5. Enable OWL reasoning (optional)

**Voiceover:**
> "GraphDB gives us interactive exploration of the entire patient graph.  
> We can see how every event is connected — perfect for clinical decision support and research."

---

## **03:30 – 04:20 | Advanced Features**

**Visuals:** Quick cuts

**Show:**
- Jupyter Notebook running
- Bulk processing script
- SHACL validation results (green checkmark)
- Gephi graph layout
- mCODE-aligned resources (if time permits)

**Narration:**
> "We also support Jupyter notebooks, bulk Synthea processing, SHACL validation, and even mCODE oncology alignment."

---

## **04:20 – 05:00 | Why This Matters + Call to Action**

**Visuals:**  
- Clean summary slide  
- GitHub link  
- "Star the repo" animation

**Narration:**
> "This POC proves that FHIR + RDF + GraphDB is not just possible — it's powerful and production-ready.  
> Whether you're in oncology research, interoperability, or building the next cancer platform, this gives you a massive head start."

**On screen text:**
- GitHub: github.com/YOUR_USERNAME/fhir-rdf-event-graph
- "Fork it. Extend it. Transform cancer data."

---

## **05:00 – 05:30 | End Screen**

**Visuals:**  
- Thank you screen  
- Key links  
- Subscribe / Follow animation

**Narration:**
> "Thanks for watching!  
> Try it yourself with Docker in under 2 minutes.  
> Link in the description.  
> Let's build the future of oncology data together."

---

## **Production Notes**

- **Total estimated runtime:** ~5 minutes
- **Key calls to action:** Docker one-liner, GitHub link, "Star the repo"
- **Suggested thumbnail:** Animated GIF of the patient journey + bold text "FHIR → Graph in 5 min"
- **Chapters (YouTube):**
  1. 00:00 – Introduction
  2. 01:10 – Docker Demo
  3. 02:30 – GraphDB Exploration
  4. 03:30 – Advanced Features
  5. 04:20 – Why It Matters

---

**Ready to record!** This script is optimized for clarity, engagement, and conversion.
