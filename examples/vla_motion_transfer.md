# Motion Transfer & Whole-Body VLA Models (Gemini Robotics 2 & 1.5)

Google DeepMind's **Gemini Robotics 2 (VLA)** and **Gemini Robotics On-Device 2** introduce state-of-the-art capabilities for **Whole-Body Motion Transfer**, solving the fundamental bottleneck of physical data scarcity and cross-embodiment generalization.

---

## 🦾 The Cross-Embodiment Challenge

Historically, training a robot to perform a task (e.g. "insert peg in socket" or "fold laundry") required thousands of teleoperated demonstrations *on that exact robot and gripper*. Switching from a parallel-jaw gripper to an anthropomorphic multi-fingered hand (such as the **Open-ENPIRE Hand** or Allegro Hand) traditionally required retraining the policy from scratch.

---

## ⚡ The Gemini Robotics 2 Solution

Gemini Robotics 2 introduces a hierarchical **Whole-Body Intelligence** pipeline trained on multi-robot datasets (Open X-Embodiment 2 and real-world multi-partner telemetry from Apptronik, Boston Dynamics, and Agile Robots):

```
                       ┌──────────────────────────────────────────────┐
                       │  High-Level Embodied Reasoning (ER 2)        │
                       │  - Spatial 3D Grounding & Planning           │
                       │  - Multimodal Video & Audio Understanding    │
                       └──────────────────────┬───────────────────────┘
                                              │ Subtask & Target 3D Pose
                                              ▼
                       ┌──────────────────────────────────────────────┐
                       │  Gemini Robotics 2 (VLA) / On-Device 2       │
                       │  - Whole-Body Trajectory Generation          │
                       │  - Feet to Fingertips Coordination           │
                       └──────────────────────┬───────────────────────┘
                                              │ Normalized Action Tokens (20Hz)
                                              ▼
                       ┌──────────────────────────────────────────────┐
                       │  Hardware Adapter / Policy Head              │
                       │  - Joint Limit Denormalization               │
                       │  - Gripper Kinematics (e.g. Open-ENPIRE)     │
                       └──────────────────────┬───────────────────────┘
                                              │ Joint Commands & Torques
                                              ▼
                       ┌──────────────────────────────────────────────┐
                       │  Robot Actuators & Motor Controllers         │
                       └──────────────────────────────────────────────┘
```

### Core Mechanisms
1. **Whole-Body Coordination**: Unlike 1.5 which focused on upper-body tabletop manipulation, Gemini Robotics 2 coordinates locomotion (walking, crouching, stretching) simultaneously with arm and hand manipulation.
2. **Fast On-Device Adaptation**: **Gemini Robotics On-Device 2** can adapt to new physical kinematics and sensor configurations locally on edge hardware with only a few hours of demonstration data.
3. **Dexterous End-Effector Control**: Direct continuous mapping for multi-axis finger joints, compliance control, and slip-aware grasp stabilization.

---

## 💻 Hardware Adapter Reference Pattern

Here is how you bridge Gemini Robotics 2 VLA normalized action outputs to hardware actuators:

```python
import numpy as np
from dataclasses import dataclass

@dataclass
class RobotHardwareLimits:
    joint_min: np.ndarray  # [rad]
    joint_max: np.ndarray  # [rad]
    max_velocity: np.ndarray  # [rad/s]
    gripper_stroke_mm: float

class OpenEnpireVlaAdapter:
    def __init__(self, limits: RobotHardwareLimits):
        self.limits = limits

    def denormalize_action(self, vla_normalized_action: np.ndarray) -> dict:
        """
        Converts Gemini Robotics 2 normalized output [-1.0, 1.0] 
        into calibrated joint angle targets and gripper stroke.
        """
        # 1. Map arm joints from [-1, 1] to physical joint limits
        arm_norm = vla_normalized_action[:7]  # 7-DoF arm
        joint_targets = self.limits.joint_min + (arm_norm + 1.0) * 0.5 * (self.limits.joint_max - self.limits.joint_min)

        # 2. Map dexterous gripper action (e.g. Open-ENPIRE tendon actuation)
        gripper_norm = vla_normalized_action[7]
        gripper_target_mm = (gripper_norm + 1.0) * 0.5 * self.limits.gripper_stroke_mm

        return {
            "joint_positions_rad": joint_targets,
            "gripper_target_mm": gripper_target_mm,
            "safety_compliant": True
        }

# Example deployment loop
# vla_action = vla_client.infer_step(camera_frame, text_goal="Grasp handle")
# physical_cmd = adapter.denormalize_action(vla_action)
# robot_interface.send_command(physical_cmd)
```

---

## 📚 References
- [Google DeepMind: Gemini Robotics 2 Announcement](https://deepmind.google/discover/blog/gemini-robotics-2-physical-ai/)
- [Open X-Embodiment Collaboration](https://robotics-transformer-x.github.io/)
- [ASIMOV-Agentic Safety Benchmark for Physical AI](https://deepmind.google/technologies/gemini/robotics/)

