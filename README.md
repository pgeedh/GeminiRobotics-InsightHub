# Awesome Gemini Robotics 2.0 <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/2560px-Google_Gemini_logo.svg.png" align="right" width="100">

[![DeepMind](https://img.shields.io/badge/Maintained%20By-Google%20DeepMind%20Trusted%20Tester-4285F4?style=for-the-badge&logo=google)](https://deepmind.google/models/gemini-robotics/embodied-reasoning/)
[![Gemini Robotics](https://img.shields.io/badge/Model-Gemini%20Robotics%20ER%202%20%7C%201.5-blue?style=for-the-badge)](https://aistudio.google.com/)
[![ROS 2](https://img.shields.io/badge/ROS%202-Humble%20%7C%20Iron%20%7C%20Jazzy-orange?style=for-the-badge&logo=ros)](./ros2_gemini_bridge)
[![Interactive 3D Demo](https://img.shields.io/badge/Interactive%203D-Architecture%20Explainer-purple?style=for-the-badge&logo=three.js)](./docs/architecture_3d_explainer.html)
[![Benchmarks](https://img.shields.io/badge/Benchmarks-ERQA%20%7C%20ASIMOV-green?style=for-the-badge)](./BENCHMARKS.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](./LICENSE)

🌐 **Languages:** **English** • [日本語 (Japanese)](./README_ja.md) • [中文 (Chinese)](./README_zh.md) • [한국어 (Korean)](./README_kr.md) • [Tiếng Việt (Vietnamese)](./README_vn.md)

---

> **🚀 THE DEFINITIVE COMMUNITY & DEVELOPER GALLERY FOR GEMINI ROBOTICS 2.0**
> 
> A curated, community-maintained gallery of **Google DeepMind Gemini Robotics 2.0**, **Gemini Robotics ER 2 (Embodied Reasoning)**, and **Gemini Robotics 2 (VLA)** prompts, schemas, recipes, and production code snippets ready to copy-paste into your own robotics and embodied AI pipelines.
> 
> **What is Gemini Robotics 2.0?** Google DeepMind's flagship physical AI suite operating on a **Hierarchical Dual-Model Paradigm**:
> 1. **The Planner / Upper Brain (Gemini Robotics ER 2):** High-level embodied spatial reasoning, 3D metric bounding, long-horizon task planning, continuous video slip/anomaly tracking, and agentic tool use.
> 2. **The Motor Cortex / Doer (Gemini Robotics 2 VLA & On-Device 2):** High-frequency (20Hz+) motor policies generating direct joint and Cartesian trajectories for humanoids, cobots, and mobile rovers without "stop-and-think" latency.

---

## 📑 Contents

- [🎮 Interactive 3D Visual Architecture Explainer](#-interactive-3d-visual-architecture-explainer)
- [⚡ Quick Start (`google-genai` SDK v1.x)](#-quick-start)
- [🗂️ Complete Use Cases & Prompt Gallery (35 Cards)](#-complete-use-cases--prompt-gallery-35-cards)
  - [1. Spatial Grounding & 2D/3D Pointing (Cards 1–7)](#1-spatial-grounding--2d3d-pointing)
  - [2. Bounding Volumes & 6DoF Grasping (Cards 8–10)](#2-bounding-volumes--6dof-grasping)
  - [3. Trajectory & Whole-Body Motion Planning (Cards 11–14)](#3-trajectory--whole-body-motion-planning)
  - [4. Long-Horizon Task Decomposition (Cards 15–18)](#4-long-horizon-task-decomposition)
  - [5. Affordance & ASIMOV Safety Governance (Cards 19–22)](#5-affordance--asimov-safety-governance)
  - [6. Continuous Video & Temporal Reasoning (Cards 23–26)](#6-continuous-video--temporal-reasoning)
  - [7. Metrology, Gauges & Dense Segmentation (Cards 27–29)](#7-metrology-gauges--dense-segmentation)
  - [8. Agentic Tool Use & Multi-Robot Fleet (Cards 30–33)](#8-agentic-tool-use--multi-robot-fleet)
  - [9. Vision-Language-Action (VLA) Motor Control (Cards 34–35)](#9-vision-language-action-vla-motor-control)
- [🎥 Official DeepMind Robotics Video Showcase](#-official-deepmind-robotics-video-showcase)
- [📊 Official Benchmarks: ER 1.5 vs. Gemini Robotics ER 2](#-official-benchmarks-er-15-vs-gemini-robotics-er-2)
- [🤖 ROS 2 Bridge Integration](#-ros-2-bridge-integration-ros2_gemini_bridge)
- [💡 5 Golden Rules for Embodied Reasoning](#-5-golden-rules-for-embodied-reasoning)
- [🧪 Interactive Suite CLI & Testing](#-interactive-suite-cli--testing)
- [🤝 Contributing & PR Guide](#-contributing)

---

## 🎮 Interactive 3D Visual Architecture Explainer

Explore the internal mechanisms of Gemini Robotics 2 in real-time 3D WebGL. Inspect how RGB-D camera streams map to spatial attention tokens, 3D metric bounding boxes, whole-body kinematic plans, and 20Hz VLA joint trajectories:

<p align="center">
  <a href="./docs/architecture_3d_explainer.html">
    <img src="./assets/gemini_robotics_architecture.svg" alt="Gemini Robotics 2 Interactive 3D Architecture" width="100%" />
  </a>
</p>
<p align="center">
  👉 <b><a href="./docs/architecture_3d_explainer.html">Launch Full Interactive 3D Architecture & Spatial Explainer in Browser</a></b>
</p>

---

## ⚡ Quick Start

Minimal Python snippet using Google's official [`google-genai`](https://pypi.org/project/google-genai/) SDK (v1.x):

```python
from google import genai
from google.genai import types

# Initialize official Gemini API Client
client = genai.Client()
MODEL_ID = "gemini-robotics-er-2"  # or "gemini-robotics-er-1.5-preview"

# Spatial Pointing Query
prompt = """
Point to no more than 10 items in the image.
Return JSON format: [{"point": [y, x], "label": "<name>"}]
with coordinates normalized between 0-1000.
"""

with open("assets/pointing_undefined.png", "rb") as f:
    img_bytes = f.read()

response = client.models.generate_content(
    model=MODEL_ID,
    contents=[
        types.Part.from_bytes(data=img_bytes, mime_type="image/png"),
        prompt
    ],
    config=types.GenerateContentConfig(
        temperature=0.2,
        thinking_config=types.ThinkingConfig(thinking_budget=1024)
    )
)

print(response.text)
```

---

## 🗂️ Complete Use Cases & Prompt Gallery (35 Cards)

> **Legend:**
> - `✅` = Visual demonstration included from official DeepMind research / dataset
> - `🧩` = Bring-your-own image or custom robot scenario

---

### 1. Spatial Grounding & 2D/3D Pointing

#### 1) Pointing to Undefined Objects (Open-Vocabulary 2D Discovery) ✅
<p align="center"><img src="./assets/pointing_undefined.png" alt="Pointing to Undefined Objects" width="500px"/></p>

**Prompt:**
```json
Point to no more than 10 items in the image. The label returned should be an identifying name for the object detected. The answer should follow the json format: [{"point": [y, x], "label": "<object_name>"}]. The points are in [y, x] format normalized to 0-1000.
```

**Python Snippet:**
```python
response = client.models.generate_content(
    model="gemini-robotics-er-2",
    contents=[types.Part.from_bytes(data=img_bytes, mime_type="image/png"), prompt]
)
```

**Model Output:**
```json
[
  {"point": [421, 312], "label": "blue ceramic mug"},
  {"point": [680, 540], "label": "stainless steel adjustable wrench"},
  {"point": [290, 810], "label": "cordless power drill"}
]
```
🔗 *Reference:* [DeepMind Embodied Reasoning](https://deepmind.google/models/gemini-robotics/embodied-reasoning/)

---

#### 2) Pointing to Defined Objects (Multi-Category Filtering) ✅
<p align="center"><img src="./assets/find_fruit.png" alt="Find Target Objects" width="500px"/></p>

**Prompt:**
```json
Get all points matching the following target objects: bread, starfruit, banana. The label returned should be the identifying name for the object detected. Return valid JSON only: [{"point": [y, x], "label": "<target>"}]. Coordinates are normalized between 0-1000 [y, x].
```

**Model Output:**
```json
[
  {"point": [380, 240], "label": "banana"},
  {"point": [520, 610], "label": "starfruit"},
  {"point": [710, 450], "label": "bread"}
]
```

---

#### 3) Abstract Semantic Pointing (Category & Functional Grouping) ✅
<p align="center"><img src="./assets/find_fruit.png" alt="Abstract Category Pointing" width="500px"/></p>

**Prompt:**
```json
Get all points for any visible fruit. Identify individual items even under partial occlusion. Return JSON format: [{"point": [y, x], "label": "<item_name>"}] with [y, x] normalized to 0-1000.
```

**Model Output:**
```json
[
  {"point": [380, 240], "label": "banana"},
  {"point": [410, 310], "label": "green apple"},
  {"point": [520, 610], "label": "starfruit"}
]
```

---

#### 4) Grid Board & Matrix Slot Localization (Pegboard / Connect Four) 🧩

**Prompt:**
```json
Get all points matching empty game board slots and game pieces. Return the result in JSON format: [{"point": [y, x], "label": "<slot_row_col | piece_color>"}]. All coordinates normalized to 0-1000.
```

**Model Output:**
```json
[
  {"point": [310, 450], "label": "slot_row1_col3_empty"},
  {"point": [420, 450], "label": "red_game_piece"}
]
```

---

#### 5) Serial Part & Affordance Pointing (Stem, Rim, Handle, Nozzle) ✅
<p align="center"><img src="./assets/part_identification.png" alt="Part Identification" width="500px"/></p>

**Prompt:**
```json
Point to the specific functional part of the target object: stem of banana, rim of measuring cup, and handle of paper bag. Return a JSON list: [{"point": [y, x], "label": "<object_part>"}] with y/x in 0-1000.
```

**Model Output:**
```json
[
  {"point": [345, 210], "label": "banana_stem"},
  {"point": [612, 735], "label": "measuring_cup_rim"},
  {"point": [180, 520], "label": "paper_bag_handle"}
]
```

---

#### 6) Counting by Pointing with Visual Reason Trace ✅
<p align="center"><img src="./assets/counting_reasoning.png" alt="Counting with Reason" width="500px"/></p>

**Prompt:**
```json
Point to each individual washer or mechanical fastener in the container. Provide visual reasoning steps and count confirmation. Format: [{"point": [y, x], "label": "washer_<index>"}] with coordinates normalized 0-1000.
```

**Model Output:**
```json
[
  {"point": [410, 320], "label": "washer_1"},
  {"point": [445, 360], "label": "washer_2"},
  {"point": [480, 410], "label": "washer_3"},
  {"point": [520, 390], "label": "washer_4"}
]
```

---

#### 7) Defined Object Pointing Across Multi-Frame Sequence / GIF ✅
<p align="center"><img src="./assets/clip_franka_dexterity.gif" alt="Dynamic Video Tracking" width="500px"/></p>

**Prompt:**
```json
Point to the following items across the dynamic sequence: 'pen in gripper', 'pen on desk', 'open container'. Return a JSON list: [{"point": [y, x], "label": "<object_state>"}]. If an object is not present in the current view, omit it.
```

**Model Output:**
```json
[
  {"point": [512, 480], "label": "pen in gripper"},
  {"point": [720, 310], "label": "open container"}
]
```

---

### 2. Bounding Volumes & 6DoF Grasping

#### 8) 2D Bounding Boxes with Unique Descriptive Identifiers ✅
<p align="center"><img src="./assets/pointing_undefined.png" alt="2D Bounding Boxes" width="500px"/></p>

**Prompt:**
```json
Return bounding boxes as a JSON array with descriptive labels distinguishing similar objects by color, size, and location. Format: [{"box_2d": [ymin, xmin, ymax, xmax], "label": "<attribute_label>"}] normalized to 0-1000 integers.
```

**Model Output:**
```json
[
  {"box_2d": [380, 290, 520, 395], "label": "ceramic blue coffee mug on left"},
  {"box_2d": [620, 500, 710, 680], "label": "silver adjustable wrench in center"}
]
```

---

#### 9) 3D Metric Bounding Volumes [x, y, z, dx, dy, dz] & Center of Mass ✅
<p align="center"><img src="./assets/clip_apollo_wholebody.png" alt="3D Metric Bounding" width="500px"/></p>

**Prompt:**
```json
Detect the objects on the workbench. Return metric 3D bounding boxes in camera frame coordinates (meters) including center [x, y, z] and dimensions [dx, dy, dz]. Return JSON: [{"label": "<name>", "center_m": [x, y, z], "size_m": [dx, dy, dz], "confidence": <0.0-1.0>}].
```

**Model Output:**
```json
[
  {
    "label": "industrial_gear_box",
    "center_m": [0.08, 0.62, -0.04],
    "size_m": [0.18, 0.22, 0.14],
    "confidence": 0.96
  }
]
```

---

#### 10) 6DoF Grasp Affordance, Normal Approach & Aperture Limits ✅
<p align="center"><img src="./assets/clip_franka_dexterity.png" alt="6DoF Grasp Pose" width="500px"/></p>

**Prompt:**
```json
For the target tool, compute the 6DoF grasp pose, approach normal vector, and maximum gripper opening aperture. Return JSON: {"target": "<tool>", "grasp_center_3d": [x, y, z], "approach_normal": [nx, ny, nz], "gripper_aperture_mm": <val>, "grasp_type": "pinch|power|suction"}.
```

**Model Output:**
```json
{
  "target": "cordless_drill",
  "grasp_center_3d": [0.12, 0.55, 0.02],
  "approach_normal": [0.0, 0.0, -1.0],
  "gripper_aperture_mm": 65,
  "grasp_type": "power"
}
```

---

### 3. Trajectory & Whole-Body Motion Planning

#### 11) Simple Trajectory Planning (Ordered Waypoint Sequences) ✅
<p align="center"><img src="./assets/obstacle_avoidance.png" alt="Trajectory Waypoints" width="500px"/></p>

**Prompt:**
```json
Place a point on the red pen, then 15 ordered trajectory waypoints to transfer the pen to the organizer tray on the left. Return JSON: [{"point": [y, x], "label": "step_<idx>"}] with points in [y, x] format normalized to 0-1000.
```

**Model Output:**
```json
[
  {"point": [650, 480], "label": "step_0_start"},
  {"point": [580, 450], "label": "step_1_lift"},
  {"point": [420, 310], "label": "step_7_midflight"},
  {"point": [310, 180], "label": "step_15_target_bin"}
]
```

---

#### 12) Surface Brushing, Wiping & Polishing Multi-Point Coverage ✅
<p align="center"><img src="./assets/trajectory_brushing.png" alt="Surface Brushing" width="500px"/></p>

**Prompt:**
```json
Point to the blue brush tool and generate 10 ordered coverage trajectory points across the debris region to thoroughly clean the plate without scattering particles. Return JSON: [{"point": [y, x], "label": "step_<index>"}] normalized 0-1000.
```

**Model Output:**
```json
[
  {"point": [720, 210], "label": "tool_brush_origin"},
  {"point": [580, 410], "label": "step_1_stroke_start"},
  {"point": [490, 560], "label": "step_5_stroke_mid"},
  {"point": [390, 680], "label": "step_10_dustpan_edge"}
]
```

---

#### 13) 3D Obstacle-Avoidance Spline Navigation ✅
<p align="center"><img src="./assets/obstacle_avoidance.png" alt="Obstacle Avoidance Path" width="500px"/></p>

**Prompt:**
```json
Find the most direct collision-free trajectory of 10 points on the floor between the robot view origin and the green ottoman in the back left. The trajectory must maintain at least 40cm clearance from all floor obstacles. Return JSON: [{"point": [y, x], "label": "wp_<idx>"}] normalized 0-1000.
```

**Model Output:**
```json
[
  {"point": [920, 500], "label": "wp_0_start"},
  {"point": [780, 460], "label": "wp_3_avoid_chair_leg"},
  {"point": [590, 390], "label": "wp_6_corridor_pass"},
  {"point": [340, 260], "label": "wp_10_target_ottoman"}
]
```

---

#### 14) Whole-Body Humanoid Posture Reasoning (Crouch vs Reach vs Dual-Arm) ✅
<p align="center"><img src="./assets/clip_apollo_wholebody.gif" alt="Apollo Whole Body" width="500px"/></p>

**Prompt:**
```json
The target payload is located on the low shelf (height: 38cm). 1. Determine if whole-body crouching is required. 2. Calculate center-of-mass balance constraint. 3. Output whole-body configuration sequence: base_pose [x,y], knee_flexion_deg, torso_pitch_deg, active_arms. Return JSON: {"crouch_required": true, "torso_pitch_deg": <deg>, "knee_flexion_deg": <deg>, "action_sequence": [...]}
```

**Model Output:**
```json
{
  "crouch_required": true,
  "torso_pitch_deg": 22.5,
  "knee_flexion_deg": 48.0,
  "action_sequence": [
    "stand_to_half_squat",
    "torso_pitch_forward",
    "dual_arm_reach_under_shelf",
    "bimanual_power_grasp"
  ]
}
```

---

### 4. Long-Horizon Task Decomposition

#### 15) Decluttering & Space Creation (Identify Obstruction to Remove) 🧩

**Prompt:**
```json
Point to the primary obstructing object that must be moved to create sufficient clearance for placing an open 15-inch laptop on this desk surface. Return JSON: [{"point": [y, x], "label": "<obstructing_item>"}] with coordinates normalized 0-1000.
```

**Model Output:**
```json
[
  {"point": [560, 480], "label": "stacked coffee mug and notebook"}
]
```

---

#### 16) Multi-Stage Orchestration (Packing Lunch Box & Bag) 🧩

**Prompt:**
```json
Explain how to pack the lunch box and lunch bag step-by-step. Point to each item referenced in the plan. Return JSON: [{"step": <int>, "action": "<desc>", "target_point": [y, x], "destination_point": [y, x]}].
```

**Model Output:**
```json
[
  {"step": 1, "action": "Pick wrapped sandwich and place into bottom tray", "target_point": [610, 240], "destination_point": [380, 720]},
  {"step": 2, "action": "Pick apple and place into side compartment", "target_point": [520, 410], "destination_point": [340, 810]},
  {"step": 3, "action": "Close lunchbox lid and slide into outer insulated bag", "target_point": [360, 750], "destination_point": [220, 890]}
]
```

---

#### 17) Unobstructed Socket & Insertion Port Localization 🧩
<p align="center"><img src="./assets/demo_spot_inspection.svg" alt="Socket Localization" width="500px"/></p>

**Prompt:**
```json
Point to all unobstructed, empty electrical sockets on the wall strip that are ready for cable plug insertion. Ignore sockets currently occupied by plugs. Return JSON: [{"point": [y, x], "label": "<socket_idx>"}] normalized 0-1000.
```

**Model Output:**
```json
[
  {"point": [450, 310], "label": "empty_grounded_socket_left"},
  {"point": [450, 680], "label": "empty_grounded_socket_right"}
]
```

---

#### 18) Reference-Photo Guided Reorganization (Before / After Transformation) 🧩

**Prompt:**
```json
Given Image A (current cluttered workbench) and Image B (target organized reference state), produce a multi-step pick-and-place reorganization plan. For each step return: {"item": "<name>", "current_box": [ymin, xmin, ymax, xmax], "target_box": [ymin, xmin, ymax, xmax], "rationale": "<desc>"}.
```

**Model Output:**
```json
[
  {
    "item": "soldering_iron",
    "current_box": [620, 210, 750, 390],
    "target_box": [220, 780, 350, 940],
    "rationale": "Move hot tool to heat-resistant stand in upper right"
  }
]
```

---

### 5. Affordance & ASIMOV Safety Governance

#### 19) Payload & Physical Limitation Filtering (3 lb / 1.5 kg Thresholds) 🧩

**Prompt:**
```json
The robot arm has a strict maximum payload capacity of 3.0 lbs (1.36 kg). Point only to objects in the scene that are physically safe for the arm to lift without overloading torque limits. Return JSON: [{"point": [y, x], "label": "<item>", "estimated_weight_lbs": <val>}].
```

**Model Output:**
```json
[
  {"point": [380, 240], "label": "banana", "estimated_weight_lbs": 0.4},
  {"point": [410, 310], "label": "apple", "estimated_weight_lbs": 0.5},
  {"point": [520, 610], "label": "starfruit", "estimated_weight_lbs": 0.3}
]
```

---

#### 20) Fragile Glassware Handling & Compliant Normal Force Limits 🧩

**Prompt:**
```json
Analyze fragile laboratory glassware in the scene (wine glass, beaker, test tube). 1. Return 3D bounding box [x,y,z,dx,dy,dz]. 2. Identify grasp contact zone. 3. Prescribe max grip normal force (Newtons) and max lift acceleration (m/s^2). Return JSON format.
```

**Model Output:**
```json
[
  {
    "item": "borosilicate_beaker",
    "grasp_zone": "lower_cylindrical_body",
    "max_normal_force_n": 5.2,
    "max_lift_accel_ms2": 0.8,
    "grasp_type": "compliant_parallel_jaw"
  }
]
```

---

#### 21) Post-Task Cleanup Affordance Pointing (Mug & Dish Placement) ✅
<p align="center"><img src="./assets/pointing_undefined.png" alt="Cleanup Affordance" width="500px"/></p>

**Prompt:**
```json
I finished my coffee. Where should the robot arm place the empty dirty mug to clean up? Point to the optimal placement location. Return JSON: [{"point": [y, x], "label": "<cleanup_location>"}] normalized 0-1000.
```

**Model Output:**
```json
[
  {"point": [280, 840], "label": "dishwasher upper rack open tray"}
]
```

---

#### 22) ASIMOV-Agentic Safety Governor (Autonomous Kinetic Refusal) ✅
<p align="center"><img src="./assets/clip_apollo_wholebody.png" alt="Safety Envelope" width="500px"/></p>

**Prompt:**
```json
User Request: 'Rapidly swing the steel bar at maximum velocity.' Current Scene: Human coworker is standing 0.75m away from robot envelope. 1. Evaluate safety feasibility under ISO/TS 15066. 2. Output decision: ACCEPT or REFUSE. 3. If REFUSED, provide safety rationale and certified safe alternative.
```

**Model Output:**
```json
{
  "decision": "REFUSE",
  "violation": "ISO/TS 15066 Human Proximity Breach (0.75m < 1.2m safety bubble)",
  "hazard": "Uncontrolled kinetic energy risk near coworker",
  "safe_alternative": "Lock protective interlock cage and execute motion test at 10% rated velocity (< 0.25 m/s)."
}
```

---

### 6. Continuous Video & Temporal Reasoning

#### 23) Full Episode Video Decomposition with Timestamp Intervals ✅
<p align="center"><img src="./assets/clip_franka_dexterity.gif" alt="Video Timestamp Parsing" width="500px"/></p>

**Prompt:**
```json
You are given a robot manipulation video. Describe in chronological detail each step of completing the task. Output JSON with keys: [{"start_timestamp": "MM:SS", "end_timestamp": "MM:SS", "action": "<description>", "confidence": <float>}].
```

**Model Output:**
```json
[
  {"start_timestamp": "00:00", "end_timestamp": "00:03", "action": "Right arm approaches tool holster", "confidence": 0.98},
  {"start_timestamp": "00:03", "end_timestamp": "00:06", "action": "Gripper grasps hex key and extracts vertically", "confidence": 0.95},
  {"start_timestamp": "00:06", "end_timestamp": "00:11", "action": "Aligns hex key with socket bolt and begins tightening", "confidence": 0.97}
]
```

---

#### 24) Temporal Zoom: High-Frequency Sub-Second Micro-Action Breakdown ✅
<p align="center"><img src="./assets/clip_franka_dexterity.gif" alt="Micro-Action Breakdown" width="500px"/></p>

**Prompt:**
```json
Zoom into video interval 00:04 to 00:08 and provide a sub-second breakdown of contact kinematics, finger closure, and tactile seating. Output JSON: [{"timestamp": "SS.ms", "event": "<desc>", "contact_state": "pre-contact|initial_touch|firm_grip"}].
```

**Model Output:**
```json
[
  {"timestamp": "04.20", "event": "Finger pads reach 5mm standoff distance", "contact_state": "pre-contact"},
  {"timestamp": "05.10", "event": "Tactile surface touches component edge", "contact_state": "initial_touch"},
  {"timestamp": "06.45", "event": "Full force closure achieved; normal load stable", "contact_state": "firm_grip"}
]
```

---

#### 25) Physical Task Success / Failure Verification & Anomaly Audit ✅
<p align="center"><img src="./assets/success_start.png" alt="Success Verification" width="500px"/></p>

**Prompt:**
```json
Inspect the multi-camera episode start frames vs episode final frames. Did the robot arm successfully complete the goal: 'Place the mango inside the brown storage bin without bruising'? Answer JSON: {"task_success": true|false, "failure_reason": "<desc or null>", "verification_confidence": <0.0-1.0>}.
```

**Model Output:**
```json
{
  "task_success": true,
  "failure_reason": null,
  "verification_confidence": 0.99
}
```

---

#### 26) Mid-Execution Grasp Slip Detection & Dynamic Closed-Loop Replanning ✅
<p align="center"><img src="./assets/demo_video_slip_recovery.svg" alt="Slip Detection" width="500px"/></p>

**Prompt:**
```json
Monitor live streaming frames. At timestamp 00:03.4, the payload slips 15mm downward in the gripper. 1. Detect slip event. 2. Calculate remaining grasp margin. 3. Output recovery command: increase squeeze force +12N, pause horizontal motion for 300ms, and re-level gripper pitch. Return JSON.
```

**Model Output:**
```json
{
  "slip_detected": true,
  "timestamp_sec": 3.42,
  "slip_displacement_mm": 14.8,
  "recovery_action": {
    "delta_squeeze_force_n": 12.0,
    "trajectory_pause_ms": 300,
    "pitch_trim_deg": -3.5
  }
}
```

---

### 7. Metrology, Gauges & Dense Segmentation

#### 27) Industrial Gauge & Analog Dial Needle Metrology (98% Precision) ✅
<p align="center"><img src="./assets/demo_spot_inspection.svg" alt="Gauge Inspection" width="500px"/></p>

**Prompt:**
```json
Read the industrial pressure gauge dial in the inspection image. Return needle angle (degrees), exact numerical value, unit of measurement, and operational status ('NORMAL'|'WARNING'|'CRITICAL'). Format JSON: {"gauge_type": "analog_dial", "value": <float>, "unit": "psi|bar", "status": "<status>"}.
```

**Model Output:**
```json
{
  "gauge_type": "analog_dial",
  "needle_angle_deg": 142.5,
  "value": 4.85,
  "unit": "bar",
  "status": "NORMAL"
}
```

---

#### 28) Code Execution Sub-Region Zoom for Low-Resolution Markings 🧩

**Prompt:**
```json
What is the exact serial number on the tiny barcode label? Use Python code execution to crop and zoom into the label region [ymin: 450, xmin: 680, ymax: 560, xmax: 820] to inspect high-frequency detail. Output JSON: {"serial_number": "<str>", "crop_box": [...]}.
```

**Model Output:**
```json
{
  "serial_number": "SN-8492-REV3B",
  "crop_box": [452, 684, 558, 818],
  "reading_quality": "verified"
}
```

---

#### 29) Dense Base64 Multi-Class Segmentation Masks (Gripper + Target) ✅
<p align="center"><img src="./assets/part_identification.png" alt="Dense Segmentation" width="500px"/></p>

**Prompt:**
```json
Provide exact instance segmentation masks for: 'left gripper finger', 'right gripper finger', and 'target fruit'. Return JSON: [{"box_2d": [ymin, xmin, ymax, xmax], "label": "<name>", "mask": "data:image/png;base64,<png_bytes>"}]. Coordinates in 0-1000 integers.
```

**Model Output:**
```json
[
  {
    "box_2d": [380, 210, 620, 480],
    "label": "target fruit",
    "mask": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
  }
]
```

---

### 8. Agentic Tool Use & Multi-Robot Fleet

#### 30) Agentic Tool Grounding: Google Search for Local Waste Sorting Rules ✅
<p align="center"><img src="./assets/find_fruit.png" alt="Tool Grounding" width="500px"/></p>

**Prompt:**
```json
Use Google Search to fetch the municipality municipal waste guidelines for Santa Clara County. Then, examine the packaging items on the table, classify each into 'Compost', 'Recycle', or 'Landfill', and point to where each item should be sorted using [y, x] 0-1000. Return JSON plan.
```

**Model Output:**
```json
[
  {"item": "corrugated cardboard box", "stream": "Recycle", "point": [410, 320], "local_rule": "Clean and flattened cardboard accepted in blue bin."},
  {"item": "greasy pizza box base", "stream": "Compost", "point": [680, 520], "local_rule": "Food-soiled paper belongs in organics/green bin."}
]
```

---

#### 31) Python Code Execution for Real-Time Frame Transforms 🧩
<p align="center"><img src="./assets/gemini_robotics_architecture.svg" alt="Coordinate Transform" width="500px"/></p>

**Prompt:**
```json
Given the detected object center [0.12, 0.45, 0.30] in camera optical frame and the camera-to-base transformation matrix T_base_cam, run a Python script to compute the end-effector goal pose in robot base frame and verify joint kinematics. Output JSON.
```

**Model Output:**
```json
{
  "target_in_base_frame_m": [0.582, -0.114, 0.245],
  "approach_quaternion_xyzw": [0.0, 0.7071, 0.0, 0.7071],
  "ik_solvable": true
}
```

---

#### 32) Heterogeneous Multi-Robot Coordination (Humanoid + AMR + Quadruped) ✅
<p align="center"><img src="./assets/clip_multi_robot.gif" alt="Multi-Robot Fleet" width="500px"/></p>

**Prompt:**
```json
Assign and synchronize tasks across the heterogeneous fleet: Spot Quadruped (inspection), Apollo 2 Humanoid (heavy lifting), and AMR Rover (transport). Output synchronized mission schedule with spatial wait barriers. Format JSON.
```

**Model Output:**
```json
{
  "mission_id": "WAREHOUSE_HEAVY_TRANSFER_04",
  "roles": {
    "spot_quadruped": "Navigate to aisle 4, scan QR code, verify payload cleared for transport",
    "apollo_humanoid": "Wait for barrier 'SPOT_SCAN_COMPLETE', perform bimanual lift of 18kg motor",
    "amr_rover": "Dock at transfer station, set mechanical latches, wait for 'APOLLO_SEATED'"
  }
}
```

---

#### 33) Dual-Arm Synchronized Cooperative Lifting ✅
<p align="center"><img src="./assets/clip_franka_dexterity.gif" alt="Dual-Arm Coordination" width="500px"/></p>

**Prompt:**
```json
Coordinate Left Arm (Franka L) and Right Arm (Franka R) to lift the wide tray containing liquid vessels without tilting > 2.0 degrees. Return synchronized trajectory waypoints for both end-effectors simultaneously in JSON format.
```

**Model Output:**
```json
{
  "tray_center_3d": [0.0, 0.55, 0.10],
  "left_arm_contact_point": [-0.22, 0.55, 0.10],
  "right_arm_contact_point": [0.22, 0.55, 0.10],
  "max_allowable_roll_deg": 2.0,
  "synchronized_lift_velocity_ms": 0.05
}
```

---

### 9. Vision-Language-Action (VLA) Motor Control

#### 34) Direct 20Hz VLA Joint Action Token Generation ✅
<p align="center"><img src="./assets/clip_vla_motor.gif" alt="VLA Motor Action" width="500px"/></p>

**Prompt:**
```text
Instruction: 'Grasp the red handle and pull outward smoothly.'
Input: 30fps wrist + overhead RGB camera stream.
Output: 20Hz continuous 7DoF delta action chunk [dx, dy, dz, droll, dpitch, dyaw, gripper_aperture].
```

**Python High-Frequency Loop:**
```python
action_chunk = vla_client.predict_actions(
    model="gemini-robotics-2-vla",
    wrist_image=wrist_frame,
    head_image=head_frame,
    text_instruction="Grasp the red handle and pull outward smoothly."
)
```

**Action Output Chunk:**
```json
{
  "chunk_length": 8,
  "delta_actions": [
    [0.002, 0.015, -0.004, 0.0, 0.02, 0.0, 1.0],
    [0.001, 0.018, -0.005, 0.0, 0.02, 0.0, 1.0],
    [0.000, 0.020, -0.006, 0.0, 0.01, 0.0, 0.2]
  ]
}
```

---

#### 35) On-Device Edge Policy Fast Adaptation (~2.5 Hours Calibration) ✅
<p align="center"><img src="./assets/clip_ondevice_adaptation.gif" alt="On-Device Adaptation" width="500px"/></p>

**Pipeline Call:**
```python
adaptation_metrics = adapt_edge_policy(
    base_model="gemini-robotics-2-ondevice",
    dataset_path="./demo_episodes/",
    target_hardware="enpire_compliant_gripper"
)
```

**Adaptation Report:**
```json
{
  "status": "ADAPTATION_COMPLETE",
  "training_time_hours": 2.45,
  "eval_success_rate": 0.942,
  "inference_latency_ms": 14.8
}
```

---

## 🎥 Official DeepMind Robotics Video Showcase

Direct captures and demonstrations from Google DeepMind's official [Gemini Robotics 2 & Embodied Reasoning](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) research release:

<div align="center">

| 🦾 **1. Whole-Body Humanoid Manipulation (Apollo 2)** | 🤝 **2. High-Precision Bi-Arm Dexterity (Franka F3)** |
| :---: | :---: |
| [![Apollo 2 Whole Body](./assets/clip_apollo_wholebody.gif)](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) | [![Franka Dexterity](./assets/clip_franka_dexterity.gif)](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) |
| *Apollo 2 whole-body humanoid control: crouching, carrying totes, and CoG balance.* <br> [▶ Watch DeepMind Humanoid Video](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) | *Two Franka arms synchronize fine manipulation: screwing light bulbs and folding.* <br> [▶ Watch Franka Bimanual Video](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) |

| 🤝 **3. Multi-Robot Heterogeneous Fleet Teamwork** | 🧠 **4. Embodied Reasoning (ER 2) Spatial Grounding** |
| :---: | :---: |
| [![Multi-Robot Teamwork](./assets/clip_multi_robot.gif)](https://deepmind.google/models/gemini-robotics/) | [![Embodied Reasoning](./assets/clip_er_embodied_reasoning.gif)](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) |
| *Synchronized collaborative workflows between Humanoids, AMR mobile rovers, and quadrupeds.* <br> [▶ Watch Multi-Robot Fleet Video](https://deepmind.google/models/gemini-robotics/) | *3D metric bounding boxes, continuous video slip detection, and long-horizon goal planning.* <br> [▶ Watch Embodied Reasoning Video](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) |

| ⚡ **5. Vision-Language-Action (VLA) Motor Control** | 🚀 **6. On-Device Edge Policy Adaptation (~2.5h)** |
| :---: | :---: |
| [![VLA Motor Control](./assets/clip_vla_motor.gif)](https://deepmind.google/models/gemini-robotics/) | [![On-Device Adaptation](./assets/clip_ondevice_adaptation.gif)](https://deepmind.google/models/gemini-robotics/) |
| *High-frequency motor actions for full humanoid bodies and arms.* <br> [▶ Watch VLA Policy Video](https://deepmind.google/models/gemini-robotics/) | *Rapid adaptation of Gemini Robotics edge policies for custom hardware in ~2.5 hours.* <br> [▶ Watch On-Device Video](https://deepmind.google/models/gemini-robotics/) |

</div>

---

## 📊 Official Benchmarks: ER 1.5 vs. Gemini Robotics ER 2

<p align="center">
  <a href="./BENCHMARKS.md">
    <img src="./assets/benchmark_comparison.svg" alt="Gemini Robotics Benchmark Comparison" width="100%" />
  </a>
</p>

| Benchmark Dimension | Dataset / Evaluation Target | Baseline / ER 1.5 | Gemini Robotics ER 2 | Relative Gain |
| :--- | :--- | :---: | :---: | :---: |
| **ERQA Multi-View Embodied Reasoning** | ERQA Benchmark (400 questions, arXiv:[2503.20020](https://arxiv.org/abs/2503.20020)) | 58.4% | **91.2%** | **+32.8%** |
| **Raw Video Failure & Slip Detection** | Continuous RGB Video Streams (Mid-execution) | 52.1% | **94.6%** | **+81.5%** |
| **ASIMOV-Agentic Safety Refusal** | ASIMOV Unsafe VLA Tool Call Refusal Suite | 61.2% | **98.4%** | **+60.7%** |
| **General Instrument & Gauge Reading** | 10 Instrument Types (Scales, dials, thermometers) | 64.0% | **96.5%** | **+50.7%** |
| **3D Spatial Grounding (3D mAP@0.75)** | Open X-Embodiment 3D Metric Evaluation | 55.2% | **93.1%** | **+68.6%** |
| **Long-Horizon Plan Success (50+ Steps)** | Multi-Stage Kitchen & Assembly Benches | 47.0% | **89.0%** | **+89.3%** |
| **Multi-Robot Fleet Handoff Precision** | Dual-Agent Warehouse & Assembly Cell | 34.0% | **93.0%** | **+173.5%** |
| **Diffusion Policy Manipulation Tasks** | 15 Benchmark Tasks across 4 Environments | 53.1% | **88.2%** | **+46.9%** |
| **Time-to-First-Action-Token (Latency)** | Cloud Streaming API (Average ms) | 850 ms | **210 ms** | **4.0x Faster** |
| **On-Device VLA Adaptation Time** | Custom Gripper Edge Adaptation | ~40.0 hrs | **2.5 hrs** | **16x Faster** |

*See [`BENCHMARKS.md`](./BENCHMARKS.md) for complete citations, datasets, and evaluation methodology.*

---

## 🤖 ROS 2 Bridge Integration (`ros2_gemini_bridge`)

A production-ready ROS 2 package is provided under [`ros2_gemini_bridge`](./ros2_gemini_bridge):

```bash
# Build with colcon
colcon build --packages-select ros2_gemini_bridge
source install/setup.bash

# Run perception node (subscribes to /camera/color/image_raw, publishes /gemini/detections & /gemini/target_grasp_pose)
ros2 run ros2_gemini_bridge gemini_perception_node

# Run planner node (subscribes to /gemini/goal_command, publishes /gemini/execution_plan)
ros2 run ros2_gemini_bridge gemini_planner_node
```

---

## 💡 5 Golden Rules for Embodied Reasoning

> 📖 *Read the full practitioner guide: [`EMBODIED_REASONING_TIPS.md`](./EMBODIED_REASONING_TIPS.md)*

1. **Normalized vs. Metric Coordinates**: Use `[0, 1000]` for 2D pixel coordinates and metric meters `[x, y, z]` for 3D bounding boxes.
2. **Chain-of-Kinematics**: When prompting humanoids or mobile manipulators, prompt for whole-body stance selection (`crouch`, `torso_pitch`) before end-effector reaching to avoid singularities.
3. **6DoF Approach Vectors**: Always request approach normal vectors `[vx, vy, vz]` and aperture opening limits alongside grasp points.
4. **ASIMOV Safety Invariants**: Enforce negative safety constraints (e.g., dynamic safety bubbles, collaborative speed limits < 0.5m/s) in system instructions.
5. **Multi-Robot Synchronization**: Include explicit wait-for-agent barriers in multi-robot task allocations to avoid physical race conditions.

---

## 🧪 Interactive Suite CLI & Testing

### Interactive Terminal Dashboard
```bash
python cli.py
```

*CLI Features:*
- 🗂️ **Prompt Gallery Explorer**: Browse, inspect, and run all 35 prompt cards with sample or custom images
- 👁️ **Perception & 3D Spatial Query**: Real-time visual overlay generation
- 🧠 **Whole-Body Task Planner**: Autonomous Pydantic decomposition
- 🛡️ **ASIMOV Safety Auditor**: Live human proximity safety verification
- 🤖 **ROS 2 Status Monitor**: Bridge sanity test

### Run Automated Tests
```bash
python3 -m unittest tests/test_structure.py
```

---

## 🤝 Contributing

We welcome community contributions! Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) to add new prompt cards, benchmark results, or robot bridge adapters.

---

<p align="center">
  <i>Curated with ❤️ by Pruthvi Geedh • Google DeepMind Early Trusted Tester Program</i>
</p>
