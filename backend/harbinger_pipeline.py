"""
Harbinger Research Repository
File: harbinger_pipeline.py

Purpose
-------
Implements the end-to-end decision-making architecture of Harbinger by
connecting prediction outputs to cost-aware checkpoint optimization and
operational recommendation generation. This module defines the system-level
pipeline that transforms predicted failure risk into actionable checkpoint
policies.

Inputs
------
Prediction Inputs:
- Feature vector representing cluster telemetry.
- Prediction timestamp.
- GPU count.
- Current checkpoint interval.
- Candidate checkpoint policies.

Dependencies:
- json
- dataclasses
- typing

Outputs
-------
Returns:
- PredictionResult objects.
- Optimization result dictionaries.
- JSON-formatted operational recommendations.

Side Effects:
- Prints the complete decision pipeline output during standalone execution.

Classes
-------
PredictionResult
    Stores prediction metadata exchanged between pipeline components.

PredictionAdapter
    Interfaces between predictive models and the decision pipeline.

DecisionEngine
    Evaluates candidate checkpoint strategies using an operational cost model
    and selects the minimum-cost policy.

ActionTranslator
    Converts optimization results into structured operational
    recommendations.

Pipeline
--------
Prediction Model
        ↓
Prediction Adapter
        ↓
Decision Engine
        ↓
Action Translator
        ↓
Operational Recommendation
"""

import json
from dataclasses import dataclass
from typing import List, Dict, Any

# --- ARCHITECTURAL ABSTRACTION ---
@dataclass
class PredictionResult:
    probability: float
    timestamp: int
    gpu_count: int
    current_interval: int

# --- MODULE 1: PREDICTION ADAPTER ---
class PredictionAdapter:
    def __init__(self, model_path=None):
        # In production, this loads the locked Logistic Regression model
        self.model_path = model_path

    def predict(self, feature_vector: Dict[str, float], timestamp: int, gpu_count: int, current_interval: int) -> PredictionResult:
        # Simulating the inference step that outputs a high risk probability
        simulated_probability = 0.81 
        return PredictionResult(
            probability=simulated_probability,
            timestamp=timestamp,
            gpu_count=gpu_count,
            current_interval=current_interval
        )

# --- MODULE 2: DECISION ENGINE ---
class DecisionEngine:
    def __init__(self, base_time_min=1.0, k_time_per_gpu=0.5, job_duration_estimate=1000):
        self.base_time_min = base_time_min
        self.k_time_per_gpu = k_time_per_gpu
        self.job_duration = job_duration_estimate

    def calculate_cost(self, interval: int, result: PredictionResult):
        # Overhead Cost
        t_ckpt = self.base_time_min + (self.k_time_per_gpu * result.gpu_count)
        pause_gpu_hours = (result.gpu_count * t_ckpt) / 60.0
        ckpt_count = self.job_duration // interval
        overhead_cost = ckpt_count * pause_gpu_hours
        
        # Expected Failure Loss
        last_ckpt = (result.timestamp // interval) * interval
        recovery_loss_min = result.timestamp - last_ckpt
        gpu_hours_lost = (recovery_loss_min * result.gpu_count) / 60.0
        expected_loss = result.probability * gpu_hours_lost
        
        return overhead_cost + expected_loss

    def optimize(self, result: PredictionResult, candidate_policies: List[int]) -> Dict[str, Any]:
        current_cost = self.calculate_cost(result.current_interval, result)
        
        costs = {policy: self.calculate_cost(policy, result) for policy in candidate_policies}
        best_policy = min(costs, key=costs.get)
        optimized_cost = costs[best_policy]
        expected_benefit = max(0.0, current_cost - optimized_cost)
        
        return {
            "prediction": result,
            "current_cost": round(current_cost, 2),
            "best_policy": best_policy,
            "optimized_cost": round(optimized_cost, 2),
            "expected_benefit": round(expected_benefit, 2)
        }

# --- MODULE 3: ACTION TRANSLATOR ---
class ActionTranslator:
    def translate(self, optimization_result: Dict[str, Any]) -> str:
        pred = optimization_result["prediction"]
        benefit = optimization_result["expected_benefit"]
        best_policy = optimization_result["best_policy"]
        
        if benefit > 0 and best_policy < pred.current_interval:
            recommendation = "Trigger Immediate Checkpoint and Increase Frequency"
        elif benefit > 0 and best_policy > pred.current_interval:
            recommendation = "Reduce Checkpoint Frequency (Overhead outweighs Risk)"
        else:
            recommendation = "Maintain Current Policy"
            
        output = {
            "failure_probability": pred.probability,
            "recommended_policy": f"Checkpoint every {best_policy} minutes",
            "current_cost_gpu_hours": optimization_result["current_cost"],
            "optimized_cost_gpu_hours": optimization_result["optimized_cost"],
            "expected_gpu_hours_saved": benefit,
            "recommendation": recommendation,
            "confidence": pred.probability 
        }
        return json.dumps(output, indent=2)

if __name__ == "__main__":
    print("--- PHASE 5: END-TO-END DECISION PIPELINE ---\n")
    
    # Initialize Pipeline Modules
    adapter = PredictionAdapter()
    engine = DecisionEngine()
    translator = ActionTranslator()
    
    # 1. Cluster State -> Prediction Engine
    simulated_telemetry = {"gpu_util_mean_60m": 94.5, "ecc_count_180m": 12}
    pred_result = adapter.predict(
        feature_vector=simulated_telemetry,
        timestamp=850,
        gpu_count=8,
        current_interval=120
    )
    
    # 2. Risk Assessment -> Decision Engine
    opt_result = engine.optimize(pred_result, candidate_policies=[120, 60, 30, 15])
    
    # 3. Decision Engine -> Action Policy
    final_output = translator.translate(opt_result)
    
    print(final_output)