#!/usr/bin/env python3
"""
SHACL Validation Report Generator for Patient Event Graph
"""

from pathlib import Path
from pyshacl import validate
import sys

DATA_FILE = Path(__file__).parent.parent / "data" / "samples" / "colorectal_patient_event_graph.ttl"
SHACL_FILE = Path(__file__).parent.parent / "shacl" / "patient_event_shacl.ttl"
REPORT_FILE = Path(__file__).parent.parent / "output" / "shacl_validation_report.txt"


def generate_validation_report():
    print("=" * 70)
    print("SHACL VALIDATION REPORT - Patient Event Graph")
    print("=" * 70)

    if not DATA_FILE.exists():
        print(f"❌ Data file not found: {DATA_FILE}")
        sys.exit(1)

    if not SHACL_FILE.exists():
        print(f"❌ SHACL file not found: {SHACL_FILE}")
        sys.exit(1)

    print(f"\nValidating: {DATA_FILE.name}")
    print(f"Using SHACL: {SHACL_FILE.name}\n")

    conforms, results_graph, results_text = validate(
        data_graph=str(DATA_FILE),
        shacl_graph=str(SHACL_FILE),
        inference='rdfs',
        advanced=True
    )

    # Generate report
    report = []
    report.append("=" * 70)
    report.append("SHACL VALIDATION REPORT")
    report.append("=" * 70)
    report.append(f"\nData File: {DATA_FILE.name}")
    report.append(f"SHACL File: {SHACL_FILE.name}")
    report.append(f"Result: {'✅ CONFORMS' if conforms else '❌ DOES NOT CONFORM'}")
    report.append("\n" + "-" * 70)

    if not conforms:
        report.append("\nVIOLATIONS FOUND:\n")
        report.append(results_text)
    else:
        report.append("\n✅ All SHACL constraints are satisfied!")
        report.append("\nThe patient event graph is valid according to the defined rules.")

    report.append("\n" + "=" * 70)
    report_text = "\n".join(report)

    # Save report
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(report_text)
    print(f"\n📄 Report saved to: {REPORT_FILE}")

    return conforms


if __name__ == "__main__":
    generate_validation_report()