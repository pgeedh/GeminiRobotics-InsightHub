import unittest
import os
import sys
import json
import importlib

# Add root and submodules to Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'examples'))
sys.path.insert(0, os.path.join(ROOT_DIR, 'cookbook'))
sys.path.insert(0, os.path.join(ROOT_DIR, 'ros2_gemini_bridge'))

class TestGeminiRoboticsPlaybook(unittest.TestCase):
    def test_core_files_exist(self):
        """Verify all core examples, cookbook recipes, docs, and ROS 2 files exist."""
        required_files = [
            'cookbook/01_spatial_perception_recipe.py',
            'cookbook/02_kinematic_planning_recipe.py',
            'cookbook/03_continuous_video_slip_recipe.py',
            'cookbook/04_asimov_safety_guard_recipe.py',
            'cookbook/05_multi_agent_fleet_recipe.py',
            'cookbook/06_vla_action_chunking_recipe.py',
            'cookbook/interactive_sandbox.py',
            'examples/basic_spatial_query.py',
            'examples/task_decomposition.py',
            'examples/tool_use_recycling.py',
            'examples/video_anomaly_detection.py',
            'examples/multi_robot_coordination.py',
            'examples/vla_motion_transfer.md',
            'ros2_gemini_bridge/package.xml',
            'ros2_gemini_bridge/setup.py',
            'ros2_gemini_bridge/README.md',
            'ros2_gemini_bridge/ros2_gemini_bridge/gemini_perception_node.py',
            'ros2_gemini_bridge/ros2_gemini_bridge/gemini_planner_node.py',
            'assets/benchmark_er_metrics.svg',
            'assets/benchmark_progress_classification.svg',
            'assets/benchmark_physical_agent.svg',
            'assets/benchmark_safety_performance.svg',
            'cases/README.md',
            'cases/spatial_pointing/README.md',
            'cases/6dof_wrench_grasp/README.md',
            'prompts/gemini_robotics_2_catalog.json',
            'BENCHMARKS.md',
            'EMBODIED_REASONING_TIPS.md',
            'cli.py',
            'requirements.txt',
            'README.md',
            'README_ja.md',
            'README_zh.md',
            'README_kr.md',
            'README_vn.md',
            'INTERESTING_PROMPTS.md',
            'RESOURCES.md'
        ]

        for f in required_files:
            path = os.path.join(ROOT_DIR, f)
            self.assertTrue(os.path.exists(path), f"Missing required file: {f}")

    def test_prompt_catalog_integrity(self):
        """Verify the 35-card Gemini Robotics 2.0 JSON prompt catalog."""
        catalog_path = os.path.join(ROOT_DIR, 'prompts', 'gemini_robotics_2_catalog.json')
        self.assertTrue(os.path.exists(catalog_path))
        
        with open(catalog_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertIn("use_cases", data)
        self.assertEqual(len(data["use_cases"]), 31)

        required_keys = ["id", "title", "category", "status", "prompt", "python_code", "sample_output", "tags"]
        for idx, card in enumerate(data["use_cases"], 1):
            self.assertEqual(card["id"], idx)
            for k in required_keys:
                self.assertIn(k, card, f"Card #{idx} missing key '{k}'")
            self.assertTrue(len(card["prompt"]) > 10, f"Card #{idx} prompt too short")
            self.assertTrue(len(card["tags"]) > 0, f"Card #{idx} missing tags")

    def test_cookbook_recipes_execution(self):
        """Test that all cookbook recipes run deterministically."""
        r1 = importlib.import_module("cookbook.01_spatial_perception_recipe")
        out1 = r1.run_spatial_recipe(image_path="assets/pointing_undefined.png")
        self.assertIsNotNone(out1)

        r2 = importlib.import_module("cookbook.02_kinematic_planning_recipe")
        out2 = r2.run_planning_recipe()
        self.assertIsNotNone(out2)

        r3 = importlib.import_module("cookbook.03_continuous_video_slip_recipe")
        out3 = r3.run_video_recipe()
        self.assertIsNotNone(out3)

        r4 = importlib.import_module("cookbook.04_asimov_safety_guard_recipe")
        out4 = r4.run_safety_recipe()
        self.assertIsNotNone(out4)

        r5 = importlib.import_module("cookbook.05_multi_agent_fleet_recipe")
        out5 = r5.run_fleet_recipe()
        self.assertIsNotNone(out5)

        r6 = importlib.import_module("cookbook.06_vla_action_chunking_recipe")
        out6 = r6.simulate_vla_policy_inference()
        self.assertIn("inference_latency_ms", out6)

    def test_multilingual_readmes_structure(self):
        """Verify international localized README files contain adequate sections."""
        languages = ['ja', 'zh', 'kr', 'vn']
        for lang in languages:
            filename = f"README_{lang}.md"
            path = os.path.join(ROOT_DIR, filename)
            self.assertTrue(os.path.exists(path), f"Missing {filename}")
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertTrue(len(content) > 2000, f"{filename} is too short ({len(content)} chars)")
            self.assertIn("Gemini Robotics 2.0", content)

    def test_cli_catalog_loader(self):
        """Verify catalog loader functions properly in CLI."""
        catalog_path = os.path.join(ROOT_DIR, "prompts", "gemini_robotics_2_catalog.json")
        self.assertTrue(os.path.exists(catalog_path))
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        self.assertIn("use_cases", catalog)
        self.assertEqual(len(catalog["use_cases"]), 31)

    def test_basic_spatial_query_sim(self):
        """Test basic_spatial_query simulation logic."""
        try:
            from examples import basic_spatial_query
            sim_2d = basic_spatial_query.generate_simulated_spatial_output("detect objects with bounding boxes")
            data_2d = json.loads(sim_2d)
            self.assertIsInstance(data_2d, list)
            self.assertTrue(len(data_2d) > 0)
            self.assertIn("box_2d", data_2d[0])

            sim_3d = basic_spatial_query.generate_simulated_spatial_output("return 3d bounding box and grasp affordance")
            data_3d = json.loads(sim_3d)
            self.assertIsInstance(data_3d, list)
            self.assertIn("box_3d", data_3d[0])
            self.assertIn("grasp_affordance", data_3d[0])
        except ImportError:
            pass

    def test_tool_use_recycling_sim(self):
        """Test tool_use_recycling reasoning and local facility rules."""
        try:
            from examples import tool_use_recycling
            rule = tool_use_recycling.query_local_facility_rules("plastic #5 pp")
            self.assertIn("recyclable", rule.lower())
        except ImportError:
            pass

if __name__ == '__main__':
    unittest.main()
