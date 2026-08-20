# Contributing to Awesome Gemini Robotics 2.0

Thank you for your interest in contributing to the **Awesome Gemini Robotics 2.0 Developer Gallery**! 🚀

As a **Google DeepMind Physical AI Early Trusted Tester**, this collection is open to the robotics community to build, experiment, and deploy faster. We welcome contributions from researchers, roboticists, and engineers.

## 🤝 How to Contribute

### 1. Adding a Use Case or Prompt Card
Have you developed a new embodied reasoning pattern or robotic control prompt with Gemini Robotics 2.0 / ER 2 / VLA?
1. Add your prompt card to [`prompts/gemini_robotics_2_catalog.json`](./prompts/gemini_robotics_2_catalog.json).
2. Document the card in [`README.md`](./README.md) with a clear schema and sample output.
3. If applicable, add a demonstration script in `examples/` and visual demonstration to `assets/`.
4. Submit a PR with the title `feat(prompt): add <use_case_name> card`.

### 2. Improving Multilingual Documentation & Benchmarks
- PRs for `README.md`, `README_ja.md`, `README_zh.md`, `README_kr.md`, `README_vn.md`, and `BENCHMARKS.md` are highly encouraged.
- Keep translations accurate, elegant, and synchronized with the primary catalog.

### 3. Reporting Issues & Hardware Adapters
- If a prompt or ROS 2 node requires adjustment for a specific robot embodiment (Franka, Universal Robots, Boston Dynamics, Unitree, Apollo), submit an issue or PR with the tag `[HARDWARE]`.

## ⚖️ Code of Conduct

- **Safety First**: Adhere to ASIMOV safety invariants and ISO/TS 15066 guidelines. Never submit prompts intended to bypass robot physical safety limits.
- **Reproducibility**: Ensure all sample outputs and schemas are valid and reproducible.

---
*By contributing, you agree that your code can be distributed under the MIT License of this repository.*
