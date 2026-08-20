# Awesome Gemini Robotics 2.0 (中文版)

[![Maintained By: Pruthvi Geedh](https://img.shields.io/badge/Maintained%20By-Pruthvi%20Geedh-4285F4?style=flat-square&logo=github)](https://github.com/pgeedh)
[![Model: Gemini Robotics ER 2 & VLA 2.0](https://img.shields.io/badge/Model-Gemini%20Robotics%20ER%202%20%7C%20VLA%202.0-blue?style=flat-square)](https://aistudio.google.com/)
[![ROS 2: Humble / Iron / Jazzy](https://img.shields.io/badge/ROS%202-Humble%20%7C%20Iron%20%7C%20Jazzy-orange?style=flat-square&logo=ros)](./ros2_gemini_bridge)
[![Benchmarks: Official DeepMind ER 2](https://img.shields.io/badge/Benchmarks-Official%20DeepMind%20ER%202-green?style=flat-square)](./BENCHMARKS.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](./LICENSE)

**语言导航:** [English](./README.md) | [日本語 (Japanese)](./README_ja.md) | **中文 (Chinese)** | [한국어 (Korean)](./README_kr.md) | [Tiếng Việt (Vietnamese)](./README_vn.md)

---

### 概述

面向 **Google DeepMind Gemini Robotics 2.0**、**Gemini Robotics ER 2（具身推理·Embodied Reasoning）** 以及 **Gemini Robotics 2（Vision-Language-Action / VLA）** 的开发者参考库，涵盖生产级提示词模式、JSON模式、Python SDK代码及ROS 2执行节点。

Gemini Robotics 2.0 采用**分层双模型架构**：
1. **规划层 / 具身推理 (Gemini Robotics ER 2):** 负责多模态空间感知、三维米级度量包围框预测、长程任务分解、实时视频流滑移检测与工具调用。
2. **控制层 / 执行策略 (Gemini Robotics 2 VLA & On-Device 2):** 以高频（20Hz以上）直接输出人形机器人、协作机械臂与移动底盘的关节角度轨迹，消除停顿延迟。

---

## 目录

- [如何使用本开发实战手册](#如何使用本开发实战手册)
- [Cookbook 实战测试轨道 (`cookbook/`)](#cookbook-实战测试轨道-cookbook)
- [快速上手 (`google-genai` SDK v1.x)](#快速上手)
- [核心应用场景与提示词画廊（35个卡片）](#核心应用场景与提示词画廊35个卡片)
  - [1. 空间定位与 2D/3D 指向](#1-空间定位与-2d3d-指向)
  - [2. 包围体积与 6DoF 抓取](#2-包围体积与-6dof-抓取)
  - [3. 轨迹规划与全身动作推理](#3-轨迹规划与全身动作推理)
  - [4. 长程任务规划与场景整理](#4-长程任务规划与场景整理)
  - [5. 物理可操作性与 ASIMOV 安全治理](#5-物理可操作性与-asimov-安全治理)
  - [6. 连续视频理解与时序推理](#6-连续视频理解与时序推理)
  - [7. 工业计量、表盘识别与精细分割](#7-工业计量表盘识别与精细分割)
  - [8. 工具调用与多机器人协同](#8-工具调用与多机器人协同)
  - [9. Vision-Language-Action (VLA) 控制](#9-vision-language-action-vla-控制)
- [官方DeepMind基准评测（ER 2 对比 SOTA）](#官方deepmind基准评测)
- [ROS 2 桥接节点集成](#ros-2-桥接节点集成)
- [具身推理五大黄金法则](#具身推理五大黄金法则)
- [贡献指南](#贡献指南)

---

## 如何使用本开发实战手册

1. **交互式终端测试面板 (`python cli.py`):** 启动命令行交互套件，一键测试35个提示词卡片与6大实战配方。
2. **模块化 Cookbook 配方 (`cookbook/`):** 包含空间感知、全身姿态、视频滑移检测、安全监管与多机器人协同独立脚本。
3. **自定义测试沙盒 (`python cookbook/interactive_sandbox.py`):** 允许传入任意图像或自定义提示词进行快速测试。
4. **ROS 2 桥接集成 (`ros2_gemini_bridge`):** 直接对接机器人相机话题与规划控制节点。

---

## Cookbook 实战测试轨道 (`cookbook/`)

| 测试轨道 / 配方 | 配方文件 | 说明 | 快速执行命令 |
| :--- | :--- | :--- | :--- |
| **1. 空间感知与 6DoF 抓取** | [`cookbook/01_spatial_perception_recipe.py`](./cookbook/01_spatial_perception_recipe.py) | 2D指向、3D米级度量框与接近法向量。 | `python cookbook/01_spatial_perception_recipe.py` |
| **2. 运动学任务规划** | [`cookbook/02_kinematic_planning_recipe.py`](./cookbook/02_kinematic_planning_recipe.py) | Pydantic全身姿态选择与无碰撞序列生成。 | `python cookbook/02_kinematic_planning_recipe.py` |
| **3. 视频滑移与异常追踪** | [`cookbook/03_continuous_video_slip_recipe.py`](./cookbook/03_continuous_video_slip_recipe.py) | 连续视频时序接触分析与闭环补偿。 | `python cookbook/03_continuous_video_slip_recipe.py` |
| **4. ASIMOV 安全监管** | [`cookbook/04_asimov_safety_guard_recipe.py`](./cookbook/04_asimov_safety_guard_recipe.py) | ISO/TS 15066安全策略强制执行与自主拒绝。 | `python cookbook/04_asimov_safety_guard_recipe.py` |
| **5. 多机器人协同** | [`cookbook/05_multi_agent_fleet_recipe.py`](./cookbook/05_multi_agent_fleet_recipe.py) | 异构机器人显式等待屏障协同调度。 | `python cookbook/05_multi_agent_fleet_recipe.py` |
| **6. 20Hz VLA 动作块生成** | [`cookbook/06_vla_action_chunking_recipe.py`](./cookbook/06_vla_action_chunking_recipe.py) | 20Hz连续7DoF电机动作块生成与延迟测试。 | `python cookbook/06_vla_action_chunking_recipe.py` |
| **交互式沙盒** | [`cookbook/interactive_sandbox.py`](./cookbook/interactive_sandbox.py) | 任意图像与自定义提示词交互式测试套件。 | `python cookbook/interactive_sandbox.py` |

---

## 快速上手

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

## 核心应用场景与提示词画廊（35个卡片）

### 1. 空间定位与 2D/3D 指向

#### 1) 开放词表未定义目标发现 `[Verified]`
- **Prompt:** `Point to no more than 10 items in the image. Return JSON: [{"point": [y, x], "label": "<object_name>"}] normalized 0-1000.`
- **输出:** `[{"point": [421, 312], "label": "blue ceramic mug"}, ...]`

#### 2) 指定目标类别过滤提取 `[Verified]`
- **Prompt:** `Get all points matching target objects: bread, starfruit, banana. Return JSON: [{"point": [y, x], "label": "<target>"}]`

#### 3) 抽象语义概念指向（如水果、工具） `[Verified]`
- **Prompt:** `Get all points for any visible fruit under partial occlusion. Return JSON format.`

#### 4) 棋盘与网格插槽定位 `[Custom Scenario]`
- **Prompt:** `Get all points matching empty game board slots and pieces. Return JSON: [{"point": [y, x], "label": "<slot_name>"}]`

#### 5) 物体局部功能部件指定（果柄、杯沿、把手） `[Verified]`
- **Prompt:** `Point to stem of banana, rim of measuring cup, and handle of bag. Return JSON: [{"point": [y, x], "label": "<part>"}]`

#### 6) 结合视觉思维链进行计数 `[Verified]`
- **Prompt:** `Point to each individual washer in container with reasoning steps. Return JSON: [{"point": [y, x], "label": "washer_<idx>"}]`

#### 7) 连续视频/GIF中的动态目标追踪 `[Verified]`
- **Prompt:** `Point to items across sequence: 'pen in gripper', 'pen on desk'. Return JSON format.`

---

### 2. 包围体积与 6DoF 抓取

#### 8) 带属性区分特征的 2D 检测框 `[Verified]`
- **Prompt:** `Return 2D bounding boxes distinguishing objects by color, size, position: [{"box_2d": [ymin, xmin, ymax, xmax], "label": "..."}]`

#### 9) 3D 米级三维度量包围框 [x, y, z, dx, dy, dz] `[Verified]`
- **Prompt:** `Detect objects and return metric 3D bounding boxes in camera frame coordinates (meters) [center_m, size_m].`

#### 10) 6DoF 抓取位姿与接近法向量计算 `[Verified]`
- **Prompt:** `Compute 6DoF grasp pose, approach normal vector [nx, ny, nz], and gripper aperture limit in mm.`

---

### 3. 轨迹规划与全身动作推理

#### 11) 抓取放置有序轨迹航点规划 `[Verified]`
- **Prompt:** `Generate 15 ordered trajectory waypoints to move the pen into the organizer tray: [{"point": [y, x], "label": "step_<idx>"}]`

#### 12) 表面清扫与擦拭路径覆盖 `[Verified]`
- **Prompt:** `Generate 10 ordered coverage points to clean the surface with the brush without scattering debris.`

#### 13) 3D 避障样条导航轨迹 `[Verified]`
- **Prompt:** `Find collision-free trajectory of 10 points maintaining 40cm clearance from floor obstacles.`

#### 14) 人形机器人全身姿态与重心推理（下蹲取物） `[Verified]`
- **Prompt:** `Calculate whole-body humanoid posture: crouch requirement, knee flexion, torso pitch, and active arm selection.`

---

### 4. 长程任务规划与场景整理

#### 15) 空间腾挪障碍物识别 `[Custom Scenario]`
- **Prompt:** `Point to the primary obstructing item to move to make room for a laptop.`

#### 16) 多阶段任务分解（便当盒与保温袋打包） `[Custom Scenario]`
- **Prompt:** `Explain multi-step packing with grounded pick and place coordinate points.`

#### 17) 空置电源插座与插入定位 `[Custom Scenario]`
- **Prompt:** `Point to unobstructed empty electrical wall sockets ready for plug insertion.`

#### 18) 基于参考图的桌面整理规划 `[Custom Scenario]`
- **Prompt:** `Compare current messy scene (A) with target state (B) and generate step-by-step reorganization plan.`

---

### 5. 物理可操作性与 ASIMOV 安全治理

#### 19) 负载重量限制过滤（3磅/1.5公斤上限） `[Custom Scenario]`
- **Prompt:** `Filter objects safe to lift under 3.0 lbs limit without motor torque violation.`

#### 20) 易碎玻璃器皿自适应抓取力限制 `[Custom Scenario]`
- **Prompt:** `Analyze glassware and prescribe grasp zone, maximum normal force (N), and acceleration limits.`

#### 21) 任务完成后的杯盘收纳位置指向 `[Verified]`
- **Prompt:** `Point to optimal placement location for dirty mug in kitchen.`

#### 22) ASIMOV 安全监管（危险物理动作自主拒绝） `[Verified]`
- **Prompt:** `Evaluate user command safety under ISO/TS 15066: Accept or REFUSE with certified safe alternative.`

---

### 6. 连续视频理解与时序推理

#### 23) 完整操作视频时间戳阶段分解 `[Verified]`
- **Prompt:** `Parse robot video into chronological steps with start/end timestamps and descriptions.`

#### 24) 亚秒级微动作放大分析 `[Verified]`
- **Prompt:** `Zoom into interval 00:04-00:08 and analyze contact kinematics and tactile seating state.`

#### 25) 物理任务成败判定与异常审计 `[Verified]`
- **Prompt:** `Inspect episode start vs end frames to verify task completion and explain any failure mode.`

#### 26) 运行中物体滑移检测与闭环重规划 `[Verified]`
- **Prompt:** `Detect payload slip mid-execution and output closed-loop recovery command (force + delta trim).`

---

### 7. 工业计量、表盘识别与精细分割

#### 27) 工业指针压力表高精度读数（98%精度） `[Verified]`
- **Prompt:** `Read analog dial gauge: needle angle (deg), value, unit (psi/bar), and operational status.`

#### 28) Python 代码执行局部放大与条码识别 `[Custom Scenario]`
- **Prompt:** `Use code execution to crop barcode region and verify serial number.`

#### 29) 夹爪指尖与目标物体稠密分割掩码 `[Verified]`
- **Prompt:** `Output base64 PNG instance segmentation masks for left/right gripper fingers and payload.`

---

### 8. 工具调用与多机器人协同

#### 30) Google 搜索工具结合本地垃圾分类规则 `[Verified]`
- **Prompt:** `Use Google Search to fetch local recycling regulations and sort items with grounded points.`

#### 31) Python 代码执行实时相机-底盘坐标变换 `[Custom Scenario]`
- **Prompt:** `Execute script to transform optical frame target to robot base frame and solve IK.`

#### 32) 异构多机器人（人形+移动底盘+四足）调度 `[Verified]`
- **Prompt:** `Assign roles across Spot quadruped, Apollo 2 humanoid, and AMR rover with sync barriers.`

#### 33) 双臂协同水平托举防倾翻控制 `[Verified]`
- **Prompt:** `Coordinate dual Franka arms to lift liquid tray keeping tilt < 2.0 degrees.`

---

### 9. Vision-Language-Action (VLA) 控制

#### 34) 20Hz VLA 关节动作令牌直接输出 `[Verified]`
- **Prompt:** `Instruction: 'Grasp handle and pull outward.' Output: 20Hz 7DoF continuous delta actions.`

#### 35) 边缘端极速策略适配（~2.5小时微调） `[Verified]`
- **Pipeline:** `adapt_edge_policy(base_model='gemini-robotics-2-ondevice', target_hardware='enpire_gripper')`

---

## 官方DeepMind基准评测

| 评测维度 | Opus 5 | GPT 5.6 Sol | Gemini Robotics ER 1.6 | Gemini 3.6 Flash | Gemini Robotics ER 2 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **图像成功判定** | 83.6% | 83.1% | 82.9% | 83.3% | **87.7%** |
| **视频成功判定** | 81.0% | 74.7% | 76.0% | 75.4% | **82.4%** |
| **ERQA 具身多视角推理** | 67.2% | 43.2% | 72.5% | 73.0% | **78.5%** |
| **工业表盘与仪器计量** | 53.0% | 61.5% | 52.8% | 52.0% | **65.7%** |
| **任务阶段进展分类** | 37.1% | 46.2% | 42.7% | 43.9% | **57.4%** |
| **实机 VLA 硬件控制** | — | — | 48.6% | — | **60.0%** |
| **安全指令遵循精度** | 95.9% | 91.4% | 47.2% | — | **97.9%** |
| **人机距离安全合规 (1m)** | 77.1% | 83.4% | 51.1% | — | **93.0%** |

---

## ROS 2 桥接节点集成

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

## 具身推理五大黄金法则

1. **归一化坐标与米制坐标分工**: 2D图像坐标采用 `[0, 1000]`，3D空间度量采用物理米制 `[x, y, z]`。
2. **运动链（Kinematic Chain）推理**: 在末端执行器到达前，优先规划人形机器人全身姿态（如深蹲、俯身），避免动力学奇异点。
3. **6DoF 接近法向量**: 在请求抓取点时同步要求输出法线向量 `[vx, vy, vz]` 与夹爪开合限制。
4. **ASIMOV 安全不变量**: 在系统提示词中硬性约束人机协作安全气泡（半径 > 1.2m）与碰撞降速策略。
5. **多智能体同步屏障**: 分布式协作中设置显式状态屏障，防止物理执行竞争冲突。

## 贡献指南

欢迎社区贡献！如需提交新的提示词卡片、基准测试评估或硬件桥接适配，请参阅 [`CONTRIBUTING.md`](./CONTRIBUTING.md)。

---

## 许可证与图像署名

- **文本与代码**: 遵循 [MIT 许可证](./LICENSE) 开源。
- **图像与视觉演示**: 标有 `[Verified]` 的示例图像均来自 Google DeepMind 的公开技术报告和博客，在此仅作为学术演示与教育参考；如需二次分发请核对上游授权许可。`[Custom Scenario]` 占位符可替换为您自己在 `assets/` 目录下的机器人实拍截图。

---

## 主要参考来源

- **Google DeepMind Physical AI**: [Gemini Robotics 2 & Embodied Reasoning](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) — 技术架构、全身人形机器人控制与双臂精细操作。
- **Google Developers Blog**: [Building Physical Agents with Gemini Robotics](https://developers.googleblog.com/en/building-the-next-generation-of-physical-agents-with-gemini-robotics-er-15/) — 空间定位、点位提取与运动学提示词模式。
- **Google AI for Developers**: [Gemini Robotics API 文档](https://ai.google.dev/gemini-api/docs/robotics-overview) — 空间标记、坐标系与结构化 API 参考。
- **研究论文**: *"Gemini Robotics: Bringing AI into the Physical World"* ([arXiv:2503.20020](https://arxiv.org/abs/2503.20020))。

---

## 致谢

本仓库收录的应用用例、配方与提示词模式得益于 Physical AI 与机器人开发者社区的开源共享。我们向所有案例贡献者与研究团队致以诚挚的感谢：

- [@GoogleDeepMind](https://x.com/GoogleDeepMind)
- [@GeminiApp](https://x.com/GeminiApp)
- Open X-Embodiment 与 ROS 2 机器人开源社区

如果您在实践中发现了更多有趣的机器人应用场景与提示词，欢迎随时提交 PR 或 Issue 与社区共同探索！

---

<p align="center">
  <i>Curated by Pruthvi Geedh</i>
</p>
