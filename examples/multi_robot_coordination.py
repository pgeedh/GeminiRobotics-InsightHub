from google import genai
from google.genai import types
import os
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# GEMINI ROBOTICS: MULTI-ROBOT COLLABORATION & SEMANTIC TASK ALLOCATION (ER 2)
# -------------------------------------------------------------------------
# Gemini Robotics ER 2 enables heterogeneous robot fleets (humanoids,
# quadrupeds, mobile manipulators, overhead vision nodes) to share a common
# semantic spatial representation, negotiate task allocation, and coordinate
# synchronized multi-agent physical operations.
# -------------------------------------------------------------------------

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

DEFAULT_MODEL = os.getenv("GEMINI_ROBOTICS_MODEL", "gemini-robotics-er-2")
FALLBACK_MODELS = [
    "gemini-robotics-er-2",
    "gemini-robotics-er-1.5-preview",
    "gemini-2.5-flash",
    "gemini-2.0-flash"
]

if api_key:
    client = genai.Client(api_key=api_key)
    print("✅ Gemini API Key loaded.")
else:
    client = None
    print("⚠️ Warning: GEMINI_API_KEY not found. Running in simulation mode.")

# Pydantic Schemas for Multi-Robot Fleet Coordination
class RobotAgentSpec(BaseModel):
    agent_id: str
    robot_type: str  # e.g., "Humanoid Manipulator", "Wheeled Logistics Rover", "Quadruped Scout"
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

def coordinate_robot_fleet(
    shared_mission: str,
    fleet_composition: List[RobotAgentSpec],
    model_name: str = DEFAULT_MODEL
) -> MultiRobotMissionPlan:
    """
    Synthesizes a coordinated multi-robot task allocation plan using Gemini Robotics ER 2.
    """
    print(f"\n🤝 Synthesizing Multi-Robot Coordination Plan for: '{shared_mission}'")
    print(f"🤖 Registered Fleet ({len(fleet_composition)} units):")
    for a in fleet_composition:
        print(f"   • [{a.agent_id}] {a.robot_type} @ {a.current_location} (Payload: {a.payload_capacity_kg}kg, DoF: {a.manipulation_dof})")

    fleet_context = json.dumps([a.model_dump() for a in fleet_composition], indent=2)

    system_prompt = """
    You are the Central Embodied Multi-Agent Coordinator powered by Gemini Robotics ER 2.
    Given a high-level warehouse / factory / domestic mission and a fleet of heterogeneous robots:
    1. Decompose the mission into complementary subtasks matching agent physical capabilities.
    2. Define synchronization barriers (e.g. Robot A must hold crate open while Robot B deposits part).
    3. Ensure inter-robot collision avoidance and minimum spatial safety buffers.
    4. Generate structured JSON conforming to MultiRobotMissionPlan schema.
    """

    user_prompt = f"""
    Mission: {shared_mission}
    Available Fleet:
    {fleet_context}
    """

    plan = None

    if client:
        for m in [model_name] + [x for x in FALLBACK_MODELS if x != model_name]:
            try:
                print(f"📡 Generating multi-robot plan with {m}...")
                response = client.models.generate_content(
                    model=m,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                        system_instruction=system_prompt,
                        response_mime_type="application/json",
                        response_schema=MultiRobotMissionPlan,
                        thinking_config=types.ThinkingConfig(thinking_budget=2048)
                    )
                )
                plan = MultiRobotMissionPlan(**json.loads(response.text))
                print(f"✅ Coordinated multi-robot mission via {m}")
                break
            except Exception as e:
                print(f"⚠️ Model '{m}' fleet coordination failed: {e}")
                continue

    if not plan:
        print("ℹ️ Using simulated ER 2 fleet allocation telemetry...")
        plan = generate_simulated_fleet_plan(shared_mission, fleet_composition)

    print_fleet_plan(plan)
    return plan

def generate_simulated_fleet_plan(mission: str, fleet: List[RobotAgentSpec]) -> MultiRobotMissionPlan:
    return MultiRobotMissionPlan(
        mission_title="Heavy Assembly & Component Transport",
        shared_objective=mission,
        participating_agents=[a.agent_id for a in fleet],
        coordination_strategy="Dynamic Dual-Agent Handoff with Quadruped Environmental Clearance",
        inter_robot_safety_buffer_m=1.5,
        synchronized_steps=[
            CollaborativeStep(
                step_id=1,
                assigned_agent="quadruped_scout_01",
                action="scan_corridor_and_clear_hazards",
                target="hallway_b_transit_path",
                parameters={"speed_mps": 1.2, "lidar_fov_deg": 360},
                sync_barrier_with=None
            ),
            CollaborativeStep(
                step_id=2,
                assigned_agent="humanoid_arm_01",
                action="dual_arm_pick_heavy_crate",
                target="heavy_parts_rack_shelf_2",
                parameters={"payload_weight_kg": 18.5, "lift_height_m": 0.8},
                sync_barrier_with="quadruped_scout_01",
                handoff_payload="Engine_Mount_Crate_#402"
            ),
            CollaborativeStep(
                step_id=3,
                assigned_agent="logistics_rover_01",
                action="dock_under_manipulator",
                target="humanoid_arm_01_payload_bed",
                parameters={"docking_tolerance_mm": 10},
                sync_barrier_with="humanoid_arm_01"
            ),
            CollaborativeStep(
                step_id=4,
                assigned_agent="humanoid_arm_01",
                action="lower_and_secure_to_flatbed",
                target="logistics_rover_01",
                parameters={"clamp_latch": True},
                sync_barrier_with="logistics_rover_01",
                handoff_payload="Engine_Mount_Crate_#402"
            ),
            CollaborativeStep(
                step_id=5,
                assigned_agent="logistics_rover_01",
                action="transit_to_assembly_bay",
                target="bay_4_intake",
                parameters={"max_accel_mps2": 0.3},
                sync_barrier_with=None
            )
        ]
    )

def print_fleet_plan(plan: MultiRobotMissionPlan):
    print("\n" + "=" * 70)
    print(f"🤖🤝🤖 MULTI-ROBOT FLEET PLAN: {plan.mission_title.upper()}")
    print("=" * 70)
    print(f"🎯 Objective: {plan.shared_objective}")
    print(f"🧠 Strategy:  {plan.coordination_strategy}")
    print(f"🛡️ Safety Buffer: {plan.inter_robot_safety_buffer_m} meters")
    print(f"👥 Agents: {', '.join(plan.participating_agents)}")
    print("-" * 70)
    print("📋 Synchronized Execution Schedule:")
    for s in plan.synchronized_steps:
        sync_str = f" ⏳ [Wait for {s.sync_barrier_with}]" if s.sync_barrier_with else ""
        handoff_str = f" 📦 [Handoff: {s.handoff_payload}]" if s.handoff_payload else ""
        print(f"  Step {s.step_id:02d} | 🤖 {s.assigned_agent:<18} -> {s.action} on '{s.target}'{sync_str}{handoff_str}")
    print("=" * 70)

if __name__ == "__main__":
    test_fleet = [
        RobotAgentSpec(
            agent_id="humanoid_arm_01",
            robot_type="Dual-Arm Humanoid (Apptronik / Boston Dynamics)",
            payload_capacity_kg=25.0,
            manipulation_dof=14,
            current_location="Tooling Station Alpha"
        ),
        RobotAgentSpec(
            agent_id="logistics_rover_01",
            robot_type="Autonomous Mobile Robot (AMR)",
            payload_capacity_kg=100.0,
            manipulation_dof=0,
            current_location="Charging Dock 3"
        ),
        RobotAgentSpec(
            agent_id="quadruped_scout_01",
            robot_type="Dynamic Quadruped",
            payload_capacity_kg=5.0,
            manipulation_dof=1,
            current_location="Perimeter Gate 1"
        )
    ]
    
    coordinate_robot_fleet(
        shared_mission="Retrieve heavy engine block component from shelf 2 and transport to assembly line 4.",
        fleet_composition=test_fleet
    )
