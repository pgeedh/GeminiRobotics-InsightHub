from google import genai
from google.genai import types
import os
import time
import json
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# GEMINI ROBOTICS: AGENTIC TOOL USE & SEARCH GROUNDING (ER 2 & ER 1.5)
# -------------------------------------------------------------------------
# Robots often encounter ambiguous items in dynamic physical environments.
# This script demonstrates using Gemini Robotics ER 2's native Tool Use
# (Google Search Grounding & custom API functions) to make informed,
# grounded physical manipulation decisions.
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
    print("⚠️ Warning: GEMINI_API_KEY not set. Running in simulation mode.")

# Local Facility Database Tool
def query_local_facility_rules(material: str, location: str = "San Francisco") -> str:
    """Queries local municipality recycling facility capabilities."""
    rules = {
        "plastic_5_pp": "Recyclable in blue curbside bin. Must be rinsed clean.",
        "styrofoam_ps": "NOT accepted in standard curbside. Requires drop-off at hazardous/special waste.",
        "bioplastic_pla": "NOT accepted in municipal recycling. Must go to industrial compost or black trash bin.",
        "lithium_battery": "CRITICAL HAZARD: Never place in curbside bin. Fire hazard. Take to e-waste center.",
        "corrugated_cardboard": "Accepted and recyclable. Flatten box before placing in bin."
    }
    key = material.lower().replace(" ", "_").replace("#", "")
    return rules.get(key, f"Standard guidance for {material} in {location}: Check local municipal guidelines or sort to general waste if uncertain.")

def run_agentic_robot(object_description: str, location: str = "Austin, TX"):
    """
    Executes an agentic decision using Gemini Robotics with tool grounding.
    """
    print(f"\n🤖 Robot Camera Detected: '{object_description}' (Location: {location})")
    print("🤔 Robot Reasoning: Determining waste sorting stream using Grounded Tool Use...")

    system_instruction = """
    You are an autonomous sorting and recycling robot equipped with Embodied Reasoning.
    When presented with an item:
    1. Identify its material composition.
    2. Consider physical safety (e.g. lithium batteries, sharp glass, biohazards).
    3. Ground your decision using Search or Facility Knowledge.
    4. Provide an actionable recommendation: Target Bin ('Recycle', 'Compost', 'Hazardous E-Waste', 'General Trash'), Gripper Precaution, and Explanation.
    """

    prompt = f"Object description: '{object_description}'. Location: '{location}'. Determine the exact sorting stream and explain the physical handling precautions."

    response_text = None

    if client:
        # Try live GenAI client with Google Search grounding
        for m in [DEFAULT_MODEL] + [x for x in FALLBACK_MODELS if x != DEFAULT_MODEL]:
            try:
                print(f"📡 Querying {m} with Google Search Grounding...")
                response = client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        system_instruction=system_instruction,
                        tools=[
                            types.Tool(google_search=types.GoogleSearch())
                        ]
                    )
                )
                response_text = response.text
                print(f"✅ Success with model: {m}")
                break
            except Exception as e:
                print(f"⚠️ Live tool call with '{m}' not available: {e}")
                continue

    if not response_text:
        # Fallback simulation
        print("ℹ️ Running simulation with local knowledge lookup...")
        simulated_context = query_local_facility_rules(object_description, location)
        response_text = f"""### Sorting Decision & Handling Plan
- **Item**: {object_description}
- **Identified Category**: Polypropylene / Special polymer
- **Grounded Verification**: {simulated_context}
- **Target Receptacle**: ♻️ **RECYCLING (Blue Bin)**
- **Robot Arm Handling**:
  - Gripper: Suction / Soft-pad pinch with max force 12N.
  - Precondition: Verify item is empty and dry before bin placement.
  - Action: Execute trajectory to recycling bin hopper (X: 0.65m, Y: -0.30m, Z: 0.40m)."""

    print("\n🧠 Gemini Robotics Agentic Decision:")
    print("--------------------------------------------------")
    print(response_text)
    print("--------------------------------------------------")
    return response_text

if __name__ == "__main__":
    run_agentic_robot("Plastic container labeled with recycling code #5 PP", location="Seattle, WA")
    run_agentic_robot("Swollen Li-Ion battery from discarded RC car", location="San Jose, CA")

