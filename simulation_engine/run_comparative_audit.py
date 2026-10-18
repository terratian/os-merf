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

def run_comparative_audit():
    andes_profile = "simulation_engine/regional_profiles/andes_profile.json"
    nile_profile = "simulation_engine/regional_profiles/nile_valley_profile.json"

    # Verify both target profile blueprints exist prior to engine init
    if not os.path.exists(andes_profile) or not os.path.exists(nile_profile):
        print("Error: Missing required profile blueprints for comparative analysis.")
        sys.exit(1)

    print("=== Initializing OS-MERF Comparative Profile Audit ===")
    andes_engine = EconomicSimulationEngine(andes_profile)
    nile_engine = EconomicSimulationEngine(nile_profile)

    # Establish shared testing matrix configurations
    simulation_years = 5
    shared_shocks = {3: "drought"}  # Synchronized environmental shock hit in Year 3
    
    # Standard testing load parameters (Moving 15,000 tons over 6 km)
    tonnage = 15000
    distance = 6
    elevation_lift = 200

    print(f"Project Parameters: {tonnage} tons | {distance} km | {elevation_lift}m vertical lift")
    print(f"Environmental Timeline: {simulation_years}-Year Cycle [Year 3 Shock: Drought]\n")

    # Execute simulation loops for both profiles
    andes_log = andes_engine.execute_multi_year_matrix(
        timeline_years=simulation_years,
        project_tonnage=tonnage,
        distance_km=distance,
        elevation_gain_m=elevation_lift,
        utility_coefficient=0,
        shock_schedule=shared_shocks
    )

    nile_log = nile_engine.execute_multi_year_matrix(
        timeline_years=simulation_years,
        project_tonnage=tonnage,
        distance_km=distance,
        elevation_gain_m=elevation_lift,
        utility_coefficient=0,
        shock_schedule=shared_shocks
    )

    # Format and output side-by-side comparative telemetry matrices
    print(f"{'Year':<6} | {'Event':<12} | {'Andean Status':<18} | {'Nile Status':<18}")
    print("-" * 65)

    max_years = max(len(andes_log), len(nile_log))
    for i in range(max_years):
        year = i + 1
        event = shared_shocks.get(year, "Baseline")
        
        andes_status = andes_log[i]["status"] if i < len(andes_log) else "HALTED"
        nile_status = nile_log[i]["status"] if i < len(nile_log) else "HALTED"
        
        print(f"{year:<6} | {event:<12} | {andes_status:<18} | {nile_status:<18}")

    print("\n=== Comparative Evaluation Concluded ===")

if __name__ == "__main__":
    run_comparative_audit()
