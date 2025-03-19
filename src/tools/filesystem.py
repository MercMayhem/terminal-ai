from autogen.tools import Tool
import os
import glob

def get_current_directory() -> str:
    return os.getcwd()

get_current_directory_tool = Tool(
    name="current_work_dir",
    description="Get the current working directory",
    func_or_tool=get_current_directory
)

def list_directory_items(path: str = ".") -> str:
    try:
        items = os.listdir(path)
        return "\n".join(items)
    except FileNotFoundError:
        return f"Directory '{path}' not found."
    except PermissionError:
        return f"Permission denied for directory '{path}'."

list_directory_tool = Tool(
    name="list_directory",
    description="List all items in a directory. Default is the current working directory.",
    func_or_tool=list_directory_items
)

def read_file(path: str) -> str:
    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"File '{path}' not found."
    except PermissionError:
        return f"Permission denied for file '{path}'."
    except Exception as e:
        return f"Failed to read file '{path}': {e}"

read_file_tool = Tool(
    name="read_file",
    description="Read the contents of a file.",
    func_or_tool=read_file
)

def write_file(path: str, content: str) -> str:
    try:
        with open(path, "w") as file:
            file.write(content)
        return f"Successfully wrote to '{path}'."
    except PermissionError:
        return f"Permission denied for file '{path}'."
    except Exception as e:
        return f"Failed to write to file '{path}': {e}"

write_file_tool = Tool(
    name="write_file",
    description="Write content to a file. Creates the file if it doesn't exist.",
    func_or_tool=write_file
)

def search_files(pattern: str, path: str = ".") -> str:
    try:
        matches = glob.glob(f"{path}/**/{pattern}", recursive=True)
        if matches:
            return "\n".join(matches)
        return f"No files matching pattern '{pattern}' found in '{path}'."
    except Exception as e:
        return f"Failed to search files: {e}"

file_search_tool = Tool(
    name="search_files",
    description="Search for files matching a pattern in a directory (supports wildcards).",
    func_or_tool=search_files
)
