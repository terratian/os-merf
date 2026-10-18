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

class EconomicSimulationEngine:
    """
    Evaluates the thermodynamic and metabolic feasibility of ancient lithic projects
    by ingesting real-world profile data and calculating dynamic labor costs.
    """
    def __init__(self, profile_path):
        self.profile = self.load_profile(profile_path)
        
        # Ingest demographic matrix constants
        demo = self.profile["demographic_constants"]
        self.population = demo["baseline_population"]
        self.labor_pool_pct = demo["active_labor_pool_pct"]
        self.base_metabolic_cost = demo["daily_metabolic_cost_per_capita"]
        
        # Ingest agricultural matrix constants
        agri = self.profile["agricultural_matrix"]
        self.caloric_yield = agri["terrace_yield_kcal_per_capita"]
        
        # Ingest logistical friction matrices
        self.friction = self.profile["logistical_friction_coefficients"]

    def load_profile(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Target regional profile matrix not found: {path}")
        with open(path, 'r') as f:
            return json.load(f)

    def calculate_feasibility(self, project_tonnage, distance_km, elevation_gain_m, utility_coefficient):
        # Calculate base regional energy availability
        total_available_calories = self.population * self.caloric_yield * 365
        societal_maintenance_calories = self.population * self.base_metabolic_cost * 365
        caloric_surplus = total_available_calories - societal_maintenance_calories

        if caloric_surplus <= 0:
            return {"status": "CRITICAL_COLLAPSE", "reason": "Subsistence deficit under local environmental limits"}

        # Calculate dynamic transport friction based on physical landscape variables
        terrain_multiplier = self.friction["rough_terrain_caloric_expenditure_multiplier"]
        incline_penalty_factor = (elevation_gain_m / 100) * self.friction["vertical_incline_penalty_per_100m"]
        
        # Caloric cost equation updated with profile friction constraints
        base_kinetic_kcal_per_ton_km = 3500
        adjusted_kinetic_cost = (project_tonnage * distance_km * base_kinetic_kcal_per_ton_km * terrain_multiplier)
        if incline_penalty_factor > 0:
            adjusted_kinetic_cost *= incline_penalty_factor

        remaining_surplus = caloric_surplus - adjusted_kinetic_cost

        if remaining_surplus < 0 and utility_coefficient == 0:
            return {
                "status": "SYSTEMIC_COLLAPSE",
                "remaining_surplus_kcal": remaining_surplus,
                "reason": "Caloric bankruptcy driven by non-utility construction under strict regional friction coefficients"
            }
        elif remaining_surplus < 0 and utility_coefficient > 0:
            retained_value = adjusted_kinetic_cost * utility_coefficient
            if (remaining_surplus + retained_value) > 0:
                return {
                    "status": "SUSTAINED_VIA_UTILITY",
                    "remaining_surplus_kcal": remaining_surplus,
                    "reason": "Initial labor deficit structurally offset by macro engineering infrastructure utility"
                }

        return {
            "status": "STABLE_EXECUTION",
            "remaining_surplus_kcal": remaining_surplus,
            "reason": "Territory possesses sufficient metabolic bandwidth to absorb construction profile limits"
        }

if __name__ == "__main__":
    # Internal validation pathway executing against the local profile blueprint
    profile_target = "simulation_engine/regional_profiles/andes_profile.json"
    
    try:
        engine = EconomicSimulationEngine(profile_target)
        # Test Parameters: Moving 12,000 tons, 8 km distance, with 300m total vertical lift
        results = engine.calculate_feasibility(
            project_tonnage=12000, 
            distance_km=8, 
            elevation_gain_m=300, 
            utility_coefficient=0
        )
        print(f"Simulation Status: {results['status']}")
        print(f"Details: {results['reason']}")
    except Exception as e:
        print(f"Engine Fault: {str(e)}")
