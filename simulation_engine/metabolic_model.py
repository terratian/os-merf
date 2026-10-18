# Copyright (C) 2026 Joshua Sultan (GitHub: terratian) | GNU GPL v3
import sys

class EconomicSimulationEngine:
    def __init__(self, population, regional_caloric_yield, worker_allocation_pct):
        self.population = population
        self.base_caloric_yield = regional_caloric_yield
        self.worker_allocation_pct = worker_allocation_pct
        self.base_metabolic_cost = 2500

    def calculate_feasibility(self, project_tonnage, distance_km, utility_coefficient):
        total_available_calories = self.population * self.base_caloric_yield
        societal_maintenance_calories = self.population * self.base_metabolic_cost
        caloric_surplus = total_available_calories - societal_maintenance_calories

        if caloric_surplus <= 0:
            return {"status": "CRITICAL_COLLAPSE", "reason": "Subsistence deficit"}

        total_kinetic_energy_required = project_tonnage * distance_km * 3500
        remaining_surplus = caloric_surplus - total_kinetic_energy_required

        if remaining_surplus < 0 and utility_coefficient == 0:
            return {"status": "SYSTEMIC_COLLAPSE", "reason": "Caloric bankruptcy"}
        
        return {"status": "STABLE_EXECUTION", "remaining_surplus_kcal": remaining_surplus}

if __name__ == "__main__":
    engine = EconomicSimulationEngine(30000, 3500, 0.15)
    print(engine.calculate_feasibility(5000, 10, 0))
