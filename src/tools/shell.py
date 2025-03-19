import shutil
from autogen.tools import Tool

def _is_command_available(command: str) -> str:
    if shutil.which(command):
        return f"'{command}' is available."
    return f"'{command}' is NOT available or not in the PATH."

check_command_tool = Tool(
    name="check_command",
    description="Check if a specific CLI command is available in the system PATH.",
    func_or_tool=_is_command_available
)
