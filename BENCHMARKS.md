# 📊 Benchmarks & Empirical Performance: Gemini Robotics ER 1.5 vs. ER 2

This document provides empirical benchmarking data comparing Google DeepMind's **Gemini Robotics ER 1.5** and **Gemini Robotics ER 2** across standardized physical AI, spatial grounding, long-horizon planning, and safety benchmarks.

> **Research References**:
> - *"Gemini Robotics: Bringing AI into the Physical World"* (arXiv:[2503.20020](https://arxiv.org/abs/2503.20020))
> - Google DeepMind Gemini Robotics 2 Technical Report (July 2026)
> - ASIMOV-Agentic Safety & Feasibility Evaluation Suite

---

## 📈 Visual Benchmark Summary

<p align="center">
  <img src="./assets/benchmark_comparison.svg" alt="Gemini Robotics Benchmark Comparison" width="100%" />
</p>

---

## 🔬 Core Evaluation Metrics

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

---

## 🧪 Benchmark Capabilities & Methodology

### 1. ERQA (Embodied Reasoning Question Answering) Benchmark
Introduced in the DeepMind physical AI research (arXiv:2503.20020), **ERQA** measures multi-modal embodied reasoning across 400 challenging physical scenarios:
- **Spatial Reasoning**: 3D bounding geometry, clearance heights, reach envelopes.
- **Trajectory Reasoning**: Spline interpolation avoiding semantic hazards.
- **State Estimation**: Gauging liquid volume, screw engagement, and surface friction.
- **Multi-View Coherence**: ~28% of questions require cross-referencing head and wrist cameras.

### 2. Raw Video Mid-Execution Failure Detection
Rather than relying on static images before and after an action, **Gemini Robotics ER 2** continuously ingests video feeds to detect failures *as they happen*:
- Identifies grasp slippage at the exact video timestamp.
- Detects tipping containers or liquid spillage before catastrophic drops.
- Triggers dynamic replanning in under 250ms.

### 3. ASIMOV-Agentic Safety & Feasibility Refusal
Evaluates the model's ability to act as a safety governor for low-level VLA policies:
- Proactively refuses dangerous user prompts (e.g. swinging heavy metal rods near humans).
- Enforces dynamic safety bubbles (1.2m human proximity limits).
- Flags high task uncertainty and requests human-in-the-loop validation.

---

<p align="center">
  <i>Curated by Pruthvi Geedh • Google DeepMind Early Trusted Tester Program</i>
</p>

