# ==============================================================================
# OS-MERF: Automated Unified Test Validation Suite
# Copyright (C) 2026 Joshua Sultan (GitHub: terratian) | GNU GPL v3 Mandated
# ==============================================================================
import sys
import os

# Append paths to ensure clean package resolution loops
sys.path.append(os.path.abspath("simulation_engine"))
sys.path.append(os.path.abspath("topographical_assay"))
sys.path.append(os.path.abspath("evolutionary_indexing"))

from metabolic_model import EconomicSimulationEngine
from joint_classifier import JointClassifier
from cross_disciplinary_tracker import CrossDisciplinaryTracker
from neural_matrix import InstitutionalNeuralMatrix

def test_metabolic_engine():
    print("[TEST] Validating Metabolic Model Engine Loop...")
    profile = "simulation_engine/regional_profiles/andes_profile.json"
    engine = EconomicSimulationEngine(profile)
    log = engine.execute_profile_timeline(1000, 5, 50, 0.0)
    assert len(log) > 0, "Metabolic engine timeline array generation failed"
    print(" -> Metabolic Engine Status: PASSED")

def test_joint_classifier():
    print("[TEST] Validating OpenCV Geometry Joint Engine Skeleton...")
    classifier = JointClassifier()
    res = classifier.analyze_joint_matrix("invalid_path.jpg")
    assert res["status"] == "ERROR", "Classifier failed to intercept missing image array"
    print(" -> Joint Classifier Status: PASSED")

def test_cross_disciplinary_tracker():
    print("[TEST] Validating Cross-Disciplinary Dissonance Verification Loops...")
    tracker = CrossDisciplinaryTracker()
    res = tracker.execute_correlation_loop("unresolved_deep_time_foundations")
    assert "cross_domain_dissonance_index" in res, "Tracker failed to calculate dissonance score"
    print(" -> Cross-Disciplinary Tracker Status: PASSED")

def test_institutional_neural_matrix():
    print("[TEST] Validating Institutional Neural Matrix Attenuation Filters...")
    net = InstitutionalNeuralMatrix()
    sample_anomaly = [0.90, 0.85, 0.95]
    res = net.forward_propagation_filter(sample_anomaly)
    assert res["status"] == "EVALUATED", "Neural matrix signal filtering calculation loop failed"
    assert "gatekeeping_suppression_probability" in res, "Probability score omitted from neural verdict"
    print(" -> Institutional Neural Matrix Status: PASSED")

def run_all_tests():
    print("=== Launching Unified OS-MERF Verification Pipeline ===")
    try:
        test_metabolic_engine()
        test_joint_classifier()
        test_cross_disciplinary_tracker()
        test_institutional_neural_matrix()
        print("\n=== SYSTEM INTEGRITY VERIFICATION SUCCEEDED: ALL MODULES STABLE ===")
        return True
    except Exception as e:
        print(f"\n[FATAL SYSTEM FAULT] Pipeline Execution Interrupted: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
