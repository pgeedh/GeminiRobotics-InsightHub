# Resource Hub: Gemini Robotics 2.0 and Physical AI

A curated reference collection of technical papers, benchmarks, datasets, physics simulators, and developer SDKs for Google DeepMind's **Gemini Robotics 2.0**, **Gemini Robotics ER 2**, and **VLA 2.0** physical AI ecosystem.

---

## 1. Core Research Papers and Benchmarks

| Milestone / Publication | Technical Summary | Link |
|-------------------------|-------------------|------|
| **Gemini Robotics 2** (July 2026) | Whole-body intelligence (feet to fingertips), dexterous manipulation, and multi-robot collaboration. | [DeepMind Announcement](https://deepmind.google/discover/blog/gemini-robotics-2-physical-ai/) |
| **Gemini Robotics ER 2** | Embodied Reasoning (ER) models specialized in 3D metric spatial grounding, dynamic task planning, and continuous multimodal video reasoning. | [Google AI Studio ER Hub](https://aistudio.google.com/) |
| **ASIMOV-Agentic Benchmark** | Safety evaluation benchmark measuring agentic physical AI safety refusal, velocity compliance, and human proximity handling. | [Safety Benchmark Paper](https://deepmind.google/technologies/gemini/robotics/) |
| **Open X-Embodiment 2** | The expanded cross-embodiment multi-robot dataset powering generalist robot policies across humanoids, quadrupeds, and manipulators. | [Project Page](https://robotics-transformer-x.github.io/) |
| **RT-2: Vision-Language-Action** | Foundational VLA work translating internet-scale vision and language into physical control tokens. | [DeepMind RT-2 Blog](https://deepmind.google/discover/blog/rt-2-new-model-translates-vision-and-language-into-action/) |
| **PaLM-E** | Ancestral embodied multimodal language model bridging sensor signals with language planners. | [ArXiv Paper](https://arxiv.org/abs/2303.03378) |

---

## 2. Developer Tools and SDKs

- **[Google GenAI SDK (`google-genai`)](https://github.com/googleapis/python-genai)**: Official modern Python SDK with native typing, Structured Outputs, and Files API.
- **[Google AI Studio](https://aistudio.google.com/)**: Fast interactive web environment for prototyping Gemini Robotics ER prompts and spatial grounding.
- **[Gemini API Cookbook](https://github.com/google-gemini/cookbook)**: Official repository of code recipes and multimodal patterns.
- **[ROS 2 Gemini Bridge](./ros2_gemini_bridge)**: Drop-in ROS 2 package for image subscription and task planning.

---

## 3. Simulators and Hardware Platforms

### Physics Engines and Digital Twins
- **[NVIDIA Isaac Sim / Isaac Lab](https://developer.nvidia.com/isaac-sim)**: GPU-accelerated photorealistic simulation standard for Sim-to-Real transfer.
- **[MuJoCo](https://mujoco.org/)**: Open-source physics engine maintained by Google DeepMind for contact-rich multi-finger manipulation.
- **[Gazebo Harmonic / Ionic](https://gazebosim.org/)**: Standard robotics simulator tightly integrated with ROS 2.

### Hardware Embodiments and End-Effectors
- **[Open-ENPIRE Hand](https://github.com/pgeedh/Open-ENPIRE-Gripper-nvidia)**: Open-source compliant anthropomorphic gripper with tendon actuation.
- **Universal Robots (UR5e / UR10e)**: Industry cobot arms.
- **Franka Emika Panda / FR3**: Research standard torque-controlled manipulator.
- **Apptronik Apollo / Boston Dynamics Atlas**: Humanoid platforms partnering with Gemini Robotics 2.

---

## 4. Technical Presentations and Tutorials

- **[Google DeepMind: Physical AI & The Future of Robotics](https://deepmind.google/discover/blog/shaping-the-future-of-robots-with-gemini/)**: Technical overview of whole-body intelligence and cross-embodiment transfer.
- **[Google I/O: Multimodal Reasoning with Gemini](https://deepmind.google/technologies/gemini/)**: Understanding long-context video comprehension and spatial tokens.

---

<p align="center">
  <i>Maintained by the Gemini Robotics 2.0 Early Access Community • Google DeepMind Early Trusted Tester Program</i>
</p>
