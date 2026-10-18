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
import json
import os
import sys
from metabolic_model import EconomicSimulationEngine

class GeospatialEconomicLinker:
    """
    Ingests geospatial telemetry vectors and links them to the macroeconomic 
    simulation engine loop to calculate the dynamic footprint of ancient infrastructure.
    """
    def __init__(self, telemetry_path):
        self.telemetry_path = telemetry_path
        self.telemetry_data = self.load_telemetry()

    def load_telemetry(self):
        if not os.path.exists(self.telemetry_path):
            raise FileNotFoundError(f"Geospatial telemetry source matrix missing: {self.telemetry_path}")
        with open(self.telemetry_path, 'r') as f:
            return json.load(f)

    def execute_linked_analysis(self, target_site_name):
        # 1. Locate targeted site node within the telemetry array
        site_node = None
        for entry in self.telemetry_data:
            if entry["site_metadata"]["site_name"] == target_site_name:
                site_node = entry
                break

        if not site_node:
            return {"status": "ERROR", "reason": f"Site '{target_site_name}' missing from telemetry registry"}

        # 2. Extract profile path mapping configurations
        profile_file = site_node["regional_economic_abundance"]["associated_profile_matrix"]
        profile_full_path = os.path.join("simulation_engine", "regional_profiles", profile_file)

        # 3. Extract structural vector data from the telemetry node
        features = site_node["geomechanical_features"]
        tonnage = features["peak_block_mass_tons"] * 10  # Scaled to project footprint array
        
        # Determine basic utility weighting values
        has_geotorsional_defense = len(features["geotorsional_adaptations"]) > 0
        utility_coeff = 0.45 if has_geotorsional_defense else 0.0

        # 4. Initialize and run the metabolic model engine using geospatial variables
        try:
            simulator = EconomicSimulationEngine(profile_full_path)
            # Standard structural bounds baseline: 12 km transit, 150m lift
            simulation_results = simulator.execute_profile_timeline(
                project_tonnage=tonnage,
                distance_km=12.0,
                elevation_gain_m=150,
                utility_coefficient=utility_coeff
            )
            return {
                "site": target_site_name,
                "coordinates": site_node["site_metadata"]["coordinates"],
                "geotorsional_utility_applied": utility_coeff,
                "timeline_log": simulation_results
            }
        except Exception as e:
            return {"status": "ENGINE_FAULT", "reason": str(e)}

if __name__ == "__main__":
    telemetry_target = "topographical_assay/geospatial_telemetry.json"
    
    try:
        linker = GeospatialEconomicLinker(telemetry_target)
        target = "Sacsayhuamán Foundation Complex"
        audit = linker.execute_linked_analysis(target)
        
        print("=== OS-MERF Geospatial-Economic Linker Loop Active ===")
        print(f"Site Node: {audit['site']}")
        print(f"Coordinates: Lat {audit['coordinates']['latitude']} | Lon {audit['coordinates']['longitude']}")
        print(f"Final Year State: {audit['timeline_log'][-1]['status']}")
        print(f"Details: {audit['timeline_log'][-1]['reason']}\n")
    except Exception as e:
        print(f"Linker Initialization Fault: {str(e)}")
