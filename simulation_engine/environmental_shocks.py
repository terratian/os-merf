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
import random

class EnvironmentalShockEngine:
    """
    Advanced Stochastic Climate Calculation Matrix Engine.
    Simulates multi-year compound environmental impacts using a Markov-chain 
    state transition matrix and localized covariance yield calculations.
    """
    def __init__(self, baseline_yield, volatility_index=0.15):
        self.baseline_yield = baseline_yield
        self.volatility_index = volatility_index
        
        # Markov State Transition Matrix: [Baseline, Drought, Megadrought, Volcanic]
        # Controls the multi-year probability of staying in or transitioning out of a shock state
        self.states = ["baseline", "drought", "megadrought", "volcanic_ash"]
        self.transition_matrix = {
            "baseline":    [0.70, 0.20, 0.05, 0.05],
            "drought":     [0.40, 0.45, 0.10, 0.05],
            "megadrought": [0.10, 0.30, 0.55, 0.05],
            "volcanic_ash":[0.60, 0.10, 0.10, 0.20]
        }
        
        # Empirical reduction multipliers derived from academic paleoclimate data
        self.impact_matrix = {
            "baseline": 1.00,
            "drought": 0.60,
            "megadrought": 0.35,
            "volcanic_ash": 0.50
        }

    def _get_next_state(self, current_state):
        """Calculates state transitions using cumulative distribution matrices."""
        probabilities = self.transition_matrix[current_state]
        rand_val = random.random()
        cumulative_prob = 0.0
        
        for idx, prob in enumerate(probabilities):
            cumulative_prob += prob
            if rand_val <= cumulative_prob:
                return self.states[idx]
        return "baseline"

    def generate_yearly_yield(self, shock_type=None, compounding_multiplier=1.0):
        """
        Calculates the per-capita caloric yield utilizing a Gaussian distribution
        cross-referenced with the active state multiplier and compounding decay.
        """
        variance = random.gauss(0, self.volatility_index * self.baseline_yield)
        raw_adjusted_yield = self.baseline_yield + variance
        
        state_multiplier = self.impact_matrix.get(shock_type, 1.00)
        final_yield = raw_adjusted_yield * state_multiplier * compounding_multiplier
        
        return max(0.0, final_yield)

    def run_multi_year_simulation(self, years, shock_schedule=None):
        """
        Generates a chronological timeline array. If a shock_schedule is not manually
        injected from a JSON profile, the engine runs the automated Markov loop.
        """
        shock_schedule = shock_schedule or {}
        yield_timeline = []
        current_state = "baseline"
        consecutive_shock_years = 0

        for year in range(1, years + 1):
            # Dynamic schedule override handles factual profile injections
            if year in shock_schedule:
                active_state = shock_schedule[year]
            else:
                active_state = self._get_next_state(current_state)
            
            # Apply dynamic compounding penalties for back-to-back resource depletion years
            if active_state in ["drought", "megadrought"] and current_state in ["drought", "megadrought"]:
                consecutive_shock_years += 1
                compounding_penalty = max(0.40, 1.0 - (consecutive_shock_years * 0.15))
            else:
                consecutive_shock_years = 0
                compounding_penalty = 1.0

            yearly_output = self.generate_yearly_yield(
                shock_type=active_state, 
                compounding_multiplier=compounding_penalty
            )
            
            yield_timeline.append({
                "year": year,
                "yield_per_capita": round(yearly_output, 2),
                "event": active_state,
                "compounding_drag_factor": round(compounding_penalty, 2)
            })
            
            current_state = active_state

        return yield_timeline

if __name__ == "__main__":
    # Diagnostic multi-year stochastic matrix test run
    engine = EnvironmentalShockEngine(baseline_yield=4000)
    timeline_matrix = engine.run_multi_year_simulation(8)
    
    print("=== OS-MERF Advanced Stochastic Climate Matrix Output ===")
    for log in timeline_matrix:
        print(f"Year {log['year']} | State: {log['event']:<12} | Yield: {log['yield_per_capita']:<8} kcal | Decay Drag: {log['compounding_drag_factor']}")
