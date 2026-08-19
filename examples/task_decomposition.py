from google import genai
from google.genai import types
import os
import json
import re
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# GEMINI ROBOTICS: WHOLE-BODY TASK DECOMPOSITION & PLANNING (ER 2 & ER 1.5)
# -------------------------------------------------------------------------
# This script shows how to use Gemini Robotics ER 2 as a high-level physical
# AI brain that decomposes complex, multi-step tasks into whole-body action
# sequences (locomotion + manipulation + safety checks + replanning).
# -------------------------------------------------------------------------

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

DEFAULT_MODEL = os.getenv("GEMINI_ROBOTICS_MODEL", "gemini-robotics-er-2")
FALLBACK_MODELS = [
    "gemini-robotics-er-2",
    "gemini-robotics-er-1.5-preview",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-pro"
]

if not api_key:
    print("⚠️ Warning: GEMINI_API_KEY not found. Running with simulation fallback.")
    client = None
else:
    print("✅ Gemini API Key loaded.")
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error initializing client: {e}")
        client = None

# Structured Schema Definition for Robot Task Planning
class PlanStep(BaseModel):
    step_id: int = Field(description="Sequential index of the step")
    action: str = Field(description="Action primitive name (e.g., navigate_to, crouch, reach, grasp, place, verify)")
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

# ER 2 Whole-Body Robot System Prompt
ROBOT_SYSTEM_PROMPT = """
You are the Embodied Reasoning (ER) brain for a full-body humanoid / mobile manipulator robot.
You control whole-body intelligence from feet to fingertips.

Available Low-Level Primitives:
1. navigate_to(target_location, clearance_m=0.5)
2. align_base(target_pose_2d)
3. crouch(height_percentage=0.5)
4. stand_up()
5. reach_arm(arm_id='left'|'right'|'dual', target_pose_3d=[x, y, z])
6. grasp(arm_id='left'|'right', grasp_type='pinch'|'power'|'suction', force_n=15)
7. release_gripper(arm_id='left'|'right')
8. place_object(target_surface, arm_id='left'|'right')
9. verify_scene_state(expected_visual_state)
10. check_human_safety(proximity_radius_m=1.0)

Safety Rules (ASIMOV-Agentic Standard):
- Always insert a check_human_safety step before high-acceleration or heavy manipulation.
- Verify scene state before and after critical grasps.
- If an object is low on the floor, crouch before reaching.

Given a user command, generate a structured task decomposition in JSON.
"""

def plan_mission(user_command: str, model_name: str = DEFAULT_MODEL, current_state_notes: str = "") -> RobotTaskPlan:
    """
    Generates a structured whole-body task plan using Gemini Robotics ER 2.
    """
    print(f"\n🎯 User Command: '{user_command}'")
    if current_state_notes:
        print(f"📌 Current State / Context: {current_state_notes}")

    full_prompt = f"""
    {ROBOT_SYSTEM_PROMPT}

    User Command: {user_command}
    Current Environment / Robot State: {current_state_notes or 'Robot standing at docking station, batteries full, dual arms homed.'}

    Generate the complete structured execution plan.
    """

    plan_data = None

    if client:
        models_to_try = [model_name] + [m for m in FALLBACK_MODELS if m != model_name]
        for m in models_to_try:
            try:
                print(f"📡 Generating whole-body plan with {m}...")
                response = client.models.generate_content(
                    model=m,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.1, # Deterministic reasoning
                        response_mime_type="application/json",
                        response_schema=RobotTaskPlan,
                        thinking_config=types.ThinkingConfig(thinking_budget=2048)
                    )
                )
                
                raw_text = response.text
                clean_json = extract_json(raw_text)
                plan_data = json.loads(clean_json)
                print(f"✅ Successfully planned mission using {m}")
                break
            except Exception as e:
                print(f"⚠️ Model '{m}' error: {e}")
                continue

    if not plan_data:
        print("ℹ️ Using simulated ER 2 whole-body planner output...")
        plan_data = generate_simulated_plan(user_command)

    try:
        parsed_plan = RobotTaskPlan(**plan_data) if isinstance(plan_data, dict) else plan_data
    except Exception as e:
        print(f"⚠️ Schema validation note: {e}")
        parsed_plan = plan_data

    print_plan_summary(parsed_plan)
    return parsed_plan

def replan_on_failure(original_command: str, failed_step_id: int, failure_reason: str) -> RobotTaskPlan:
    """
    Triggers dynamic replanning when a step execution fails or unexpected obstacles occur.
    """
    print(f"\n🚨 Execution Failure at Step {failed_step_id}: {failure_reason}")
    print("🔄 Invoking Gemini Robotics ER 2 Dynamic Replanner...")
    
    replan_context = f"Step {failed_step_id} failed because: '{failure_reason}'. Generate an alternative recovery plan."
    return plan_mission(original_command, current_state_notes=replan_context)

def extract_json(text: str) -> str:
    """Extracts valid JSON from markdown code fences or raw string."""
    json_match = re.search(r'```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```', text, re.DOTALL)
    if json_match:
        return json_match.group(1).strip()
    return text.strip()

def generate_simulated_plan(command: str) -> Dict[str, Any]:
    """Generates a whole-body simulated plan matching Gemini Robotics ER 2 format."""
    return {
        "task_name": "whole_body_manipulation_mission",
        "overall_goal": command,
        "estimated_duration_sec": 42,
        "steps": [
            {
                "step_id": 1,
                "action": "check_human_safety",
                "target": "workspace_perimeter",
                "parameters": {"proximity_radius_m": 1.2},
                "safety_precondition": "Ensure no humans within 1m before robot initiates base movement",
                "expected_outcome": "Perimeter clear"
            },
            {
                "step_id": 2,
                "action": "navigate_to",
                "target": "kitchen_table_zone",
                "parameters": {"clearance_m": 0.4, "max_vel_mps": 0.6},
                "safety_precondition": "Dynamic obstacle avoidance active",
                "expected_outcome": "Robot base positioned 0.5m in front of table"
            },
            {
                "step_id": 3,
                "action": "verify_scene_state",
                "target": "target_item_on_table",
                "parameters": {"camera_view": "head_rgbd"},
                "safety_precondition": "RGBD point cloud depth verified",
                "expected_outcome": "Object 3D coordinates and grasp affordance computed"
            },
            {
                "step_id": 4,
                "action": "reach_arm",
                "target": "target_item",
                "parameters": {"arm_id": "right", "target_pose_3d": [0.05, 0.45, 0.12]},
                "safety_precondition": "Joint velocity limits < 0.8 rad/s",
                "expected_outcome": "Gripper positioned 3cm above object"
            },
            {
                "step_id": 5,
                "action": "grasp",
                "target": "target_item",
                "parameters": {"arm_id": "right", "grasp_type": "power", "force_n": 18},
                "safety_precondition": "Tactile sensor slip feedback enabled",
                "expected_outcome": "Object securely grasped in right hand"
            },
            {
                "step_id": 6,
                "action": "navigate_to",
                "target": "trash_bin_zone",
                "parameters": {"clearance_m": 0.5},
                "safety_precondition": "Keep payload stable during locomotion",
                "expected_outcome": "Robot positioned adjacent to receptacle"
            },
            {
                "step_id": 7,
                "action": "place_object",
                "target": "trash_bin",
                "parameters": {"arm_id": "right"},
                "safety_precondition": "Check drop receptacle depth",
                "expected_outcome": "Object released safely into trash bin"
            }
        ],
        "recovery_plan": "If grasp slip is detected, reposition arm by 2cm along normal and retry with 25N force."
    }

def print_plan_summary(plan: Any):
    print("\n📋 Generated Whole-Body Robot Plan (Gemini Robotics ER 2):")
    print("=" * 65)
    if isinstance(plan, RobotTaskPlan):
        print(f"📌 Task: {plan.task_name} | Est. Duration: {plan.estimated_duration_sec}s")
        print(f"🎯 Goal: {plan.overall_goal}")
        print("-" * 65)
        for s in plan.steps:
            safety_tag = f" [🛡️ {s.safety_precondition}]" if s.safety_precondition else ""
            print(f"  Step {s.step_id}: {s.action.upper()} -> {s.target} (Params: {s.parameters}){safety_tag}")
        if plan.recovery_plan:
            print(f"🔄 Recovery Strategy: {plan.recovery_plan}")
    elif isinstance(plan, dict):
        print(f"📌 Task: {plan.get('task_name')} | Est. Duration: {plan.get('estimated_duration_sec', 30)}s")
        print(f"🎯 Goal: {plan.get('overall_goal')}")
        print("-" * 65)
        for s in plan.get("steps", []):
            print(f"  Step {s.get('step_id')}: {s.get('action', '').upper()} -> {s.get('target')} (Params: {s.get('parameters')})")
    print("=" * 65)

if __name__ == "__main__":
    plan = plan_mission("Find the fallen water bottle under the desk, pick it up, and place it on the shelf.")
    
    # Demonstrate dynamic replanning
    print("\n--- Simulating Dynamic Replanning Scenario ---")
    replan_on_failure(
        original_command="Place water bottle on shelf",
        failed_step_id=4,
        failure_reason="Obstacle detected in reach corridor: human arm entered workspace"
    )

