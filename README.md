# BROS (Better ROS)

## 🚀 Welcome to BROS: Better Robotics Operating System

BROS is an ambitious, next-generation robotics framework designed to overcome the limitations of traditional robotics middleware like ROS2. Our core vision is to build a modern, GPU-native ecosystem that excels at parallelism and scales efficiently across CPU and GPU cores, eliminating the overhead of complex infrastructure and CUDA boilerplate.

Inspired by the developer experience of `colcon` but built for unparalleled performance, BROS aims to empower robotics engineers with a streamlined workflow and unprecedented computational efficiency.

### ✨ Key Principles

* **GPU-Native Performance:** Leverage Bendlang, a language built for parallelism, to run critical robotics algorithms directly on the GPU.

* **Minimal Overhead:** Direct integration with Fast DDS (Data Distribution Service) for lean and high-performance inter-node communication.

* **Developer-Friendly Tooling:** A powerful command-line interface (`brocode`) to manage workspaces, projects, nodes, builds, and launches seamlessly.

* **Simplified Architecture:** A lightweight framework free from unnecessary layers and complexity.

### 🧠 Core Ideas

1.  **`brocode` CLI Tool:** Your primary interface for scaffolding, building, and running robot software components.

2.  **Fast DDS Integration:** The high-speed communication backbone for all BROS modules.

3.  **ROS Code Conversion (Future):** Tools to help migrate existing ROS packages to the BROS ecosystem.

4.  **Optimized Core Functionality:** Re-implementing high-impact robotics packages (like SLAM, navigation) to maximize GPU utilization and simplicity.

### 🛠️ Getting Started

To begin developing with BROS, you'll primarily interact with the `brocode` CLI.

#### 1. Prerequisites

* **Python 3.x:** Ensure you have Python installed.

* **PyYAML:** A Python library for handling YAML files.

    ```bash
    pip install PyYAML
    ```

#### 2. Install `brocode` CLI (Local Development)

For now, you can run the `brocode` CLI directly from its source.

1.  Clone this repository:

    ```bash
    git clone [https://github.com/your-username/bros.git](https://github.com/your-username/bros.git) # Replace with your actual repo URL
    cd bros
    ```

2.  Navigate to the `brocode` CLI directory:

    ```bash
    cd src/brocode_cli
    ```

3.  You can then invoke `brocode` commands using `python brocode.py`:

    ```bash
    python brocode.py --help
    ```

#### 3. Creating Your First BROS Workspace & Project

Refer to the [Getting Started Guide](docs/en/getting_started.md) for a detailed walkthrough on setting up your first BROS workspace and project.

### 📂 Repository Structure

For an in-depth understanding of the project's layout, please see the [Architecture Documentation](docs/en/architecture.md). A high-level overview is provided in the [docs/README.md](docs/README.md).

### 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### 📜 License

BROS is released under the [LICENSE](LICENSE) (e.g., Apache 2.0).