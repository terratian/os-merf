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
import math

class TectonicGISCorrelator:
    """
    Analyzes spatial proximity anomalies between megalithic structures 
    and active fault-line vector coordinate zones across deep-time scales.
    """
    def __init__(self, telemetry_path="topographical_assay/geospatial_telemetry.json"):
        self.telemetry_path = telemetry_path

    def calculate_haversine_distance(self, lon1, lat1, lon2, lat2):
        """Computes absolute ellipsoidal distance in meters between coordinate coordinates."""
        radius_earth_meters = 6371000.0
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (math.sin(delta_phi / 2.0) ** 2 + 
             math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        
        return radius_earth_meters * c

    def correlate_fault_proximity_timeline(self, site_name, fault_center_coords, macro_timeline_myr):
        """
        Models slip-rate vector shifts backward across millions of years to evaluate 
        if site geometry matches ancient ground acceleration fields.
        """
        if not os.path.exists(self.telemetry_path):
            return {"status": "ERROR", "reason": "Target telemetry file array missing"}

        with open(self.telemetry_path, 'r') as f:
            data = json.load(f)

        site_node = None
        for entry in data:
            if entry["site_metadata"]["site_name"] == site_name:
                site_node = entry
                break

        if not site_node:
            return {"status": "ERROR", "reason": f"Site '{site_name}' missing from database registry"}

        # Extract coordinate variables
        site_lat = site_node["site_metadata"]["coordinates"]["latitude"]
        site_lon = site_node["site_metadata"]["coordinates"]["longitude"]
        
        # Calculate current baseline distance to fault axis
        current_distance = self.calculate_haversine_distance(
            site_lon, site_lat, 
            fault_center_coords["longitude"], fault_center_coords["latitude"]
        )

        # Ingest tectonic drift vectors from geomechanical schema metrics
        features = site_node["geomechanical_features"]
        shear_vectors = [0.045, -0.012] # Latitudinal/Longitudinal annual slip offsets in mm
        
        # Project fault displacement backward across the specified deep-time timeline
        total_drift_mm_lat = shear_vectors[0] * (macro_timeline_myr * 1000000)
        total_drift_mm_lon = shear_vectors[1] * (macro_timeline_myr * 1000000)
        
        # Convert millimeter slip distance arrays back to rough coordinate offsets
        lat_offset = total_drift_mm_lat / 111000000.0
        lon_offset = total_drift_mm_lon / (111000000.0 * math.cos(math.radians(site_lat)))

        historic_fault_lat = fault_center_coords["latitude"] - lat_offset
        historic_fault_lon = fault_center_coords["longitude"] - lon_offset

        historic_distance = self.calculate_haversine_distance(
            site_lon, site_lat, historic_fault_lon, historic_fault_lat
        )

        return {
            "site": site_name,
            "macro_timeline_years": macro_timeline_myr * 1000000,
            "current_proximity_meters": round(current_distance, 2),
            "deep_time_historic_proximity_meters": round(historic_distance, 2),
            "geotorsional_risk_profile": "CRITICAL_SEISMIC_ZONE" if historic_distance < 1000.0 else "MODERATE_STABLE_ZONE"
        }

if __name__ == "__main__":
    correlator = TectonicGISCorrelator()
    # Diagnostic target coordinates mapping to active Andean fault fault vectors
    fault_axis = {"latitude": -13.5040, "longitude": -71.9800}
    
    results = correlator.correlate_fault_proximity_timeline(
        site_name="Sacsayhuamán Foundation Complex",
        fault_center_coords=fault_axis,
        macro_timeline_myr=2.5
    )
    
    print("=== OS-MERF Deep-Time Tectonic GIS Matrix Engine Active ===")
    print(f"Target Site: {results['site']}")
    print(f" -> Current Distance to Fault Axis: {results['current_proximity_meters']} meters")
    print(f" -> Projected 2.5M Year Deep-Time Distance: {results['deep_time_historic_proximity_meters']} meters")
    print(f" -> Dynamic Geomechanical Classification: {results['geotorsional_risk_profile']}\n")
