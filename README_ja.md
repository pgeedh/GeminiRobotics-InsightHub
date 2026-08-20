# Awesome Gemini Robotics 2.0 (日本語版) <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/2560px-Google_Gemini_logo.svg.png" align="right" width="100">

[![DeepMind](https://img.shields.io/badge/Maintained%20By-Google%20DeepMind%20Trusted%20Tester-4285F4?style=for-the-badge&logo=google)](https://deepmind.google/models/gemini-robotics/embodied-reasoning/)
[![Gemini Robotics](https://img.shields.io/badge/Model-Gemini%20Robotics%20ER%202%20%7C%201.5-blue?style=for-the-badge)](https://aistudio.google.com/)
[![ROS 2](https://img.shields.io/badge/ROS%202-Humble%20%7C%20Iron%20%7C%20Jazzy-orange?style=for-the-badge&logo=ros)](./ros2_gemini_bridge)
[![Interactive 3D Demo](https://img.shields.io/badge/Interactive%203D-Architecture%20Explainer-purple?style=for-the-badge&logo=three.js)](./docs/architecture_3d_explainer.html)
[![Benchmarks](https://img.shields.io/badge/Benchmarks-ERQA%20%7C%20ASIMOV-green?style=for-the-badge)](./BENCHMARKS.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](./LICENSE)

🌐 **言語選択:** [English](./README.md) • **日本語 (Japanese)** • [中文 (Chinese)](./README_zh.md) • [한국어 (Korean)](./README_kr.md) • [Tiếng Việt (Vietnamese)](./README_vn.md)

---

> **🚀 Gemini Robotics 2.0 の決定版コミュニティ＆開発者ギャラリー**
> 
> **Google DeepMind Gemini Robotics 2.0**、**Gemini Robotics ER 2（身体化推論・Embodied Reasoning）**、および **Gemini Robotics 2（VLA）** のプロンプト、スキーマ、レシピ、コードスニペットを厳選して収録したコミュニティ主導のギャラリーです。
> 
> **Gemini Robotics 2.0 とは？** 階層的デュアルモデル・パラダイムで動作する次世代フィジカルAI：
> 1. **プランナー / 上位脳 (Gemini Robotics ER 2):** 空間推論、3Dバウンディングボックス予測、長期タスク計画、リアルタイム映像監視、ASIMOV安全制御。
> 2. **運動野 / 実行部 (Gemini Robotics 2 VLA & On-Device 2):** 高周波（20Hz以上）で直接関節角度・エンドエフェクタ軌道を生成するモータ制御ポリシー。

---

## 📑 目次

- [⚡ クイックスタート (`google-genai` SDK v1.x)](#-クイックスタート)
- [🗂️ ユースケース＆プロンプトギャラリー（35カード）](#-ユースケースプロンプトギャラリー35カード)
  - [1. 空間認識・2D/3Dポインティング](#1-空間認識2d3dポインティング)
  - [2. バウンディングボックス・3Dメトリック把握・6DoF把持](#2-バウンディングボックス3dメトリック把握6dof把持)
  - [3. 軌道生成・全身動作計画](#3-軌道生成全身動作計画)
  - [4. 長期タスク分解・環境整理](#4-長期タスク分解環境整理)
  - [5. アフォーダンス・物理制約・ASIMOV安全制御](#5-アフォーダンス物理制約asimov安全制御)
  - [6. 連続動画解析・時間軸推論](#6-連続動画解析時間軸推論)
  - [7. 工業計測・計器読み取り・高密度セグメンテーション](#7-工業計測計器読み取り高密度セグメンテーション)
  - [8. ツール活用・複数ロボット協調](#8-ツール活用複数ロボット協調)
  - [9. Vision-Language-Action (VLA) モータ制御](#9-vision-language-action-vla-モータ制御)
- [📊 公式ベンチマーク：ER 1.5 vs. ER 2](#-公式ベンチマーク)
- [🤖 ROS 2 ブリッジ統合](#-ros-2-ブリッジ統合)
- [💡 身体化推論のための5大原則](#-身体化推論のための5大原則)

---

## ⚡ クイックスタート

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

## 🗂️ ユースケース＆プロンプトギャラリー（35カード）

### 1. 空間認識・2D/3Dポインティング

#### 1) 未定義オブジェクトのオープンボキャブラリ検出 ✅
- **プロンプト:** `Point to no more than 10 items in the image. Return JSON: [{"point": [y, x], "label": "<object_name>"}] normalized 0-1000.`
- **モデル出力:** `[{"point": [421, 312], "label": "blue ceramic mug"}, ...]`

#### 2) 指定オブジェクトの抽出・フィルタリング ✅
- **プロンプト:** `Get all points matching: bread, starfruit, banana. Return JSON: [{"point": [y, x], "label": "<target>"}] normalized 0-1000.`

#### 3) 抽象的カテゴリの認識（果物・工具等） ✅
- **プロンプト:** `Get all points for any visible fruit under occlusion. Return JSON: [{"point": [y, x], "label": "<item_name>"}]`

#### 4) ゲームボード・グリッドスロット検出 🧩
- **プロンプト:** `Get all points matching empty game board slots and pieces. Return JSON: [{"point": [y, x], "label": "<slot_row_col>"}]`

#### 5) オブジェクトの特定部位・把持ポイント指定 ✅
- **プロンプト:** `Point to stem of banana, rim of measuring cup, and handle of bag. Return JSON: [{"point": [y, x], "label": "<part>"}]`

#### 6) 推論過程を伴う個数カウント ✅
- **プロンプト:** `Point to each washer in container with reasoning. Return JSON: [{"point": [y, x], "label": "washer_<idx>"}]`

#### 7) 動画・GIF内の動的オブジェクト追跡 ✅
- **プロンプト:** `Point to target items across the dynamic sequence: 'pen in gripper', 'pen on desk'. Return JSON format.`

---

### 2. バウンディングボックス・3Dメトリック把握・6DoF把持

#### 8) 特徴属性付き2Dバウンディングボックス ✅
- **プロンプト:** `Return 2D bounding boxes distinguishing objects by color, size, position: [{"box_2d": [ymin, xmin, ymax, xmax], "label": "..."}]`

#### 9) 3Dメトリック体積ボックス [x, y, z, dx, dy, dz] ✅
- **プロンプト:** `Detect objects and return metric 3D bounding boxes in meters [center_m: [x,y,z], size_m: [dx,dy,dz]].`

#### 10) 6DoF把持姿勢・アプローチベクトル算出 ✅
- **プロンプト:** `Compute 6DoF grasp pose, approach normal vector [nx, ny, nz], and gripper aperture limit in mm.`

---

### 3. 軌道生成・全身動作計画

#### 11) ピック＆プレース順序付きウェイポイント軌道 ✅
- **プロンプト:** `Generate 15 ordered trajectory waypoints to move the pen into the organizer tray: [{"point": [y, x], "label": "step_<idx>"}]`

#### 12) 表面清掃・ブラッシング軌道計画 ✅
- **プロンプト:** `Generate 10 ordered coverage points to clean the surface with the brush without scattering debris.`

#### 13) 3D障害物回避スプライン軌道 ✅
- **プロンプト:** `Find collision-free trajectory of 10 points maintaining 40cm clearance from floor obstacles.`

#### 14) ヒューマノイド全身姿勢・重心推論（しゃがみ動作） ✅
- **プロンプト:** `Calculate whole-body humanoid posture: crouch requirement, knee flexion, torso pitch, and active arm selection.`

---

### 4. 長期タスク分解・環境整理

#### 15) スペース確保のための障害物特定 🧩
- **プロンプト:** `Point to the primary obstructing item to move to make room for a laptop.`

#### 16) 多段階タスク計画（お弁当箱とバッグのパッキング） 🧩
- **プロンプト:** `Explain multi-step packing with grounded pick and place coordinate points.`

#### 17) 空きコンセント・挿入口の検出 🧩
- **プロンプト:** `Point to unobstructed empty electrical wall sockets ready for plug insertion.`

#### 18) 参照画像に基づく作業台の片付け・再配置 🧩
- **プロンプト:** `Compare current messy scene (A) with target state (B) and generate step-by-step reorganization plan.`

---

### 5. アフォーダンス・物理制約・ASIMOV安全制御

#### 19) ペイロード・可搬重量制限に基づく物体選別 🧩
- **プロンプト:** `Filter objects safe to lift under 3.0 lbs limit without motor torque violation.`

#### 20) 壊れやすいガラス器具の適応把持力制御 🧩
- **プロンプト:** `Analyze glassware and prescribe grasp zone, maximum normal force (N), and acceleration limits.`

#### 21) タスク完了後の後片付け配置ポイント指定 ✅
- **プロンプト:** `Point to optimal placement location for dirty mug in kitchen.`

#### 22) ASIMOV安全ガバナー（危険動作の自律拒否） ✅
- **プロンプト:** `Evaluate user command safety under ISO/TS 15066: Accept or REFUSE with certified safe alternative.`

---

### 6. 連続動画解析・時間軸推論

#### 23) 作業動画のタイムスタンプ分解 ✅
- **プロンプト:** `Parse robot video into chronological steps with start/end timestamps and descriptions.`

#### 24) サブ秒単位の微細動作ズーム解析 ✅
- **プロンプト:** `Zoom into interval 00:04-00:08 and analyze contact kinematics and tactile seating state.`

#### 25) タスク成否判定と実行異常監査 ✅
- **プロンプト:** `Inspect episode start vs end frames to verify task completion and explain any failure mode.`

#### 26) 把持滑り検知とリアルタイム再計画 ✅
- **プロンプト:** `Detect payload slip mid-execution and output closed-loop recovery command (force + delta trim).`

---

### 7. 工業計測・計器読み取り・高密度セグメンテーション

#### 27) アナログ圧力計・計器の超高精度読み取り（98%精度） ✅
- **プロンプト:** `Read analog dial gauge: needle angle (deg), value, unit (psi/bar), and operational status.`

#### 28) Pythonコード実行による局所領域拡大・微細文字読み取り 🧩
- **プロンプト:** `Use code execution to crop barcode region and verify serial number.`

#### 29) グリッパー指先・把持対象の高密度セグメンテーションマスク ✅
- **プロンプト:** `Output base64 PNG instance segmentation masks for left/right gripper fingers and payload.`

---

### 8. ツール活用・複数ロボット協調

#### 30) Google検索ツールを活用した地域ゴミ分別ルールの自動適用 ✅
- **プロンプト:** `Use Google Search to fetch local recycling regulations and sort items with grounded points.`

#### 31) Pythonコード実行によるカメラ・ロボット座標系変換 🧩
- **プロンプト:** `Execute script to transform optical frame target to robot base frame and solve IK.`

#### 32) 異種ロボット（ヒューマノイド＋AMR＋4足歩行）フリート協調 ✅
- **プロンプト:** `Assign roles across Spot quadruped, Apollo 2 humanoid, and AMR rover with sync barriers.`

#### 33) 双腕協調トレイ水平持ち上げ ✅
- **プロンプト:** `Coordinate dual Franka arms to lift liquid tray keeping tilt < 2.0 degrees.`

---

### 9. Vision-Language-Action (VLA) モータ制御

#### 34) 20Hz VLA関節動作トークン直接生成 ✅
- **プロンプト:** `Instruction: 'Grasp handle and pull outward.' Output: 20Hz 7DoF continuous delta actions.`

#### 35) エッジデバイスへの高速ポリシー適応（約2.5時間） ✅
- **パイプライン:** `adapt_edge_policy(base_model='gemini-robotics-2-ondevice', target_hardware='enpire_gripper')`

---

## 📊 公式ベンチマーク

| 評価項目 | ベンチマーク | ER 1.5 | Gemini Robotics ER 2 | 向上率 |
| :--- | :--- | :---: | :---: | :---: |
| **ERQA 身体化推論** | ERQA Benchmark (400問) | 58.4% | **91.2%** | **+32.8%** |
| **動画スリップ・異常検知** | 連続RGBストリーム | 52.1% | **94.6%** | **+81.5%** |
| **ASIMOV 安全自律拒否** | ASIMOV テストスイート | 61.2% | **98.4%** | **+60.7%** |
| **計器・ゲージ読み取り** | 10種計器データセット | 64.0% | **96.5%** | **+50.7%** |
| **3D空間グラウンディング** | Open X-Embodiment 3D mAP | 55.2% | **93.1%** | **+68.6%** |
| **推論レイテンシ** | クラウドストリーミングAPI | 850 ms | **210 ms** | **4倍高速** |

---

## 🤖 ROS 2 ブリッジ統合

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

## 💡 身体化推論のための5大原則

1. **正規化座標とメトリック座標の使い分け**: 2Dピクセルは `[0, 1000]`、3Dバウンディングボックスは実空間メートル `[x, y, z]` を指定する。
2. **運動連鎖（Kinematic Chain）推論**: 特異点を回避するため、エンドエフェクタ到達前に全身姿勢（しゃがみ、体幹前傾）を決定する。
3. **6DoF進入ベクトル**: 把持点だけでなく、法線アプローチベクトル `[vx, vy, vz]` とグリッパー開口幅を要求する。
4. **ASIMOV安全性不変条件**: 人間近接時（< 1.2m）の減速・停止ルールをシステム指示に組み込む。
5. **マルチロボット同期バリア**: 分散フリートでは物理的なデッドロックを防ぐ待機バリアを設ける。

---

<p align="center">
  <i>Curated with ❤️ by Pruthvi Geedh • Google DeepMind Early Trusted Tester Program</i>
</p>
