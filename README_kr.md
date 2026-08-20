# Awesome Gemini Robotics 2.0 (한국어판)

[![Maintained By: Pruthvi Geedh](https://img.shields.io/badge/Maintained%20By-Pruthvi%20Geedh-4285F4?style=flat-square&logo=github)](https://github.com/pgeedh)
[![Model: Gemini Robotics ER 2 & VLA 2.0](https://img.shields.io/badge/Model-Gemini%20Robotics%20ER%202%20%7C%20VLA%202.0-blue?style=flat-square)](https://aistudio.google.com/)
[![ROS 2: Humble / Iron / Jazzy](https://img.shields.io/badge/ROS%202-Humble%20%7C%20Iron%20%7C%20Jazzy-orange?style=flat-square&logo=ros)](./ros2_gemini_bridge)
[![Benchmarks: Official DeepMind ER 2](https://img.shields.io/badge/Benchmarks-Official%20DeepMind%20ER%202-green?style=flat-square)](./BENCHMARKS.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](./LICENSE)

**언어 선택:** [English](./README.md) | [日本語 (Japanese)](./README_ja.md) | [中文 (Chinese)](./README_zh.md) | **한국어 (Korean)** | [Tiếng Việt (Vietnamese)](./README_vn.md)

---

### 개요

**Google DeepMind Gemini Robotics 2.0**, **Gemini Robotics ER 2(체화된 추론·Embodied Reasoning)**, 및 **Gemini Robotics 2(Vision-Language-Action / VLA)** 모델을 위한 프롬프트 패턴, JSON 스키마, Python SDK 스니펫, ROS 2 실행 노드 레퍼런스입니다.

Gemini Robotics 2.0 은 **계층적 이중 모델 아키텍처**로 동작합니다:
1. **플래너 / 체화된 추론 (Gemini Robotics ER 2):** 공간 인식, 3D 미터법 바운딩 박스, 장기 과업 계획, 실시간 비디오 슬립 감지 및 도구 호출.
2. **모터 제어 / 실행 정책 (Gemini Robotics 2 VLA & On-Device 2):** 휴머노이드, 협동 로봇, 모바일 플랫폼을 위해 20Hz 이상 고주파로 관절 궤적을 직접 생성하여 딜레이 없는 제어를 수행.

---

## 목차

- [플레이북 활용 가이드](#플레이북-활용-가이드)
- [쿡북 실전 테스트 트랙 (`cookbook/`)](#쿡북-실전-테스트-트랙-cookbook)
- [빠른 시작 (`google-genai` SDK v1.x)](#빠른-시작)
- [핵심 활용 사례 및 프롬프트 갤러리 (35개 카드)](#핵심-활용-사례-및-프롬프트-갤러리-35개-카드)
  - [1. 공간 인식 및 2D/3D 포인팅](#1-공간-인식-및-2d3d-포인팅)
  - [2. 바운딩 박스 및 6DoF 파지](#2-바운딩-박스-및-6dof-파지)
  - [3. 궤적 생성 및 전신 모션 계획](#3-궤적-생성-및-전신-모션-계획)
  - [4. 장기 과업 분해 및 환경 정리](#4-장기-과업-분해-및-환경-정리)
  - [5. 어포던스 및 ASIMOV 안전 거버넌스](#5-어포던스-및-asimov-안전-거버넌스)
  - [6. 연속 비디오 이해 및 시계열 추론](#6-연속-비디오-이해-및-시계열-추론)
  - [7. 산업 계측, 게이지 인식 및 고밀도 세그멘테이션](#7-산업-계측-게이지-인식-및-고밀도-세그멘테이션)
  - [8. 도구 활용 및 다중 로봇 협업](#8-도구-활용-및-다중-로봇-협업)
  - [9. Vision-Language-Action (VLA) 모터 제어](#9-vision-language-action-vla-모터-제어)
- [공식 DeepMind 벤치마크 (ER 2 vs SOTA)](#공식-deepmind-벤치마크)
- [ROS 2 브리지 연동](#ros-2-브리지-연동)
- [체화된 추론을 위한 5대 황금 법칙](#체화된-추론을-위한-5대-황금-법칙)
- [기여 안내](#기여-안내)

---

## 플레이북 활용 가이드

1. **대화형 터미널 대시보드 (`python cli.py`):** 35개 프롬프트 카드 및 6대 쿡북 레시피를 실시간으로 테스트.
2. **모듈식 쿡북 레시피 (`cookbook/`):** 공간 인식, 전신 자세, 비디오 슬립 감지, 안전 정책, 다중 로봇 협업 독립 실행.
3. **커스텀 테스트 샌드박스 (`python cookbook/interactive_sandbox.py`):** 임의의 이미지 및 커스텀 프롬프트를 즉시 평가.
4. **ROS 2 브리지 연동 (`ros2_gemini_bridge`):** 로봇 카메라 토픽을 직접 Gemini 인식 및 계획 노드에 연결.

---

## 쿡북 실전 테스트 트랙 (`cookbook/`)

| 트랙 / 레시피 | 레시피 파일 | 설명 | 빠른 실행 명령어 |
| :--- | :--- | :--- | :--- |
| **1. 공간 인식 & 6DoF 파지** | [`cookbook/01_spatial_perception_recipe.py`](./cookbook/01_spatial_perception_recipe.py) | 2D 포인팅, 3D 미터법 볼륨, 접근 법선 벡터. | `python cookbook/01_spatial_perception_recipe.py` |
| **2. 기구학적 과업 계획** | [`cookbook/02_kinematic_planning_recipe.py`](./cookbook/02_kinematic_planning_recipe.py) | Pydantic 전신 자세 선택 및 무충돌 순서 생성. | `python cookbook/02_kinematic_planning_recipe.py` |
| **3. 비디오 슬립 & 이상 감지** | [`cookbook/03_continuous_video_slip_recipe.py`](./cookbook/03_continuous_video_slip_recipe.py) | 연속 프레임 접촉 분석 및 폐루프 보정. | `python cookbook/03_continuous_video_slip_recipe.py` |
| **4. ASIMOV 안전 거버넌스** | [`cookbook/04_asimov_safety_guard_recipe.py`](./cookbook/04_asimov_safety_guard_recipe.py) | ISO/TS 15066 안전 기준 강제 및 자율 거부. | `python cookbook/04_asimov_safety_guard_recipe.py` |
| **5. 다중 로봇 협업** | [`cookbook/05_multi_agent_fleet_recipe.py`](./cookbook/05_multi_agent_fleet_recipe.py) | 명시적 대기 배리어를 통한 이종 로봇 스케줄링. | `python cookbook/05_multi_agent_fleet_recipe.py` |
| **6. 20Hz VLA 동작 청킹** | [`cookbook/06_vla_action_chunking_recipe.py`](./cookbook/06_vla_action_chunking_recipe.py) | 20Hz 연속 7DoF 모터 동작 청크 생성. | `python cookbook/06_vla_action_chunking_recipe.py` |
| **대화형 샌드박스** | [`cookbook/interactive_sandbox.py`](./cookbook/interactive_sandbox.py) | 임의 이미지 및 프롬프트 테스트 하네스. | `python cookbook/interactive_sandbox.py` |

---

## 빠른 시작

```python
from google import genai
from google.genai import types

client = genai.Client()
MODEL_ID = "gemini-robotics-er-2"

prompt = """
이미지 내의 최대 10개 객체를 포인팅하세요.
JSON 형식으로 반환: [{"point": [y, x], "label": "<이름>"}]
좌표는 0-1000으로 정규화하세요.
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

## 핵심 활용 사례 및 프롬프트 갤러리 (35개 카드)

### 1. 공간 인식 및 2D/3D 포인팅

#### 1) 미정의 객체 오픈 보캐블러리 감지 `[Verified]`
- **프롬프트:** `Point to no more than 10 items in the image. Return JSON: [{"point": [y, x], "label": "<object_name>"}] normalized 0-1000.`

#### 2) 지정 대상 객체 필터링 추출 `[Verified]`
- **프롬프트:** `Get all points matching: bread, starfruit, banana. Return JSON: [{"point": [y, x], "label": "<target>"}]`

#### 3) 추상적 의미 범주 지정 (과일, 위험물 등) `[Verified]`
- **프롬프트:** `Get all points for any visible fruit under occlusion. Return JSON format.`

#### 4) 보드게임 및 그리드 슬롯 위치 감지 `[Verified]`
- **프롬프트:** `Get all points matching empty game board slots and pieces. Return JSON format.`

#### 5) 객체 세부 기능 부위 및 파지점 지정 `[Verified]`
- **프롬프트:** `Point to stem of banana, rim of measuring cup, and handle of bag. Return JSON list.`

#### 6) 시각적 연쇄 추론(CoT)을 통한 수량 계수 `[Verified]`
- **프롬프트:** `Point to each washer in container with reasoning. Return JSON format.`

#### 7) 연속 비디오/GIF 내 동적 객체 추적 `[Verified]`
- **프롬프트:** `Point to target items across dynamic sequence: 'pen in gripper', 'pen on desk'. Return JSON.`

---

### 2. 바운딩 박스 및 6DoF 파지

#### 8) 고유 속성 구분을 포함한 2D 검출 박스 `[Verified]`
- **프롬프트:** `Return 2D bounding boxes distinguishing objects by color, size, position: [{"box_2d": [ymin, xmin, ymax, xmax], "label": "..."}]`

#### 9) 3D 미터법 볼륨 박스 [x, y, z, dx, dy, dz] `[Verified]`
- **프롬프트:** `Detect objects and return metric 3D bounding boxes in camera frame coordinates (meters) [center_m, size_m].`

#### 10) 6DoF 파지 포즈 및 진입 법선 벡터 산출 `[Verified]`
- **프롬프트:** `Compute 6DoF grasp pose, approach normal vector [nx, ny, nz], and gripper aperture limit in mm.`

---

### 3. 궤적 생성 및 전신 모션 계획

#### 11) 픽앤플레이스 순차 웨이포인트 궤적 `[Verified]`
- **프롬프트:** `Generate 15 ordered trajectory waypoints to move the pen into the organizer tray: [{"point": [y, x], "label": "step_<idx>"}]`

#### 12) 표면 청소 및 와이핑 경로 커버리지 `[Verified]`
- **프롬프트:** `Generate 10 ordered coverage points to clean the surface with the brush without scattering debris.`

#### 13) 3D 장애물 회피 스플라인 네비게이션 `[Verified]`
- **프롬프트:** `Find collision-free trajectory of 10 points maintaining 40cm clearance from floor obstacles.`

#### 14) 휴머노이드 전신 자세 및 무게중심 추론 (쪼그려 앉기) `[Verified]`
- **프롬프트:** `Calculate whole-body humanoid posture: crouch requirement, knee flexion, torso pitch, and active arm selection.`

---

### 4. 장기 과업 분해 및 환경 정리

#### 15) 공간 확보를 위한 방해물 식별 `[Verified]`
- **프롬프트:** `Point to the primary obstructing item to move to make room for a laptop.`

#### 16) 다단계 과업 분해 (도시락통 및 가방 패킹) `[Verified]`
- **프롬프트:** `Explain multi-step packing with grounded pick and place coordinate points.`

#### 17) 빈 콘센트 및 케이블 삽입 포트 검출 `[Verified]`
- **프롬프트:** `Point to unobstructed empty electrical wall sockets ready for plug insertion.`

#### 18) 목표 참조 사진 기반 작업대 재정리 `[Verified]`
- **프롬프트:** `Compare current messy scene (A) with target state (B) and generate step-by-step reorganization plan.`

---

### 5. 어포던스 및 ASIMOV 안전 거버넌스

#### 19) 페이로드 중량 제한 기반 객체 선별 (3파운드 한계) `[Verified]`
- **프롬프트:** `Filter objects safe to lift under 3.0 lbs limit without motor torque violation.`

#### 20) 파손 위험 유리 기구 순응 파지력 제어 `[Verified]`
- **프롬프트:** `Analyze glassware and prescribe grasp zone, maximum normal force (N), and acceleration limits.`

#### 21) 과업 완료 후 컵 정리 배치점 지정 `[Verified]`
- **프롬프트:** `Point to optimal placement location for dirty mug in kitchen.`

#### 22) ASIMOV 안전 거버넌스 (위험 물리 동작 자율 거부) `[Verified]`
- **프롬프트:** `Evaluate user command safety under ISO/TS 15066: Accept or REFUSE with certified safe alternative.`

---

### 6. 연속 비디오 이해 및 시계열 추론

#### 23) 작업 비디오 타임스탬프 구간 분해 `[Verified]`
- **프롬프트:** `Parse robot video into chronological steps with start/end timestamps and descriptions.`

#### 24) 서브초 단위 미세 동작 확대 분석 `[Verified]`
- **프롬프트:** `Zoom into interval 00:04-00:08 and analyze contact kinematics and tactile seating state.`

#### 25) 물리 과업 성공/실패 판정 및 이상 감사 `[Verified]`
- **프롬프트:** `Inspect episode start vs end frames to verify task completion and explain any failure mode.`

#### 26) 파지 미끄러짐 감지 및 실시간 재계획 `[Verified]`
- **프롬프트:** `Detect payload slip mid-execution and output closed-loop recovery command (force + delta trim).`

---

### 7. 산업 계측, 게이지 인식 및 고밀도 세그멘테이션

#### 27) 아날로그 압력 게이지 초정밀 판독 (98% 정확도) `[Verified]`
- **프롬프트:** `Read analog dial gauge: needle angle (deg), value, unit (psi/bar), and operational status.`

#### 28) Python 코드 실행 기반 바코드 영역 국소 확대 `[Verified]`
- **프롬프트:** `Use code execution to crop barcode region and verify serial number.`

#### 29) 그리퍼 핑거 및 대상 객체 고밀도 세그멘테이션 마스크 `[Verified]`
- **프롬프트:** `Output base64 PNG instance segmentation masks for left/right gripper fingers and payload.`

---

### 8. 도구 활용 및 다중 로봇 협업

#### 30) Google 검색 도구 기반 지역 분리수거 규칙 적용 `[Verified]`
- **프롬프트:** `Use Google Search to fetch local recycling regulations and sort items with grounded points.`

#### 31) Python 코드 실행 카메라-베이스 좌표계 변환 `[Verified]`
- **프롬프트:** `Execute script to transform optical frame target to robot base frame and solve IK.`

#### 32) 이종 로봇(휴머노이드+AMR+4족보행) 협동 스케줄링 `[Verified]`
- **프롬프트:** `Assign roles across Spot quadruped, Apollo 2 humanoid, and AMR rover with sync barriers.`

#### 33) 양팔 협업 트레이 수평 리프팅 제어 `[Verified]`
- **프롬프트:** `Coordinate dual Franka arms to lift liquid tray keeping tilt < 2.0 degrees.`

---

### 9. Vision-Language-Action (VLA) 모터 제어

#### 34) 20Hz VLA 관절 모터 동작 토큰 직접 생성 `[Verified]`
- **프롬프트:** `Instruction: 'Grasp handle and pull outward.' Output: 20Hz 7DoF continuous delta actions.`

#### 35) 엣지 디바이스 초고속 정책 적응 (~2.5시간 교정) `[Verified]`
- **파이프라인:** `adapt_edge_policy(base_model='gemini-robotics-2-ondevice', target_hardware='enpire_gripper')`

---

## 공식 DeepMind 벤치마크

| 평가 항목 | Opus 5 | GPT 5.6 Sol | Gemini Robotics ER 1.6 | Gemini 3.6 Flash | Gemini Robotics ER 2 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **이미지 성공 판정** | 83.6% | 83.1% | 82.9% | 83.3% | **87.7%** |
| **비디오 성공 판정** | 81.0% | 74.7% | 76.0% | 75.4% | **82.4%** |
| **ERQA 체화 추론** | 67.2% | 43.2% | 72.5% | 73.0% | **78.5%** |
| **산업 계측기 판독** | 53.0% | 61.5% | 52.8% | 52.0% | **65.7%** |
| **진행 단계 분류** | 37.1% | 46.2% | 42.7% | 43.9% | **57.4%** |
| **실제 VLA 제어 성공률** | — | — | 48.6% | — | **60.0%** |
| **안전 지시 준수율** | 95.9% | 91.4% | 47.2% | — | **97.9%** |
| **인간 근접 안전 회피 (1m)** | 77.1% | 83.4% | 51.1% | — | **93.0%** |

---

## ROS 2 브리지 연동

```bash
# 빌드
colcon build --packages-select ros2_gemini_bridge
source install/setup.bash

# 인식 노드 실행
ros2 run ros2_gemini_bridge gemini_perception_node

# 플래너 노드 실행
ros2 run ros2_gemini_bridge gemini_planner_node
```

---

## 체화된 추론을 위한 5대 황금 법칙

1. **정규화 좌표 vs 미터법 단위**: 2D 이미지 좌표는 `[0, 1000]`, 3D 바운딩 박스는 실제 미터 `[x, y, z]`를 명시합니다.
2. **기구학적 연쇄(Kinematic Chain) 고려**: 특이점 방지를 위해 말단 장치 도달 전 전신 자세(스쿼트, 상체 숙임)를 먼저 결정합니다.
3. **6DoF 진입 법선 벡터**: 파지점뿐만 아니라 법선 벡터 `[vx, vy, vz]` 및 그리퍼 개구 폭을 함께 요청합니다.
4. **ASIMOV 안전 불변식**: 사람과의 안전 반경(< 1.2m) 침범 시 즉시 감속/거부하도록 시스템 지침에 설정합니다.
5. **다중 에이전트 동기화 배리어**: 분산 협업 시 물리적 충돌을 방지하기 위해 명시적 대기 배리어를 설정합니다.

## 기여 안내

커뮤니티 기여를 적극 환영합니다. 새로운 프롬프트 카드, 벤치마크 평가, 하드웨어 어댑터 제안은 [`CONTRIBUTING.md`](./CONTRIBUTING.md)를 참고해 주세요.

---

## 라이선스 및 이미지 출처

- **텍스트 및 코드**: [MIT 라이선스](./LICENSE) 하에 배포됩니다.
- **이미지 및 시각 데모**: `[Verified]`로 표시된 데모 이미지는 Google DeepMind의 공식 기술 보고서 및 블로그에서 인용되었으며, 교육 및 연구 목적으로만 사용됩니다. 재배포 시 원본 라이선스를 확인하십시오.

---

## 주요 참고 출처

- **Google DeepMind Physical AI**: [Gemini Robotics 2 & Embodied Reasoning](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) — 기술 아키텍처, 전신 휴머노이드 제어 및 양팔 조작.
- **Google Developers Blog**: [Building Physical Agents with Gemini Robotics](https://developers.googleblog.com/en/building-the-next-generation-of-physical-agents-with-gemini-robotics-er-15/) — 공간 그라운딩, 포인팅 및 기구학적 프롬프트 패턴.
- **Google AI for Developers**: [Gemini Robotics API 문서](https://ai.google.dev/gemini-api/docs/robotics-overview) — 공간 토큰, 좌표계 및 API 가이드.
- **연구 논문**: *"Gemini Robotics: Bringing AI into the Physical World"* ([arXiv:2503.20020](https://arxiv.org/abs/2503.20020)).

---

## 감사의 글

본 저장소의 활용 사례와 레시피는 물리적 AI 및 로보틱스 개발자 커뮤니티의 오픈소스 공유를 기반으로 합니다. 모든 기여자 및 연구진에게 깊은 감사를 표합니다:

- [@GoogleDeepMind](https://x.com/GoogleDeepMind)
- [@GeminiApp](https://x.com/GeminiApp)
- Open X-Embodiment 및 ROS 2 로보틱스 커뮤니티

새로운 프롬프트 발견이나 로보틱스 활용 사례가 있다면 언제든지 PR이나 이슈를 통해 공유해 주시기 바랍니다.

---

<p align="center">
  <i>Curated by Pruthvi Geedh</i>
</p>
