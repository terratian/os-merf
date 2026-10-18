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
from environmental_shocks import EnvironmentalShockEngine

class EconomicSimulationEngine:
    """
    Evaluates thermodynamic feasibility by parsing factual multi-year drought loops
    and empirical agricultural constants directly from regional JSON profiles.
    """
    def __init__(self, profile_path):
        self.profile = self.load_profile(profile_path)
        
        # Ingest demographic matrix constants
        demo = self.profile["demographic_constants"]
        self.population = demo["baseline_population"]
        self.base_metabolic_cost = demo["daily_metabolic_cost_per_capita"]
        
        # Ingest agricultural matrix constants
        agri = self.profile["agricultural_matrix"]
        self.base_caloric_yield = agri["terrace_yield_kcal_per_capita"]
        
        # Ingest logistical friction matrices
        self.friction = self.profile["logistical_friction_coefficients"]
        
        # Initialize the climate engine with the baseline factual yield
        self.shock_engine = EnvironmentalShockEngine(baseline_yield=self.base_caloric_yield)

    def load_profile(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Target regional profile matrix not found: {path}")
        with open(path, 'r') as f:
            return json.load(f)

    def execute_profile_timeline(self, project_tonnage, distance_km, elevation_gain_m, utility_coefficient):
        """
        Parses the factual multi-year climate loop embedded inside the JSON profile
        and evaluates metabolic survival thresholds year-by-year.
        """
        # Ingest the historical paleoclimatic/academic shock loop from the profile
        historical_timeline = self.profile.get("historical_climate_loop", [])
        if not historical_timeline:
            return {"status": "ERROR", "reason": "No historical climate loop array found in profile"}

        # Calculate localized transport friction variables
        terrain_multiplier = self.friction["rough_terrain_caloric_expenditure_multiplier"]
        incline_penalty_factor = (elevation_gain_m / 100) * self.friction["vertical_incline_penalty_per_100m"]
        
        base_kinetic_kcal_per_ton_km = 3500
        annual_kinetic_cost = (project_tonnage * distance_km * base_kinetic_kcal_per_ton_km * terrain_multiplier)
        if incline_penalty_factor > 0:
            annual_kinetic_cost *= incline_penalty_factor

        simulation_log = []
        cumulative_surplus_pool = 0

        for year_data in historical_timeline:
            year = year_data["year"]
            active_shock = year_data["environmental_event"]
            
            # Use the environmental engine to generate the exact yield adjusted by the recorded event
            current_yield = self.shock_engine.generate_yearly_yield(shock_type=active_shock)

            # Calculate annual metabolic bandwidth
            total_available_calories = self.population * current_yield * 365
            societal_maintenance_calories = self.population * self.base_metabolic_cost * 365
            yearly_surplus = total_available_calories - societal_maintenance_calories
            
            net_yearly_balance = yearly_surplus - annual_kinetic_cost
            cumulative_surplus_pool += net_yearly_balance

            status = "STABLE"
            reason = "Metabolic bandwidth sustained"

            if cumulative_surplus_pool < 0:
                if utility_coefficient == 0:
                    status = "SYSTEMIC_COLLAPSE"
                    reason = f"Bankruptcy in Year {year} under factual {active_shock} loop condition"
                else:
                    retained_value = annual_kinetic_cost * utility_coefficient
                    if (cumulative_surplus_pool + retained_value) > 0:
                        status = "SUSTAINED_VIA_UTILITY"
                        reason = "Caloric deficit offset by infrastructure utility returns"
                    else:
                        status = "TOTAL_SYSTEMIC_COLLAPSE"
                        reason = f"catastrophic failure: System overwhelmed by factual multi-year {active_shock} shock loop"

            simulation_log.append({
                "year": year,
                "event": active_shock,
                "net_yearly_balance_kcal": round(net_yearly_balance, 2),
                "cumulative_pool_kcal": round(cumulative_surplus_pool, 2),
                "status": status,
                "reason": reason
            })

            if status in ["SYSTEMIC_COLLAPSE", "TOTAL_SYSTEMIC_COLLAPSE"]:
                break

        return simulation_log

if __name__ == "__main__":
    profile_target = "simulation_engine/regional_profiles/andes_profile.json"
    try:
        engine = EconomicSimulationEngine(profile_target)
        print("OS-MERF Factual JSON Parser Loop Initialized successfully.")
    except Exception as e:
        print(f"Engine Fault: {str(e)}")
