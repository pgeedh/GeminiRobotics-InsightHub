# Contributing to Awesome Gemini Robotics 2.0

Contributions from researchers, roboticists, and physical AI practitioners are welcome to expand this collection of prompts, schemas, and robotic workflows for Google DeepMind's **Gemini Robotics 2.0** suite.

---

## Contribution Guidelines

### 1. Adding a Case under `cases/<short-name>/`

To add a new scenario or prompt pattern, create a dedicated folder under `cases/<short-name>/` containing:

1. **`README.md`**:
   - 1–2 sentences describing the physical robotic scenario and setup.
   - The exact copy-runnable prompt definition.
   - Sample Pydantic schema or expected JSON output.
2. **`image.jpg` / `image.png`** (or link):
   - The visual input frame or camera capture.
3. **Primary Source Citation**:
   - Cite your primary source(s) (e.g. official Google DeepMind docs, blog posts, arXiv research papers, or video demonstrations).

### 2. Prompt Standards

- **Model-Friendly Coordinates**: Prefer normalized `[y, x]` in `0–1000` for points, or `[ymin, xmin, ymax, xmax]` for bounding boxes.
- **Copy-Runnable & JSON-Friendly**: Prompts must be self-contained and specify unambiguous structured output constraints.
- **Thinking Budget Guidance**: Specify recommended thinking budget tokens (e.g., 512, 1024, 2048) if the task requires deep multi-step kinematic planning.

### 3. Adding a Prompt Card to Catalog

- Add the structured entry to [`prompts/gemini_robotics_2_catalog.json`](./prompts/gemini_robotics_2_catalog.json).
- Document the card in [`README.md`](./README.md) under the appropriate category.

### 4. Submitting Pull Requests

- Branch naming: `feat/case-<short-name>` or `fix/docs-<language>`.
- Title format: `feat(case): add <short-name> physical scenario`.
- Verify that `python3 -m unittest tests/test_structure.py` passes before opening your PR.

---

## Code of Conduct & Safety

- **ASIMOV Safety Compliance**: All submissions must respect collaborative robot safety principles and ISO/TS 15066 guidelines. Prompts intended to bypass safety barriers or force limits will not be merged.
- **Reproducibility**: All sample JSON outputs, schemas, and code snippets must be syntactically valid and reproducible against official Gemini Robotics models.

---

<p align="center">
  <i>Curated by Pruthvi Geedh</i>
</p>
