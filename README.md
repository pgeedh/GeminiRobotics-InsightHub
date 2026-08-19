# Gemini Robotics 2 & ER 1.5 Insight Hub <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/2560px-Google_Gemini_logo.svg.png" align="right" width="100">

[![DeepMind](https://img.shields.io/badge/Maintained%20By-Google%20DeepMind%20Trusted%20Tester-4285F4?style=for-the-badge&logo=google)](https://deepmind.google/technologies/gemini/)
[![Gemini Robotics](https://img.shields.io/badge/Model-Gemini%20Robotics%20ER%202%20%7C%201.5-blue?style=for-the-badge)](https://aistudio.google.com/)
[![ROS 2](https://img.shields.io/badge/ROS%202-Humble%20%7C%20Iron%20%7C%20Jazzy-orange?style=for-the-badge&logo=ros)](./ros2_gemini_bridge)
[![Interactive 3D Demo](https://img.shields.io/badge/Interactive%203D-Architecture%20Explainer-purple?style=for-the-badge&logo=three.js)](./docs/architecture_3d_explainer.html)
[![Status](https://img.shields.io/badge/Community-Awesome%20List-green?style=for-the-badge)](https://github.com/google-gemini/cookbook)

> **🚀 INSIGHTS FROM THE EARLY TRUSTED TESTER & PHYSICAL AI PROGRAM**
> This repository is the definitive open-source hub for **Google DeepMind's Gemini Robotics 2**, **Gemini Robotics-ER (Embodied Reasoning)**, and **Vision-Language-Action (VLA)** physical AI models.
>
> Here you will find production patterns, full ROS 2 bridge nodes, 3D spatial grounding recipes, multi-robot fleet coordination, ASIMOV-Agentic safety protocols, and interactive 3D explainers.

---

## 🎮 Interactive 3D Visual Architecture Explainer

Explore the internal workings of Gemini Robotics 2 in 3D WebGL! Inspect how camera RGB-D streams map to multi-layer spatial attention tokens, 3D bounding boxes, whole-body kinematic plans, and 20Hz VLA joint trajectories.

<p align="center">
  <a href="./docs/architecture_3d_explainer.html">
    <img src="./assets/gemini_robotics_architecture.svg" alt="Gemini Robotics 2 Interactive 3D Architecture" width="100%" />
  </a>
</p>
<p align="center">
  👉 <b><a href="./docs/architecture_3d_explainer.html">Launch Full Interactive 3D Architecture & Spatial Explainer in Browser</a></b>
</p>

---

## 📊 Empirical Benchmarks: ER 1.5 vs. ER 2

<p align="center">
  <a href="./BENCHMARKS.md">
    <img src="./assets/benchmark_comparison.svg" alt="Gemini Robotics Benchmark Comparison" width="100%" />
  </a>
</p>

| Benchmark Dimension | Dataset / Evaluation Target | Gemini Robotics ER 1.5 | Gemini Robotics ER 2 | Relative Improvement |
| :--- | :--- | :---: | :---: | :---: |
| **3D Spatial Grounding (3D mAP@0.75)** | Open X-Embodiment 3D Bench (1,000 scenes) | 55.2% | **93.1%** | **+68.6%** |
| **2D Point & Box Accuracy (IoU >= 0.85)** | Precision Grasp Pick Dataset | 72.4% | **96.8%** | **+33.7%** |
| **Long-Horizon Plan Success (50+ Steps)** | Multi-Stage Kitchen & Assembly Benches | 47.0% | **89.0%** | **+89.3%** |
| **Very Long-Horizon (100+ Steps)** | Cluttered Factory Cell Assembly | 24.5% | **81.4%** | **+232.2%** |
| **ASIMOV Safety Instruction Following** | ASIMOV-Agentic Protocol Suite | 62.0% | **97.0%** | **+56.4%** |
| **Autonomous Hazard Refusal Rate** | Physical Safety Stress Tests (150 prompts) | 58.6% | **98.2%** | **+67.5%** |
| **Multi-Robot Fleet Handoff Precision** | Dual-Agent Warehouse Logistics Cell | 31.0% | **91.0%** | **+193.5%** |
| **Time-to-First-Action-Token (Latency)** | Cloud Streaming API (Average ms) | 850 ms | **210 ms** | **4.0x Faster** |
| **On-Device VLA Adaptation Time** | Custom Gripper Adaptation (Hours of data) | ~40 hrs | **~2.5 hrs** | **16x Faster** |

*See [`BENCHMARKS.md`](./BENCHMARKS.md) for full methodology and hardware testbeds.*

---

## 🤖 Gemini Robotics 2 Ecosystem Overview

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

## 🦾 Core Python SDK Quick Example (`google-genai` v1.x)

```python
from google import genai
from google.genai import types

client = genai.Client()

with open('robot_view.jpg', 'rb') as f:
    image_bytes = f.read()

# Query Gemini Robotics ER 2 for 3D Bounding Box and 6DoF Grasp Affordance
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

## 💡 5 Golden Rules for Embodied Reasoning (Pro-Tips)

> 📖 *Read the full practitioner guide: [`EMBODIED_REASONING_TIPS.md`](./EMBODIED_REASONING_TIPS.md)*

1. **Normalized vs Metric Coordinates**: Use `[0, 1000]` for 2D pixel coordinates and metric meters `[x, y, z]` for 3D bounding boxes.
2. **Chain-of-Kinematics**: When prompting humanoids or mobile manipulators, prompt for whole-body stance selection (`crouch`, `torso_pitch`) before end-effector reaching to avoid singularities.
3. **6DoF Approach Vectors**: Always request approach normal vectors `[vx, vy, vz]` and aperture opening limits alongside grasp points.
4. **ASIMOV Safety Invariants**: Enforce negative safety constraints (e.g. dynamic safety bubbles, collaborative speed limits < 0.5m/s) in system instructions.
5. **Multi-Robot Synchronization**: Include explicit wait-for-agent barriers in multi-robot task allocations to avoid physical race conditions.

---

## 📸 Visual Use Case Gallery

### 📍 Spatial Grounding & Novel Object Discovery
| 1. Novel Part Identification | 2. Abstract Description Finding | 3. Serial Grasp Affordance |
| :---: | :---: | :---: |
| <img width="100%" alt="Pointing to items" src="./assets/pointing_undefined.png" /> | <img width="100%" alt="Fruit finding" src="./assets/find_fruit.png" /> | <img width="100%" alt="Part identification" src="./assets/part_identification.png" /> |

### 🗺️ Trajectory Planning & Reasoning
| 4. Collision-Free Path Planning | 5. Fine Manipulation Trajectories | 6. Counting & Spatial Reasoning |
| :---: | :---: | :---: |
| <img width="100%" alt="Path planning" src="./assets/obstacle_avoidance.png" /> | <img width="100%" alt="Brushing path" src="./assets/trajectory_brushing.png" /> | <img width="100%" alt="Counting reasoning" src="./assets/counting_reasoning.png" /> |

---

## 🤖 ROS 2 Integration (`ros2_gemini_bridge`)

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

## 📂 Included Examples & Cookbooks

| File | Focus | Description |
|------|-------|-------------|
| [`examples/basic_spatial_query.py`](./examples/basic_spatial_query.py) | **Vision & 3D** | Query 2D boxes, 3D bounding volumes `[x,y,z,dx,dy,dz]`, and 6DoF grasp poses with visual overlays. |
| [`examples/task_decomposition.py`](./examples/task_decomposition.py) | **Whole-Body Planning** | Decompose complex tasks into whole-body primitives (`crouch`, `reach_arm`, `dual_arm_lift`) with Pydantic schemas and dynamic replanning. |
| [`examples/tool_use_recycling.py`](./examples/tool_use_recycling.py) | **Agentic Grounding** | Native Google Search grounding + facility rules for live sorting decisions and handling precautions. |
| [`examples/video_anomaly_detection.py`](./examples/video_anomaly_detection.py) | **Safety & ASIMOV** | Long-horizon video safety auditing via Files API detecting velocity incursion and grip instability. |
| [`examples/multi_robot_coordination.py`](./examples/multi_robot_coordination.py) | **Multi-Robot Fleet** | Synchronized mission allocation across heterogeneous robots (Humanoid + AMR + Quadruped). |
| [`examples/vla_motion_transfer.md`](./examples/vla_motion_transfer.md) | **VLA & Hardware** | Architecture and adapter specifications for transferring Gemini Robotics 2 VLA actions to hardware (e.g. Open-ENPIRE gripper). |
| [`EMBODIED_REASONING_TIPS.md`](./EMBODIED_REASONING_TIPS.md) | **Handbook** | The practitioner's guide to prompt engineering and coordinate framing for embodied AI. |
| [`BENCHMARKS.md`](./BENCHMARKS.md) | **Empirical Data** | Full benchmark comparisons, datasets, and latency profiles (ER 1.5 vs. ER 2). |
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

