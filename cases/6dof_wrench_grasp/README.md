# Case: 6DoF Grasp Affordance with Approach Vector

**Description:** Evaluates a target mechanical tool and outputs an approach normal vector, grip aperture width, and grasp point.  
**Target Model:** `gemini-robotics-er-2`  
**Primary Source:** [Google DeepMind Gemini Robotics Technical Documentation](https://deepmind.google/models/gemini-robotics/embodied-reasoning/)

### Prompt
```text
Identify the calibration wrench on the table.
Compute the 6DoF grasp affordance for a parallel-jaw gripper.
Return JSON format:
{
  "grasp_point_2d": [y, x],
  "approach_normal_vector": [vx, vy, vz],
  "recommended_gripper_aperture_mm": 45,
  "grasp_type": "pinch_precision"
}
```

### Sample Output (JSON)
```json
{
  "grasp_point_2d": [535, 365],
  "approach_normal_vector": [0.0, 0.0, -1.0],
  "recommended_gripper_aperture_mm": 32,
  "grasp_type": "pinch_precision"
}
```
