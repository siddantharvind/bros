# brocode.py
import argparse
import os
import yaml
import time # For simulation of node execution
from colorama import Fore, Style, init # Import colorama for colorful output

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

# --- Configuration for BROS workspace and project structures ---
BROS_WORKSPACE_CONFIG_FILE = ".bros_workspace.yaml"
BROS_PROJECT_MANIFEST_FILE = "package.yaml" # Or project.toml, user's preference later

def _find_project_root(start_path):
    """
    Helper function to find the project root by looking for package.yaml
    and then the workspace root by looking for .bros_workspace.yaml
    """
    current_path = start_path
    while True:
        # Check for project manifest
        project_manifest_path = os.path.join(current_path, BROS_PROJECT_MANIFEST_FILE)
        if os.path.exists(project_manifest_path):
            # Verify if it's within a workspace
            temp_path = current_path
            while True:
                if os.path.exists(os.path.join(temp_path, BROS_WORKSPACE_CONFIG_FILE)):
                    return current_path, project_manifest_path
                parent_path = os.path.dirname(temp_path)
                if parent_path == temp_path: # Reached root directory
                    break
                temp_path = parent_path
            return None, None # Found project but not in a workspace

        parent_path = os.path.dirname(current_path)
        if parent_path == current_path: # Reached root directory
            break
        current_path = parent_path
    return None, None

def _get_workspace_path():
    """Helper to find the workspace root from the current directory."""
    current_dir = os.getcwd()
    path = current_dir
    while True:
        if os.path.exists(os.path.join(path, BROS_WORKSPACE_CONFIG_FILE)):
            return path
        parent_path = os.path.dirname(path)
        if parent_path == path: # Reached filesystem root
            return None
        path = parent_path


def create_workspace(name):
    """
    Creates a new BROS workspace with standard directory structure and config.
    Equivalent to preparing your engineering workbench.
    """
    print(f"{Fore.CYAN}Bro-tip: Initiating a new realm of robotics excellence...{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Creating BROS workspace: {name}{Style.RESET_ALL}")
    try:
        if os.path.exists(name):
            print(f"{Fore.RED}Error: Directory '{name}' already exists. Please choose a different name or remove it.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Remember the Brocode: No duplicate territories.{Style.RESET_ALL}")
            return

        os.makedirs(name)
        os.chdir(name) # Change into the new workspace directory

        # Create core directories
        workspace_dirs = ["src", "build", "install", "log"]
        for d in workspace_dirs:
            os.makedirs(d)
            print(f"  {Fore.BLUE}Created directory: {d}/{Style.RESET_ALL}")

        # Create workspace configuration file
        workspace_config = {
            "workspace_name": name,
            "version": "0.1.0", # Initial version of the workspace config
            "projects": [] # List to track projects within this workspace
        }
        with open(BROS_WORKSPACE_CONFIG_FILE, 'w') as f:
            yaml.dump(workspace_config, f, default_flow_style=False)
        print(f"  {Fore.BLUE}Created workspace config file: {BROS_WORKSPACE_CONFIG_FILE}{Style.RESET_ALL}")

        print(f"{Fore.GREEN}BROS workspace '{name}' created successfully in {os.getcwd()}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Bro-tip: Your journey into a better robotics future begins now!{Style.RESET_ALL}")
        print(f"Now you can navigate into your workspace: {Fore.YELLOW}cd {name}{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error creating workspace: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: Check permissions or path issues.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: Even the best bros hit snags. Report this.{Style.RESET_ALL}")
    finally:
        pass


def create_project(project_name):
    """
    Creates a new BROS project within the current workspace.
    Equivalent to starting a new board design for a specific module.
    """
    workspace_path = _get_workspace_path()
    if not workspace_path:
        print(f"{Fore.RED}Error: Not in a BROS workspace. '{BROS_WORKSPACE_CONFIG_FILE}' not found in current or parent directories.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: First, get into a workspace. Try 'brocode create workspace <name>' or 'cd' into one.{Style.RESET_ALL}")
        return

    # Ensure we are operating relative to the workspace root's src directory
    original_cwd = os.getcwd()
    os.chdir(workspace_path) # Go to workspace root to ensure correct paths

    print(f"{Fore.CYAN}Bro-tip: Defining a new module, ready for some serious GPU action...{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Creating BROS project: {project_name}{Style.RESET_ALL}")
    try:
        project_path = os.path.join("src", project_name)
        if os.path.exists(project_path):
            print(f"{Fore.RED}Error: Project directory '{project_path}' already exists. Please choose a different name or remove it.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Remember the Brocode: Redundancy is for backups, not project names.{Style.RESET_ALL}")
            return

        os.makedirs(project_path)
        print(f"  {Fore.BLUE}Created project directory: {project_path}/{Style.RESET_ALL}")

        # Create subdirectories typical for a project
        project_subdirs = ["nodes", "msg", "srv", "action", "launch", "config"]
        for d in project_subdirs:
            os.makedirs(os.path.join(project_path, d))
            print(f"  {Fore.BLUE}Created subdirectory: {project_path}/{d}/{Style.RESET_ALL}")

        # Create project manifest file (package.yaml)
        project_manifest = {
            "package_name": project_name,
            "version": "0.0.1",
            "description": f"A BROS package for {project_name}",
            "maintainers": [
                {"name": "Your Name", "email": "your.email@example.com"}
            ],
            "dependencies": [], # Other BROS packages this one depends on
            "executables": [] # List of nodes that can be built/run
        }
        manifest_path = os.path.join(project_path, BROS_PROJECT_MANIFEST_FILE)
        with open(manifest_path, 'w') as f:
            yaml.dump(project_manifest, f, default_flow_style=False)
        print(f"  {Fore.BLUE}Created project manifest file: {manifest_path}{Style.RESET_ALL}")

        # Add project to workspace config
        workspace_config_path = os.path.join(workspace_path, BROS_WORKSPACE_CONFIG_FILE)
        with open(workspace_config_path, 'r+') as f:
            workspace_config = yaml.safe_load(f)
            if project_name not in workspace_config.get("projects", []):
                workspace_config.setdefault("projects", []).append(project_name)
                f.seek(0) # Go to the beginning of the file
                yaml.dump(workspace_config, f, default_flow_style=False)
                f.truncate() # Remove remaining part
                print(f"  {Fore.BLUE}Added '{project_name}' to workspace config.{Style.RESET_ALL}")
            else:
                print(f"  {Fore.YELLOW}Project '{project_name}' already listed in workspace config. All good!{Style.RESET_ALL}")


        print(f"{Fore.GREEN}BROS project '{project_name}' created successfully. Time to build some awesome robots!{Style.RESET_ALL}")

    except OSError as e:
        print(f"{Fore.RED}Error creating project: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: Paths are picky. Double-check yours.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: Even the best bros hit snags. Report this.{Style.RESET_ALL}")
    finally:
        os.chdir(original_cwd) # Return to the original directory


def create_node(node_name, node_type, project_name=None):
    """
    Creates a new BROS node (Bendlang file) within a specified or current project.
    Generates boilerplate code for publisher, subscriber, or service nodes.
    """
    current_dir = os.getcwd()
    project_root, project_manifest_path = _find_project_root(current_dir)

    print(f"{Fore.CYAN}Bro-tip: Forging a new Bendlang node, ready for the GPU furnace...{Style.RESET_ALL}")

    if not project_root:
        if not project_name:
            print(f"{Fore.RED}Error: Not in a BROS project and no project name provided.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Bro-tip: Navigate into a project or specify one using '--project'. Code responsibly.{Style.RESET_ALL}")
            return
        
        # If project_name is provided, try to find it from workspace root
        workspace_path = _get_workspace_path()
        if not workspace_path:
            print(f"{Fore.RED}Error: Cannot find workspace. '{BROS_WORKSPACE_CONFIG_FILE}' not found. Cannot create node in specified project '{project_name}'.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Bro-tip: Ensure you're in a workspace, or it exists.{Style.RESET_ALL}")
            return
        
        project_root = os.path.join(workspace_path, "src", project_name)
        project_manifest_path = os.path.join(project_root, BROS_PROJECT_MANIFEST_FILE)
        
        if not os.path.exists(project_manifest_path):
            print(f"{Fore.RED}Error: Specified project '{project_name}' not found at '{project_root}'.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Bro-tip: Project path seems off. Did you create it?{Style.RESET_ALL}")
            return
        print(f"{Fore.GREEN}Creating node '{node_name}' in specified project '{project_name}'...{Style.RESET_ALL}")
    else:
        # If project_name was explicitly passed but differs from detected, warn
        if project_name and os.path.basename(project_root) != project_name:
            print(f"{Fore.YELLOW}Warning: Detected project '{os.path.basename(project_root)}' but '{project_name}' was specified. Using detected project. Stay consistent, bro!{Style.RESET_ALL}")
        project_name = os.path.basename(project_root)
        print(f"{Fore.GREEN}Creating node '{node_name}' in current project '{project_name}'...{Style.RESET_ALL}")


    nodes_dir = os.path.join(project_root, "nodes")
    node_file_path = os.path.join(nodes_dir, f"{node_name}_node.bend")

    if os.path.exists(node_file_path):
        print(f"{Fore.RED}Error: Node file '{node_file_path}' already exists.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Remember the Brocode: Don't overwrite a brother's work.{Style.RESET_ALL}")
        return

    # Determine boilerplate based on node_type
    boilerplate_content = ""
    if node_type == "pub":
        boilerplate_content = f"""
// {node_name}_node.bend
// BROS Publisher Node (GPU-native with Fast DDS)

import bros.dds
import bros.time
import bros.system

// Define your message type (conceptual example)
// This would typically come from a .msg file compiled by BROS
// type MyMessageType:
//     field1: int32
//     field2: float32
//     data_array: array<float32> # GPU-friendly array

// Or a simple struct for testing
struct MySimpleMessage:
    data: float32
    timestamp: bros.time.Time

fn main():
    system.log("Starting {node_name}_node (Publisher)...")

    // Initialize DDS participant (conceptual)
    let participant = bros.dds.create_participant("{project_name}_participant");
    if participant.is_null():
        system.log_error("Failed to create DDS participant.");
        return

    // Create a publisher for a topic
    let topic_name = "/{project_name}/{node_name}/data";
    let publisher = bros.dds.create_publisher(participant, topic_name, MySimpleMessage);
    if publisher.is_null():
        system.log_error("Failed to create publisher for topic: {{topic_name}}"); // Fixed: Escape for Bendlang variable
        bros.dds.shutdown_participant(participant);
        return

    system.log("Publishing on topic: {{topic_name}}"); // Fixed: Escape for Bendlang variable

    let count = 0;
    while system.ok(): // Loop while the system is running
        let msg = MySimpleMessage:
            data: count as float32
            timestamp: bros.time.now()
        
        publisher.publish(msg)

        system.log("Published: {{msg.data}}"); // Fixed: Escape for Bendlang variable
        bros.time.sleep(1000) // Sleep for 1000 milliseconds (1 second)
        count = count + 1
"""
    elif node_type == "sub":
        boilerplate_content = f"""
// {node_name}_node.bend
// BROS Subscriber Node (GPU-native with Fast DDS)

import bros.dds
import bros.time
import bros.system

// Define your message type (must match publisher's type)
struct MySimpleMessage:
    data: float32
    timestamp: bros.time.Time

fn message_callback(msg: MySimpleMessage):
    // This function will be executed when a new message is received
    // 'msg' data is ideally already on GPU or efficiently transferred
    system.log("Received message: {{msg.data}} at {{msg.timestamp}}"); // Fixed: Escape for Bendlang variables

    // Example of GPU-accelerated processing (conceptual)
    // let processed_data_gpu = bros.math.process_on_gpu(msg.data);
    // system.log("Processed on GPU: {{processed_data_gpu}}");

fn main():
    system.log("Starting {node_name}_node (Subscriber)...")

    // Initialize DDS participant
    let participant = bros.dds.create_participant("{project_name}_participant");
    if participant.is_null():
        system.log_error("Failed to create DDS participant.");
        return

    // Create a subscriber for a topic
    let topic_name = "/{project_name}/{node_name.replace('_subscriber', '')}/data"; // Infer topic name
    let subscriber = bros.dds.create_subscriber(participant, topic_name, MySimpleMessage, message_callback);
    if subscriber.is_null():
        system.log_error("Failed to create subscriber for topic: {{topic_name}}"); // Fixed: Escape for Bendlang variable
        bros.dds.shutdown_participant(participant);
        return

    system.log("Subscribing to topic: {{topic_name}}"); // Fixed: Escape for Bendlang variable

    // Keep the node alive to receive messages
    while system.ok():
        bros.time.sleep(100) // Small sleep to prevent busy-waiting
"""
    elif node_type == "service":
        boilerplate_content = f"""
// {node_name}_node.bend
// BROS Service Server Node (GPU-native with Fast DDS)

import bros.dds
import bros.time
import bros.system

// Define your service request and response types
struct MyServiceRequest:
    input_value: int32

struct MyServiceResponse:
    output_value: int32
    success: bool

fn service_callback(request: MyServiceRequest) -> MyServiceResponse:
    system.log("Received service request with input: {{request.input_value}}"); // Fixed: Escape for Bendlang variable
    
    // Perform some GPU-accelerated computation (conceptual)
    // let result = request.input_value * 2; // Simple example
    // let gpu_processed_result = bros.math.perform_complex_gpu_op(request.input_value);

    let response = MyServiceResponse:
        output_value: result
        success: true
    
    system.log("Responding with: {{response.output_value}}"); // Fixed: Escape for Bendlang variable
    return response

fn main():
    system.log("Starting {node_name}_node (Service Server)...")

    // Initialize DDS participant
    let participant = bros.dds.create_participant("{project_name}_participant");
    if participant.is_null():
        system.log_error("Failed to create DDS participant.");
        return

    // Create a service server
    let service_name = "/{project_name}/{node_name}";
    let service_server = bros.dds.create_service_server(participant, service_name, MyServiceRequest, MyServiceResponse, service_callback);
    if service_server.is_null():
        system.log_error("Failed to create service server for: {{service_name}}"); // Fixed: Escape for Bendlang variable
        bros.dds.shutdown_participant(participant);
        return

    system.log("Service server listening on: {{service_name}}"); // Fixed: Escape for Bendlang variable

    // Keep the node alive to receive service requests
    while system.ok():
        bros.time.sleep(100) // Small sleep to prevent busy-waiting
"""
    else:
        print(f"{Fore.RED}Error: Invalid node type '{node_type}'. Must be 'pub', 'sub', or 'service'.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: Choose your node's purpose wisely!{Style.RESET_ALL}")
        return

    try:
        # Create the 'nodes' directory if it somehow doesn't exist (e.g. user manually deleted it)
        os.makedirs(nodes_dir, exist_ok=True)
        with open(node_file_path, 'w') as f:
            f.write(boilerplate_content.strip()) # .strip() to remove leading/trailing newlines
        print(f"  {Fore.BLUE}Created node file: {node_file_path}{Style.RESET_ALL}")

        # Update project manifest (package.yaml)
        with open(project_manifest_path, 'r+') as f:
            project_manifest = yaml.safe_load(f)
            if "executables" not in project_manifest:
                project_manifest["executables"] = []
            
            # Add node to executables list if not already present
            node_executable_name = f"{node_name}_node"
            if node_executable_name not in project_manifest["executables"]:
                project_manifest["executables"].append(node_executable_name)
                f.seek(0)
                yaml.dump(project_manifest, f, default_flow_style=False)
                f.truncate()
                print(f"  {Fore.BLUE}Added '{node_executable_name}' to {BROS_PROJECT_MANIFEST_FILE}.{Style.RESET_ALL}")
            else:
                print(f"  {Fore.YELLOW}Node '{node_executable_name}' already listed in {BROS_PROJECT_MANIFEST_FILE}. You're consistent, bro!{Style.RESET_ALL}")

        print(f"{Fore.GREEN}BROS node '{node_name}' of type '{node_type}' created successfully! Go forth and code!{Style.RESET_ALL}")

    except OSError as e:
        print(f"{Fore.RED}Error creating node: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: Permissions or path issues. Check your access.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: Even the best bros hit snags. Report this.{Style.RESET_ALL}")


def build_projects():
    """
    Simulates the build process for all projects in the current BROS workspace.
    This involves finding Bendlang nodes and creating placeholder executables.
    """
    workspace_path = _get_workspace_path()
    if not workspace_path:
        print(f"{Fore.RED}Error: Not in a BROS workspace. Cannot build projects.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: Navigate into your workspace before building.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}Bro-tip: Initiating the BROS build sequence. Optimizing for maximum GPU gains!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Building projects in workspace: {os.path.basename(workspace_path)}{Style.RESET_ALL}")

    original_cwd = os.getcwd()
    os.chdir(workspace_path) # Operate from workspace root

    try:
        with open(BROS_WORKSPACE_CONFIG_FILE, 'r') as f:
            workspace_config = yaml.safe_load(f)
        
        projects = workspace_config.get("projects", [])
        if not projects:
            print(f"{Fore.YELLOW}No projects found in workspace '{os.path.basename(workspace_path)}'. Nothing to build.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Bro-tip: Use 'brocode create project <name>' to add projects.{Style.RESET_ALL}")
            return

        build_dir = os.path.join(workspace_path, "build")
        install_dir = os.path.join(workspace_path, "install")
        
        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(install_dir, exist_ok=True) # Ensure install directory exists for artifacts

        overall_success = True
        for project_name in projects:
            print(f"\n{Fore.MAGENTA}--- Building project: {project_name} ---{Style.RESET_ALL}")
            project_path = os.path.join("src", project_name)
            project_manifest_path = os.path.join(project_path, BROS_PROJECT_MANIFEST_FILE)

            if not os.path.exists(project_manifest_path):
                print(f"{Fore.RED}  Error: Project manifest '{project_manifest_path}' not found for project '{project_name}'. Skipping.{Style.RESET_ALL}")
                overall_success = False
                continue

            try:
                with open(project_manifest_path, 'r') as f:
                    project_manifest = yaml.safe_load(f)
                
                executables = project_manifest.get("executables", [])
                if not executables:
                    print(f"{Fore.YELLOW}  No executables (nodes) defined in '{project_name}'. Nothing to build in this project.{Style.RESET_ALL}")
                    continue

                for executable_name in executables:
                    bend_node_file = os.path.join(project_path, "nodes", f"{executable_name}.bend")
                    
                    print(f"  {Fore.CYAN}Compiling {executable_name} from {bend_node_file}...{Style.RESET_ALL}")

                    # Simulate compilation process
                    if os.path.exists(bend_node_file):
                        # Create a placeholder executable in build/ and install/
                        # In a real scenario, bendc would generate actual binaries
                        build_artifact_path = os.path.join(build_dir, f"{executable_name}")
                        install_artifact_path = os.path.join(install_dir, f"{executable_name}") # Often installed executables go directly here or in a bin/ subdir

                        with open(build_artifact_path, 'w') as f:
                            f.write(f"#!/usr/bin/env bendlang_runtime\n")
                            f.write(f"# This is a placeholder executable for {executable_name} (Built by BROS)\n")
                            f.write(f"# In a real BROS system, this would be a compiled GPU-native binary.\n")
                        os.chmod(build_artifact_path, 0o755) # Make it executable

                        # Also "install" it (copy or link)
                        import shutil
                        shutil.copy(build_artifact_path, install_artifact_path)
                        os.chmod(install_artifact_path, 0o755) # Make it executable

                        print(f"  {Fore.GREEN}Successfully built and installed: {executable_name}{Style.RESET_ALL}")
                        print(f"    Build artifact: {os.path.relpath(build_artifact_path, workspace_path)}{Style.RESET_ALL}")
                        print(f"    Install artifact: {os.path.relpath(install_artifact_path, workspace_path)}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}  Error: Source file for '{executable_name}' not found at '{bend_node_file}'. Skipping.{Style.RESET_ALL}")
                        overall_success = False

            except Exception as e:
                print(f"{Fore.RED}  Error processing project '{project_name}': {e}{Style.RESET_ALL}")
                overall_success = False
                
        print(f"\n{Fore.CYAN}--- BROS Build Summary ---{Style.RESET_ALL}")
        if overall_success:
            print(f"{Fore.GREEN}All selected projects built successfully! Your GPU is ready!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Bro-tip: Now you can launch your nodes!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Build completed with errors. Check the logs above.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Bro-tip: Even the best code needs debugging. Stay strong, bro!{Style.RESET_ALL}")

    except FileNotFoundError:
        print(f"{Fore.RED}Error: Workspace config file '{BROS_WORKSPACE_CONFIG_FILE}' not found. Are you in a BROS workspace?{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: Ensure you're in a workspace, or it exists.{Style.RESET_ALL}")
    except yaml.YAMLError as e:
        print(f"{Fore.RED}Error parsing YAML file: {e}. Check your workspace config or project manifests.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred during build: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: This shouldn't happen. Report this to your bros!{Style.RESET_ALL}")
    finally:
        os.chdir(original_cwd) # Return to the original directory


def launch_nodes(launch_file_path):
    """
    Simulates launching BROS nodes based on a .bendlaunch file.
    """
    workspace_path = _get_workspace_path()
    if not workspace_path:
        print(f"{Fore.RED}Error: Not in a BROS workspace. Cannot launch nodes.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: Navigate into your workspace before launching.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}Bro-tip: Launching into the BROS runtime! Prepare for high-performance robot action!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Loading launch file: {launch_file_path}{Style.RESET_ALL}")

    original_cwd = os.getcwd()
    os.chdir(workspace_path) # Operate from workspace root

    try:
        # Load the .bendlaunch file (using YAML for now to simulate structured content)
        # In a real Bendlang system, this would be a custom parser for .bendlaunch syntax
        with open(launch_file_path, 'r') as f:
            launch_config = yaml.safe_load(f)

        if not launch_config or "launch" not in launch_config:
            print(f"{Fore.RED}Error: Invalid launch file format. 'launch' key not found.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Bro-tip: Ensure your .bendlaunch file follows the correct structure.{Style.RESET_ALL}")
            return

        system_name = next(iter(launch_config["launch"])) # Get the name of the system
        nodes_to_launch = launch_config["launch"][system_name]

        if not nodes_to_launch:
            print(f"{Fore.YELLOW}No nodes defined in launch file '{launch_file_path}'. Nothing to launch.{Style.RESET_ALL}")
            return

        install_dir = os.path.join(workspace_path, "install")

        print(f"\n{Fore.MAGENTA}--- Launching System: {system_name} ---{Style.RESET_ALL}")
        launched_nodes = []

        for node_config in nodes_to_launch:
            # Assuming a structure like:
            # - node: "sensor_publisher"
            #   from: "my_sensors_pkg"
            #   executable: "lidar_publisher_node"
            #   args: ["--port", "/dev/ttyUSB0"]
            #   remap: {"/old_topic": "/new_topic"}
            #   params: {"~filter_alpha": 0.9}

            node_name_in_launch = node_config.get("node")
            project_name = node_config.get("from")
            executable_name = node_config.get("executable")
            args = node_config.get("args", [])
            remap = node_config.get("remap", {})
            params = node_config.get("params", {})

            if not all([node_name_in_launch, project_name, executable_name]):
                print(f"{Fore.RED}  Error: Malformed node entry in launch file. Missing 'node', 'from', or 'executable'. Skipping.{Style.RESET_ALL}")
                continue

            # Construct the path to the executable in the install directory
            executable_path = os.path.join(install_dir, executable_name)

            if not os.path.exists(executable_path):
                print(f"{Fore.RED}  Error: Executable '{executable_name}' not found at '{executable_path}'. Did you build it? Skipping.{Style.RESET_ALL}")
                continue

            print(f"  {Fore.BLUE}Launching node: {node_name_in_launch} ({executable_name}) from project '{project_name}'{Style.RESET_ALL}")
            if args:
                print(f"    {Fore.LIGHTBLACK_EX}Arguments: {args}{Style.RESET_ALL}")
            if remap:
                print(f"    {Fore.LIGHTBLACK_EX}Remappings: {remap}{Style.RESET_ALL}")
            if params:
                print(f"    {Fore.LIGHTBLACK_EX}Parameters: {params}{Style.RESET_ALL}")

            # Simulate running the node. In a real system, this would be a subprocess call.
            print(f"    {Fore.GREEN}[SIMULATING] Executing: {executable_path}{' ' + ' '.join(args) if args else ''}{Style.RESET_ALL}")
            launched_nodes.append(node_name_in_launch)
            time.sleep(0.5) # Simulate startup time

        if launched_nodes:
            print(f"\n{Fore.GREEN}All specified nodes launched successfully! Your robot is alive!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Bro-tip: Keep an eye on your log files for node output.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No nodes were launched due to errors or empty launch configuration.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Bro-tip: Double-check your launch file and ensure nodes are built.{Style.RESET_ALL}")

    except FileNotFoundError:
        print(f"{Fore.RED}Error: Launch file '{launch_file_path}' not found.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: Check the path and file name. Is it in the right place?{Style.RESET_ALL}")
    except yaml.YAMLError as e:
        print(f"{Fore.RED}Error parsing launch file YAML: {e}. Check its syntax.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred during launch: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Bro-tip: Even the best bros hit snags. Report this.{Style.RESET_ALL}")
    finally:
        os.chdir(original_cwd) # Return to the original directory


def main():
    parser = argparse.ArgumentParser(
        description=f"{Fore.CYAN}BROS CLI Tool for robotics development. Your partner in GPU-native glory!{Style.RESET_ALL}",
        epilog=f"{Fore.MAGENTA}Use '{Style.BRIGHT}brocode <command> --help{Style.RESET_ALL}{Fore.MAGENTA}' for more information on a specific command. Let's make robots better!{Style.RESET_ALL}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- 'create' command parser ---
    create_parser = subparsers.add_parser(
        "create",
        help=f"{Fore.GREEN}Commands for creating new BROS entities (workspace, project, node).{Style.RESET_ALL}"
    )
    create_subparsers = create_parser.add_subparsers(dest="create_command", help="Create commands")

    # 'create workspace' sub-command
    workspace_parser = create_subparsers.add_parser(
        "workspace",
        help=f"{Fore.GREEN}Create a new BROS workspace.{Style.RESET_ALL}",
        description="Initializes a new BROS workspace directory structure."
    )
    workspace_parser.add_argument(
        "name",
        type=str,
        help="Name of the new workspace."
    )
    workspace_parser.set_defaults(func=lambda args: create_workspace(args.name))

    # 'create project' sub-command
    project_parser = create_subparsers.add_parser(
        "project",
        help=f"{Fore.GREEN}Create a new BROS project within the current workspace.{Style.RESET_ALL}",
        description="Scaffolds a new project directory with manifest file."
    )
    project_parser.add_argument(
        "project_name",
        type=str,
        help="Name of the new project."
    )
    project_parser.set_defaults(func=lambda args: create_project(args.project_name))

    # 'create node' sub-command
    node_parser = create_subparsers.add_parser(
        "node",
        help=f"{Fore.GREEN}Create a new BROS node (Bendlang file).{Style.RESET_ALL}",
        description="Generates boilerplate Bendlang code for a new node (publisher, subscriber, or service)."
    )
    node_parser.add_argument(
        "node_name",
        type=str,
        help="Name of the new node (e.g., 'lidar_publisher', 'odom_calculator')."
    )
    node_parser.add_argument(
        "--type",
        choices=["pub", "sub", "service"],
        required=True,
        help="Type of the node to create ('pub' for publisher, 'sub' for subscriber, 'service' for service server)."
    )
    node_parser.add_argument(
        "--project",
        type=str,
        help="Optional: The name of the project to create the node in. If not provided, it assumes the current directory is within a BROS project."
    )
    node_parser.set_defaults(func=lambda args: create_node(args.node_name, args.type, args.project))

    # --- 'build' command parser ---
    build_parser = subparsers.add_parser(
        "build",
        help=f"{Fore.GREEN}Build BROS projects in the current workspace.{Style.RESET_ALL}",
        description="Discovers and 'compiles' all Bendlang nodes within the workspace."
    )
    build_parser.set_defaults(func=lambda args: build_projects())

    # --- 'launch' command parser ---
    launch_parser = subparsers.add_parser(
        "launch",
        help=f"{Fore.GREEN}Launch BROS nodes from a .bendlaunch file.{Style.RESET_ALL}",
        description="Executes multiple compiled Bendlang nodes based on a structured launch file."
    )
    launch_parser.add_argument(
        "launch_file",
        type=str,
        help="Path to the .bendlaunch file (e.g., 'my_robot_system.bendlaunch')."
    )
    launch_parser.set_defaults(func=lambda args: launch_nodes(args.launch_file))


    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        # If no subcommand is given, print help and a bro-tip
        parser.print_help()
        print(f"\n{Fore.CYAN}Bro-tip: Command not found or incomplete. The brocode always guides!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
