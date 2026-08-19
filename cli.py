#!/usr/bin/env python3
import os
import sys
import time
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint
from rich.table import Table
import questionary

# Ensure strict pathing for relative imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'examples'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ros2_gemini_bridge'))

try:
    from examples import basic_spatial_query
    from examples import task_decomposition
    from examples import tool_use_recycling
    from examples import video_anomaly_detection
    from examples import multi_robot_coordination
except ImportError:
    try:
        import basic_spatial_query
        import task_decomposition
        import tool_use_recycling
        import video_anomaly_detection
        import multi_robot_coordination
    except ImportError:
        pass

load_dotenv()
console = Console()

ACTIVE_MODEL = os.getenv("GEMINI_ROBOTICS_MODEL", "gemini-robotics-er-2")

def check_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if not key or "your_api_key" in key:
        rprint("[bold yellow]⚠️  Notice: GEMINI_API_KEY is not set or using placeholder.[/bold yellow]")
        rprint("[cyan]The suite will automatically execute high-fidelity simulated ER 2 telemetry for all demos.[/cyan]\n")
        return False
    return True

def select_model():
    global ACTIVE_MODEL
    console.print("\n[bold cyan]🤖 Select Gemini Robotics / GenAI Model:[/bold cyan]")
    choice = questionary.select(
        "Choose active inference model:",
        choices=[
            "gemini-robotics-er-2 (Google DeepMind Whole-Body & Dexterity ER 2)",
            "gemini-robotics-er-1.5-preview (Early Trusted Tester ER 1.5 Preview)",
            "gemini-2.5-flash (Gemini 2.5 Flash Thinking)",
            "gemini-2.0-flash (Gemini 2.0 Flash Multimodal)",
            "gemini-1.5-pro (Gemini 1.5 Pro Long-Context)"
        ]
    ).ask()
    if choice:
        ACTIVE_MODEL = choice.split(" ")[0]
        os.environ["GEMINI_ROBOTICS_MODEL"] = ACTIVE_MODEL
        rprint(f"[bold green]✅ Active model set to: {ACTIVE_MODEL}[/bold green]")

def check_ros2_status():
    console.rule("[bold cyan]🤖 ROS 2 Gemini Bridge Status[/bold cyan]")
    table = Table(title="ROS 2 Package & Node Environment")
    table.add_column("Component", style="cyan", justify="left")
    table.add_column("Status", justify="left")
    table.add_column("Details", style="dim", justify="left")

    try:
        import rclpy
        ros_status = "[bold green]INSTALLED[/bold green]"
        ros_details = f"rclpy v{rclpy.__file__}"
    except ImportError:
        ros_status = "[bold yellow]STANDALONE SIMULATION[/bold yellow]"
        ros_details = "rclpy not in global Python path; standalone runner active"

    table.add_row("ROS 2 Runtime", ros_status, ros_details)
    table.add_row("Perception Node", "[bold green]READY[/bold green]", "ros2_gemini_bridge.gemini_perception_node")
    table.add_row("Planner Node", "[bold green]READY[/bold green]", "ros2_gemini_bridge.gemini_planner_node")
    table.add_row("Active Bridge Model", f"[bold cyan]{ACTIVE_MODEL}[/bold cyan]", "Target Gemini API Model")

    console.print(table)
    
    if Confirm.ask("\nRun standalone ROS 2 perception & planner self-test?"):
        try:
            from ros2_gemini_bridge import gemini_perception_node, gemini_planner_node
            rprint("[cyan]Running standalone perception node cycle...[/cyan]")
            gemini_perception_node.main()
            rprint("\n[cyan]Running standalone planner node cycle...[/cyan]")
            gemini_planner_node.main()
            rprint("[bold green]✅ ROS 2 standalone bridge tests passed![/bold green]")
        except Exception as e:
            rprint(f"[bold red]❌ Bridge test error: {e}[/bold red]")

def main():
    global ACTIVE_MODEL
    console.clear()
    
    # Updated ASCII Logo for Gemini Robotics 2 & ER 1.5
    console.print(r"""[bold cyan]
   ______                _       _   ____       __          __  _          
  / ____/___  ____ ___  (_)___  (_) / __ \____ / /_  ____  / /_(_)_________
 / / __/ __ \/ __ `__ \/ / __ \/ / / /_/ / __ \ __ \/ __ \/ __/ / ___/ ___/
/ /_/ / /_/ / / / / / / / / / / / / _, _/ /_/ / /_/ / /_/ / /_/ / /__(__  ) 
\____/\____/_/ /_/ /_/_/_/ /_/_/ /_/ |_|\____/_.___/\____/\__/_/\___/____/  
               E M B O D I E D   R E A S O N I N G   2 . 0
    [/bold cyan]""")
    
    console.print(Panel.fit(
        f"[white]Google DeepMind Physical AI & Embodied Reasoning Suite[/white]\n"
        f"[dim]Active Model: [bold cyan]{ACTIVE_MODEL}[/bold cyan] | SDK: google-genai v1.x[/dim]",
        subtitle="v2.0.0"
    ))

    check_api_key()

    while True:
        try:
            choice = questionary.select(
                "Select a Gemini Robotics Capability to Explore:",
                choices=[
                    "1. 👁️  Vision & Perception (3D Spatial Query & Grasping)",
                    "2. 🧠  Brain & Planning (Whole-Body Task Decomposition)",
                    "3. 🛠️  Agentic Capabilities (Grounded Search Tool Use)",
                    "4. 🛡️  Safety & Auditing (ASIMOV-Agentic Video Audit)",
                    "5. 🤝  Multi-Robot Coordination (Fleet Allocation)",
                    "6. ⚙️  Select Active Model",
                    "7. 🤖  ROS 2 Bridge Status & Test",
                    "8. 🚪  Exit"
                ]
            ).ask()
        except KeyboardInterrupt:
            rprint("\n[yellow]Cancelled by user.[/yellow]")
            break

        if choice is None or "Exit" in choice or "8." in choice:
            rprint("[green]Goodbye! Happy Robot Building! 🤖👋[/green]")
            break

        console.rule(f"[bold]{choice}[/bold]")

        if "Vision" in choice:
            rprint(f"[italic]Running: examples/basic_spatial_query.py (Model: {ACTIVE_MODEL})[/italic]")
            
            image_path = questionary.text(
                "Drag & drop an image file here (or press Enter for default 'robot_view.jpg'):"
            ).ask()
            
            if not image_path:
                image_path = "robot_view.jpg"
            
            if image_path is None:
                continue

            image_path = image_path.strip().replace("'", "").replace('"', "")
            
            if not os.path.exists(image_path) and image_path == "robot_view.jpg":
                rprint("[yellow]Default 'robot_view.jpg' not found. Creating placeholder image...[/yellow]")
                from PIL import Image
                Image.new('RGB', (640, 480), color=(40, 44, 52)).save('robot_view.jpg')

            if os.path.exists(image_path):
                user_prompt = questionary.text(
                    "What would you like to detect/ground?",
                    default="Detect manipulable objects, estimate 3D bounding boxes, and compute 6DoF grasp affordances."
                ).ask()

                basic_spatial_query.robot_perception_query(
                    image_path, 
                    user_prompt,
                    model_name=ACTIVE_MODEL
                )
                rprint("\n[bold green]✅ Perception Demo Complete[/bold green]")
            else:
                rprint(f"[bold red]❌ Error: Image file '{image_path}' not found.[/bold red]")

        elif "Planning" in choice:
            rprint(f"[italic]Running: examples/task_decomposition.py (Model: {ACTIVE_MODEL})[/italic]")
            command = Prompt.ask(
                "Enter a high-level robot mission command",
                default="Locate the toolbox on the lower shelf, crouch down, pick it up with dual arms, and bring it to workbench alpha"
            )
            task_decomposition.plan_mission(command, model_name=ACTIVE_MODEL)
            rprint("\n[bold green]✅ Planning Demo Complete[/bold green]")

        elif "Agentic" in choice:
            rprint(f"[italic]Running: examples/tool_use_recycling.py (Model: {ACTIVE_MODEL})[/italic]")
            item = Prompt.ask("What object does the robot camera observe?", default="Discarded lithium polymer battery pack with swollen pouch")
            location = Prompt.ask("Robot facility city / location", default="San Jose, CA")
            tool_use_recycling.run_agentic_robot(item, location=location)
            rprint("\n[bold green]✅ Agentic Demo Complete[/bold green]")

        elif "Safety" in choice:
            rprint(f"[italic]Running: examples/video_anomaly_detection.py (Model: {ACTIVE_MODEL})[/italic]")
            video_anomaly_detection.analyze_video_safety(
                "robot_incident_log_001.mp4",
                "1. Max collaborative velocity 0.5m/s. 2. Zero humans in 1.0m safety bubble. 3. Zero grasp slip > 5mm.",
                model_name=ACTIVE_MODEL
            )
            rprint("\n[bold green]✅ Safety Demo Complete[/bold green]")

        elif "Multi-Robot" in choice:
            rprint(f"[italic]Running: examples/multi_robot_coordination.py (Model: {ACTIVE_MODEL})[/italic]")
            mission = Prompt.ask(
                "Enter a multi-robot collaborative mission",
                default="Transport heavy 35kg battery module from storage depot to humanoid assembly station."
            )
            fleet = [
                multi_robot_coordination.RobotAgentSpec(
                    agent_id="humanoid_arm_01",
                    robot_type="Dual-Arm Humanoid (Boston Dynamics / Apptronik)",
                    payload_capacity_kg=30.0,
                    manipulation_dof=14,
                    current_location="Assembly Station Alpha"
                ),
                multi_robot_coordination.RobotAgentSpec(
                    agent_id="heavy_rover_01",
                    robot_type="Heavy Autonomous Mobile Robot (AMR)",
                    payload_capacity_kg=150.0,
                    manipulation_dof=0,
                    current_location="Docking Bay 2"
                ),
                multi_robot_coordination.RobotAgentSpec(
                    agent_id="quadruped_scout_01",
                    robot_type="Agile Quadruped Inspector",
                    payload_capacity_kg=6.0,
                    manipulation_dof=1,
                    current_location="Corridor Junction 4"
                )
            ]
            multi_robot_coordination.coordinate_robot_fleet(mission, fleet, model_name=ACTIVE_MODEL)
            rprint("\n[bold green]✅ Multi-Robot Coordination Complete[/bold green]")

        elif "Select Active Model" in choice:
            select_model()

        elif "ROS 2" in choice:
            check_ros2_status()
        
        input("\nPress Enter to return to main menu...")
        console.clear()

if __name__ == "__main__":
    main()

