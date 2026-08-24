from google import genai
from google.genai import types
import os
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# GEMINI ROBOTICS 2.0: MULTI-ROBOT COLLABORATION & FLEET ALLOCATION (ER 2)
# -------------------------------------------------------------------------
# Coordinates heterogeneous robot fleets (humanoids, quadrupeds, AMR rovers)
# with explicit spatial synchronization barriers.
# -------------------------------------------------------------------------

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

DEFAULT_MODEL = os.getenv("GEMINI_ROBOTICS_MODEL", "gemini-robotics-er-2")
FALLBACK_MODELS = [
    "gemini-robotics-er-2",
    "gemini-2.5-flash",
    "gemini-2.0-flash"
]

if api_key:
    client = genai.Client(api_key=api_key)
    print("[INFO] Gemini API Key loaded.")
else:
    client = None
    print("[INFO] GEMINI_API_KEY not configured. Running in simulation mode.")

class RobotAgentSpec(BaseModel):
    agent_id: str
    robot_type: str
    payload_capacity_kg: float
    manipulation_dof: int
    current_location: str

class CollaborativeStep(BaseModel):
    step_id: int
    assigned_agent: str
    action: str
    target: str
    parameters: Dict[str, Any]
    sync_barrier_with: Optional[str] = Field(None, description="Agent ID to synchronize with before commencing")
    handoff_payload: Optional[str] = None

class MultiRobotMissionPlan(BaseModel):
    mission_title: str
    shared_objective: str
    participating_agents: List[str]
    coordination_strategy: str
    synchronized_steps: List[CollaborativeStep]
    inter_robot_safety_buffer_m: float

def coordinate_robot_fleet(mission_goal: str, fleet_specs: List[RobotAgentSpec], model_name: str = DEFAULT_MODEL) -> MultiRobotMissionPlan:
    print(f"\n[FLEET] Coordinating Multi-Robot Fleet for: '{mission_goal}'")
    
    fleet_json = json.dumps([agent.model_dump() for agent in fleet_specs], indent=2)
    
    if client:
        try:
            prompt = f"""
            You are the Fleet Orchestration Brain for a heterogeneous robotics cell.
            Available Robots:
            {fleet_json}
            
            Mission Goal: "{mission_goal}"
            
            Synthesize a synchronized, collision-free multi-agent execution schedule.
            Enforce spatial synchronization barriers for all handover and collaborative operations.
            """

            response = client.models.generate_content(
                model=model_name,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=MultiRobotMissionPlan,
                    temperature=0.1,
                    thinking_config=types.ThinkingConfig(thinking_budget=2048)
                )
            )
            plan = MultiRobotMissionPlan.model_validate_json(response.text)
            print_fleet_plan(plan)
            return plan
        except Exception as e:
            print(f"[WARN] Live API call failed: {e}. Executing simulated fleet plan...")

    plan = generate_simulated_fleet_plan(mission_goal, fleet_specs)
    print_fleet_plan(plan)
    return plan

def generate_simulated_fleet_plan(mission_goal: str, fleet_specs: List[RobotAgentSpec]) -> MultiRobotMissionPlan:
    return MultiRobotMissionPlan(
        mission_title="Heavy Transmission Component Relocation & Inspection",
        shared_objective=mission_goal,
        participating_agents=["humanoid_arm_01", "heavy_rover_01", "quadruped_scout_01"],
        coordination_strategy="Sequential Handover with Quadruped Pre-Inspection Barrier",
        inter_robot_safety_buffer_m=1.5,
        synchronized_steps=[
            CollaborativeStep(
                step_id=1,
                assigned_agent="quadruped_scout_01",
                action="inspect_path_and_qr_scan",
                target="aisle_4_storage_bay",
                parameters={"inspection_speed_ms": 1.2, "enable_lidar_3d": True},
                sync_barrier_with=None
            ),
            CollaborativeStep(
                step_id=2,
                assigned_agent="heavy_rover_01",
                action="navigate_and_dock",
                target="assembly_transfer_bay_alpha",
                parameters={"docking_speed_ms": 0.5, "engage_magnetic_latches": True},
                sync_barrier_with="quadruped_scout_01"
            ),
            CollaborativeStep(
                step_id=3,
                assigned_agent="humanoid_arm_01",
                action="bimanual_lift_and_handoff",
                target="heavy_transmission_part_35kg",
                parameters={"lift_speed_ms": 0.08, "grip_force_n": 45.0},
                sync_barrier_with="heavy_rover_01",
                handoff_payload="heavy_transmission_part_35kg"
            ),
            CollaborativeStep(
                step_id=4,
                assigned_agent="heavy_rover_01",
                action="transport_payload",
                target="workstation_bravo",
                parameters={"cruising_speed_ms": 0.8, "payload_latches_locked": True},
                sync_barrier_with="humanoid_arm_01"
            )
        ]
    )

def print_fleet_plan(plan: MultiRobotMissionPlan):
    print("\nMulti-Robot Coordinated Execution Schedule:")
    print("==================================================")
    print(f"Mission: {plan.mission_title}")
    print(f"Objective: {plan.shared_objective}")
    print(f"Strategy: {plan.coordination_strategy}")
    print(f"Participating Agents: {', '.join(plan.participating_agents)}")
    print(f"Inter-Robot Safety Buffer: {plan.inter_robot_safety_buffer_m}m\n")
    for step in plan.synchronized_steps:
        sync = f" [WAIT FOR: {step.sync_barrier_with}]" if step.sync_barrier_with else " [AUTONOMOUS START]"
        print(f"  Step {step.step_id}: {step.assigned_agent.upper()} -> {step.action}{sync}")
        print(f"    Target: {step.target} | Params: {step.parameters}")
        if step.handoff_payload:
            print(f"    Physical Handoff: {step.handoff_payload}")
    print("==================================================")

if __name__ == "__main__":
    fleet = [
        RobotAgentSpec(
            agent_id="humanoid_arm_01",
            robot_type="Dual-Arm Humanoid",
            payload_capacity_kg=30.0,
            manipulation_dof=14,
            current_location="Assembly Station Alpha"
        ),
        RobotAgentSpec(
            agent_id="heavy_rover_01",
            robot_type="Heavy Autonomous Mobile Robot (AMR)",
            payload_capacity_kg=150.0,
            manipulation_dof=0,
            current_location="Docking Bay 2"
        ),
        RobotAgentSpec(
            agent_id="quadruped_scout_01",
            robot_type="Agile Quadruped Inspector",
            payload_capacity_kg=6.0,
            manipulation_dof=1,
            current_location="Corridor Junction 4"
        )
    ]
    coordinate_robot_fleet("Transfer 35kg battery module from storage depot to humanoid assembly station.", fleet)
