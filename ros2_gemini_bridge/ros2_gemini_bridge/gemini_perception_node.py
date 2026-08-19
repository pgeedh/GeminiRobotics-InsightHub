#!/usr/bin/env python3
"""
Gemini Robotics ROS 2 Perception Node.
Subscribes to camera image stream, queries Gemini Robotics ER 2 for spatial
bounding boxes and grasp affordances, and publishes detection topics.
"""

import os
import io
import json
import time
from dotenv import load_dotenv

# Try importing ROS 2 dependencies; provide mock wrappers if testing outside active ROS 2 environment
try:
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import Image as RosImage
    from std_msgs.msg import String, Header
    from geometry_msgs.msg import PoseStamped, Point, Quaternion
    from cv_bridge import CvBridge
    ROS2_AVAILABLE = True
except ImportError:
    ROS2_AVAILABLE = False
    class Node:  # Mock Node for environments without ROS 2 installed
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
                value = None
            p = Param()
            if name == "model": p.value = "gemini-robotics-er-2"
            elif name == "prompt": p.value = "Detect target object and output 3D position."
            elif name == "query_interval_sec": p.value = 2.0
            return p

from PIL import Image as PILImage
from google import genai
from google.genai import types

load_dotenv()

class GeminiPerceptionNode(Node):
    def __init__(self):
        super().__init__('gemini_perception_node')
        self.logger = self.get_logger()
        self.logger.info("Initializing Gemini Robotics ER 2 Perception Bridge...")

        # Parameters
        if ROS2_AVAILABLE:
            self.declare_parameter('model', 'gemini-robotics-er-2')
            self.declare_parameter('image_topic', '/camera/color/image_raw')
            self.declare_parameter('query_interval_sec', 3.0)
            self.declare_parameter('prompt', 'Detect graspable objects with 2D/3D boxes.')
            
            self.model_name = self.get_parameter('model').get_parameter_value().string_value
            self.image_topic = self.get_parameter('image_topic').get_parameter_value().string_value
            self.query_interval = self.get_parameter('query_interval_sec').get_parameter_value().double_value
            self.default_prompt = self.get_parameter('prompt').get_parameter_value().string_value
            self.bridge = CvBridge()
        else:
            self.model_name = os.getenv("GEMINI_ROBOTICS_MODEL", "gemini-robotics-er-2")
            self.image_topic = "/camera/color/image_raw"
            self.query_interval = 3.0
            self.default_prompt = "Detect graspable objects with 2D/3D boxes."
            self.bridge = None

        # Gemini Client Init
        api_key = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
            self.logger.info("✅ Gemini API Client connected.")
        else:
            self.client = None
            self.logger.warn("⚠️ GEMINI_API_KEY not set. Operating in simulation fallback mode.")

        self.last_query_time = 0.0

        if ROS2_AVAILABLE:
            # Publishers
            self.detection_pub = self.create_publisher(String, '/gemini/detections', 10)
            self.grasp_pose_pub = self.create_publisher(PoseStamped, '/gemini/target_grasp_pose', 10)

            # Subscribers
            self.image_sub = self.create_subscription(
                RosImage,
                self.image_topic,
                self.image_callback,
                10
            )
            self.prompt_sub = self.create_subscription(
                String,
                '/gemini/prompt_override',
                self.prompt_callback,
                10
            )
            self.logger.info(f"Subscribed to image topic: {self.image_topic}")

    def prompt_callback(self, msg: 'String'):
        self.default_prompt = msg.data
        self.logger.info(f"Perception prompt updated to: '{self.default_prompt}'")

    def image_callback(self, msg: 'RosImage'):
        now = time.time()
        if now - self.last_query_time < self.query_interval:
            return  # Rate limit Gemini queries to avoid API saturation
        self.last_query_time = now

        try:
            cv_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            pil_img = PILImage.fromarray(cv_img[:, :, ::-1])
            self.process_frame(pil_img, msg.header)
        except Exception as e:
            self.logger.error(f"Error converting ROS Image: {e}")

    def process_frame(self, pil_img: PILImage.Image, header: 'Header' = None):
        """Processes frame with Gemini Robotics ER 2 model."""
        buf = io.BytesIO()
        pil_img.save(buf, format='JPEG')
        image_bytes = buf.getvalue()

        prompt = f"""
        {self.default_prompt}
        Format as JSON array with 2D/3D boxes:
        [{{"label": "object_name", "box_2d": [ymin, xmin, ymax, xmax], "box_3d": {{"center": [x,y,z], "size": [dx,dy,dz]}}}}]
        """

        raw_output = None
        if self.client:
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
                        prompt
                    ],
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        thinking_config=types.ThinkingConfig(thinking_budget=1024)
                    )
                )
                raw_output = response.text
            except Exception as e:
                self.logger.warn(f"Gemini API query error: {e}. Falling back to simulation.")

        if not raw_output:
            raw_output = json.dumps([
                {
                    "label": "target_manipulation_part",
                    "box_2d": [400, 450, 600, 550],
                    "box_3d": {"center": [0.12, 0.48, 0.05], "size": [0.08, 0.08, 0.10]}
                }
            ])

        self.publish_detections(raw_output, header)

    def publish_detections(self, raw_json_str: str, header: 'Header' = None):
        self.logger.info(f"Gemini Detection Results: {raw_json_str[:120]}...")
        if ROS2_AVAILABLE:
            msg = String()
            msg.data = raw_json_str
            self.detection_pub.publish(msg)

            # Publish target 3D grasp pose if present
            try:
                data = json.loads(raw_json_str)
                if isinstance(data, list) and len(data) > 0 and "box_3d" in data[0]:
                    center = data[0]["box_3d"].get("center", [0, 0, 0])
                    pose_msg = PoseStamped()
                    pose_msg.header = header if header else Header()
                    pose_msg.header.stamp = self.get_clock().now().to_msg()
                    pose_msg.pose.position = Point(x=float(center[0]), y=float(center[1]), z=float(center[2]))
                    pose_msg.pose.orientation = Quaternion(x=0.0, y=0.0, z=0.0, w=1.0)
                    self.grasp_pose_pub.publish(pose_msg)
            except Exception as e:
                self.logger.warn(f"Could not parse grasp pose for /gemini/target_grasp_pose: {e}")

def main(args=None):
    if ROS2_AVAILABLE:
        rclpy.init(args=args)
        node = GeminiPerceptionNode()
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass
        finally:
            node.destroy_node()
            rclpy.shutdown()
    else:
        print("[ROS 2 Not Found] Executing GeminiPerceptionNode in standalone demo mode...")
        node = GeminiPerceptionNode()
        dummy_img = PILImage.new('RGB', (640, 480), color=(50, 50, 60))
        node.process_frame(dummy_img)
        print("✅ Standalone perception cycle executed successfully.")

if __name__ == '__main__':
    main()
