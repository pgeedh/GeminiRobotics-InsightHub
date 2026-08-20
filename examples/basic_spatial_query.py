from google import genai
from google.genai import types
import os
import json
import re
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# GEMINI ROBOTICS 2.0: SPATIAL QUERY & 3D GROUNDING (ER 2)
# -------------------------------------------------------------------------
# Demonstrates querying Google DeepMind's Gemini Robotics ER 2
# for 2D bounding boxes, pixel points, 3D bounding boxes, and 6DoF grasp poses.
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
    print("⚠️ Warning: GEMINI_API_KEY not found in .env or environment.")
else:
    print("✅ Gemini API Key loaded.")

try:
    client = genai.Client(api_key=api_key) if api_key else None
except Exception as e:
    print(f"Error initializing client: {e}")
    client = None

def get_mime_type(image_path: str) -> str:
    ext = os.path.splitext(image_path)[1].lower()
    if ext in ['.png']:
        return 'image/png'
    elif ext in ['.webp']:
        return 'image/webp'
    return 'image/jpeg'

def robot_perception_query(image_path: str, prompt_text: str, model_name: str = DEFAULT_MODEL):
    """
    Executes a visual spatial perception query using Gemini Robotics ER 2.
    Supports 2D bounding boxes, point coordinates, and 3D spatial bounding boxes.
    """
    print(f"\n🤖 Robot: Analyzing {image_path} with model '{model_name}'...")
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found.")
        return None

    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    mime_type = get_mime_type(image_path)
    response_text = None

    if client:
        models_to_try = [model_name] + [m for m in FALLBACK_MODELS if m != model_name]
        for m in models_to_try:
            try:
                print(f"📡 Sending request to {m}...")
                response = client.models.generate_content(
                    model=m,
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                        prompt_text
                    ],
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        thinking_config=types.ThinkingConfig(thinking_budget=2048)
                    )
                )
                response_text = response.text
                print(f"✅ Success with model: {m}")
                break
            except Exception as e:
                print(f"⚠️ Failed with model '{m}': {e}")
                continue

    if not response_text:
        print("ℹ️ Running in simulated demo mode (offline / mock output)...")
        response_text = generate_simulated_spatial_output(prompt_text)

    print("\n🔍 Gemini Robotics Spatial Output:")
    print("--------------------------------------------------")
    print(response_text)
    print("--------------------------------------------------")
    
    visualize_results(image_path, response_text)
    return response_text

def generate_simulated_spatial_output(prompt_text: str) -> str:
    """Generates high-fidelity simulated ER 2 output for offline or demonstration mode."""
    prompt_lower = prompt_text.lower()
    if "3d" in prompt_lower or "metric" in prompt_lower or "grasp" in prompt_lower:
        mock_data = [
            {
                "label": "industrial_gear_box",
                "box_3d": {
                    "center": [0.08, 0.62, -0.04],
                    "size": [0.18, 0.22, 0.14],
                    "rotation_rpy": [0.0, 0.0, 15.0]
                },
                "grasp_affordance": {
                    "target_point_2d": [520, 480],
                    "approach_vector": [0.0, 0.0, -1.0],
                    "gripper_aperture_mm": 65,
                    "grasp_type": "power"
                },
                "confidence": 0.96
            },
            {
                "label": "calibration_wrench",
                "box_3d": {
                    "center": [-0.15, 0.48, -0.08],
                    "size": [0.06, 0.24, 0.03],
                    "rotation_rpy": [0.0, 0.0, -45.0]
                },
                "grasp_affordance": {
                    "target_point_2d": [680, 240],
                    "approach_vector": [0.0, 0.0, -1.0],
                    "gripper_aperture_mm": 28,
                    "grasp_type": "pinch"
                },
                "confidence": 0.94
            }
        ]
    elif "point" in prompt_lower and "box" not in prompt_lower:
        mock_data = [
            {"point": [421, 312], "label": "blue mug"},
            {"point": [680, 540], "label": "wrench"},
            {"point": [290, 810], "label": "power drill"}
        ]
    else:
        mock_data = [
            {"box_2d": [380, 290, 520, 395], "label": "blue ceramic mug"},
            {"box_2d": [620, 500, 710, 680], "label": "silver adjustable wrench"}
        ]
    return json.dumps(mock_data, indent=2)

def parse_spatial_json(response_text: str):
    """Extracts JSON arrays or dictionaries from response text."""
    try:
        clean_text = re.sub(r'```json\s*', '', response_text)
        clean_text = re.sub(r'```\s*', '', clean_text).strip()
        match = re.search(r'(\[.*\]|\{.*\})', clean_text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except Exception as e:
        print(f"Warning: could not parse spatial JSON: {e}")
    return None

def visualize_results(image_path: str, response_text: str, output_path: str = "output_perception.jpg"):
    """Draws 2D/3D overlays, bounding boxes, and grasp vectors onto the image."""
    try:
        image = Image.open(image_path).convert('RGB')
        draw = ImageDraw.Draw(image)
        w, h = image.size
        
        data = parse_spatial_json(response_text)
        if not data:
            return None

        if isinstance(data, dict):
            data = [data]

        colors = ["#00FF88", "#00C3FF", "#FF3366", "#FFDD00", "#AA00FF"]

        for idx, item in enumerate(data):
            color = colors[idx % len(colors)]
            label = item.get("label") or item.get("name") or f"Item {idx+1}"

            # 1. 2D Bounding Box [ymin, xmin, ymax, xmax] in 0-1000
            if "box_2d" in item:
                box = item["box_2d"]
                ymin, xmin, ymax, xmax = box
                abs_ymin = int((ymin / 1000.0) * h)
                abs_xmin = int((xmin / 1000.0) * w)
                abs_ymax = int((ymax / 1000.0) * h)
                abs_xmax = int((xmax / 1000.0) * w)
                draw.rectangle([abs_xmin, abs_ymin, abs_xmax, abs_ymax], outline=color, width=3)
                draw.text((abs_xmin + 5, max(0, abs_ymin - 15)), label, fill=color)

            # 2. 2D Point [y, x] in 0-1000
            if "point" in item:
                pt = item["point"]
                py = int((pt[0] / 1000.0) * h)
                px = int((pt[1] / 1000.0) * w)
                r = 6
                draw.ellipse([px - r, py - r, px + r, py + r], fill=color, outline="white", width=2)
                draw.text((px + 8, py - 6), label, fill=color)

            # 3. 3D Bounding Box / Grasp Affordance
            if "grasp_affordance" in item:
                ga = item["grasp_affordance"]
                if "target_point_2d" in ga:
                    gpt = ga["target_point_2d"]
                    gpy = int((gpt[0] / 1000.0) * h)
                    gpx = int((gpt[1] / 1000.0) * w)
                    r = 8
                    draw.ellipse([gpx - r, gpy - r, gpx + r, gpy + r], fill="#FF0055", outline="white", width=2)
                    draw.text((gpx + 10, gpy - 8), f"6DoF Grasp: {label}", fill="#FF0055")

        image.save(output_path)
        print(f"🖼️ Perception visualization saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Warning: visualization failed: {e}")
        return None

if __name__ == "__main__":
    test_img = "assets/pointing_undefined.png"
    if not os.path.exists(test_img):
        test_img = "robot_view.jpg"
        if not os.path.exists(test_img):
            Image.new('RGB', (640, 480), color=(30, 30, 40)).save(test_img)

    query = """
    Detect all manipulable objects. Return 3D bounding boxes and 6DoF grasp affordances in JSON:
    [{"label": "name", "box_3d": {"center": [x,y,z], "size": [dx,dy,dz]}, "grasp_affordance": {"target_point_2d": [y,x], "approach_vector": [vx,vy,vz], "gripper_aperture_mm": 50}}]
    """
    robot_perception_query(test_img, query)
