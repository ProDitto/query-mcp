from fastmcp import FastMCP, Context
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

# @mcp.tool
# def roll_dice(n_dice: int) -> list[int]:
#     """Roll `n_dice` 6-sided dice and return the results."""
#     return [random.randint(1, 6) for _ in range(n_dice)]

# # Base Images Tools
# @mcp.tool
# def create_base_image(name: str, version: str, release_date: Optional[date] = None) -> Optional[int]:
#     """
#     Create a new base image entry in the database.
    
#     Args:
#         name: Name of the base image (e.g., "ubuntu")
#         version: Version of the base image (e.g., "20.04")
#         release_date: Optional release date of the base image
        
#     Returns:
#         The ID of the newly created base image or None if creation failed
#     """
#     return db_manager.create_base_image(name, version, release_date)

# @mcp.tool
# def get_base_images(name_filter: Optional[str] = None, 
#                    version_filter: Optional[str] = None) -> List[Dict]:
#     """
#     Retrieve base images, optionally filtered by name or version.
    
#     Args:
#         name_filter: Optional string to filter base image names (partial match)
#         version_filter: Optional string to filter base image versions (partial match)
        
#     Returns:
#         List of dictionaries representing base image records
#     """
#     results = db_manager.get_base_images(name_filter, version_filter)
#     return [dict(zip(['id', 'name', 'version', 'release_date'], row)) for row in results]

# # Packages Tools
# @mcp.tool
# def create_package(name: str, base_image_id: int) -> Optional[int]:
#     """
#     Create a new package associated with a base image.
    
#     Args:
#         name: Name of the package (e.g., "openssl")
#         base_image_id: ID of the associated base image
        
#     Returns:
#         The ID of the newly created package or None if creation failed
#     """
#     return db_manager.create_package(name, base_image_id)

# @mcp.tool
# def get_packages_for_base_image(base_image_id: int) -> List[Dict]:
#     """
#     Retrieve all packages associated with a specific base image.
    
#     Args:
#         base_image_id: ID of the base image
    
#     Returns:
#         List of dictionaries representing package records
#     """
#     results = db_manager.get_packages_for_base_image(base_image_id)
#     return [dict(zip(['id', 'name', 'base_image_id'], row)) for row in results]

# # Package Tags Tools
# @mcp.tool
# def create_package_tag(package_id: int, tag: str) -> Optional[int]:
#     """
#     Create a new tag for a package.
    
#     Args:
#         package_id: ID of the package
#         tag: Tag name/version (e.g., "1.1.1")
        
#     Returns:
#         The ID of the newly created tag or None if creation failed
#     """
#     return db_manager.create_package_tag(package_id, tag)

# @mcp.tool
# def get_tags_for_package(package_id: int) -> List[Dict]:
#     """
#     Retrieve all tags associated with a specific package.
    
#     Args:
#         package_id: ID of the package
    
#     Returns:
#         List of dictionaries representing package tag records
#     """
#     results = db_manager.get_tags_for_package(package_id)
#     return [dict(zip(['id', 'package_id', 'tag', 'created_at'], row)) for row in results]

# # Vulnerabilities Tools
# @mcp.tool
# def create_vulnerability(cve_id: str, 
#                         description: Optional[str] = None, 
#                         discovered_at: Optional[date] = None) -> Optional[int]:
#     """
#     Create a new vulnerability record.
    
#     Args:
#         cve_id: CVE identifier (e.g., "CVE-2022-2068")
#         description: Optional description of the vulnerability
#         discovered_at: Optional date the vulnerability was discovered
        
#     Returns:
#         The ID of the newly created vulnerability or None if creation failed
#     """
#     return db_manager.create_vulnerability(cve_id, description, discovered_at)

# @mcp.tool
# def get_vulnerability_by_cve(cve_id: str) -> Optional[Dict]:
#     """
#     Retrieve a vulnerability by its CVE ID.
    
#     Args:
#         cve_id: CVE identifier (e.g., "CVE-2022-2068")
    
#     Returns:
#         Dictionary representing the vulnerability record or None if not found
#     """
#     result = db_manager.get_vulnerability_by_cve(cve_id)
#     if result:
#         return dict(zip(['id', 'cve_id', 'description', 'discovered_at'], result))
#     return None

# # Tag-Vulnerability Relationship Tools
# @mcp.tool
# def add_vulnerability_to_tag(package_tag_id: int, 
#                            vulnerability_id: int, 
#                            severity: Optional[str] = None) -> bool:
#     """
#     Associate a vulnerability with a package tag.
    
#     Args:
#         package_tag_id: ID of the package tag
#         vulnerability_id: ID of the vulnerability
#         severity: Optional severity level (e.g., "HIGH", "MEDIUM", "LOW")
        
#     Returns:
#         True if the association was successful, False otherwise
#     """
#     return db_manager.add_vulnerability_to_tag(package_tag_id, vulnerability_id, severity)

# @mcp.tool
# def get_vulnerabilities_for_tag(package_tag_id: int) -> List[Dict]:
#     """
#     Retrieve all vulnerabilities associated with a package tag.
    
#     Args:
#         package_tag_id: ID of the package tag
    
#     Returns:
#         List of dictionaries with vulnerability information and severity
#     """
#     results = db_manager.get_vulnerabilities_for_tag(package_tag_id)
#     return [dict(zip(['id', 'cve_id', 'description', 'discovered_at', 'severity'], row)) for row in results]

# # Commits Tools
# @mcp.tool
# def create_commit(package_tag_id: int, 
#                  commit_hash: str, 
#                  author: Optional[str] = None, 
#                  message: Optional[str] = None) -> Optional[int]:
#     """
#     Create a new commit record associated with a package tag.
    
#     Args:
#         package_tag_id: ID of the package tag
#         commit_hash: Git commit hash (e.g., "a1b2c3d4e5f6")
#         author: Optional author name
#         message: Optional commit message
        
#     Returns:
#         The ID of the newly created commit or None if creation failed
#     """
#     return db_manager.create_commit(package_tag_id, commit_hash, author, message)

# @mcp.tool
# def get_commits_for_tag(package_tag_id: int) -> List[Dict]:
#     """
#     Retrieve all commits associated with a package tag.
    
#     Args:
#         package_tag_id: ID of the package tag
    
#     Returns:
#         List of dictionaries representing commit records
#     """
#     results = db_manager.get_commits_for_tag(package_tag_id)
#     return [dict(zip(['id', 'package_tag_id', 'commit_hash', 'author', 'committed_at', 'message'], row)) for row in results]

# # Database Management Tools
# @mcp.tool
# def reset_database() -> str:
#     """
#     Reset the entire database (warning: this will delete all data).
    
#     Returns:
#         Status message indicating success or failure
#     """
#     try:
#         db_manager.reset_database()
#         seed_result = db_manager.setup_database()
#         return f"Database reset and schema recreated successfully; {seed_result}"
#     except Exception as e:
#         return f"Error resetting database: {str(e)}"

SCHEMA_BRIEF = """
format: `tablename: attributes`
- base_images: id(int,pk), name(str), version(str), release_date(date)
- packages: id(int, pk), name(str), base_image_id(fk)
- package_tags: id(int,pk), package_id(fk), tag(str), created_at(timestamp)
- vulnerabilities: id(int,pk), cve_id(str,unique), description(str), discovered_at(date)
- tag_vulnerabilities: package_tag_id(fk), vulnerability_id(fk), severity(str)
- commits: id(int,pk), package_tag_id(fk), commit_hash(str,unique), author(str), committed_at(timestamp), message(str)
* indexes for performance
- idx_packages_base_image ON packages(base_image_id);
- idx_tags_package_id ON package_tags(package_id);
- idx_tag_vuln_vulnerability_id ON tag_vulnerabilities(vulnerability_id);
- idx_commits_package_tag_id ON commits(package_tag_id);
"""

# Get Database Schema
@mcp.resource("schema://database")
def get_schema_resource() -> str:
    """Returns a brief description of the PostgreSQL database schema."""
    return SCHEMA_BRIEF

@mcp.tool(
    name="execute_raw_query",
    description="Execute arbitrary SQL query (SELECT) using database manager.",
    annotations={"readOnlyHint": False, "openWorldHint": True}
)
async def tool_execute_raw_query(query: str, ctx: Context) -> list[list]:
    """Executes the query and returns rows; logs schema context for reference."""
    # Fetch schema context
    # resource_contents = await ctx.read_resource("schema://database")
    # schema_text = ""
    # for part in resource_contents:
    #     if hasattr(part, "content") and isinstance(part.content, str):
    #         schema_text = part.content
    #         break

    # await ctx.info("Executing query using the following schema:\n" + schema_text)
    await ctx.info("Executing query :\n" + query)

    try:
        rows = db_manager.execute_raw_query(query)
        return [list(row) for row in (rows or [])]
    except Exception as e:
        await ctx.error(f"Error executing raw query: {e}")
        raise


@mcp.tool(
    name="get_schema",
    description="Retrieve the database schema description.",
    annotations={
        "title": "Get Database Schema",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def tool_get_schema(ctx: Context) -> str:
    """Returns a brief description of the PostgreSQL database schema."""
    await ctx.info("Tool `get_schema` invoked. Delivering schema details.")
    schema = SCHEMA_BRIEF
    return schema


if __name__ == "__main__":
    mcp.run()
    db_manager.close_connection()
