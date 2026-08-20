# 📊 Official Benchmarks & Performance: Gemini Robotics ER 2

Official empirical benchmarking data for Google DeepMind's **Gemini Robotics ER 2** across standardized physical AI, embodied reasoning, VLA execution control, and safety governance benchmarks.

> **Research & Technical Citations**:
> - *"Gemini Robotics: Bringing AI into the Physical World"* (Google DeepMind, arXiv:[2503.20020](https://arxiv.org/abs/2503.20020))
> - Google DeepMind Gemini Robotics ER 2 Technical Benchmark Suite
> - ASIMOV-Agentic Human Proximity & Physical Safety Evaluation Benchmark

---

## 📈 1. Embodied Reasoning (ER) Metrics Comparison

<p align="center">
  <img src="./assets/benchmark_er_metrics.svg" alt="ER Metrics Comparison" width="100%" />
</p>

| Benchmark Evaluation Metric | Opus 5 | GPT 5.6 Sol | Gemini Robotics ER 1.6 | Gemini 3.6 Flash | Gemini Robotics ER 2 | SOTA Margin |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Success Detection (Image-Based)** | 83.6% | 83.1% | 82.9% | 83.3% | **87.7%** | **+4.1%** |
| **Success Detection (Video-Based)** | 81.0% | 74.7% | 76.0% | 75.4% | **82.4%** | **+1.4%** |
| **Question Answering (ERQA)** | 67.2% | 43.2% | 72.5% | 73.0% | **78.5%** | **+5.5%** |
| **Generalized Instrument Reading** | 53.0% | 61.5% | 52.8% | 52.0% | **65.7%** | **+4.2%** |

---

## ⏱️ 2. Progress Classification Comparison

<p align="center">
  <img src="./assets/benchmark_progress_classification.svg" alt="Progress Classification Comparison" width="100%" />
</p>

| Model | Progress Classification Accuracy | Relative Gain vs Opus 5 | Relative Gain vs GPT 5.6 Sol |
| :--- | :---: | :---: | :---: |
| **Opus 5** | 37.1% | — | — |
| **GPT 5.6 Sol** | 46.2% | +24.5% | — |
| **Gemini Robotics ER 1.6** | 42.7% | +15.1% | -7.6% |
| **Gemini 3.6 Flash** | 43.9% | +18.3% | -5.0% |
| **Gemini Robotics ER 2** | **57.4%** | **+54.7%** | **+24.2%** |

---

## 🦾 3. Physical Agent Execution Performance

<p align="center">
  <img src="./assets/benchmark_physical_agent.svg" alt="Physical Agent Performance" width="100%" />
</p>

| Control Modality | Gemini Robotics ER 1.6 | Gemini Robotics ER 2 | Net Improvement |
| :--- | :---: | :---: | :---: |
| **Controlling Real VLA Hardware** | 48.6% | **60.0%** | **+11.4% (Relative +23.5%)** |
| **Controlling Simulation VLA** | 37.4% | **42.9%** | **+5.5% (Relative +14.7%)** |
| **Controlling Human Tele-Op Assistance** | 63.6% | **74.0%** | **+10.4% (Relative +16.4%)** |

---

## 🛡️ 4. Safety & Human Proximity Governance

<p align="center">
  <img src="./assets/benchmark_safety_performance.svg" alt="Safety Performance" width="100%" />
</p>

| Safety Evaluation Dimension | Opus 5 | GPT 5.6 Sol | Gemini Robotics ER 1.6 | Gemini Robotics ER 2 |
| :--- | :---: | :---: | :---: | :---: |
| **Safety Instruction Following Accuracy** | 95.9% | 91.4% | 47.2% | **97.9%** |
| **Human Proximity Safety Violation Avoidance (1m)** | 77.1% | 83.4% | 51.1% | **93.0%** |

---

## 🔬 Benchmark Methodology & Evaluation Protocol

### 1. ERQA (Embodied Reasoning Question Answering)
- Evaluates multi-camera spatial reasoning across 400 questions.
- Tests coordinate grounding, affordance mapping, multi-view consistency, and kinematic feasibility.

### 2. Video-Based Success & Slip Detection
- Evaluates mid-execution RGB video stream reasoning to detect object drops, grasp shifts, and container tipping in real time without static assumptions.

### 3. VLA Policy Control
- Evaluates closed-loop high-frequency motor trajectory generation transferring Gemini Robotics ER 2 high-level plans to physical 7DoF robot arms and humanoid end-effectors.

---

<p align="center">
  <i>Curated by Pruthvi Geedh • Google DeepMind Early Trusted Tester Program</i>
</p>
