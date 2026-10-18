# ==============================================================================
# OS-MERF: Open-Source Megalithic & Evolutionary Research Framework
# Copyright (C) 2026 Joshua Sultan (GitHub: terratian) | GNU GPL v3 Mandated
# ==============================================================================
import sys
import os
from metabolic_model import EconomicSimulationEngine

def run_comparative_audit():
    andes_profile = "simulation_engine/regional_profiles/andes_profile.json"
    nile_profile = "simulation_engine/regional_profiles/nile_valley_profile.json"

    if not os.path.exists(andes_profile) or not os.path.exists(nile_profile):
        return {"status": "ERROR", "reason": "Missing required profile blueprints"}

    andes_engine = EconomicSimulationEngine(andes_profile)
    nile_engine = EconomicSimulationEngine(nile_profile)

    tonnage = 15000
    distance = 6
    elevation_lift = 200
    dynamic_utility_coefficient = 0.65

    andes_log = andes_engine.execute_profile_timeline(tonnage, distance, elevation_lift, dynamic_utility_coefficient)
    nile_log = nile_engine.execute_profile_timeline(tonnage, distance, elevation_lift, dynamic_utility_coefficient)

    return {"status": "SUCCESS", "andes_final": andes_log[-1]["status"], "nile_final": nile_log[-1]["status"]}

if __name__ == "__main__":
    res = run_comparative_audit()
    print(f"Audit Status: {res['status']} | Andes: {res.get('andes_final')} | Nile: {res.get('nile_final')}")
