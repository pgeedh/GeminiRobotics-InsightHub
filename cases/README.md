# Physical AI Scenario Cases (`cases/`)

This directory contains modular, community-contributed physical AI test cases for **Gemini Robotics 2.0**.

## Directory Convention

Each case lives in its own subdirectory named `cases/<short-name>/`:

```text
cases/
├── spatial_pointing/
│   ├── README.md
│   └── image.png
├── 6dof_wrench_grasp/
│   ├── README.md
│   └── image.png
└── <your-case-name>/
    ├── README.md
    └── image.jpg
```

## Template for `cases/<short-name>/README.md`

```markdown
# Case: <Case Title>

**Description:** 1–2 sentences explaining the robotic setup and goal.
**Target Model:** `gemini-robotics-er-2` | `gemini-2.5-flash`
**Primary Source:** [Link to primary document / research paper / video]

### Input Image
![Scene Frame](./image.png)

### Prompt
```text
<Exact copy-runnable prompt>
```

### Sample Output (JSON)
```json
{
  "status": "..."
}
```
```
