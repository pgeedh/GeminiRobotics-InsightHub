# Awesome Gemini Robotics 2.0 (Tiếng Việt)

[![Maintained By: Pruthvi Geedh](https://img.shields.io/badge/Maintained%20By-Pruthvi%20Geedh-4285F4?style=flat-square&logo=github)](https://github.com/pgeedh)
[![Model: Gemini Robotics ER 2 & VLA 2.0](https://img.shields.io/badge/Model-Gemini%20Robotics%20ER%202%20%7C%20VLA%202.0-blue?style=flat-square)](https://aistudio.google.com/)
[![ROS 2: Humble / Iron / Jazzy](https://img.shields.io/badge/ROS%202-Humble%20%7C%20Iron%20%7C%20Jazzy-orange?style=flat-square&logo=ros)](./ros2_gemini_bridge)
[![Benchmarks: Official DeepMind ER 2](https://img.shields.io/badge/Benchmarks-Official%20DeepMind%20ER%202-green?style=flat-square)](./BENCHMARKS.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](./LICENSE)

**Ngôn ngữ:** [English](./README.md) | [日本語 (Japanese)](./README_ja.md) | [中文 (Chinese)](./README_zh.md) | [한국어 (Korean)](./README_kr.md) | **Tiếng Việt (Vietnamese)**

---

### Tổng quan

Thư viện tài liệu dành cho nhà phát triển tập hợp các mẫu câu lệnh (prompts), lược đồ JSON, mã nguồn Python và node thực thi ROS 2 dành cho **Google DeepMind Gemini Robotics 2.0**, **Gemini Robotics ER 2 (Embodied Reasoning - Suy luận thể nhập)** và **Gemini Robotics 2 (Vision-Language-Action / VLA)**.

Gemini Robotics 2.0 hoạt động theo **Kiến trúc Phân tầng Kép**:
1. **Bộ lập kế hoạch / Suy luận thể nhập (Gemini Robotics ER 2):** Suy luận không gian 3D, hộp bao thể tích tính bằng mét, lập kế hoạch nhiệm vụ dài hạn, phát hiện trượt rơi qua video thời gian thực và điều phối công cụ.
2. **Kiểm soát vận động / Chính sách thực thi (Gemini Robotics 2 VLA & On-Device 2):** Điều khiển động cơ tần số cao (20Hz+) tạo quỹ đạo khớp trực tiếp cho robot hình người, tay máy và xe tự hành không độ trễ ngắt quãng.

---

## Mục lục

- [Hướng dẫn sử dụng Playbook](#hướng-dẫn-sử-dụng-playbook)
- [Các bài kiểm tra thực hành Cookbook (`cookbook/`)](#các-bài-kiểm-tra-thực-hành-cookbook-cookbook)
- [Bắt đầu nhanh (`google-genai` SDK v1.x)](#bắt-đầu-nhanh)
- [Thư viện 35 Thẻ Prompt Ứng Dụng](#thư-viện-35-thẻ-prompt-ứng-dụng)
  - [1. Định vị không gian & Điểm trỏ 2D/3D](#1-định-vị-không-gian--điểm-trỏ-2d3d)
  - [2. Hộp bao thể tích & Gắp 6DoF](#2-hộp-bao-thể-tích--gắp-6dof)
  - [3. Lập kế hoạch quỹ đạo & Tư thế toàn thân](#3-lập-kế-hoạch-quỹ-đạo--tư-thế-toàn-thân)
  - [4. Phân rã nhiệm vụ dài hạn & Dọn dẹp không gian](#4-phân-rã-nhiệm-vụ-dài-hạn--dọn-dẹp-không-gian)
  - [5. Khả năng tương tác & Quản trị an toàn ASIMOV](#5-khả-năng-tương-tác--quản-trị-an-toàn-asimov)
  - [6. Phân tích video liên tục & Suy luận thời gian](#6-phân-tích-video-liên-tục--suy-luận-thời-gian)
  - [7. Đo lường công nghiệp, Đồng hồ đo & Phân đoạn chi tiết](#7-đo-lường-công-nghiệp-đồng-hồ-đo--phân-đoạn-chi-tiết)
  - [8. Sử dụng công cụ & Phối hợp hạm đội robot](#8-sử-dụng-công-cụ--phối-hợp-hạm-đội-robot)
  - [9. Điều khiển động cơ Vision-Language-Action (VLA)](#9-điều-khiển-động-cơ-vision-language-action-vla)
- [Bảng so chuẩn chính thức DeepMind (ER 2 vs SOTA)](#bảng-so-chuẩn-chính-thức-deepmind)
- [Tích hợp cầu nối ROS 2](#tích-hợp-cầu-nối-ros-2)
- [5 Quy tắc vàng cho Suy luận thể nhập](#5-quy-tắc-vàng-cho-suy-luận-thể-nhập)
- [Đóng góp](#đóng-góp)

---

## Hướng dẫn sử dụng Playbook

1. **Giao diện dòng lệnh tương tác (`python cli.py`):** Khởi chạy bộ CLI để kiểm tra 35 thẻ prompt và 6 công thức thực hành theo thời gian thực.
2. **Các công thức Cookbook dạng module (`cookbook/`):** Chạy các tệp script Python độc lập để thử nghiệm nhận thức 3D, lập kế hoạch tư thế, theo dõi trượt qua video và quản trị an toàn.
3. **Sandbox thử nghiệm tùy chỉnh (`python cookbook/interactive_sandbox.py`):** Nhập ảnh bất kỳ từ camera hoặc câu lệnh tùy chỉnh để đánh giá kết quả mô hình.
4. **Tích hợp ROS 2 (`ros2_gemini_bridge`):** Kết nối trực tiếp các topic camera robot với các node nhận thức và lập kế hoạch.

---

## Các bài kiểm tra thực hành Cookbook (`cookbook/`)

| Bài thực hành / Recipe | Tệp mã nguồn | Mô tả | Lệnh chạy nhanh |
| :--- | :--- | :--- | :--- |
| **1. Nhận thức không gian & Gắp 6DoF** | [`cookbook/01_spatial_perception_recipe.py`](./cookbook/01_spatial_perception_recipe.py) | Điểm trỏ 2D, hộp bao 3D theo mét và vector pháp tuyến. | `python cookbook/01_spatial_perception_recipe.py` |
| **2. Kế hoạch động học toàn thân** | [`cookbook/02_kinematic_planning_recipe.py`](./cookbook/02_kinematic_planning_recipe.py) | Chọn tư thế ngồi xổm Pydantic và chuỗi tránh va chạm. | `python cookbook/02_kinematic_planning_recipe.py` |
| **3. Theo dõi trượt & Bất thường video** | [`cookbook/03_continuous_video_slip_recipe.py`](./cookbook/03_continuous_video_slip_recipe.py) | Suy luận tiếp xúc chuỗi video và điều chỉnh vòng kín. | `python cookbook/03_continuous_video_slip_recipe.py` |
| **4. Quản trị an toàn ASIMOV** | [`cookbook/04_asimov_safety_guard_recipe.py`](./cookbook/04_asimov_safety_guard_recipe.py) | Thực thi tiêu chuẩn ISO/TS 15066 và tự động từ chối lệnh. | `python cookbook/04_asimov_safety_guard_recipe.py` |
| **5. Phối hợp hạm đội robot** | [`cookbook/05_multi_agent_fleet_recipe.py`](./cookbook/05_multi_agent_fleet_recipe.py) | Đồng bộ hạm đội không đồng nhất với rào chắn chờ. | `python cookbook/05_multi_agent_fleet_recipe.py` |
| **6. Khối hành động VLA 20Hz** | [`cookbook/06_vla_action_chunking_recipe.py`](./cookbook/06_vla_action_chunking_recipe.py) | Tạo khối hành động điều khiển 7DoF tần số 20Hz. | `python cookbook/06_vla_action_chunking_recipe.py` |
| **Sandbox tương tác** | [`cookbook/interactive_sandbox.py`](./cookbook/interactive_sandbox.py) | Bộ khung kiểm thử tương tác với ảnh và prompt tùy chọn. | `python cookbook/interactive_sandbox.py` |

---

## Bắt đầu nhanh

```python
from google import genai
from google.genai import types

client = genai.Client()
MODEL_ID = "gemini-robotics-er-2"

prompt = """
Chỉ ra tối đa 10 đối tượng trong hình.
Trả về định dạng JSON: [{"point": [y, x], "label": "<tên_đối_tượng>"}]
Tọa độ được chuẩn hóa từ 0 đến 1000.
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

## Thư viện 35 Thẻ Prompt Ứng Dụng

### 1. Định vị không gian & Điểm trỏ 2D/3D

#### 1) Phát hiện đối tượng mở không định trước `[Verified]`
- **Prompt:** `Point to no more than 10 items in the image. Return JSON: [{"point": [y, x], "label": "<object_name>"}] normalized 0-1000.`

#### 2) Lọc và trỏ vào đối tượng được chỉ định `[Verified]`
- **Prompt:** `Get all points matching: bread, starfruit, banana. Return JSON: [{"point": [y, x], "label": "<target>"}]`

#### 3) Chỉ điểm theo khái niệm trừu tượng (Hoa quả, đồ nguy hiểm) `[Verified]`
- **Prompt:** `Get all points for any visible fruit under occlusion. Return JSON format.`

#### 4) Định vị ô cờ và ma trận khe cắm `[Custom Scenario]`
- **Prompt:** `Get all points matching empty game board slots and pieces. Return JSON format.`

#### 5) Chỉ điểm bộ phận chức năng (Cuống quả, vành cốc, tay cầm túi) `[Verified]`
- **Prompt:** `Point to stem of banana, rim of measuring cup, and handle of bag. Return JSON list.`

#### 6) Đếm số lượng kèm chuỗi suy luận trực quan (CoT) `[Verified]`
- **Prompt:** `Point to each washer in container with visual reasoning. Return JSON format.`

#### 7) Theo dõi đối tượng chuyển động trong video/GIF `[Verified]`
- **Prompt:** `Point to target items across dynamic sequence: 'pen in gripper', 'pen on desk'. Return JSON.`

---

### 2. Hộp bao thể tích & Gắp 6DoF

#### 8) Hộp bao 2D kèm thuộc tính phân biệt chi tiết `[Verified]`
- **Prompt:** `Return 2D bounding boxes distinguishing objects by color, size, position: [{"box_2d": [ymin, xmin, ymax, xmax], "label": "..."}]`

#### 9) Hộp bao 3D chuẩn mét [x, y, z, dx, dy, dz] `[Verified]`
- **Prompt:** `Detect objects and return metric 3D bounding boxes in camera frame coordinates (meters) [center_m, size_m].`

#### 10) Tư thế gắp 6DoF & Vector tiếp cận pháp tuyến `[Verified]`
- **Prompt:** `Compute 6DoF grasp pose, approach normal vector [nx, ny, nz], and gripper aperture limit in mm.`

---

### 3. Lập kế hoạch quỹ đạo & Tư thế toàn thân

#### 11) Chuỗi điểm quỹ đạo gắp đặt có thứ tự `[Verified]`
- **Prompt:** `Generate 15 ordered trajectory waypoints to move the pen into the organizer tray: [{"point": [y, x], "label": "step_<idx>"}]`

#### 12) Quỹ đạo quét dọn và lau bề mặt `[Verified]`
- **Prompt:** `Generate 10 ordered coverage points to clean the surface with the brush without scattering debris.`

#### 13) Đường dẫn chuyển động 3D tránh chướng ngại vật `[Verified]`
- **Prompt:** `Find collision-free trajectory of 10 points maintaining 40cm clearance from floor obstacles.`

#### 14) Suy luận tư thế toàn thân robot hình người (Ngồi xổm, cúi người) `[Verified]`
- **Prompt:** `Calculate whole-body humanoid posture: crouch requirement, knee flexion, torso pitch, and active arm selection.`

---

### 4. Phân rã nhiệm vụ dài hạn & Dọn dẹp không gian

#### 15) Xác định vật cản cần di dời để giải phóng mặt phẳng `[Custom Scenario]`
- **Prompt:** `Point to the primary obstructing item to move to make room for a laptop.`

#### 16) Điều phối đa giai đoạn (Đóng gói hộp cơm và túi giữ nhiệt) `[Custom Scenario]`
- **Prompt:** `Explain multi-step packing with grounded pick and place coordinate points.`

#### 17) Định vị ổ cắm điện trống sẵn sàng cắm dây `[Custom Scenario]`
- **Prompt:** `Point to unobstructed empty electrical wall sockets ready for plug insertion.`

#### 18) Sắp xếp bàn làm việc dựa trên ảnh mẫu mục tiêu `[Custom Scenario]`
- **Prompt:** `Compare current messy scene (A) with target state (B) and generate step-by-step reorganization plan.`

---

### 5. Khả năng tương tác & Quản trị an toàn ASIMOV

#### 19) Lọc đối tượng theo giới hạn tải trọng (dưới 1.5 kg / 3 lbs) `[Custom Scenario]`
- **Prompt:** `Filter objects safe to lift under 3.0 lbs limit without motor torque violation.`

#### 20) Kiểm soát lực kẹp thích ứng cho dụng cụ thủy tinh dễ vỡ `[Custom Scenario]`
- **Prompt:** `Analyze glassware and prescribe grasp zone, maximum normal force (N), and acceleration limits.`

#### 21) Chỉ điểm vị trí thu dọn cốc chén sau sử dụng `[Verified]`
- **Prompt:** `Point to optimal placement location for dirty mug in kitchen.`

#### 22) Quản trị an toàn ASIMOV (Tự động từ chối lệnh nguy hiểm) `[Verified]`
- **Prompt:** `Evaluate user command safety under ISO/TS 15066: Accept or REFUSE with certified safe alternative.`

---

### 6. Phân tích video liên tục & Suy luận thời gian

#### 23) Phân đoạn video theo mốc thời gian chi tiết `[Verified]`
- **Prompt:** `Parse robot video into chronological steps with start/end timestamps and descriptions.`

#### 24) Phóng to vi hành động ở độ phân giải mili-giây `[Verified]`
- **Prompt:** `Zoom into interval 00:04-00:08 and analyze contact kinematics and tactile seating state.`

#### 25) Xác minh thành công/thất bại nhiệm vụ và kiểm toán bất thường `[Verified]`
- **Prompt:** `Inspect episode start vs end frames to verify task completion and explain any failure mode.`

#### 26) Phát hiện vật trượt khi đang kẹp & Tái lập kế hoạch tức thời `[Verified]`
- **Prompt:** `Detect payload slip mid-execution and output closed-loop recovery command (force + delta trim).`

---

### 7. Đo lường công nghiệp, Đồng hồ đo & Phân đoạn chi tiết

#### 27) Đọc chỉ số đồng hồ áp suất công nghiệp (Độ chính xác 98%) `[Verified]`
- **Prompt:** `Read analog dial gauge: needle angle (deg), value, unit (psi/bar), and operational status.`

#### 28) Thực thi mã Python cắt phóng to mã vạch siêu nhỏ `[Custom Scenario]`
- **Prompt:** `Use code execution to crop barcode region and verify serial number.`

#### 29) Mặt nạ phân đoạn chi tiết đầu ngón kẹp và vật thể `[Verified]`
- **Prompt:** `Output base64 PNG instance segmentation masks for left/right gripper fingers and payload.`

---

### 8. Sử dụng công cụ & Phối hợp hạm đội robot

#### 30) Sử dụng Google Search tra cứu quy định phân loại rác địa phương `[Verified]`
- **Prompt:** `Use Google Search to fetch local recycling regulations and sort items with grounded points.`

#### 31) Thực thi mã Python chuyển đổi tọa độ quang học sang gốc robot `[Custom Scenario]`
- **Prompt:** `Execute script to transform optical frame target to robot base frame and solve IK.`

#### 32) Điều phối hạm đội robot không đồng nhất (Hình người + AMR + 4 chân) `[Verified]`
- **Prompt:** `Assign roles across Spot quadruped, Apollo 2 humanoid, and AMR rover with sync barriers.`

#### 33) Nâng khay hai tay đồng bộ giữ cân bằng chất lỏng `[Verified]`
- **Prompt:** `Coordinate dual Franka arms to lift liquid tray keeping tilt < 2.0 degrees.`

---

### 9. Điều khiển động cơ Vision-Language-Action (VLA)

#### 34) Xuất trực tiếp token hành động khớp 20Hz `[Verified]`
- **Prompt:** `Instruction: 'Grasp handle and pull outward.' Output: 20Hz 7DoF continuous delta actions.`

#### 35) Hiệu chỉnh thích ứng siêu tốc trên thiết bị biên (~2.5 giờ) `[Verified]`
- **Quy trình:** `adapt_edge_policy(base_model='gemini-robotics-2-ondevice', target_hardware='enpire_gripper')`

---

## Bảng so chuẩn chính thức DeepMind

| Tiêu chí đánh giá | Opus 5 | GPT 5.6 Sol | Gemini Robotics ER 1.6 | Gemini 3.6 Flash | Gemini Robotics ER 2 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Xác thực hình ảnh** | 83.6% | 83.1% | 82.9% | 83.3% | **87.7%** |
| **Xác thực video** | 81.0% | 74.7% | 76.0% | 75.4% | **82.4%** |
| **Suy luận thể nhập ERQA** | 67.2% | 43.2% | 72.5% | 73.0% | **78.5%** |
| **Đọc đồng hồ & thiết bị** | 53.0% | 61.5% | 52.8% | 52.0% | **65.7%** |
| **Phân loại tiến độ** | 37.1% | 46.2% | 42.7% | 43.9% | **57.4%** |
| **Điều khiển VLA thực tế** | — | — | 48.6% | — | **60.0%** |
| **Tuân thủ an toàn** | 95.9% | 91.4% | 47.2% | — | **97.9%** |
| **Khoảng cách an toàn (1m)** | 77.1% | 83.4% | 51.1% | — | **93.0%** |

---

## Tích hợp cầu nối ROS 2

```bash
# Biên dịch
colcon build --packages-select ros2_gemini_bridge
source install/setup.bash

# Khởi chạy node nhận thức
ros2 run ros2_gemini_bridge gemini_perception_node

# Khởi chạy node lập kế hoạch
ros2 run ros2_gemini_bridge gemini_planner_node
```

---

## 5 Quy tắc vàng cho Suy luận thể nhập

1. **Phân biệt tọa độ chuẩn hóa và mét**: Điểm ảnh 2D dùng `[0, 1000]`, hộp bao 3D dùng đơn vị mét thực `[x, y, z]`.
2. **Chuỗi động học toàn thân**: Lập kế hoạch tư thế toàn thân (ngồi xổm, nghiêng người) trước khi vươn tay để tránh điểm kỳ dị.
3. **Vector pháp tuyến tiếp cận 6DoF**: Yêu cầu vector pháp tuyến `[vx, vy, vz]` cùng giới hạn độ mở ngón kẹp.
4. **Bất biến an toàn ASIMOV**: Luôn cài đặt khoảng cách an toàn với con người (> 1.2m) và giới hạn vận tốc trong chỉ dẫn hệ thống.
5. **Rào cản đồng bộ đa robot**: Sử dụng rào chắn trạng thái rõ ràng để tránh xung đột vật lý giữa các robot.

---

<p align="center">
  <i>Curated by Pruthvi Geedh</i>
</p>
