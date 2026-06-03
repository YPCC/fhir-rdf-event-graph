"""
Simple FHIR Fetcher for public servers (HAPI R4) or local Synthea JSON.
Focus on colorectal / cancer patient journeys.
"""

import requests
from pathlib import Path
import json
from typing import Optional


HAPI_BASE = "http://hapi.fhir.org/baseR4"


def fetch_patient_bundle(patient_id: Optional[str] = None, condition_code: str = "363406005") -> dict:
    """
    Fetch a realistic patient bundle.
    Priority: specific patient_id → search for colorectal Condition → fallback to public example.
    """
    if patient_id:
        url = f"{HAPI_BASE}/Patient/{patient_id}/$everything"
        resp = requests.get(url, headers={"Accept": "application/fhir+json"}, timeout=30)
        if resp.ok:
            return resp.json()

    # Search for patients with colorectal cancer condition
    search_url = f"{HAPI_BASE}/Condition?code=http://snomed.info/sct|{condition_code}&_include=Condition:subject&_count=5"
    resp = requests.get(search_url, headers={"Accept": "application/fhir+json"}, timeout=30)
    if resp.ok:
        bundle = resp.json()
        if bundle.get("entry"):
            # Return first full patient everything bundle
            patient_ref = bundle["entry"][0]["resource"]["subject"]["reference"]
            pid = patient_ref.split("/")[-1]
            everything_url = f"{HAPI_BASE}/Patient/{pid}/$everything"
            everything_resp = requests.get(everything_url, headers={"Accept": "application/fhir+json"}, timeout=30)
            if everything_resp.ok:
                return everything_resp.json()

    # Final fallback: well-known public test patient with rich data
    print("[fetcher] Using public fallback patient (rich history)")
    fallback_url = f"{HAPI_BASE}/Patient/example/$everything"
    resp = requests.get(fallback_url, headers={"Accept": "application/fhir+json"}, timeout=30)
    return resp.json() if resp.ok else {"resourceType": "Bundle", "type": "searchset", "entry": []}


def load_local_synthea(path: Path) -> dict:
    """Load a local Synthea FHIR Bundle JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    bundle = fetch_patient_bundle()
    print(f"Fetched bundle with {len(bundle.get('entry', []))} resources")
    print(json.dumps(bundle, indent=2)[:2000])
