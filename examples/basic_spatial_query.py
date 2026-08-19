from google import genai
from google.genai import types
import os
import json
import re
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# GEMINI ROBOTICS: ADVANCED SPATIAL QUERY & 3D GROUNDING (ER 2 & ER 1.5)
# -------------------------------------------------------------------------
# This script demonstrates querying Google DeepMind's Gemini Robotics ER 2
# (and ER 1.5) for 2D bounding boxes, pixel points, and 3D bounding boxes
# / 6DoF grasp poses for robotic manipulation and perception.
# -------------------------------------------------------------------------

# 1. SETUP & MODEL DEFINITIONS
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
    print("⚠️ Warning: GEMINI_API_KEY not found in .env or environment.")
else:
    print("✅ Gemini API Key loaded.")

# 2. CLIENT CONFIGURATION
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
        # Try requested model, then fall back if model unavailable in region/tier
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
                        temperature=0.2, # Low temperature for accurate spatial grounding
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
    """Generates a realistic simulated output matching ER 2 schema."""
    if "3d" in prompt_text.lower() or "box_3d" in prompt_text.lower():
        return json.dumps([
            {
                "label": "manipulation_target (mug)",
                "box_2d": [380, 420, 620, 580],
                "box_3d": {
                    "center": [0.05, 0.45, 0.12],
                    "size": [0.10, 0.08, 0.12],
                    "rotation_rpy": [0.0, 0.0, 45.0]
                },
                "grasp_affordance": {
                    "point": [480, 560],
                    "approach_vector": [0.0, 1.0, 0.0],
                    "gripper_opening_width_mm": 45
                }
            }
        ], indent=2)
    elif "point" in prompt_text.lower():
        return json.dumps([
            {"label": "mug_handle_grasp_point", "point": [500, 550]},
            {"label": "table_surface_center", "point": [750, 500]}
        ], indent=2)
    else:
        return json.dumps([
            {"label": "robot_arm_base", "box_2d": [600, 100, 950, 400]},
            {"label": "target_object", "box_2d": [420, 450, 610, 580]}
        ], indent=2)

def visualize_results(image_path: str, response_text: str, output_path: str = "output_perception.jpg"):
    """
    Parses spatial JSON results and renders bounding boxes (2D/3D) and grasp points on the image.
    """
    try:
        # Extract JSON block if wrapped in markdown
        json_match = re.search(r'```(?:json)?\s*(\[.*?\]|\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            raw_json = json_match.group(1)
        else:
            raw_json = response_text.strip()

        data = json.loads(raw_json)
        if isinstance(data, dict) and "detections" in data:
            data = data["detections"]
        elif not isinstance(data, list):
            data = [data]

        img = Image.open(image_path).convert('RGB')
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        print(f"\n🎨 Drawing {len(data)} detected spatial features on '{output_path}'...")
        
        for item in data:
            if not isinstance(item, dict):
                continue

            label = item.get("label", "detected_object")

            # 1. Render Point
            if 'point' in item:
                y, x = item['point']
                pixel_x = int((x / 1000.0) * width)
                pixel_y = int((y / 1000.0) * height)
                r = 8
                draw.ellipse((pixel_x - r, pixel_y - r, pixel_x + r, pixel_y + r), fill='#00FFCC', outline='#003333', width=2)
                draw.text((pixel_x + 12, pixel_y - 8), f"📍 {label} ({x},{y})", fill="#00FFCC")

            # 2. Render 2D Bounding Box
            if 'box_2d' in item:
                ymin, xmin, ymax, xmax = item['box_2d']
                pixel_xmin = int((xmin / 1000.0) * width)
                pixel_xmax = int((xmax / 1000.0) * width)
                pixel_ymin = int((ymin / 1000.0) * height)
                pixel_ymax = int((ymax / 1000.0) * height)
                
                draw.rectangle([pixel_xmin, pixel_ymin, pixel_xmax, pixel_ymax], outline='#FF3366', width=3)
                draw.text((pixel_xmin + 4, max(0, pixel_ymin - 16)), f"📦 {label}", fill="#FF3366")

            # 3. Render 3D Bounding Box Annotations if available
            if 'box_3d' in item:
                b3 = item['box_3d']
                center = b3.get("center", [0, 0, 0])
                c_text = f"3D Pos: x={center[0]:.2f}m, y={center[1]:.2f}m, z={center[2]:.2f}m"
                if 'box_2d' in item:
                    draw.text((pixel_xmin + 4, min(height - 15, pixel_ymax + 4)), c_text, fill="#33CCFF")

            # 4. Render Grasp Affordance
            if 'grasp_affordance' in item:
                g = item['grasp_affordance']
                if 'point' in g:
                    gy, gx = g['point']
                    g_px = int((gx / 1000.0) * width)
                    g_py = int((gy / 1000.0) * height)
                    gr = 10
                    draw.ellipse((g_px - gr, g_py - gr, g_px + gr, g_py + gr), fill='#FFFF00', outline='black', width=2)
                    draw.text((g_px + 12, g_py + 4), f"🤏 Grasp Point", fill="#FFFF00")

        img.save(output_path)
        print(f"✅ Saved perception overlay visualization to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"⚠️ Could not visualize results: {e}")
        return None

if __name__ == "__main__":
    test_image = "robot_view.jpg"
    if not os.path.exists(test_image):
        print("Creating dummy robot_view.jpg for demonstration...")
        Image.new('RGB', (640, 480), color=(45, 55, 72)).save(test_image)

    # Example: 3D-aware spatial bounding box and grasp query for ER 2
    prompt = """
    Detect all manipulable objects and robots in the scene.
    Return 2D bounding boxes, estimated 3D bounding boxes (in meters relative to camera frame), and 6DoF grasp points.
    Format as JSON:
    [
      {
        "label": "object_name",
        "box_2d": [ymin, xmin, ymax, xmax],
        "box_3d": {"center": [x, y, z], "size": [dx, dy, dz], "rotation_rpy": [r, p, y]},
        "grasp_affordance": {"point": [y, x], "approach_vector": [x, y, z], "gripper_opening_width_mm": 50}
      }
    ]
    """
    robot_perception_query(test_image, prompt)
