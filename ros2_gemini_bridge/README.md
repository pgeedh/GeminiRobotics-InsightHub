# ROS 2 Gemini Robotics Bridge (`ros2_gemini_bridge`)

This package provides native **ROS 2 Humble / Iron / Jazzy** nodes connecting robotic sensor topics (cameras, RGB-D streams, goal commands) directly to Google DeepMind's **Gemini Robotics ER 2** and **ER 1.5** models.

---

## 📦 Package Contents

| Node | Executable | Description |
|------|------------|-------------|
| **Perception Node** | `gemini_perception_node` | Subscribes to camera image stream (`/camera/color/image_raw`), queries Gemini Robotics ER 2 for 2D/3D spatial bounding boxes and grasp affordance points, and publishes detections to `/gemini/detections` and `/gemini/target_grasp_pose`. |
| **Planner Node** | `gemini_planner_node` | Listens for natural language commands on `/gemini/goal_command`, performs whole-body task decomposition, and publishes executable action plans to `/gemini/execution_plan`. |

---

## 🚀 Quick Start & Build

### 1. Source ROS 2 and Build Package
```bash
# In your ROS 2 colcon workspace (e.g. ~/ros2_ws)
cd ~/ros2_ws/src
ln -s /path/to/GeminiRobotics_ER1.5-InsightHub/ros2_gemini_bridge .
cd ~/ros2_ws
colcon build --packages-select ros2_gemini_bridge
source install/setup.bash
```

### 2. Configure Environment
```bash
export GEMINI_API_KEY="your-gemini-api-key"
export GEMINI_ROBOTICS_MODEL="gemini-robotics-er-2"  # or gemini-robotics-er-1.5-preview
```

### 3. Run Nodes
```bash
# Launch Perception Bridge
ros2 run ros2_gemini_bridge gemini_perception_node --ros-args -p image_topic:=/camera/color/image_raw

# Launch Planner Bridge in another terminal
ros2 run ros2_gemini_bridge gemini_planner_node
```

### 4. Test with Sample Goal Command
```bash
ros2 topic pub --once /gemini/goal_command std_msgs/msg/String "data: 'Find the red cylinder, pick it up with right arm, and place on assembly table'"
```

---

## 📡 Published & Subscribed Topics

### `gemini_perception_node`
- **Subscribed**:
  - `/camera/color/image_raw` (`sensor_msgs/msg/Image`) - Camera feed
  - `/gemini/prompt_override` (`std_msgs/msg/String`) - Dynamic query override
- **Published**:
  - `/gemini/detections` (`std_msgs/msg/String`) - JSON formatted 2D/3D bounding boxes
  - `/gemini/target_grasp_pose` (`geometry_msgs/msg/PoseStamped`) - 3D Grasp Target

### `gemini_planner_node`
- **Subscribed**:
  - `/gemini/goal_command` (`std_msgs/msg/String`) - High-level task command
- **Published**:
  - `/gemini/execution_plan` (`std_msgs/msg/String`) - JSON structured multi-step plan
