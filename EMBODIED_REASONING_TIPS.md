# 🧠 The Physical AI Practitioner's Handbook: Mastering Embodied Reasoning with Gemini Robotics ER 2

Welcome to the definitive engineering guide for **Embodied Reasoning (ER)** with Google DeepMind's Gemini Robotics models. This guide provides battle-tested prompting patterns, coordinate frame conversions, safety constraints, and latency optimizations derived from the Early Trusted Tester program.

---

## 📐 1. Coordinate Framing & Spatial Grounding

Gemini Robotics ER models output spatial tokens in a normalized **`[0, 1000]` coordinate system** for 2D bounding boxes/points and metric meters `[x, y, z]` for 3D bounding boxes.

### Golden Rule of 2D Coordinates
- Top-Left Origin: `(ymin=0, xmin=0)` is the top-left pixel.
- Bottom-Right: `(ymax=1000, xmax=1000)` is the bottom-right pixel.
- To convert normalized coordinates `[ymin, xmin, ymax, xmax]` to pixel values:
  ```python
  pixel_xmin = int((xmin / 1000.0) * image_width)
  pixel_xmax = int((xmax / 1000.0) * image_width)
  pixel_ymin = int((ymin / 1000.0) * image_height)
  pixel_ymax = int((ymax / 1000.0) * image_height)
  ```

### 3D Metric Coordinate Prompt Template
When prompting for 3D boxes, always provide camera intrinsics hints or ask for metric meters relative to camera optical center:
```text
Conditioning: Camera optical center is (0,0,0). Forward is +Z, Right is +X, Down is +Y.
Prompt: Detect all manipulable tools on the workbench.
Return 3D oriented bounding boxes in meters:
[{"label": "name", "box_3d": {"center": [x, y, z], "size": [dx, dy, dz], "rotation_rpy": [roll, pitch, yaw]}}]
```

---

## ⚡ 2. 10 Essential Embodied Reasoning Prompt Patterns

### Pattern 1: Chain-of-Kinematics (Whole-Body Stance Selection)
*Prevents joint limit singularities by forcing the model to select whole-body posture before arm movement.*
```text
Task: Pick up the dropped bolt beneath the assembly jig (clearance height: 35cm).
Reasoning Steps:
1. Analyze if the humanoid robot can reach while standing or if it must crouch.
2. Evaluate left arm vs right arm reach corridor to avoid occluding the head camera.
3. Output the whole-body stance: crouch(height_fraction=0.4), torso_pitch_deg=18.0.
4. Output arm trajectory waypoints.
```

### Pattern 2: 6DoF Grasp Affordance Grounding
*Specifies the exact approach normal vector and finger opening width rather than just a center point.*
```text
Identify the screwdriver on the table.
Return the 6DoF grasp affordance for a tendon-driven gripper:
- grasp_point: [y, x]
- approach_vector: [vx, vy, vz] normalized
- grasp_type: ('pinch_precision', 'power_cylinder', 'suction')
- target_grip_aperture_mm: 35
```

### Pattern 3: ASIMOV-Agentic Safety Invariant
*Embeds hard safety guarantees directly into the model's high-priority system instructions.*
```text
System Invariant:
- If a human operator is visible within a 1.2m radius of the manipulator, cap all joint speeds to 0.2 rad/s.
- If a human hand enters the active grasp corridor, immediately output an ASIMOV_SAFETY_PAUSE state.
- Never swing heavy payloads (>5kg) with angular acceleration > 0.5 rad/s^2.
```

### Pattern 4: Multimodal Video State Verification (Before/After)
*Audits execution success across temporal video frames.*
```text
Watch the start state frame (Frame 0) and final state frame (Frame 60).
Did the robot successfully mate the connector into the port?
Checklist:
1. Is the connector fully seated without gap > 1mm?
2. Did any wire harness snag on the fixture?
3. Output state: 'SUCCESS' or 'FAILURE_RETRY' with spatial coordinate of defect.
```

### Pattern 5: Multi-Robot Fleet Task Allocation
*Coordinates dual agents with synchronization barriers to avoid deadlock.*
```text
Available Fleet:
- Robot A (Humanoid Manipulator, 20kg payload)
- Robot B (Mobile Logistics Rover, flatbed bed)
Mission: Relocate the heavy engine casting.
Requirement: Output synchronized schedule with explicit wait_for_agent barriers so Robot B does not drive away before Robot A completes clamp release.
```

---

## 🛠️ 3. Temperature & Thinking Budget Guidelines

| Task Type | Recommended Temperature | Thinking Budget | Notes |
| :--- | :--- | :--- | :--- |
| **3D Spatial Bounding Boxes** | `0.1 - 0.2` | `1024 - 2048` | Low temperature ensures tight bounding box coordinates. |
| **Whole-Body Mission Planning** | `0.1` | `2048` | Structured JSON outputs require deterministic logic. |
| **Creative / Open-Ended Handoffs** | `0.4` | `1024` | Allows exploring alternative collaborative pathways. |
| **ASIMOV Safety Auditing** | `0.0` | `2048` | Zero temperature for strict rule-based violation detection. |

---

## 🚨 4. Handling Occlusion and Ambiguity

When parts are partially occluded or reflective:
1. **Request Multi-View Confirmation**: Prompt Gemini ER 2 to combine wrist camera and head camera views.
2. **Confidence Bounds**: Instruct the model to return an `occlusion_ratio` (0.0 to 1.0) and specify a secondary exploratory viewpoint if confidence is below 0.85.

---

*Curated for Google DeepMind Gemini Robotics Early Access Program.*
