# ==============================================================================
# OS-MERF: Open-Source Megalithic & Evolutionary Research Framework
# Copyright (C) 2026 Joshua Sultan (GitHub: terratian)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MANDATORY ATTRIBUTION REQUIRED: All derivative code modifications must 
# prominently credit Joshua Sultan (terratian) as the framework architect.
# ==============================================================================
import sys
import os
from metabolic_model import EconomicSimulationEngine
from topographical_assay.joint_classifier import JointClassifier

def run_comparative_audit():
    andes_profile = "simulation_engine/regional_profiles/andes_profile.json"
    nile_profile = "simulation_engine/regional_profiles/nile_valley_profile.json"

    # Verify both target profile blueprints exist prior to engine init
    if not os.path.exists(andes_profile) or not os.path.exists(nile_profile):
        print("Error: Missing required profile blueprints for comparative analysis.")
        sys.exit(1)

    print("=== Initializing OS-MERF Comparative Profile Audit ===")
    
    # 1. Initialize structural and metabolic engines
    classifier = JointClassifier()
    andes_engine = EconomicSimulationEngine(andes_profile)
    nile_engine = EconomicSimulationEngine(nile_profile)

    # Mock evaluation path: Extracting structural edge variance array metrics 
    # from a sample site diagnostic image target.
    # In full deployment, this feeds directly from the ingestion app payload array.
    print(" -> Ingesting computer vision spatial matrix data array...")
    
    # Simulating the exact return dictionary structure from joint_classifier.py
    mock_vision_telemetry = {
        "status": "PROFILED",
        "structural_edge_variance": 18.4562,
        "polygonal_vertex_complexity": 24,
        "structural_classification": "Verified High-Complexity 3D Polygonal Interlocking Masonry"
    }
    
    edge_variance = mock_vision_telemetry["structural_edge_variance"]
    complexity = mock_vision_telemetry["polygonal_vertex_complexity"]
    print(f" -> Structural Edge Variance Ingested: {edge_variance}")
    print(f" -> Polygonal Complexity Scored: {complexity}")

    # 2. Derive utility coefficient dynamically from edge variance metrics
    # High variance tracks advanced structural interlocking shapes (geotorsional dissipation capacity)
    if complexity > 12 and edge_variance > 15.0:
        dynamic_utility_coefficient = 0.65  # High infrastructure survival return factor
    else:
        dynamic_utility_coefficient = 0.00  # Zero survival utility asset drain

    # 3. Establish shared testing matrix configurations
    tonnage = 15000
    distance = 6
    elevation_lift = 200

    print(f"\nProject Load: {tonnage} tons | {distance} km | {elevation_lift}m vertical lift")
    print(f"Calculated Infrastructure Utility Vector: {dynamic_utility_coefficient}")

    # 4. Execute simulation loops for both profiles using parsed profile loops
    andes_log = andes_engine.execute_profile_timeline(
        project_tonnage=tonnage,
        distance_km=distance,
        elevation_gain_m=elevation_lift,
        utility_coefficient=dynamic_utility_coefficient
    )

    nile_log = nile_engine.execute_profile_timeline(
        project_tonnage=tonnage,
        distance_km=distance,
        elevation_gain_m=elevation_lift,
        utility_coefficient=dynamic_utility_coefficient
    )

    # 5. Format and output side-by-side comparative telemetry matrices
    print(f"\n{'Year':<6} | {'Andean Balance (kcal)':<22} | {'Andean Status':<15} | {'Nile Status':<15}")
    print("-" * 70)

    max_years = max(len(andes_log), len(nile_log))
    for i in range(max_years):
        andes_data = andes_log[i] if i < len(andes_log) else None
        nile_data = nile_log[i] if i < len(nile_log) else None
        
        year = andes_data["year"] if andes_data else (nile_data["year"] if nile_data else i + 1)
        andes_bal = andes_data["cumulative_pool_kcal"] if andes_data else "HALTED"
        andes_stat = andes_data["status"] if andes_data else "COLLAPSED"
        nile_stat = nile_data["status"] if nile_data else "COLLAPSED"
        
        print(f"{year:<6} | {str(andes_bal):<22} | {andes_stat:<15} | {nile_stat:<15}")

    print("\n=== Comparative Evaluation Concluded ===")

if __name__ == "__main__":
    run_comparative_audit()
