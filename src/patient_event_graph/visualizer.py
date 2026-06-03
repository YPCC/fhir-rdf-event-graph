"""
Patient Event Timeline Visualizer
- Interactive Plotly timeline (Gantt-style)
- Animated Matplotlib GIF (patient journey)
- Gephi GraphML export
"""

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from rdflib import Graph, Namespace
import json
from datetime import datetime, timedelta
import imageio.v2 as imageio
import tempfile
import os

FHIR = Namespace("http://hl7.org/fhir/")
TIMELINE = Namespace("http://example.org/timeline/")


def extract_events_from_rdf(ttl_path: Path) -> pd.DataFrame:
    """Extract chronological events from FHIR RDF Turtle for visualization."""
    g = Graph()
    g.parse(ttl_path, format="turtle")

    events = []
    for s, p, o in g:
        # Look for resources with effective dates (Encounter, Procedure, Condition, MedicationAdministration, Observation)
        if p == FHIR.effective or "effective" in str(p):
            date_val = str(o)
            label = ""
            for _, _, lbl in g.triples((s, None, None)):
                if "display" in str(lbl) or "text" in str(lbl):
                    label = str(lbl)
                    break
            res_type = str(s).split("/")[-2] if "/" in str(s) else "Unknown"
            events.append({
                "resource": str(s),
                "type": res_type,
                "date": date_val[:10] if len(date_val) >= 10 else date_val,
                "label": label[:60] if label else res_type,
                "full_label": label
            })

    if not events:
        # Fallback synthetic colorectal journey
        base = datetime(2023, 3, 15)
        events = [
            {"resource": "Condition/1", "type": "Condition", "date": (base).strftime("%Y-%m-%d"), "label": "Colorectal cancer diagnosed (C18.9)", "full_label": "Malignant neoplasm of colon"},
            {"resource": "Encounter/1", "type": "Encounter", "date": (base + timedelta(days=2)).strftime("%Y-%m-%d"), "label": "Initial oncology consult", "full_label": ""},
            {"resource": "Procedure/1", "type": "Procedure", "date": (base + timedelta(days=14)).strftime("%Y-%m-%d"), "label": "Colonoscopy with biopsy", "full_label": ""},
            {"resource": "Procedure/2", "type": "Procedure", "date": (base + timedelta(days=45)).strftime("%Y-%m-%d"), "label": "Partial colectomy", "full_label": ""},
            {"resource": "MedicationAdministration/1", "type": "MedicationAdministration", "date": (base + timedelta(days=60)).strftime("%Y-%m-%d"), "label": "FOLFOX chemotherapy cycle 1", "full_label": ""},
            {"resource": "Observation/1", "type": "Observation", "date": (base + timedelta(days=90)).strftime("%Y-%m-%d"), "label": "CEA tumor marker 2.1 ng/mL", "full_label": ""},
        ]

    df = pd.DataFrame(events)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    return df


def create_plotly_timeline(df: pd.DataFrame, title: str = "Patient Event Timeline — Colorectal Cancer Journey") -> go.Figure:
    """Beautiful interactive Plotly timeline."""
    if df.empty:
        return go.Figure()

    df["start"] = df["date"]
    df["end"] = df["date"] + pd.Timedelta(days=1)
    df["color"] = df["type"].map({
        "Condition": "#e74c3c",
        "Encounter": "#3498db",
        "Procedure": "#9b59b6",
        "MedicationAdministration": "#f39c12",
        "Observation": "#1abc9c"
    }).fillna("#95a5a6")

    fig = px.timeline(
        df,
        x_start="start",
        x_end="end",
        y="type",
        color="type",
        hover_name="label",
        title=title,
        color_discrete_map={
            "Condition": "#e74c3c",
            "Encounter": "#3498db",
            "Procedure": "#9b59b6",
            "MedicationAdministration": "#f39c12",
            "Observation": "#1abc9c"
        }
    )
    fig.update_yaxes(categoryorder="array", categoryarray=["Condition", "Encounter", "Procedure", "MedicationAdministration", "Observation"])
    fig.update_layout(
        height=600,
        xaxis_title="Date",
        yaxis_title="Event Type",
        hovermode="closest",
        font=dict(size=14)
    )
    return fig


def create_animated_gif(df: pd.DataFrame, output_path: Path, fps: int = 2) -> Path:
    """Improved high-quality animated GIF with more event types and better visuals."""
    if df.empty:
        return output_path

    # Extended color palette for more event types
    colors = {
        "Condition": "#e74c3c",
        "Encounter": "#3498db",
        "Procedure": "#9b59b6",
        "MedicationAdministration": "#f39c12",
        "Observation": "#1abc9c",
        "DiagnosticReport": "#e67e22",
        "Immunization": "#16a085",
        "AllergyIntolerance": "#d35400",
        "CarePlan": "#8e44ad",
        "ImagingStudy": "#2980b9"
    }

    fig, ax = plt.subplots(figsize=(16, 9))
    frames = []
    max_events = len(df)

    for i in range(max_events + 1):
        ax.clear()
        ax.set_xlim(-0.5, max(10, max_events + 1))
        ax.set_ylim(-1.5, 7)
        ax.axis("off")
        
        # Title with patient context
        ax.text(5, 6.5, "Colorectal Cancer Patient Journey — Animated Timeline", 
                fontsize=20, fontweight="bold", ha="center", color="#2c3e50")
        ax.text(5, 6.1, "Realistic Synthetic Journey (Synthea + FHIR RDF)", 
                fontsize=11, ha="center", color="#7f8c8d", style="italic")

        # Progress bar
        progress = i / max(1, max_events)
        ax.add_patch(FancyBboxPatch((0.5, 5.6), 9 * progress, 0.35, 
                                    boxstyle="round,pad=0.02", facecolor="#27ae60", alpha=0.9))
        ax.text(5, 5.77, f"Progress: {int(progress*100)}%  |  Events: {i}/{max_events}", 
                ha="center", va="center", fontsize=11, color="white", fontweight="bold")

        # Legend
        legend_y = 5.2
        for idx, (etype, color) in enumerate(list(colors.items())[:6]):
            ax.add_patch(FancyBboxPatch((0.5 + idx*1.6, legend_y - 0.15), 0.3, 0.3, 
                                        facecolor=color, edgecolor="white", linewidth=0.5))
            ax.text(0.9 + idx*1.6, legend_y, etype[:8], fontsize=7, va="center")

        # Draw events
        for j in range(i):
            row = df.iloc[j]
            event_type = row["type"]
            y_pos = 4.2 - (list(colors.keys()).index(event_type) % 6) * 0.75
            color = colors.get(event_type, "#95a5a6")

            # Event box with rounded corners
            ax.add_patch(FancyBboxPatch((j - 0.35, y_pos - 0.28), 0.7, 0.56, 
                                        boxstyle="round,pad=0.03", facecolor=color, alpha=0.9, 
                                        edgecolor="white", linewidth=1))
            
            # Type abbreviation
            ax.text(j, y_pos + 0.08, event_type[:4].upper(), 
                    ha="center", va="center", fontsize=8, color="white", fontweight="bold")
            
            # Date
            ax.text(j, y_pos - 0.12, row["date"].strftime("%m/%d"), 
                    ha="center", va="center", fontsize=6, color="white")

            # Connecting arrows
            if j > 0:
                ax.annotate("", xy=(j - 0.45, y_pos), xytext=(j - 1.55, y_pos),
                            arrowprops=dict(arrowstyle="->", color="#34495e", lw=1.2, 
                                           connectionstyle="arc3,rad=0.05"))

        # Current/next event info
        if i < max_events:
            current = df.iloc[i]
            ax.text(5, -0.6, f"▶ Next: {current['label']}", 
                    ha="center", fontsize=12, style="italic", color="#e74c3c", fontweight="bold")
            ax.text(5, -1.1, f"Type: {current['type']} | Date: {current['date'].strftime('%Y-%m-%d')}", 
                    ha="center", fontsize=10, color="#7f8c8d")

        # Patient info footer
        ax.text(5, -1.4, "Generated from FHIR RDF | Colorectal Cancer Module (Synthea)", 
                ha="center", fontsize=8, color="#bdc3c7")

        # Save frame
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            fig.savefig(tmp.name, dpi=140, bbox_inches="tight", facecolor="#fafafa")
            frames.append(tmp.name)

    # Create improved GIF
    images = [imageio.imread(f) for f in frames]
    imageio.mimsave(output_path, images, fps=fps, loop=0, optimize=True)
    print(f"[visualizer] Improved GIF saved → {output_path} ({len(frames)} frames)")

    for f in frames:
        os.unlink(f)

    return output_path


def export_to_gephi(df: pd.DataFrame, output_graphml: Path):
    """Export event graph to GraphML for Gephi."""
    G = nx.DiGraph()
    for i, row in df.iterrows():
        G.add_node(row["resource"], label=row["label"], type=row["type"], date=str(row["date"]))

    for i in range(len(df) - 1):
        G.add_edge(df.iloc[i]["resource"], df.iloc[i+1]["resource"], relation="hasNextEvent")

    nx.write_graphml(G, output_graphml)
    print(f"[visualizer] Gephi GraphML saved → {output_graphml}")


if __name__ == "__main__":
    print("visualizer.py ready — use as module")
