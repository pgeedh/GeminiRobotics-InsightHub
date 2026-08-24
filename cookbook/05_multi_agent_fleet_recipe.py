"""
Gemini Robotics 2.0 Cookbook: Recipe 5 - Multi-Agent Fleet Coordination
Orchestrate heterogeneous fleets (Humanoids, AMR rovers, Quadrupeds) with spatial wait barriers.

Usage:
  python cookbook/05_multi_agent_fleet_recipe.py --mission "Relocate 25kg motor from dock to workstation"
"""

import os
import sys
import json
import argparse

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

API_KEY = os.getenv("GEMINI_API_KEY")

def run_fleet_recipe(mission: str = "Relocate 25kg motor from dock to workstation", model_name: str = "gemini-robotics-er-2"):
    print("=" * 60)
    print("Recipe 5: Multi-Agent Fleet Coordination")
    print(f"Target Model: {model_name}")
    print(f"Mission:      '{mission}'")
    print("=" * 60)

    prompt = f"""
    You are the Fleet Synchronization Brain for a factory cell.
    Available Fleet:
    - Robot A: Boston Dynamics Atlas / Apollo Humanoid (30kg bimanual lift)
    - Robot B: Heavy Autonomous Mobile Robot (AMR Rover, 200kg flatbed)
    - Robot C: Spot Quadruped (Aisle Inspector with 3D LiDAR)
    
    Mission: "{mission}"
    
    Synthesize an orchestrated timeline with explicit wait barriers to eliminate deadlock.
    Return JSON format.
    """

    if API_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=API_KEY)
            response = client.models.generate_content(
                model=model_name,
                contents=[prompt]
            )
            print("\n[LIVE FLEET ORCHESTRATION]")
            print(response.text)
            return response.text
        except Exception as e:
            print(f"[WARN] Live API call failed ({e}). Running simulated recipe...")

    sim_schedule = {
        "mission_title": "Heavy Payload Relocation with Pre-Inspection",
        "inter_robot_safety_buffer_m": 1.5,
        "timeline": [
            {
                "phase": 1,
                "agent": "Spot Quadruped",
                "action": "Aisle inspection & path clearance verification",
                "barrier_out": "PATH_CLEAR_01"
            },
            {
                "phase": 2,
                "agent": "AMR Rover",
                "wait_for_barrier": "PATH_CLEAR_01",
                "action": "Dock at pickup station under humanoid reach envelope",
                "barrier_out": "AMR_DOCKED_LATCHED"
            },
            {
                "phase": 3,
                "agent": "Humanoid Manipulator",
                "wait_for_barrier": "AMR_DOCKED_LATCHED",
                "action": "Bimanual power grasp and lower 25kg motor onto AMR bed",
                "barrier_out": "WEIGHT_TRANSFERRED"
            },
            {
                "phase": 4,
                "agent": "AMR Rover",
                "wait_for_barrier": "WEIGHT_TRANSFERRED",
                "action": "Transport payload to target workstation at 0.8 m/s",
                "barrier_out": "MISSION_COMPLETE"
            }
        ]
    }
    print("\n[GROUNDED RECIPE OUTPUT]")
    print(json.dumps(sim_schedule, indent=2))
    return json.dumps(sim_schedule)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recipe 5: Multi-Agent Fleet Coordination")
    parser.add_argument("--mission", default="Relocate 25kg motor from dock to workstation", help="Mission description")
    parser.add_argument("--model", default="gemini-robotics-er-2", help="Model ID")
    args = parser.parse_args()
    run_fleet_recipe(args.mission, args.model)
