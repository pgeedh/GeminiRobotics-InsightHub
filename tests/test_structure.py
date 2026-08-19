import unittest
import os
import sys
import json
from PIL import Image

# Add root and submodules to Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'examples'))
sys.path.insert(0, os.path.join(ROOT_DIR, 'ros2_gemini_bridge'))

class TestGeminiRoboticsHub(unittest.TestCase):
    def test_core_files_exist(self):
        """Verify all core examples, docs, and ROS 2 files exist."""
        required_files = [
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
            'docs/architecture_3d_explainer.html',
            'assets/gemini_robotics_architecture.svg',
            'assets/benchmark_comparison.svg',
            'BENCHMARKS.md',
            'EMBODIED_REASONING_TIPS.md',
            'cli.py',
            'requirements.txt',
            'README.md',
            'INTERESTING_PROMPTS.md',
            'RESOURCES.md'
        ]
        for f in required_files:
            path = os.path.join(ROOT_DIR, f)
            self.assertTrue(os.path.exists(path), f"Missing required file: {f}")

    def test_basic_spatial_query_sim(self):
        """Test basic_spatial_query simulation and visualization."""
        from examples import basic_spatial_query
        
        # Test 2D simulated output
        sim_2d = basic_spatial_query.generate_simulated_spatial_output("detect objects with bounding boxes")
        data_2d = json.loads(sim_2d)
        self.assertIsInstance(data_2d, list)
        self.assertTrue(len(data_2d) > 0)
        self.assertIn("box_2d", data_2d[0])

        # Test 3D simulated output
        sim_3d = basic_spatial_query.generate_simulated_spatial_output("return 3d bounding box and grasp affordance")
        data_3d = json.loads(sim_3d)
        self.assertIsInstance(data_3d, list)
        self.assertIn("box_3d", data_3d[0])
        self.assertIn("grasp_affordance", data_3d[0])

        # Test visualization drawing
        dummy_img_path = os.path.join(ROOT_DIR, "tests", "test_view.jpg")
        Image.new('RGB', (320, 240), color=(50, 50, 50)).save(dummy_img_path)
        out_path = os.path.join(ROOT_DIR, "tests", "test_perception_out.jpg")
        res = basic_spatial_query.visualize_results(dummy_img_path, sim_3d, output_path=out_path)
        self.assertIsNotNone(res)
        self.assertTrue(os.path.exists(out_path))

        # Cleanup
        if os.path.exists(dummy_img_path): os.remove(dummy_img_path)
        if os.path.exists(out_path): os.remove(out_path)

    def test_task_decomposition_sim(self):
        """Test task_decomposition whole-body planner simulation & Pydantic schema."""
        from examples import task_decomposition
        
        plan = task_decomposition.plan_mission("Pick up water bottle from floor")
        self.assertIsNotNone(plan)
        if isinstance(plan, task_decomposition.RobotTaskPlan):
            self.assertTrue(len(plan.steps) > 0)
            self.assertEqual(plan.steps[0].step_id, 1)

    def test_tool_use_recycling_sim(self):
        """Test tool_use_recycling reasoning and local facility rules."""
        from examples import tool_use_recycling
        
        rule = tool_use_recycling.query_local_facility_rules("plastic #5 pp")
        self.assertIn("recyclable", rule.lower())
        
        res = tool_use_recycling.run_agentic_robot("Plastic #5 PP cup")
        self.assertIn("RECYCLING", res)

    def test_video_anomaly_detection_sim(self):
        """Test video safety auditing and ASIMOV report generation."""
        from examples import video_anomaly_detection
        
        report = video_anomaly_detection.analyze_video_safety("dummy_incident.mp4", "Max speed 0.5m/s")
        self.assertEqual(report.status, "UNSAFE")
        self.assertTrue(len(report.violations) >= 1)

    def test_multi_robot_coordination_sim(self):
        """Test multi-robot fleet task allocation and synchronization."""
        from examples import multi_robot_coordination
        
        fleet = [
            multi_robot_coordination.RobotAgentSpec(
                agent_id="humanoid_1",
                robot_type="Humanoid",
                payload_capacity_kg=20.0,
                manipulation_dof=14,
                current_location="Bay 1"
            ),
            multi_robot_coordination.RobotAgentSpec(
                agent_id="rover_1",
                robot_type="AMR Rover",
                payload_capacity_kg=80.0,
                manipulation_dof=0,
                current_location="Dock 1"
            )
        ]
        fleet_plan = multi_robot_coordination.coordinate_robot_fleet("Move heavy engine", fleet)
        self.assertEqual(len(fleet_plan.participating_agents), 2)
        self.assertTrue(len(fleet_plan.synchronized_steps) > 0)

    def test_ros2_standalone_bridge(self):
        """Test ROS 2 perception and planner nodes in standalone mode."""
        from ros2_gemini_bridge import gemini_perception_node, gemini_planner_node
        
        # Test perception node
        p_node = gemini_perception_node.GeminiPerceptionNode()
        dummy_img = Image.new('RGB', (100, 100), color=(10, 20, 30))
        p_node.process_frame(dummy_img)
        
        # Test planner node
        pl_node = gemini_planner_node.GeminiPlannerNode()
        pl_node.generate_plan("Test robot mission")

if __name__ == '__main__':
    unittest.main()

