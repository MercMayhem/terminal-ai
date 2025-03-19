import subprocess
from autogen.tools import Tool

def list_docker_containers() -> str:
    try:
        result = subprocess.run(["docker", "ps"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout if result.stdout.strip() else "No running Docker containers."
    except FileNotFoundError:
        return "Docker is not installed or not in the PATH."
    except subprocess.CalledProcessError as e:
        return f"Failed to list Docker containers: {e.stderr}"
    except Exception as e:
        return f"An error occurred while listing Docker containers: {e}"

docker_ps_tool = Tool(
    name="docker_ps",
    description="List all running Docker containers.",
    func_or_tool=list_docker_containers
)
