# Awesome Gemini Robotics 2.0 (日本語版)

[![Maintained By: Google DeepMind Trusted Tester](https://img.shields.io/badge/Maintained%20By-Google%20DeepMind%20Trusted%20Tester-4285F4?style=flat-square&logo=google)](https://deepmind.google/models/gemini-robotics/embodied-reasoning/)
[![Model: Gemini Robotics ER 2 & VLA 2.0](https://img.shields.io/badge/Model-Gemini%20Robotics%20ER%202%20%7C%20VLA%202.0-blue?style=flat-square)](https://aistudio.google.com/)
[![ROS 2: Humble / Iron / Jazzy](https://img.shields.io/badge/ROS%202-Humble%20%7C%20Iron%20%7C%20Jazzy-orange?style=flat-square&logo=ros)](./ros2_gemini_bridge)
[![Benchmarks: Official DeepMind ER 2](https://img.shields.io/badge/Benchmarks-Official%20DeepMind%20ER%202-green?style=flat-square)](./BENCHMARKS.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](./LICENSE)

**言語選択:** [English](./README.md) | **日本語 (Japanese)** | [中文 (Chinese)](./README_zh.md) | [한국어 (Korean)](./README_kr.md) | [Tiếng Việt (Vietnamese)](./README_vn.md)

---

### 概要

**Google DeepMind Gemini Robotics 2.0**、**Gemini Robotics ER 2（身体化推論・Embodied Reasoning）**、および **Gemini Robotics 2（Vision-Language-Action / VLA）** のプロンプトパターン、JSONスキーマ、Python SDKスニペット、ROS 2ノードを体系的にまとめた開発者向けリファレンスです。

Gemini Robotics 2.0 は**階層的デュアルモデル・アーキテクチャ**を採用しています：
1. **プランナー / 身体化推論 (Gemini Robotics ER 2):** 高度な空間認識、3Dメトリックバウンディングボックス予測、長期タスク計画、動画ベースのリアルタイム滑り監視、ツール呼び出しを担当。
2. **運動制御 / 実行ポリシー (Gemini Robotics 2 VLA & On-Device 2):** 高周波（20Hz以上）で直接関節角度およびCartesian軌道を生成し、停止遅延のない滑らかな動作を実現。

---

## 目次

- [クイックスタート (`google-genai` SDK v1.x)](#クイックスタート)
- [ユースケース＆プロンプトギャラリー（35カード）](#ユースケースプロンプトギャラリー35カード)
  - [1. 空間認識・2D/3Dポインティング](#1-空間認識2d3dポインティング)
  - [2. バウンディングボックス・3Dメトリック把握・6DoF把持](#2-バウンディングボックス3dメトリック把握6dof把持)
  - [3. 軌道生成・全身動作計画](#3-軌道生成全身動作計画)
  - [4. 長期タスク分解・環境整理](#4-長期タスク分解環境整理)
  - [5. アフォーダンス・物理制約・ASIMOV安全制御](#5-アフォーダンス物理制約asimov安全制御)
  - [6. 連続動画解析・時間軸推論](#6-連続動画解析時間軸推論)
  - [7. 工業計測・計器読み取り・高密度セグメンテーション](#7-工業計測計器読み取り高密度セグメンテーション)
  - [8. ツール活用・複数ロボット協調](#8-ツール活用複数ロボット協調)
  - [9. Vision-Language-Action (VLA) モータ制御](#9-vision-language-action-vla-モータ制御)
- [公式DeepMindベンチマーク（ER 2 vs SOTA）](#公式deepmindベンチマーク)
- [ROS 2 ブリッジ統合](#ros-2-ブリッジ統合)
- [身体化推論のための5大原則](#身体化推論のための5大原則)
- [コントリビューション](#コントリビューション)

---

## クイックスタート

```python
from google import genai
from google.genai import types

client = genai.Client()
MODEL_ID = "gemini-robotics-er-2"

prompt = """
画像内の最大10個のオブジェクトをポインティングしてください。
JSON形式で出力してください: [{"point": [y, x], "label": "<名前>"}]
座標は0-1000に正規化してください。
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

## ユースケース＆プロンプトギャラリー（35カード）

### 1. 空間認識・2D/3Dポインティング

#### 1) 未定義オブジェクトのオープンボキャブラリ検出 `[Verified]`
- **プロンプト:** `Point to no more than 10 items in the image. Return JSON: [{"point": [y, x], "label": "<object_name>"}] normalized 0-1000.`
- **モデル出力:** `[{"point": [421, 312], "label": "blue ceramic mug"}, ...]`

#### 2) 指定オブジェクトの抽出・フィルタリング `[Verified]`
- **プロンプト:** `Get all points matching: bread, starfruit, banana. Return JSON: [{"point": [y, x], "label": "<target>"}] normalized 0-1000.`

#### 3) 抽象的カテゴリの認識（果物・工具等） `[Verified]`
- **プロンプト:** `Get all points for any visible fruit under occlusion. Return JSON: [{"point": [y, x], "label": "<item_name>"}]`

#### 4) ゲームボード・グリッドスロット検出 `[Custom Scenario]`
- **プロンプト:** `Get all points matching empty game board slots and pieces. Return JSON: [{"point": [y, x], "label": "<slot_row_col>"}]`

#### 5) オブジェクトの特定部位・把持ポイント指定 `[Verified]`
- **プロンプト:** `Point to stem of banana, rim of measuring cup, and handle of bag. Return JSON: [{"point": [y, x], "label": "<part>"}]`

#### 6) 推論過程を伴う個数カウント `[Verified]`
- **プロンプト:** `Point to each washer in container with reasoning. Return JSON: [{"point": [y, x], "label": "washer_<idx>"}]`

#### 7) 動画・GIF内の動的オブジェクト追跡 `[Verified]`
- **プロンプト:** `Point to target items across the dynamic sequence: 'pen in gripper', 'pen on desk'. Return JSON format.`

---

### 2. バウンディングボックス・3Dメトリック把握・6DoF把持

#### 8) 特徴属性付き2Dバウンディングボックス `[Verified]`
- **プロンプト:** `Return 2D bounding boxes distinguishing objects by color, size, position: [{"box_2d": [ymin, xmin, ymax, xmax], "label": "..."}]`

#### 9) 3Dメトリック体積ボックス [x, y, z, dx, dy, dz] `[Verified]`
- **プロンプト:** `Detect objects and return metric 3D bounding boxes in meters [center_m: [x,y,z], size_m: [dx,dy,dz]].`

#### 10) 6DoF把持姿勢・アプローチベクトル算出 `[Verified]`
- **プロンプト:** `Compute 6DoF grasp pose, approach normal vector [nx, ny, nz], and gripper aperture limit in mm.`

---

### 3. 軌道生成・全身動作計画

#### 11) ピック＆プレース順序付きウェイポイント軌道 `[Verified]`
- **プロンプト:** `Generate 15 ordered trajectory waypoints to move the pen into the organizer tray: [{"point": [y, x], "label": "step_<idx>"}]`

#### 12) 表面清掃・ブラッシング軌道計画 `[Verified]`
- **プロンプト:** `Generate 10 ordered coverage points to clean the surface with the brush without scattering debris.`

#### 13) 3D障害物回避スプライン軌道 `[Verified]`
- **プロンプト:** `Find collision-free trajectory of 10 points maintaining 40cm clearance from floor obstacles.`

#### 14) ヒューマノイド全身姿勢・重心推論（しゃがみ動作） `[Verified]`
- **プロンプト:** `Calculate whole-body humanoid posture: crouch requirement, knee flexion, torso pitch, and active arm selection.`

---

### 4. 長期タスク分解・環境整理

#### 15) スペース確保のための障害物特定 `[Custom Scenario]`
- **プロンプト:** `Point to the primary obstructing item to move to make room for a laptop.`

#### 16) 多段階タスク計画（お弁当箱とバッグのパッキング） `[Custom Scenario]`
- **プロンプト:** `Explain multi-step packing with grounded pick and place coordinate points.`

#### 17) 空きコンセント・挿入口の検出 `[Custom Scenario]`
- **プロンプト:** `Point to unobstructed empty electrical wall sockets ready for plug insertion.`

#### 18) 参照画像に基づく作業台の片付け・再配置 `[Custom Scenario]`
- **プロンプト:** `Compare current messy scene (A) with target state (B) and generate step-by-step reorganization plan.`

---

### 5. アフォーダンス・物理制約・ASIMOV安全制御

#### 19) ペイロード・可搬重量制限に基づく物体選別 `[Custom Scenario]`
- **プロンプト:** `Filter objects safe to lift under 3.0 lbs limit without motor torque violation.`

#### 20) 壊れやすいガラス器具の適応把持力制御 `[Custom Scenario]`
- **プロンプト:** `Analyze glassware and prescribe grasp zone, maximum normal force (N), and acceleration limits.`

#### 21) タスク完了後の後片付け配置ポイント指定 `[Verified]`
- **プロンプト:** `Point to optimal placement location for dirty mug in kitchen.`

#### 22) ASIMOV安全ガバナー（危険動作の自律拒否） `[Verified]`
- **プロンプト:** `Evaluate user command safety under ISO/TS 15066: Accept or REFUSE with certified safe alternative.`

---

### 6. 連続動画解析・時間軸推論

#### 23) 作業動画のタイムスタンプ分解 `[Verified]`
- **プロンプト:** `Parse robot video into chronological steps with start/end timestamps and descriptions.`

#### 24) サブ秒単位の微細動作ズーム解析 `[Verified]`
- **プロンプト:** `Zoom into interval 00:04-00:08 and analyze contact kinematics and tactile seating state.`

#### 25) タスク成否判定と実行異常監査 `[Verified]`
- **プロンプト:** `Inspect episode start vs end frames to verify task completion and explain any failure mode.`

#### 26) 把持滑り検知とリアルタイム再計画 `[Verified]`
- **プロンプト:** `Detect payload slip mid-execution and output closed-loop recovery command (force + delta trim).`

---

### 7. 工業計測・計器読み取り・高密度セグメンテーション

#### 27) アナログ圧力計・計器の超高精度読み取り（98%精度） `[Verified]`
- **プロンプト:** `Read analog dial gauge: needle angle (deg), value, unit (psi/bar), and operational status.`

#### 28) Pythonコード実行による局所領域拡大・微細文字読み取り `[Custom Scenario]`
- **プロンプト:** `Use code execution to crop barcode region and verify serial number.`

#### 29) グリッパー指先・把持対象の高密度セグメンテーションマスク `[Verified]`
- **プロンプト:** `Output base64 PNG instance segmentation masks for left/right gripper fingers and payload.`

---

### 8. ツール活用・複数ロボット協調

#### 30) Google検索ツールを活用した地域ゴミ分別ルールの自動適用 `[Verified]`
- **プロンプト:** `Use Google Search to fetch local recycling regulations and sort items with grounded points.`

#### 31) Pythonコード実行によるカメラ・ロボット座標系変換 `[Custom Scenario]`
- **プロンプト:** `Execute script to transform optical frame target to robot base frame and solve IK.`

#### 32) 異種ロボット（ヒューマノイド＋AMR＋4足歩行）フリート協調 `[Verified]`
- **プロンプト:** `Assign roles across Spot quadruped, Apollo 2 humanoid, and AMR rover with sync barriers.`

#### 33) 双腕協調トレイ水平持ち上げ `[Verified]`
- **プロンプト:** `Coordinate dual Franka arms to lift liquid tray keeping tilt < 2.0 degrees.`

---

### 9. Vision-Language-Action (VLA) モータ制御

#### 34) 20Hz VLA関節動作トークン直接生成 `[Verified]`
- **プロンプト:** `Instruction: 'Grasp handle and pull outward.' Output: 20Hz 7DoF continuous delta actions.`

#### 35) エッジデバイスへの高速ポリシー適応（約2.5時間） `[Verified]`
- **パイプライン:** `adapt_edge_policy(base_model='gemini-robotics-2-ondevice', target_hardware='enpire_gripper')`

---

## 公式DeepMindベンチマーク

| 評価項目 | Opus 5 | GPT 5.6 Sol | Gemini Robotics ER 1.6 | Gemini 3.6 Flash | Gemini Robotics ER 2 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **画像成功判定** | 83.6% | 83.1% | 82.9% | 83.3% | **87.7%** |
| **動画成功判定** | 81.0% | 74.7% | 76.0% | 75.4% | **82.4%** |
| **ERQA 身体化推論** | 67.2% | 43.2% | 72.5% | 73.0% | **78.5%** |
| **計器・ゲージ読み取り** | 53.0% | 61.5% | 52.8% | 52.0% | **65.7%** |
| **タスク進捗分類** | 37.1% | 46.2% | 42.7% | 43.9% | **57.4%** |
| **実機VLA制御成功率** | — | — | 48.6% | — | **60.0%** |
| **安全指示遵守精度** | 95.9% | 91.4% | 47.2% | — | **97.9%** |
| **人近接安全回避 (1m)** | 77.1% | 83.4% | 51.1% | — | **93.0%** |

---

## ROS 2 ブリッジ統合

```bash
# ビルド
colcon build --packages-select ros2_gemini_bridge
source install/setup.bash

# 認識ノード起動
ros2 run ros2_gemini_bridge gemini_perception_node

# 計画ノード起動
ros2 run ros2_gemini_bridge gemini_planner_node
```

---

## 身体化推論のための5大原則

1. **正規化座標とメトリック座標の使い分け**: 2Dピクセルは `[0, 1000]`、3Dバウンディングボックスは実空間メートル `[x, y, z]` を指定する。
2. **運動連鎖（Kinematic Chain）推論**: 特異点を回避するため、エンドエフェクタ到達前に全身姿勢（しゃがみ、体幹前傾）を決定する。
3. **6DoF進入ベクトル**: 把持点だけでなく、法線アプローチベクトル `[vx, vy, vz]` とグリッパー開口幅を要求する。
4. **ASIMOV安全性不変条件**: 人間近接時（< 1.2m）の減速・停止ルールをシステム指示に組み込む。
5. **マルチロボット同期バリア**: 分散フリートでは物理的なデッドロックを防ぐ待機バリアを設ける。

---

<p align="center">
  <i>Curated by Pruthvi Geedh • Google DeepMind Early Trusted Tester Program</i>
</p>
