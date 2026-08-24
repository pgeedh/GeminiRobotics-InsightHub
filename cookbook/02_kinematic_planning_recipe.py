"""
Gemini Robotics 2.0 Cookbook: Recipe 2 - Whole-Body Kinematic Planning
Decompose high-level mission goals into whole-body posture and manipulation actions.

Usage:
  python cookbook/02_kinematic_planning_recipe.py --goal "Retrieve engine component from lower shelf"
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Any, Optional

try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def model_dump_json(self, indent=2):
            return json.dumps(self.__dict__, default=lambda o: getattr(o, '__dict__', str(o)), indent=indent)
    def Field(*args, **kwargs):
        return None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

API_KEY = os.getenv("GEMINI_API_KEY")

class KinematicAction(BaseModel):
    step_idx: int
    action_type: str = Field(description="stand_to_crouch, base_navigate, bimanual_reach, grasp, transfer")
    kinematic_params: Dict[str, Any] = Field(description="Torso pitch deg, knee flexion, velocity limits")
    safety_check: str
    completion_criteria: str

class WholeBodyPlan(BaseModel):
    mission_name: str
    target_hardware: str
    estimated_duration_s: float
    crouch_required: bool
    actions: List[KinematicAction]

def run_planning_recipe(goal: str = "Retrieve heavy component from lower shelf and place on workstation", model_name: str = "gemini-robotics-er-2"):
    print("=" * 60)
    print("Recipe 2: Whole-Body Kinematic Planning")
    print(f"Target Model: {model_name}")
    print(f"Mission Goal: {goal}")
    print("=" * 60)

    if API_KEY:
        try:
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=API_KEY)
            prompt = f"""
            You are the Whole-Body Embodied Reasoning brain for a bipedal humanoid manipulator.
            Mission: '{goal}'
            Generate a Pydantic-compliant structured execution plan with stance selection and safety barriers.
            """
            response = client.models.generate_content(
                model=model_name,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=WholeBodyPlan,
                    temperature=0.1
                )
            )
            print("\n[LIVE STRUCTURED PLAN]")
            print(response.text)
            return response.text
        except Exception as e:
            print(f"[WARN] Live API request failed ({e}). Running simulated recipe...")

    sim_plan = WholeBodyPlan(
        mission_name="Low-Shelf Heavy Component Extraction",
        target_hardware="Humanoid Bipedal Manipulator (Apollo 2 / Atlas)",
        estimated_duration_s=28.5,
        crouch_required=True,
        actions=[
            KinematicAction(
                step_idx=1,
                action_type="base_navigate",
                kinematic_params={"target_xy": [1.2, 0.4], "max_vel_ms": 0.5},
                safety_check="1.2m human proximity buffer clear",
                completion_criteria="Base positioned within 0.7m of shelf aperture"
            ),
            KinematicAction(
                step_idx=2,
                action_type="stand_to_crouch",
                kinematic_params={"torso_pitch_deg": 24.0, "knee_flexion_deg": 46.0, "com_height_m": 0.65},
                safety_check="Zero-Moment Point (ZMP) within support polygon",
                completion_criteria="End-effectors aligned with lower tray height (35cm)"
            ),
            KinematicAction(
                step_idx=3,
                action_type="bimanual_reach_and_grasp",
                kinematic_params={"left_grip_force_n": 30.0, "right_grip_force_n": 30.0, "approach_vector": [0, 0, -1]},
                safety_check="Torque limits < 75% rated maximum",
                completion_criteria="Dual force-closure confirmed"
            )
        ]
    )
    print("\n[GROUNDED RECIPE OUTPUT]")
    try:
        output_str = sim_plan.model_dump_json(indent=2)
    except AttributeError:
        output_str = sim_plan.model_dump_json()
    print(output_str)
    return output_str

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recipe 2: Kinematic Planning")
    parser.add_argument("--goal", default="Retrieve heavy component from lower shelf and place on workstation", help="Mission goal")
    parser.add_argument("--model", default="gemini-robotics-er-2", help="Model ID")
    args = parser.parse_args()
    run_planning_recipe(args.goal, args.model)
