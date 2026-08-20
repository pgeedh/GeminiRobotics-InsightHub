from google import genai
from google.genai import types
import os
import time
import json
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# GEMINI ROBOTICS 2.0: AGENTIC TOOL USE & SEARCH GROUNDING (ER 2)
# -------------------------------------------------------------------------
# Uses Gemini Robotics ER 2's native Tool Use (Google Search Grounding &
# local API functions) to make grounded manipulation decisions.
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

def query_local_facility_rules(material: str, location: str = "San Francisco") -> str:
    """Queries local municipality recycling facility capabilities."""
    rules = {
        "plastic_5_pp": "Recyclable in blue curbside bin. Must be rinsed clean.",
        "styrofoam_ps": "NOT accepted in standard curbside. Requires drop-off at hazardous/special waste.",
        "greasy_pizza_box": "Compostable in green organics bin. Do NOT place in blue recycling.",
        "lithium_ion_battery": "CRITICAL HAZARD: Do not place in curbside. Must be insulated and taken to e-waste."
    }
    key = material.lower().replace(" ", "_").replace("#", "")
    for k, v in rules.items():
        if k in key or key in k:
            return v
    return "Recyclable if clean rigid plastic/metal; otherwise general landfill."

def run_agentic_robot(item_description: str, location: str = "San Jose, CA"):
    print(f"\n[AGENT] Robot observing item: '{item_description}' in '{location}'...")
    
    if client:
        try:
            prompt = f"""
            The robot arm camera observes: '{item_description}'.
            Location: '{location}'.
            Use Google Search grounding or query local facility rules to determine:
            1. Waste stream (Compost, Recycle, Landfill, Hazardous).
            2. Handling precaution (e.g. fire hazard, puncture risk).
            3. Target bin placement location.
            """
            response = client.models.generate_content(
                model=DEFAULT_MODEL,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    temperature=0.2
                )
            )
            print("\nLive Agentic Reasoning Result:")
            print(response.text)
            return response.text
        except Exception as e:
            print(f"[WARN] Live API call failed: {e}. Falling back to simulation...")

    sim_res = simulate_agentic_decision(item_description, location)
    print("\nSimulated Agentic Decision:")
    print(sim_res)
    return sim_res

def simulate_agentic_decision(item: str, location: str) -> str:
    rule = query_local_facility_rules(item, location)
    return f"""
    [Decision: RECYCLING STREAM DETERMINATION]
    - Item: {item}
    - Location: {location}
    - Local Rule Match: {rule}
    - Planned Action: Route to Blue Recycling Bin (Bin #2) with compliant parallel grasp.
    """

if __name__ == "__main__":
    run_agentic_robot("Plastic #5 PP cup with coffee residue")
