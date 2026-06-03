#!/usr/bin/env python3
"""
FHIR Data Validation using project-fhir-lens
https://github.com/zpak96/project-fhir-lens

This script validates FHIR JSON resources against official HL7 FHIR specifications
before converting to RDF.
"""

import json
from pathlib import Path
import sys

try:
    from fhirlens import fhirlens
except ImportError:
    print("❌ fhirlens not installed. Install with:")
    print("   pip install git+https://github.com/zpak96/project-fhir-lens.git")
    sys.exit(1)


def validate_fhir_resource(resource: dict, resource_type: str = None) -> bool:
    """
    Validate a single FHIR resource using fhirlens.
    """
    try:
        validator = fhirlens.FHIRLens()
        is_valid = validator.validate(resource)
        
        if is_valid:
            print(f"✅ {resource_type or resource.get('resourceType', 'Resource')} is VALID")
            return True
        else:
            print(f"❌ {resource_type or resource.get('resourceType', 'Resource')} is INVALID")
            errors = validator.get_errors()
            for error in errors[:5]:  # Show first 5 errors
                print(f"   - {error}")
            return False
            
    except Exception as e:
        print(f"⚠️  Validation error: {e}")
        return False


def validate_fhir_bundle(bundle: dict) -> bool:
    """
    Validate all resources in a FHIR Bundle.
    """
    if bundle.get("resourceType") != "Bundle":
        print("❌ Input is not a FHIR Bundle")
        return False
    
    print(f"\n🔍 Validating FHIR Bundle with {len(bundle.get('entry', []))} entries...\n")
    
    all_valid = True
    
    for i, entry in enumerate(bundle.get("entry", []), 1):
        resource = entry.get("resource", {})
        resource_type = resource.get("resourceType", "Unknown")
        
        print(f"[{i}] Validating {resource_type}...")
        if not validate_fhir_resource(resource, resource_type):
            all_valid = False
    
    print("\n" + "=" * 60)
    if all_valid:
        print("✅ ALL RESOURCES ARE VALID according to HL7 FHIR R4")
    else:
        print("⚠️  SOME RESOURCES HAVE VALIDATION ISSUES")
    print("=" * 60 + "\n")
    
    return all_valid


def main():
    # Example: Validate our sample Synthea patient
    sample_file = Path(__file__).parent.parent / "data" / "synthea" / "colorectal_sample_patient.json"
    
    if sample_file.exists():
        print(f"Validating sample file: {sample_file.name}")
        with open(sample_file, "r", encoding="utf-8") as f:
            bundle = json.load(f)
        
        validate_fhir_bundle(bundle)
    else:
        print("No sample file found. Please provide a FHIR JSON file to validate.")
        print("Usage: python scripts/validate_fhir.py <path-to-fhir-json>")


if __name__ == "__main__":
    main()