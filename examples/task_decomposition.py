from google import genai
from google.genai import types
import os
import json
import re
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# GEMINI ROBOTICS 2.0: WHOLE-BODY TASK DECOMPOSITION & PLANNING (ER 2)
# -------------------------------------------------------------------------
# Decomposes complex physical missions into structured whole-body action
# sequences with explicit ASIMOV safety checks and parameters.
# -------------------------------------------------------------------------

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

DEFAULT_MODEL = os.getenv("GEMINI_ROBOTICS_MODEL", "gemini-robotics-er-2")
FALLBACK_MODELS = [
    "gemini-robotics-er-2",
    "gemini-2.5-flash",
    "gemini-2.0-flash"
]

if not api_key:
    print("[INFO] GEMINI_API_KEY not configured. Running with simulated planner.")
    client = None
else:
    print("[INFO] Gemini API Key loaded.")
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"[ERROR] Error initializing client: {e}")
        client = None

class PlanStep(BaseModel):
    step_id: int = Field(description="Sequential index of the step")
    action: str = Field(description="Action primitive (e.g. navigate_to, crouch, reach, grasp, place, verify)")
    target: str = Field(description="Target entity or landmark name")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Execution parameters (e.g. speed, height_cm, grip_force_N)")
    safety_precondition: Optional[str] = Field(None, description="ASIMOV safety check before executing step")
    expected_outcome: str = Field(description="Condition to verify step completion")

class RobotTaskPlan(BaseModel):
    task_name: str
    overall_goal: str
    estimated_duration_sec: int
    steps: List[PlanStep]
    recovery_plan: Optional[str] = None

ROBOT_SYSTEM_PROMPT = """
You are the Embodied Reasoning (ER) brain for a full-body humanoid / mobile manipulator robot.
You control whole-body intelligence from feet to fingertips.
Always decompose missions into structured kinematic steps with ASIMOV safety checks.
"""

def plan_mission(mission_goal: str, model_name: str = DEFAULT_MODEL) -> Optional[RobotTaskPlan]:
    print(f"\n[PLANNER] Planning robot mission: '{mission_goal}' (Model: {model_name})...")
    
    if client:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    ROBOT_SYSTEM_PROMPT,
                    f"Create an executable whole-body robot plan for: '{mission_goal}'"
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RobotTaskPlan,
                    temperature=0.1,
                    thinking_config=types.ThinkingConfig(thinking_budget=2048)
                )
            )
            plan_obj = RobotTaskPlan.model_validate_json(response.text)
            print_plan(plan_obj)
            return plan_obj
        except Exception as e:
            print(f"[WARN] API call error: {e}. Running simulated planner...")

    sim_plan = generate_simulated_plan(mission_goal)
    print_plan(sim_plan)
    return sim_plan

def generate_simulated_plan(mission_goal: str) -> RobotTaskPlan:
    return RobotTaskPlan(
        task_name="Heavy Part Transfer with Whole-Body Squat",
        overall_goal=mission_goal,
        estimated_duration_sec=32,
        steps=[
            PlanStep(
                step_id=1,
                action="navigate_to_shelf",
                target="shelf_lower_tier_alpha",
                parameters={"standoff_distance_m": 0.65, "speed_ms": 0.4},
                safety_precondition="Check 1.2m human proximity buffer",
                expected_outcome="Base located within reach envelope"
            ),
            PlanStep(
                step_id=2,
                action="whole_body_crouch",
                target="knee_and_torso_actuators",
                parameters={"torso_pitch_deg": 22.0, "knee_flexion_deg": 48.0},
                safety_precondition="Center of gravity aligned with support polygon",
                expected_outcome="Gripper level matches shelf height (38cm)"
            ),
            PlanStep(
                step_id=3,
                action="dual_arm_grasp",
                target="heavy_toolbox",
                parameters={"grasp_type": "bimanual_power", "force_n": 24.0},
                safety_precondition="Verify payload < 25kg capacity limit",
                expected_outcome="Force closure confirmed on left and right grips"
            ),
            PlanStep(
                step_id=4,
                action="stand_and_carry",
                target="workbench_alpha",
                parameters={"speed_ms": 0.3, "transport_height_m": 0.9},
                safety_precondition="Maintain active slip monitoring",
                expected_outcome="Payload deposited on workbench latches"
            )
        ],
        recovery_plan="If grip slip > 5mm detected, pause base locomotion, increase grip force +10N, and lower CoG."
    )

def print_plan(plan: RobotTaskPlan):
    print("\nExecutable Whole-Body Plan:")
    print("==================================================")
    print(f"Goal: {plan.overall_goal}")
    print(f"Estimated Duration: {plan.estimated_duration_sec}s")
    for step in plan.steps:
        print(f"  Step {step.step_id}: [{step.action}] on '{step.target}'")
        print(f"    Params: {step.parameters}")
        print(f"    Safety: {step.safety_precondition}")
    if plan.recovery_plan:
        print(f"Recovery: {plan.recovery_plan}")
    print("==================================================")

if __name__ == "__main__":
    plan_mission("Retrieve heavy part from low shelf and place on assembly table")
