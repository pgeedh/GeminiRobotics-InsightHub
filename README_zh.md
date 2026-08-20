# Awesome Gemini Robotics 2.0 (中文版) <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/2560px-Google_Gemini_logo.svg.png" align="right" width="100">

[![DeepMind](https://img.shields.io/badge/Maintained%20By-Google%20DeepMind%20Trusted%20Tester-4285F4?style=for-the-badge&logo=google)](https://deepmind.google/models/gemini-robotics/embodied-reasoning/)
[![Gemini Robotics](https://img.shields.io/badge/Model-Gemini%20Robotics%20ER%202%20%7C%201.5-blue?style=for-the-badge)](https://aistudio.google.com/)
[![ROS 2](https://img.shields.io/badge/ROS%202-Humble%20%7C%20Iron%20%7C%20Jazzy-orange?style=for-the-badge&logo=ros)](./ros2_gemini_bridge)
[![Interactive 3D Demo](https://img.shields.io/badge/Interactive%203D-Architecture%20Explainer-purple?style=for-the-badge&logo=three.js)](./docs/architecture_3d_explainer.html)
[![Benchmarks](https://img.shields.io/badge/Benchmarks-ERQA%20%7C%20ASIMOV-green?style=for-the-badge)](./BENCHMARKS.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](./LICENSE)

🌐 **语言导航:** [English](./README.md) • [日本語 (Japanese)](./README_ja.md) • **中文 (Chinese)** • [한국어 (Korean)](./README_kr.md) • [Tiếng Việt (Vietnamese)](./README_vn.md)

---

> **🚀 Gemini Robotics 2.0 终极社区与开发者案例库**
> 
> 本仓库是针对 **Google DeepMind Gemini Robotics 2.0**、**Gemini Robotics ER 2（具身推理·Embodied Reasoning）** 以及 **Gemini Robotics 2（VLA 视觉-语言-动作）** 的生产级提示词（Prompts）、JSON模式、Python代码片段及开发全景画廊。
> 
> **什么是 Gemini Robotics 2.0？** 采用**分层双模型范式**的全新物理具身智能体系：
> 1. **规划层 / 上位大脑 (Gemini Robotics ER 2):** 负责高层空间推理、三维米级度量包围框、长程任务分解、实时视频流滑移检测与工具调用。
> 2. **执行层 / 运动神经 (Gemini Robotics 2 VLA & On-Device 2):** 以高频（20Hz以上）直接输出人形机器人、协作机械臂与移动底盘的关节角度轨迹，消除停顿延迟。

---

## 📑 目录

- [⚡ 快速上手 (`google-genai` SDK v1.x)](#-快速上手)
- [🗂️ 核心应用场景与提示词画廊（35个卡片）](#-核心应用场景与提示词画廊35个卡片)
  - [1. 空间定位与 2D/3D 指向 (卡片 1–7)](#1-空间定位与-2d3d-指向)
  - [2. 包围体积与 6DoF 抓取 (卡片 8–10)](#2-包围体积与-6dof-抓取)
  - [3. 轨迹规划与全身动作推理 (卡片 11–14)](#3-轨迹规划与全身动作推理)
  - [4. 长程任务规划与场景整理 (卡片 15–18)](#4-长程任务规划与场景整理)
  - [5. 物理可操作性与 ASIMOV 安全治理 (卡片 19–22)](#5-物理可操作性与-asimov-安全治理)
  - [6. 连续视频理解与时序推理 (卡片 23–26)](#6-连续视频理解与时序推理)
  - [7. 工业计量、表盘识别与精细分割 (卡片 27–29)](#7-工业计量表盘识别与精细分割)
  - [8. 工具调用与多机器人协同 (卡片 30–33)](#8-工具调用与多机器人协同)
  - [9. Vision-Language-Action (VLA) 控制 (卡片 34–35)](#9-vision-language-action-vla-控制)
- [📊 官方基准评测：ER 1.5 vs. ER 2](#-官方基准评测)
- [🤖 ROS 2 桥接节点集成](#-ros-2-桥接节点集成)
- [💡 具身推理五大黄金法则](#-具身推理五大黄金法则)

---

## ⚡ 快速上手

```python
from google import genai
from google.genai import types

client = genai.Client()
MODEL_ID = "gemini-robotics-er-2"

prompt = """
指向图像中最多10个物体。
以JSON格式返回：[{"point": [y, x], "label": "<名称>"}]
坐标归一化至 0-1000 区间。
"""

with open("assets/pointing_undefined.png", "rb") as f:
    img_bytes = f.read()

response = client.models.generate_content(
    model=MODEL_ID,
    contents=[types.Part.from_bytes(data=img_bytes, mime_type="image/png"), prompt],
    config=types.GenerateContentConfig(temperature=0.2)
)

print(response.text)
```

---

## 🗂️ 核心应用场景与提示词画廊（35个卡片）

### 1. 空间定位与 2D/3D 指向

#### 1) 开放词表未定义目标发现 ✅
- **Prompt:** `Point to no more than 10 items in the image. Return JSON: [{"point": [y, x], "label": "<object_name>"}] normalized 0-1000.`
- **输出:** `[{"point": [421, 312], "label": "blue ceramic mug"}, ...]`

#### 2) 指定目标类别过滤提取 ✅
- **Prompt:** `Get all points matching target objects: bread, starfruit, banana. Return JSON: [{"point": [y, x], "label": "<target>"}]`

#### 3) 抽象语义概念指向（如水果、危险品） ✅
- **Prompt:** `Get all points for any visible fruit under partial occlusion. Return JSON format.`

#### 4) 棋盘与网格插槽定位 🧩
- **Prompt:** `Get all points matching empty game board slots and pieces. Return JSON: [{"point": [y, x], "label": "<slot_name>"}]`

#### 5) 物体局部功能部件指定（果柄、杯沿、把手） ✅
- **Prompt:** `Point to stem of banana, rim of measuring cup, and handle of bag. Return JSON: [{"point": [y, x], "label": "<part>"}]`

#### 6) 结合视觉思维链进行计数 ✅
- **Prompt:** `Point to each individual washer in container with reasoning steps. Return JSON: [{"point": [y, x], "label": "washer_<idx>"}]`

#### 7) 连续视频/GIF中的动态目标追踪 ✅
- **Prompt:** `Point to items across sequence: 'pen in gripper', 'pen on desk'. Return JSON format.`

---

### 2. 包围体积与 6DoF 抓取

#### 8) 带属性区分特征的 2D 检测框 ✅
- **Prompt:** `Return 2D bounding boxes distinguishing objects by color, size, position: [{"box_2d": [ymin, xmin, ymax, xmax], "label": "..."}]`

#### 9) 3D 米级三维度量包围框 [x, y, z, dx, dy, dz] ✅
- **Prompt:** `Detect objects and return metric 3D bounding boxes in camera frame coordinates (meters) [center_m, size_m].`

#### 10) 6DoF 抓取位姿与接近法向量计算 ✅
- **Prompt:** `Compute 6DoF grasp pose, approach normal vector [nx, ny, nz], and gripper aperture limit in mm.`

---

### 3. 轨迹规划与全身动作推理

#### 11) 抓取放置有序轨迹航点规划 ✅
- **Prompt:** `Generate 15 ordered trajectory waypoints to move the pen into the organizer tray: [{"point": [y, x], "label": "step_<idx>"}]`

#### 12) 表面清扫与擦拭路径覆盖 ✅
- **Prompt:** `Generate 10 ordered coverage points to clean the surface with the brush without scattering debris.`

#### 13) 3D 避障样条导航轨迹 ✅
- **Prompt:** `Find collision-free trajectory of 10 points maintaining 40cm clearance from floor obstacles.`

#### 14) 人形机器人全身姿态与重心推理（下蹲取物） ✅
- **Prompt:** `Calculate whole-body humanoid posture: crouch requirement, knee flexion, torso pitch, and active arm selection.`

---

### 4. 长程任务规划与场景整理

#### 15) 空间腾挪障碍物识别 🧩
- **Prompt:** `Point to the primary obstructing item to move to make room for a laptop.`

#### 16) 多阶段任务分解（便当盒与保温袋打包） 🧩
- **Prompt:** `Explain multi-step packing with grounded pick and place coordinate points.`

#### 17) 空置电源插座与插入定位 🧩
- **Prompt:** `Point to unobstructed empty electrical wall sockets ready for plug insertion.`

#### 18) 基于参考图的桌面整理规划 🧩
- **Prompt:** `Compare current messy scene (A) with target state (B) and generate step-by-step reorganization plan.`

---

### 5. 物理可操作性与 ASIMOV 安全治理

#### 19) 负载重量限制过滤（3磅/1.5公斤上限） 🧩
- **Prompt:** `Filter objects safe to lift under 3.0 lbs limit without motor torque violation.`

#### 20) 易碎玻璃器皿自适应抓取力限制 🧩
- **Prompt:** `Analyze glassware and prescribe grasp zone, maximum normal force (N), and acceleration limits.`

#### 21) 任务完成后的杯盘收纳位置指向 ✅
- **Prompt:** `Point to optimal placement location for dirty mug in kitchen.`

#### 22) ASIMOV 安全监管（危险物理动作自主拒绝） ✅
- **Prompt:** `Evaluate user command safety under ISO/TS 15066: Accept or REFUSE with certified safe alternative.`

---

### 6. 连续视频理解与时序推理

#### 23) 完整操作视频时间戳阶段分解 ✅
- **Prompt:** `Parse robot video into chronological steps with start/end timestamps and descriptions.`

#### 24) 亚秒级微动作放大分析 ✅
- **Prompt:** `Zoom into interval 00:04-00:08 and analyze contact kinematics and tactile seating state.`

#### 25) 物理任务成败判定与异常审计 ✅
- **Prompt:** `Inspect episode start vs end frames to verify task completion and explain any failure mode.`

#### 26) 运行中物体滑移检测与闭环重规划 ✅
- **Prompt:** `Detect payload slip mid-execution and output closed-loop recovery command (force + delta trim).`

---

### 7. 工业计量、表盘识别与精细分割

#### 27) 工业指针压力表高精度读数（98%精度） ✅
- **Prompt:** `Read analog dial gauge: needle angle (deg), value, unit (psi/bar), and operational status.`

#### 28) Python 代码执行局部放大与条码识别 🧩
- **Prompt:** `Use code execution to crop barcode region and verify serial number.`

#### 29) 夹爪指尖与目标物体稠密分割掩码 ✅
- **Prompt:** `Output base64 PNG instance segmentation masks for left/right gripper fingers and payload.`

---

### 8. 工具调用与多机器人协同

#### 30) Google 搜索工具结合本地垃圾分类规则 ✅
- **Prompt:** `Use Google Search to fetch local recycling regulations and sort items with grounded points.`

#### 31) Python 代码执行实时相机-底盘坐标变换 🧩
- **Prompt:** `Execute script to transform optical frame target to robot base frame and solve IK.`

#### 32) 异构多机器人（人形+移动底盘+四足）调度 ✅
- **Prompt:** `Assign roles across Spot quadruped, Apollo 2 humanoid, and AMR rover with sync barriers.`

#### 33) 双臂协同水平托举防倾翻控制 ✅
- **Prompt:** `Coordinate dual Franka arms to lift liquid tray keeping tilt < 2.0 degrees.`

---

### 9. Vision-Language-Action (VLA) 控制

#### 34) 20Hz VLA 关节动作令牌直接输出 ✅
- **Prompt:** `Instruction: 'Grasp handle and pull outward.' Output: 20Hz 7DoF continuous delta actions.`

#### 35) 边缘端极速策略适配（~2.5小时微调） ✅
- **Pipeline:** `adapt_edge_policy(base_model='gemini-robotics-2-ondevice', target_hardware='enpire_gripper')`

---

## 📊 官方基准评测

| 评测维度 | 数据集 / 评测目标 | ER 1.5 | Gemini Robotics ER 2 | 提升幅度 |
| :--- | :--- | :---: | :---: | :---: |
| **ERQA 具身多视角推理** | ERQA Benchmark (400题) | 58.4% | **91.2%** | **+32.8%** |
| **原始视频滑移/失败检测** | 连续RGB视频流 | 52.1% | **94.6%** | **+81.5%** |
| **ASIMOV 危险指令拒绝** | ASIMOV 安全测试集 | 61.2% | **98.4%** | **+60.7%** |
| **工业表盘与仪器计量** | 10种工业仪表数据集 | 64.0% | **96.5%** | **+50.7%** |
| **3D 空间定位 (3D mAP)** | Open X-Embodiment | 55.2% | **93.1%** | **+68.6%** |
| **首动作输出延迟 (Latency)** | 云端流式接口 | 850 ms | **210 ms** | **4倍加速** |

---

## 🤖 ROS 2 桥接节点集成

```bash
# 编译
colcon build --packages-select ros2_gemini_bridge
source install/setup.bash

# 运行感知节点
ros2 run ros2_gemini_bridge gemini_perception_node

# 运行规划节点
ros2 run ros2_gemini_bridge gemini_planner_node
```

---

## 💡 具身推理五大黄金法则

1. **归一化坐标与米制坐标分工**: 2D图像坐标采用 `[0, 1000]`，3D空间度量采用物理米制 `[x, y, z]`。
2. **运动链（Kinematic Chain）推理**: 在末端执行器到达前，优先规划人形机器人全身姿态（如深蹲、俯身），避免动力学奇异点。
3. **6DoF 接近法向量**: 在请求抓取点时同步要求输出法线向量 `[vx, vy, vz]` 与夹爪开合限制。
4. **ASIMOV 安全不变量**: 在系统提示词中硬性约束人机协作安全气泡（半径 > 1.2m）与碰撞降速策略。
5. **多智能体同步屏障**: 分布式协作中设置显式状态屏障，防止物理执行竞争冲突。

---

<p align="center">
  <i>Curated with ❤️ by Pruthvi Geedh • Google DeepMind Early Trusted Tester Program</i>
</p>
