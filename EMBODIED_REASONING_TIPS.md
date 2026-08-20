# The Physical AI Practitioner's Handbook: Embodied Reasoning with Gemini Robotics ER 2

Engineering reference and prompt design guidelines for **Embodied Reasoning (ER)** with Google DeepMind's Gemini Robotics models. This guide covers spatial coordinate conventions, kinematic planning patterns, safety constraints, and latency optimization.

---

## 1. Coordinate Framing and Spatial Grounding

Gemini Robotics ER models output spatial tokens in a normalized **`[0, 1000]` coordinate system** for 2D bounding boxes and points, and metric meters `[x, y, z]` for 3D bounding volumes.

### 2D Coordinates Convention
- Top-Left Origin: `(ymin=0, xmin=0)` is the top-left pixel.
- Bottom-Right: `(ymax=1000, xmax=1000)` is the bottom-right pixel.
- Python pixel conversion formula:
  ```python
  pixel_xmin = int((xmin / 1000.0) * image_width)
  pixel_xmax = int((xmax / 1000.0) * image_width)
  pixel_ymin = int((ymin / 1000.0) * image_height)
  pixel_ymax = int((ymax / 1000.0) * image_height)
  ```

### 3D Metric Coordinate Prompt Template
When prompting for 3D boxes, specify camera optical center conventions:
```text
Conditioning: Camera optical center is (0,0,0). Forward is +Z, Right is +X, Down is +Y.
Prompt: Detect all manipulable tools on the workbench.
Return 3D oriented bounding boxes in meters:
[{"label": "name", "box_3d": {"center": [x, y, z], "size": [dx, dy, dz], "rotation_rpy": [roll, pitch, yaw]}}]
```

---

## 2. Embodied Reasoning Prompt Patterns

### Pattern 1: Chain-of-Kinematics (Whole-Body Stance Selection)
*Prevents joint limit singularities by prompting the model to resolve whole-body posture before arm movement.*
```text
Task: Pick up the dropped bolt beneath the assembly jig (clearance height: 35cm).
Reasoning Steps:
1. Analyze if the humanoid robot can reach while standing or if it must crouch.
2. Evaluate left arm vs right arm reach corridor to avoid occluding the head camera.
3. Output the whole-body stance: crouch(height_fraction=0.4), torso_pitch_deg=18.0.
4. Output arm trajectory waypoints.
```

### Pattern 2: 6DoF Grasp Affordance Grounding
*Specifies approach normal vectors and finger opening widths alongside contact coordinates.*
```text
Identify the screwdriver on the table.
Return the 6DoF grasp affordance for a tendon-driven gripper:
- grasp_point: [y, x]
- approach_vector: [vx, vy, vz] normalized
- grasp_type: ('pinch_precision', 'power_cylinder', 'suction')
- target_grip_aperture_mm: 35
```

### Pattern 3: ASIMOV Safety Invariant
*Embeds hard safety guarantees directly into high-priority system instructions.*
```text
System Invariants:
- If a human operator is visible within a 1.2m radius of the manipulator, cap all joint speeds to 0.2 rad/s.
- If a human hand enters the active grasp corridor, immediately output an ASIMOV_SAFETY_PAUSE state.
- Never swing payloads (>5kg) with angular acceleration > 0.5 rad/s^2.
```

### Pattern 4: Multimodal Video State Verification
*Audits execution success across temporal video frames.*
```text
Watch the start state frame (Frame 0) and final state frame (Frame 60).
Did the robot successfully mate the connector into the port?
Checklist:
1. Is the connector fully seated without gap > 1mm?
2. Did any wire harness snag on the fixture?
3. Output state: 'SUCCESS' or 'FAILURE_RETRY' with spatial coordinate of defect.
```

### Pattern 5: Multi-Robot Task Allocation and Synchronization
*Coordinates multi-agent fleets with synchronization barriers to prevent deadlock.*
```text
Available Fleet:
- Robot A (Humanoid Manipulator, 20kg payload)
- Robot B (Mobile Logistics Rover, flatbed bed)
Mission: Relocate the heavy engine casting.
Requirement: Output synchronized schedule with explicit wait_for_agent barriers so Robot B does not drive away before Robot A completes clamp release.
```

---

## 3. Temperature and Thinking Budget Guidelines

| Task Type | Recommended Temperature | Thinking Budget | Notes |
| :--- | :--- | :--- | :--- |
| **3D Spatial Bounding Boxes** | `0.1 - 0.2` | `1024 - 2048` | Low temperature ensures tight bounding box coordinates. |
| **Whole-Body Mission Planning** | `0.1` | `2048` | Structured JSON outputs require deterministic logic. |
| **Collaborative Handoffs** | `0.3` | `1024` | Allows exploring alternative collaborative pathways. |
| **ASIMOV Safety Auditing** | `0.0` | `2048` | Zero temperature for strict rule-based violation detection. |

---

## 4. Handling Occlusion and Ambiguity

When targets are partially occluded or reflective:
- Query multi-view inputs (wrist camera + overhead camera) simultaneously.
- Request confidence bounds alongside coordinate outputs.
- Trigger active perception maneuvers (e.g., tilt head camera +15 degrees) if confidence falls below 0.85.

---

<p align="center">
  <i>Maintained by Pruthvi Geedh • Google DeepMind Early Trusted Tester Program</i>
</p>
