from google import genai
from google.genai import types
import time
import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# GEMINI ROBOTICS: VIDEO SAFETY AUDITING & ANOMALY DETECTION (ER 2)
# -------------------------------------------------------------------------
# Gemini Robotics ER 2 can reason across long-horizon robotic video logs
# (from seconds to hours) and detect physical anomalies, near-miss collisions,
# grip slip, and safety protocol violations against ASIMOV-Agentic standards.
# -------------------------------------------------------------------------

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

DEFAULT_MODEL = os.getenv("GEMINI_ROBOTICS_MODEL", "gemini-robotics-er-2")
FALLBACK_MODELS = [
    "gemini-robotics-er-2",
    "gemini-robotics-er-1.5-preview",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-pro"
]

if api_key:
    client = genai.Client(api_key=api_key)
    print("✅ Gemini API Key loaded.")
else:
    client = None
    print("⚠️ Warning: GEMINI_API_KEY not found. Running in simulation mode.")

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
    """
    Performs multimodal video analysis to audit robot executions against safety specifications.
    """
    print(f"\n🎬 Auditing Robot Video Log: '{video_path}'")
    print(f"📋 Safety Guidelines / Protocols:\n   {safety_guidelines}")

    audit_result = None

    if client and os.path.exists(video_path):
        try:
            print(f"⬆️ Uploading video to Gemini File API...")
            video_file = client.files.upload(file=video_path)
            
            # Wait for video processing if required
            while video_file.state.name == "PROCESSING":
                print("⏳ Processing video frames in Gemini cloud...")
                time.sleep(3)
                video_file = client.files.get(name=video_file.name)

            if video_file.state.name == "FAILED":
                raise ValueError("Video processing failed on server.")

            print(f"🧠 Video ready (URI: {video_file.uri}). Running ASIMOV safety audit with {model_name}...")
            
            prompt = f"""
            You are a certified Robot Safety Auditor analyzing video telemetry from an autonomous robot.
            Audit this video strictly against the following guidelines:
            {safety_guidelines}

            Identify any near-misses, sudden acceleration spikes, human workspace intrusions, or unstable grasps.
            Return structured JSON matching the audit report schema.
            """

            response = client.models.generate_content(
                model=model_name,
                contents=[video_file, prompt],
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                    response_schema=VideoSafetyAuditReport,
                    thinking_config=types.ThinkingConfig(thinking_budget=2048)
                )
            )
            audit_result = VideoSafetyAuditReport(**json.loads(response.text))
            print(f"✅ Completed live video audit with model '{model_name}'")

        except Exception as e:
            print(f"⚠️ Live video analysis error: {e}")

    if not audit_result:
        print("ℹ️ Using simulated ASIMOV-Agentic audit telemetry report...")
        audit_result = generate_simulated_audit_report(video_path)

    print_audit_report(audit_result)
    return audit_result

def generate_simulated_audit_report(video_path: str) -> VideoSafetyAuditReport:
    return VideoSafetyAuditReport(
        status="UNSAFE",
        audit_summary=f"Audit of '{video_path}' identified 2 protocol violations. Human entered active manipulator zone while velocity exceeded collaborative threshold.",
        violations=[
            SafetyViolation(
                timestamp_range="00:12 - 00:16",
                severity="HIGH",
                violation_type="Human Proximity Violation",
                description="Operator hand entered robot primary envelope within 35cm without robot pausing motion.",
                corrective_action="Activate 0.8m dynamic safety bubble trigger to ramp speed to 0 m/s when optical sensor detects human."
            ),
            SafetyViolation(
                timestamp_range="00:38 - 00:41",
                severity="MEDIUM",
                violation_type="Unstable Grasp Affordance",
                description="Heavy part lifted with high angular velocity causing 12mm tactile slip before restabilizing.",
                corrective_action="Increase normal grip force to 28N and constrain angular roll velocity to < 0.3 rad/s."
            )
        ],
        human_in_loop_interventions_needed=True
    )

def print_audit_report(report: VideoSafetyAuditReport):
    status_icon = "🟢" if report.status == "SAFE" else "🟡" if report.status == "CAUTION" else "🔴"
    print("\n" + "=" * 65)
    print(f"🛡️ ASIMOV-AGENTIC ROBOT SAFETY AUDIT: {status_icon} [{report.status}]")
    print("=" * 65)
    print(f"📝 Summary: {report.audit_summary}\n")
    print(f"🚨 Detected Violations ({len(report.violations)}):")
    for i, v in enumerate(report.violations, 1):
        print(f"  {i}. [{v.timestamp_range}] [{v.severity}] {v.violation_type}")
        print(f"     Details: {v.description}")
        print(f"     Fix: {v.corrective_action}")
    print(f"\n⚠️ Human-in-the-loop intervention required: {report.human_in_loop_interventions_needed}")
    print("=" * 65)

if __name__ == "__main__":
    guidelines = """
    1. Maximum end-effector velocity: 0.5 m/s when humans are present within 2 meters.
    2. Zero humans allowed in the red exclusion envelope (1.0m radius from base).
    3. Tactile grip feedback must remain stable without slip > 5mm during payload transport.
    """
    analyze_video_safety(
        video_path="robot_incident_log_001.mp4",
        safety_guidelines=guidelines
    )

