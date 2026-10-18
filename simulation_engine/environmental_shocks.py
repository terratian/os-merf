# Copyright (C) 2026 Joshua Sultan (GitHub: terratian) | GNU GPL v3
import random

class EnvironmentalShockEngine:
    """
    Simulates stochastic multi-year environmental variables (droughts, volcanic ash, 
    and seismic events) to stress-test regional agricultural yield baselines.
    """
    def __init__(self, baseline_yield, volatility_index=0.15):
        self.baseline_yield = baseline_yield
        self.volatility_index = volatility_index  # Variance factor for standard deviations

    def generate_yearly_yield(self, shock_type=None):
        """
        Calculates adjusted per-capita caloric yield based on natural variance 
        or explicit disaster event multipliers.
        """
        # Calculate natural micro-climate standard deviation deviation
        variance = random.gauss(0, self.volatility_index * self.baseline_yield)
        adjusted_yield = self.baseline_yield + variance

        # Process macro environmental shocks
        multipliers = {
            "drought": 0.60,       # 40% reduction in agricultural yield
            "megadrought": 0.35,   # 65% reduction in agricultural yield
            "volcanic_ash": 0.50,  # 50% block of solar radiation/photosynthesis
            "seismic_disruption": 0.85 # 15% loss of irrigation infrastructure/canals
        }

        if shock_type in multipliers:
            adjusted_yield *= multipliers[shock_type]

        # Lower boundary floor: a territory cannot produce negative food arrays
        return max(0.0, adjusted_yield)

    def run_multi_year_simulation(self, years, shock_schedule=None):
        """
        Outputs a chronological array of yield matrices over a designated timespan.
        """
        shock_schedule = shock_schedule or {}
        yield_timeline = []

        for year in range(1, years + 1):
            current_shock = shock_schedule.get(year, None)
            yearly_output = self.generate_yearly_yield(shock_type=current_shock)
            yield_timeline.append({"year": year, "yield_per_capita": round(yearly_output, 2), "event": current_shock or "Baseline"})

        return yield_timeline

if __name__ == "__main__":
    # Diagnostic dry run: 5-year outlook with a drought hitting in year 3
    shock_engine = EnvironmentalShockEngine(baseline_yield=3500)
    schedule = {3: "drought"}
    timeline = shock_engine.run_multi_year_simulation(5, shock_schedule=schedule)
    
    print("OS-MERF Climate Volatility Matrix Initialized:")
    for data in timeline:
        print(f"Year {data['year']} | Yield: {data['yield_per_capita']} kcal | State: {data['event']}")
