# Gemini Robotics 2 & ER 1.5 Insight Hub <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/2560px-Google_Gemini_logo.svg.png" align="right" width="100">

[![DeepMind](https://img.shields.io/badge/Maintained%20By-Google%20DeepMind%20Trusted%20Tester-4285F4?style=for-the-badge&logo=google)](https://deepmind.google/technologies/gemini/)
[![Gemini Robotics](https://img.shields.io/badge/Model-Gemini%20Robotics%20ER%202%20%7C%201.5-blue?style=for-the-badge)](https://aistudio.google.com/)
[![ROS 2](https://img.shields.io/badge/ROS%202-Humble%20%7C%20Iron%20%7C%20Jazzy-orange?style=for-the-badge&logo=ros)](./ros2_gemini_bridge)
[![Status](https://img.shields.io/badge/Community-Awesome%20List-green?style=for-the-badge)](https://github.com/google-gemini/cookbook)

> **🚀 INSIGHTS FROM THE EARLY TRUSTED TESTER & PHYSICAL AI PROGRAM**
> This repository is a curated collection of resources, patterns, and "better" updates for **Gemini Robotics 2** and **Gemini Robotics-ER (Embodied Reasoning)**, maintained by an **Early Trusted Tester**.
>
> Our goal is to bridge the gap between frontier research and practical robotics deployment. Here you will find production patterns, full ROS 2 bridge nodes, 3D grounding recipes, multi-robot fleet coordination, and ASIMOV-Agentic safety protocols.

---

## 🤖 What is Gemini Robotics 2 & ER 2?

**Gemini Robotics 2** is Google DeepMind's suite of Physical AI models designed to give robots whole-body intelligence, spatial understanding, and autonomous physical reasoning:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      GEMINI ROBOTICS 2 ECOSYSTEM                        │
├──────────────────────────────┬──────────────────────────────────────────┤
│ 🧠 Gemini Robotics ER 2      │ The "Brain": High-level embodied         │
│    (Embodied Reasoning)      │ reasoning, 3D bounding boxes, long-      │
│                              │ horizon planning, multi-robot fleet sync │
├──────────────────────────────┼──────────────────────────────────────────┤
│ 🦾 Gemini Robotics 2 (VLA)   │ The "Motor Cortex": Direct whole-body    │
│    (Vision-Language-Action)  │ coordination from feet to fingertips     │
├──────────────────────────────┼──────────────────────────────────────────┤
│ ⚡ Gemini Robotics           │ The "Edge Engine": Ultra-low latency     │
│    On-Device 2               │ on-robot policy adapted in hours         │
└──────────────────────────────┴──────────────────────────────────────────┘
```

### Key Capabilities Matrix
| Capability | Gemini Robotics ER 1.5 | Gemini Robotics ER 2 & 2.0 Models | Real-World Application |
|------------|------------------------|-----------------------------------|------------------------|
| **Spatial Grounding** | 2D Points & Boxes (`[ymin, xmin, ymax, xmax]`) | **3D Bounding Boxes & 6DoF Grasp Affordances** | Precise dexterous picking, 3D navigation, collision avoidance |
| **Body Scope** | Upper-body / tabletop manipulation | **Whole-Body Intelligence (locomotion + manipulation)** | Humanoid crouch/stretch, mobile manipulation, dual-arm lifts |
| **Multi-Agent Coordination** | Single robot focus | **Heterogeneous Fleet Synchronization** | AMR + Humanoid + Quadruped shared assembly tasks |
| **Tool Grounding** | Text-based prompt simulation | **Native Google GenAI Search & API Grounding** | Material hazard lookup, real-time live environmental verification |
| **Safety Auditing** | Basic heuristic logs | **ASIMOV-Agentic Safety Protocol Verification** | Dynamic safety bubbles, velocity checks, slip detection |

---

## ⚡ Quick Start

### 1. Installation
```bash
git clone https://github.com/pgeedh/GeminiRobotics_ER1.5-InsightHub.git
cd GeminiRobotics_ER1.5-InsightHub
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file or export your Gemini API key:
```bash
export GEMINI_API_KEY="your-api-key-here"
export GEMINI_ROBOTICS_MODEL="gemini-robotics-er-2"  # or gemini-robotics-er-1.5-preview, gemini-2.5-flash
```

### 3. Run the Interactive Suite CLI
```bash
python cli.py
```

*Interactive terminal dashboard with drag-and-drop image support, dynamic model switching, and real-time simulations:*
```text
   ______                _       _   ____       __          __  _          
  / ____/___  ____ ___  (_)___  (_) / __ \____ / /_  ____  / /_(_)_________
 / / __/ __ \/ __ `__ \/ / __ \/ / / /_/ / __ \ __ \/ __ \/ __/ / ___/ ___/
/ /_/ / /_/ / / / / / / / / / / / / _, _/ /_/ / /_/ / /_/ / /_/ / /__(__  ) 
\____/\____/_/ /_/ /_/_/_/ /_/_/ /_/ |_|\____/_.___/\____/\__/_/\___/____/  
               E M B O D I E D   R E A S O N I N G   2 . 0

? Select a Gemini Robotics Capability to Explore:
 » 1. 👁️  Vision & Perception (3D Spatial Query & Grasping)
   2. 🧠  Brain & Planning (Whole-Body Task Decomposition)
   3. 🛠️  Agentic Capabilities (Grounded Search Tool Use)
   4. 🛡️  Safety & Auditing (ASIMOV-Agentic Video Audit)
   5. 🤝  Multi-Robot Coordination (Fleet Allocation)
   6. ⚙️  Select Active Model
   7. 🤖  ROS 2 Bridge Status & Test
   8. 🚪  Exit
```

---

## 🦾 Core Python SDK Quick Example (google-genai v1.x)

```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

with open('robot_view.jpg', 'rb') as f:
    image_bytes = f.read()

# Query Gemini Robotics ER 2 for 3D Bounding Box and Grasp Affordance
response = client.models.generate_content(
    model='gemini-robotics-er-2',
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
        """Detect the target object. Return 3D bounding box (meters) and grasp affordance.
        Format: [{"label": "mug", "box_3d": {"center": [x,y,z], "size": [dx,dy,dz]}, "grasp": [y,x]}]"""
    ],
    config=types.GenerateContentConfig(
        temperature=0.2,
        thinking_config=types.ThinkingConfig(thinking_budget=2048)
    )
)
print(response.text)
```

---

## 🤖 ROS 2 Integration (`ros2_gemini_bridge`)

A drop-in ROS 2 package is provided under [`ros2_gemini_bridge`](./ros2_gemini_bridge):

```bash
# Build with colcon
colcon build --packages-select ros2_gemini_bridge
source install/setup.bash

# Run perception node (subscribes to /camera/color/image_raw, publishes /gemini/detections)
ros2 run ros2_gemini_bridge gemini_perception_node

# Run planner node (subscribes to /gemini/goal_command, publishes /gemini/execution_plan)
ros2 run ros2_gemini_bridge gemini_planner_node
```

---

## 📂 Included Examples & Cookbooks

| File | Focus | Description |
|------|-------|-------------|
| [`examples/basic_spatial_query.py`](./examples/basic_spatial_query.py) | **Vision & 3D** | Query 2D boxes, 3D bounding volumes `[x,y,z,dx,dy,dz]`, and 6DoF grasp poses with visual overlays. |
| [`examples/task_decomposition.py`](./examples/task_decomposition.py) | **Whole-Body Planning** | Decompose complex tasks into whole-body primitives (`crouch`, `reach_arm`, `dual_arm_lift`) with Pydantic schemas and dynamic replanning. |
| [`examples/tool_use_recycling.py`](./examples/tool_use_recycling.py) | **Agentic Grounding** | Native Google Search grounding + facility rules for live sorting decisions and handling precautions. |
| [`examples/video_anomaly_detection.py`](./examples/video_anomaly_detection.py) | **Safety & ASIMOV** | Long-horizon video safety auditing via Files API detecting velocity incursion and grip instability. |
| [`examples/multi_robot_coordination.py`](./examples/multi_robot_coordination.py) | **Multi-Robot Fleet** | Synchronized mission allocation across heterogeneous robots (Humanoid + AMR + Quadruped). |
| [`examples/vla_motion_transfer.md`](./examples/vla_motion_transfer.md) | **VLA & Hardware** | Architecture and adapter specifications for transferring Gemini Robotics 2 VLA actions to hardware (e.g. Open-ENPIRE gripper). |
| [`INTERESTING_PROMPTS.md`](./INTERESTING_PROMPTS.md) | **Prompt Lab** | Advanced physical AI prompts for hazardous environments, whole-body reaching, and multi-robot handoffs. |
| [`RESOURCES.md`](./RESOURCES.md) | **Papers & Links** | Curated research papers, datasets (Open X-Embodiment 2), and simulation links. |

---

## 🧪 Testing Suite

Run the automated test suite:
```bash
python3 -m unittest tests/test_structure.py
```

---

<p align="center">
  <i>Curated with ❤️ by Pruthvi Geedh • Google DeepMind Early Trusted Tester Program</i>
</p>

