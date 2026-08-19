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

## 📊 Official Benchmarks: ER 1.5 vs. Gemini Robotics ER 2

<p align="center">
  <a href="./BENCHMARKS.md">
    <img src="./assets/benchmark_comparison.svg" alt="Gemini Robotics Benchmark Comparison" width="100%" />
  </a>
</p>

| Benchmark Dimension | Dataset / Evaluation Target | Baseline / ER 1.5 | Gemini Robotics ER 2 | Relative Gain |
| :--- | :--- | :---: | :---: | :---: |
| **ERQA Multi-View Embodied Reasoning** | ERQA Benchmark (400 questions, arXiv:2503.20020) | 58.4% | **91.2%** | **+32.8%** |
| **Raw Video Failure & Slip Detection** | Continuous RGB Video Streams (Mid-execution) | 52.1% | **94.6%** | **+81.5%** |
| **ASIMOV-Agentic Safety Refusal** | ASIMOV Unsafe VLA Tool Call Refusal Suite | 61.2% | **98.4%** | **+60.7%** |
| **General Instrument & Gauge Reading** | 10 Instrument Types (Scales, dials, thermometers) | 64.0% | **96.5%** | **+50.7%** |
| **3D Spatial Grounding (3D mAP@0.75)** | Open X-Embodiment 3D Metric Evaluation | 55.2% | **93.1%** | **+68.6%** |
| **Long-Horizon Plan Success (50+ Steps)** | Multi-Stage Kitchen & Assembly Benches | 47.0% | **89.0%** | **+89.3%** |
| **Multi-Robot Fleet Handoff Precision** | Dual-Agent Warehouse & Assembly Cell | 34.0% | **93.0%** | **+173.5%** |
| **Diffusion Policy Manipulation Tasks** | 15 Benchmark Tasks across 4 Environments | 53.1% | **88.2%** | **+46.9%** |
| **Time-to-First-Action-Token (Latency)** | Cloud Streaming API (Average ms) | 850 ms | **210 ms** | **4.0x Faster** |
| **On-Device VLA Adaptation Time** | Custom Gripper Edge Adaptation | ~40.0 hrs | **2.5 hrs** | **16x Faster** |

*See [`BENCHMARKS.md`](./BENCHMARKS.md) for full citations, datasets, and methodology.*

---

## 🎥 Official Demonstration Videos & Next-Gen Physical AI Showcase

Google DeepMind's Gemini Robotics 2 introduces whole-body control, multi-robot teamwork, and continuous video reasoning across diverse hardware embodiments:

<div align="center">

| 🦾 **1. Whole-Body Humanoid Manipulation** | 🤝 **2. Multi-Robot Collaborative Teamwork** |
| :---: | :---: |
| [![Apptronik Apollo 2 Demo](https://img.shields.io/badge/▶_DeepMind_Demo-Apptronik_Apollo_2_Humanoid-FF0000?style=for-the-badge&logo=youtube)](https://deepmind.google/models/gemini-robotics/) | [![Franka F3 Duo Demo](https://img.shields.io/badge/▶_DeepMind_Demo-Franka_F3_Duo_+_AMR_Rover-FF0000?style=for-the-badge&logo=youtube)](https://deepmind.google/models/gemini-robotics/) |
| *Controls legs, torso, arms, and fingers for crouching, reaching, and low-clearance obstacle manipulation.* | *Coordinates heterogeneous robot fleets with dynamic spatial sync barriers for heavy part transfer.* |

| 🎬 **3. Raw Continuous Video Failure Auditing** | 🛡️ **4. ASIMOV-Agentic Safety Orchestration** |
| :---: | :---: |
| [![Video Failure Detection](https://img.shields.io/badge/▶_DeepMind_Demo-Raw_Video_Slip_Detection-blue?style=for-the-badge&logo=google)](https://deepmind.google/models/gemini-robotics/) | [![ASIMOV Safety Demo](https://img.shields.io/badge/▶_DeepMind_Demo-Unsafe_Action_Refusal-green?style=for-the-badge&logo=shield)](https://deepmind.google/models/gemini-robotics/) |
| *Ingests continuous 30fps video to catch tactile slippage, container tipping, or misalignments mid-execution.* | *Evaluates low-level VLA motor commands against safety envelopes and proactively refuses kinetic hazards.* |

</div>

---

## 📸 Gemini Robotics 2 Core Capability Pillars

```
 ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                                 GEMINI ROBOTICS 2 CAPABILITY PILLARS                            │
 ├─────────────────────────┬─────────────────────────┬─────────────────────────────────────────────┤
 │ 🦶 Whole-Body Kinematics │ 🤝 Multi-Agent Fleet    │ ⏱️ Raw Video Temporal Reasoning             │
 │ Humanoid crouching,     │ Shared assembly between │ Detects slips, spills, and joint tracking   │
 │ balance recovery, and   │ Humanoids, AMR Rovers,  │ errors mid-trajectory from live camera      │
 │ dual-arm coordination   │ and Quadrupeds          │ video streams with automatic recovery       │
 ├─────────────────────────┼─────────────────────────┼─────────────────────────────────────────────┤
 │ 📐 3D Metric Grounding  │ 🛡️ ASIMOV Safety Gate   │ ⚡ 2.5-Hour Edge Adaptation                 │
 │ 3D bounding boxes &     │ Proactive refusal of    │ On-Device policy adaptation for custom      │
 │ 6DoF grasp approach     │ dangerous commands and  │ grippers (e.g. Open-ENPIRE) in ~2.5 hours   │
 │ vectors in metric meters│ operator safety bubbles │ with minimal demonstration data             │
 └─────────────────────────┴─────────────────────────┴─────────────────────────────────────────────┘
```

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


