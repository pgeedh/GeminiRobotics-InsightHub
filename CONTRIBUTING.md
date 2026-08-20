# Contributing to Awesome Gemini Robotics 2.0

Contributions from researchers, roboticists, and engineers are welcome to expand this collection of prompts, schemas, and robotic workflows for Google DeepMind's **Gemini Robotics 2.0** suite.

---

## Contribution Guidelines

### 1. Adding a Use Case or Prompt Card
To contribute a new embodied reasoning pattern or physical AI prompt:
1. Add the prompt card schema to [`prompts/gemini_robotics_2_catalog.json`](./prompts/gemini_robotics_2_catalog.json).
2. Document the card in [`README.md`](./README.md) with an input prompt, Python execution snippet, and sample JSON output.
3. If applicable, add a demonstration script to `examples/` and test asset to `assets/`.
4. Open a Pull Request titled `feat(prompt): add <use_case_name> card`.

### 2. Documentation and Localizations
- Pull Requests improving accuracy or adding translations for `README.md`, `README_ja.md`, `README_zh.md`, `README_kr.md`, `README_vn.md`, and `BENCHMARKS.md` are encouraged.
- Ensure all translations maintain consistency with the primary schema IDs and technical terminology.

### 3. Reporting Issues and Hardware Adapters
- If a prompt or ROS 2 node requires modification for a specific robotic hardware embodiment (e.g. Franka Emika, Universal Robots, Boston Dynamics, Unitree, Apollo), open an Issue or Pull Request labeled `[HARDWARE]`.

---

## Code of Conduct

- **Safety Compliance**: All submissions must respect ASIMOV safety guidelines and ISO/TS 15066 collaborative robot safety standards. Prompts intended to bypass velocity limits, proximity barriers, or safety invariants will not be accepted.
- **Reproducibility**: All sample JSON outputs, schemas, and code snippets must be syntactically valid and reproducible against official Gemini Robotics models.

---

<p align="center">
  <i>Distributed under the MIT License</i>
</p>
