"""
Gemini Robotics 2.0 Cookbook: Interactive Testing Sandbox
Allows developers to immediately test custom prompts with custom images and models.

Usage:
  python cookbook/interactive_sandbox.py
"""

import os
import sys
import json
from PIL import Image, ImageDraw
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def interactive_test_loop():
    print("=" * 60)
    print("Gemini Robotics 2.0 Interactive Testing Sandbox")
    print("=" * 60)
    print("Feed any image and test prompt to evaluate spatial grounding & planning.")
    print("API Key Status:", "Configured" if API_KEY else "Not set (Running high-fidelity mock telemetry)")
    print("=" * 60)

    model_id = input("\nEnter Model ID [default: gemini-robotics-er-2]: ").strip() or "gemini-robotics-er-2"
    img_path = input("Enter path to test image [default: assets/pointing_undefined.png]: ").strip() or "assets/pointing_undefined.png"

    if not os.path.exists(img_path):
        print(f"[INFO] Generating test frame at: {img_path}")
        Image.new('RGB', (640, 480), color=(35, 40, 50)).save(img_path)

    default_prompt = "Point to all manipulable tools and return JSON: [{\"point\": [y, x], \"label\": \"<name>\"}] with coordinates in 0-1000."
    print(f"\nDefault Prompt: {default_prompt}")
    user_prompt = input("Enter prompt (or press Enter to use default): ").strip() or default_prompt

    print(f"\n[EXECUTING TEST QUERY with {model_id}]...")
    
    if API_KEY:
        try:
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=API_KEY)
            with open(img_path, "rb") as f:
                img_data = f.read()
            res = client.models.generate_content(
                model=model_id,
                contents=[types.Part.from_bytes(data=img_data, mime_type="image/png"), user_prompt],
                config=types.GenerateContentConfig(temperature=0.2)
            )
            print("\n[RESPONSE]")
            print(res.text)
            return
        except Exception as e:
            print(f"[WARN] Live execution error ({e}). Returning grounded simulation...")

    mock_result = [
        {"point": [410, 320], "label": "test_object_alpha"},
        {"point": [680, 540], "label": "test_object_bravo"}
    ]
    print("\n[RESPONSE (GROUNDED SIMULATION)]")
    print(json.dumps(mock_result, indent=2))

if __name__ == "__main__":
    interactive_test_loop()
