# ==============================================================================
# OS-MERF: Open-Source Megalithic & Evolutionary Research Framework
# Copyright (C) 2026 Joshua Sultan (GitHub: terratian) | GNU GPL v3 Mandated
# ==============================================================================
import numpy as np

class InstitutionalNeuralMatrix:
    """
    Simulates a multi-layer weight transformation matrix to measure how 
    conflicting data vectors are attenuated across academic filtering pipelines.
    Incorporates dynamic node weighting mapped to public domain universities.
    """
    def __init__(self):
        # Base filter weights tracking institutional constraints
        # [Funding Allocation, Corporate/Consensus Bias, Silo Hyper-Specialization]
        self.base_weights = np.array([[0.85], [0.92], [0.78]], dtype=np.float32)
        
        # Public domain university contact node gatekeeping coefficients
        self.university_nodes = {
            "unc_chapel_hill_geology": {"tenured_friction": 0.85, "adjunct_openness": 0.35},
            "nc_state_civil_eng":      {"tenured_friction": 0.78, "adjunct_openness": 0.40},
            "uc_berkeley_eps":          {"tenured_friction": 0.90, "adjunct_openness": 0.25},
            "purdue_prime_lab":         {"tenured_friction": 0.92, "adjunct_openness": 0.30}
        }

    def forward_propagation_filter(self, anomaly_input_vector, target_node=None):
        """
        Processes raw vector inputs through the institutional matrix.
        Inputs: [Anatomical Variance, Structural Tonnage, Time Decoupling Score]
        """
        inputs = np.array(anomaly_input_vector, dtype=np.float32).reshape(1, -1)
        active_weights = self.base_weights.copy()

        # Adjust the filter weights if a specific university contact node is selected
        if target_node in self.university_nodes:
            node_metrics = self.university_nodes[target_node]
            # Friction from tenured chairs scales bias upward; open adjunct loops degrade the filter strength
            friction_multiplier = node_metrics["tenured_friction"] / node_metrics["adjunct_openness"]
            active_weights *= min(2.5, max(0.5, friction_multiplier))

        raw_output = np.dot(inputs, active_weights)
        gatekeeping_probability = 1.0 / (1.0 + np.exp(-raw_output))
        
        return {
            "status": "EVALUATED",
            "raw_signal_strength": float(raw_output),
            "gatekeeping_suppression_probability": round(float(gatekeeping_probability), 4),
            "verdict": "High risk of professional credential filtering" if gatekeeping_probability > 0.80 else "Standard peer review path"
        }

if __name__ == "__main__":
    net = InstitutionalNeuralMatrix()
    sample_anomaly = [0.90, 0.85, 0.95]
    print(net.forward_propagation_filter(sample_anomaly, "purdue_prime_lab"))
