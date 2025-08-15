import random
from fastmcp import FastMCP
import os
import sys
import importlib.util

# ===================================== import modules as path =====================================
def import_module_from_path(file_path, module_name=None):
    """
    Dynamically imports a Python module from a given file path.

    Args:
        file_path (str): The absolute path to the .py file.
        module_name (str, optional): The name to assign to the imported module.
                                     If None, the base filename (without .py)
                                     is used as the module name.

    Returns:
        module: The imported module object.

    Raises:
        FileNotFoundError: If the file_path does not exist.
        ImportError: If there's an issue importing the module.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Module file not found: {file_path}")

    if module_name is None:
        module_name = os.path.splitext(os.path.basename(file_path))[0] # 1.2.1, 1.2.4

    # Create a module specification
    spec = importlib.util.spec_from_file_location(module_name, file_path) # 1.1.1, 1.8.4

    if spec is None:
        raise ImportError(f"Could not create module spec for: {file_path}")

    # Create a module object
    module = importlib.util.module_from_spec(spec) # 1.1.1, 1.8.4

    # Add the module to sys.modules (makes it behave like a regular import)
    sys.modules[module_name] = module # 1.1.3, 1.3.4

    # Execute the module's code
    spec.loader.exec_module(module) # 1.1.1, 1.3.2

    return module

# ==================================================================================================

database_module = import_module_from_path("/workspaces/query-mcp/mcp/mcp_server/database.py")

DatabaseManager = database_module.DatabaseManager

mcp = FastMCP(name="Query MCP")
postgres = "postgres"
db_manager = DatabaseManager(
    db_name=postgres,
    host="localhost",
    password=postgres,
    port=5432,
    user=postgres,
) 

@mcp.tool
def roll_dice(n_dice: int) -> list[int]:
    """Roll `n_dice` 6-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]

if __name__ == "__main__":
    # # for debug purpose only 
    # print("server",os.getcwd())
    # with open("/workspaces/query-mcp/extra/log.txt", "w+") as f:
    #     f.write("server "+os.getcwd()+"\n")
    #     f.write(db_manager.get_name()+"\n")
    mcp.run()
