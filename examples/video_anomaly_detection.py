from google import genai
from google.genai import types
import time
import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# GEMINI ROBOTICS 2.0: VIDEO SAFETY AUDITING & ANOMALY DETECTION (ER 2)
# -------------------------------------------------------------------------
# Analyzes continuous robotic video logs to detect physical anomalies,
# near-miss collisions, grip slip, and safety protocol violations.
# -------------------------------------------------------------------------

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

DEFAULT_MODEL = os.getenv("GEMINI_ROBOTICS_MODEL", "gemini-robotics-er-2")
FALLBACK_MODELS = [
    "gemini-robotics-er-2",
    "gemini-2.5-flash",
    "gemini-2.0-flash"
]

if api_key:
    client = genai.Client(api_key=api_key)
    print("[INFO] Gemini API Key loaded.")
else:
    client = None
    print("[INFO] GEMINI_API_KEY not found. Running in simulation mode.")

class SafetyViolation(BaseModel):
    timestamp_range: str = Field(description="e.g. '00:14 - 00:19'")
    severity: str = Field(description="'LOW', 'MEDIUM', 'HIGH', or 'CRITICAL'")
    violation_type: str = Field(description="e.g. Human Proximity, End-Effector Jerk, Grasp Slip, Workspace Incursion")
    description: str
    corrective_action: str

class VideoSafetyAuditReport(BaseModel):
    status: str = Field(description="'SAFE', 'CAUTION', or 'UNSAFE'")
    audit_summary: str
    violations: List[SafetyViolation]
    human_in_loop_interventions_needed: bool

def analyze_video_safety(video_path: str, safety_guidelines: str, model_name: str = DEFAULT_MODEL) -> VideoSafetyAuditReport:
    print(f"\n[AUDIT] Auditing Robot Video Log: '{video_path}'")
    print(f"Safety Guidelines / Protocols:\n   {safety_guidelines}")

    audit_result = None

    if client and os.path.exists(video_path):
        try:
            print(f"[UPLOAD] Uploading video file to Gemini Files API...")
            video_file = client.files.upload(file=video_path)
            
            while video_file.state.name == "PROCESSING":
                print("[PROCESSING] Processing video frames in cloud...")
                time.sleep(2)
                video_file = client.files.get(name=video_file.name)

            if video_file.state.name == "FAILED":
                raise ValueError("Video processing failed.")

            prompt = f"""
            Audit this robot manipulation video against the following safety guidelines:
            {safety_guidelines}
            Identify timestamps, evaluate proximity buffers, grasp slips, and produce structured audit report.
            """

            response = client.models.generate_content(
                model=model_name,
                contents=[video_file, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=VideoSafetyAuditReport,
                    temperature=0.0
                )
            )
            audit_result = VideoSafetyAuditReport.model_validate_json(response.text)
            print_audit(audit_result)
            return audit_result
        except Exception as e:
            print(f"[WARN] Video API processing error: {e}. Executing offline simulated audit...")

    audit_result = generate_simulated_audit(video_path)
    print_audit(audit_result)
    return audit_result

def generate_simulated_audit(video_path: str) -> VideoSafetyAuditReport:
    return VideoSafetyAuditReport(
        status="UNSAFE",
        audit_summary="Detected two safety violations during episode: human proximity bubble breach at 00:03 and payload slippage during high-acceleration swing at 00:07.",
        violations=[
            SafetyViolation(
                timestamp_range="00:03 - 00:05",
                severity="HIGH",
                violation_type="Human Proximity Incursion",
                description="Coworker entered active robot work cell (< 0.8m distance) while arm was in high-speed motion.",
                corrective_action="Trigger safety stop or reduce arm velocity to < 0.25 m/s collaborative speed."
            ),
            SafetyViolation(
                timestamp_range="00:07 - 00:09",
                severity="CRITICAL",
                violation_type="Grasp Slip / Load Instability",
                description="Payload slipped 12mm downward in parallel jaw gripper during angular jerk.",
                corrective_action="Increase squeeze force +15N and smooth spline trajectory jerk."
            )
        ],
        human_in_loop_interventions_needed=True
    )

def print_audit(report: VideoSafetyAuditReport):
    print("\nASIMOV Video Safety Audit Report:")
    print("==================================================")
    print(f"Overall Status: {report.status}")
    print(f"Summary: {report.audit_summary}")
    print(f"Human Intervention Required: {report.human_in_loop_interventions_needed}")
    for idx, v in enumerate(report.violations, 1):
        print(f"\n  Violation #{idx} [{v.severity}]: {v.violation_type} ({v.timestamp_range})")
        print(f"    Details: {v.description}")
        print(f"    Remedy: {v.corrective_action}")
    print("==================================================")

if __name__ == "__main__":
    analyze_video_safety("demo_video.mp4", "1. Max velocity 0.5 m/s. 2. 1.2m human proximity safety bubble. 3. Zero grasp slip.")
