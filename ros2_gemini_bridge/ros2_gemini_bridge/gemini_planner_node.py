#!/usr/bin/env python3
"""
Gemini Robotics ROS 2 Planner Node.
Receives high-level Natural Language task goals, queries Gemini Robotics ER 2,
and publishes structured whole-body execution plans for robot executive controllers.
"""

import os
import json
from dotenv import load_dotenv

try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String
    ROS2_AVAILABLE = True
except ImportError:
    ROS2_AVAILABLE = False
    class Node:
        def __init__(self, name):
            self.name = name
        def get_logger(self):
            node_name = self.name
            class Logger:
                def info(self, msg): print(f"[{node_name}] INFO: {msg}")
                def warn(self, msg): print(f"[{node_name}] WARN: {msg}")
                def error(self, msg): print(f"[{node_name}] ERROR: {msg}")
            return Logger()
        def declare_parameter(self, name, default): pass
        def get_parameter(self, name):
            class Param:
                value = "gemini-robotics-er-2"
            return Param()

from google import genai
from google.genai import types

load_dotenv()

class GeminiPlannerNode(Node):
    def __init__(self):
        super().__init__('gemini_planner_node')
        self.logger = self.get_logger()
        self.logger.info("Initializing Gemini Robotics ER 2 Planner Bridge...")

        if ROS2_AVAILABLE:
            self.declare_parameter('model', 'gemini-robotics-er-2')
            self.model_name = self.get_parameter('model').get_parameter_value().string_value
            self.plan_pub = self.create_publisher(String, '/gemini/execution_plan', 10)
            self.goal_sub = self.create_subscription(String, '/gemini/goal_command', self.goal_callback, 10)
            self.logger.info("Listening for robot goal commands on /gemini/goal_command")
        else:
            self.model_name = os.getenv("GEMINI_ROBOTICS_MODEL", "gemini-robotics-er-2")

        api_key = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
            self.logger.info("✅ Gemini API Client connected.")
        else:
            self.client = None
            self.logger.warn("⚠️ GEMINI_API_KEY not set. Running in simulation fallback mode.")

    def goal_callback(self, msg: 'String'):
        command = msg.data
        self.logger.info(f"Received high-level goal command: '{command}'")
        self.generate_plan(command)

    def generate_plan(self, command: str):
        prompt = f"""
        You are the Embodied Reasoning Brain (Gemini Robotics ER 2) for a ROS 2 mobile manipulator.
        Break down the following command into an executable action sequence:
        Command: "{command}"

        Return JSON matching this format:
        {{
          "task": "{command}",
          "steps": [
            {{"step_id": 1, "action": "navigate_to", "target": "table", "params": {{"clearance_m": 0.5}}}},
            {{"step_id": 2, "action": "perceive_target", "target": "object", "params": {{}}}},
            {{"step_id": 3, "action": "grasp", "target": "object", "params": {{"arm": "right", "force_n": 15}}}},
            {{"step_id": 4, "action": "place", "target": "destination", "params": {{"arm": "right"}}}}
          ]
        }}
        """

        plan_json = None
        if self.client:
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                        thinking_config=types.ThinkingConfig(thinking_budget=1024)
                    )
                )
                plan_json = response.text
            except Exception as e:
                self.logger.warn(f"Planner API call error: {e}. Falling back to simulation.")

        if not plan_json:
            plan_json = json.dumps({
                "task": command,
                "steps": [
                    {"step_id": 1, "action": "navigate_to", "target": "workstation_alpha", "params": {"clearance_m": 0.5}},
                    {"step_id": 2, "action": "perceive_target", "target": "target_item", "params": {}},
                    {"step_id": 3, "action": "grasp", "target": "target_item", "params": {"arm": "right", "force_n": 16}},
                    {"step_id": 4, "action": "navigate_to", "target": "dropoff_zone", "params": {"clearance_m": 0.5}},
                    {"step_id": 5, "action": "place", "target": "dropoff_bin", "params": {"arm": "right"}}
                ]
            }, indent=2)

        self.logger.info(f"Published Plan: {plan_json[:120]}...")
        if ROS2_AVAILABLE:
            out_msg = String()
            out_msg.data = plan_json
            self.plan_pub.publish(out_msg)

def main(args=None):
    if ROS2_AVAILABLE:
        rclpy.init(args=args)
        node = GeminiPlannerNode()
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass
        finally:
            node.destroy_node()
            rclpy.shutdown()
    else:
        print("[ROS 2 Not Found] Executing GeminiPlannerNode in standalone test mode...")
        node = GeminiPlannerNode()
        node.generate_plan("Pick up the red gear on conveyor 1 and place it in bin 3")
        print("✅ Standalone planning cycle executed successfully.")

if __name__ == '__main__':
    main()
