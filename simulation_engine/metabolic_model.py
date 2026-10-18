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
    Evaluates the thermodynamic and metabolic feasibility of ancient lithic projects
    across multi-year timelines by incorporating dynamic JSON profile constants
    and stochastic environmental shock data models.
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
        self.base_caloric_yield = agri["terrace_yield_kcal_per_capita"]
        
        # Ingest logistical friction matrices
        self.friction = self.profile["logistical_friction_coefficients"]
        
        # Initialize the localized climate engine
        self.shock_engine = EnvironmentalShockEngine(baseline_yield=self.base_caloric_yield)

    def load_profile(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Target regional profile matrix not found: {path}")
        with open(path, 'r') as f:
            return json.load(f)

    def execute_multi_year_matrix(self, timeline_years, project_tonnage, distance_km, elevation_gain_m, utility_coefficient, shock_schedule=None):
        # Generate the environmental agricultural timeline matrix
        climate_timeline = self.shock_engine.run_multi_year_simulation(timeline_years, shock_schedule)
        
        # Calculate localized transport friction variables
        terrain_multiplier = self.friction["rough_terrain_caloric_expenditure_multiplier"]
        incline_penalty_factor = (elevation_gain_m / 100) * self.friction["vertical_incline_penalty_per_100m"]
        
        base_kinetic_kcal_per_ton_km = 3500
        annual_kinetic_cost = (project_tonnage * distance_km * base_kinetic_kcal_per_ton_km * terrain_multiplier)
        if incline_penalty_factor > 0:
            annual_kinetic_cost *= incline_penalty_factor

        simulation_log = []
        cumulative_surplus_pool = 0

        for year_data in climate_timeline:
            year = year_data["year"]
            current_yield = year_data["yield_per_capita"]
            active_shock = year_data["event"]

            # Calculate metabolic pool values for the current year cycle
            total_available_calories = self.population * current_yield * 365
            societal_maintenance_calories = self.population * self.base_metabolic_cost * 365
            yearly_surplus = total_available_calories - societal_maintenance_calories
            
            # Deduct infrastructure construction costs
            net_yearly_balance = yearly_surplus - annual_kinetic_cost
            cumulative_surplus_pool += net_yearly_balance

            # Evaluate system stability flags
            status = "STABLE"
            reason = "Metabolic bandwidth sustained"

            if cumulative_surplus_pool < 0:
                if utility_coefficient == 0:
                    status = "SYSTEMIC_COLLAPSE"
                    reason = f"Caloric bankruptcy triggered in Year {year} via non-utility architecture under {active_shock} stress"
                else:
                    retained_value = annual_kinetic_cost * utility_coefficient
                    if (cumulative_surplus_pool + retained_value) > 0:
                        status = "SUSTAINED_VIA_UTILITY"
                        reason = "Caloric stress structurally mitigated by infrastructure system utility returns"
                    else:
                        status = "TOTAL_SYSTEMIC_COLLAPSE"
                        reason = f"Catastrophic failure: System utility threshold overwhelmed by multi-year {active_shock} degradation"

            simulation_log.append({
                "year": year,
                "event": active_shock,
                "net_yearly_balance_kcal": round(net_yearly_balance, 2),
                "cumulative_pool_kcal": round(cumulative_surplus_pool, 2),
                "status": status,
                "reason": reason
            })

            # Terminate simulation if total systemic failure occurs
            if status in ["SYSTEMIC_COLLAPSE", "TOTAL_SYSTEMIC_COLLAPSE"]:
                break

        return simulation_log

if __name__ == "__main__":
    profile_target = "simulation_engine/regional_profiles/andes_profile.json"
    
    try:
        engine = EconomicSimulationEngine(profile_target)
        
        # Test Parameters: 5-Year timeline with an El Niño scale drought hitting in Year 3
        custom_shocks = {3: "drought"}
        
        results = engine.execute_multi_year_matrix(
            timeline_years=5,
            project_tonnage=15000,
            distance_km=6,
            elevation_gain_m=250,
            utility_coefficient=0,
            shock_schedule=custom_shocks
        )
        
        print(f"=== Running Protected OS-MERF Multi-Year Stress Array ===")
        for log in results:
            print(f"Year {log['year']} | Event: {log['event']} | Status: {log['status']}")
            print(f" -> Cumulative Pool: {log['cumulative_pool_kcal']} kcal")
            print(f" -> Diagnosis: {log['reason']}\n")
            
    except Exception as e:
        print(f"Engine Fault: {str(e)}")
