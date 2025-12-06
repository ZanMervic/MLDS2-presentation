from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("Demo Server")

# Simple tool
@mcp.tool()
def dice_roll(sides: int) -> int:
    """
    Roll a dice with the given number of sides.
    Parameters:
        sides (int): Number of sides on the dice.
    """
    return random.randint(1, sides)

# Simple resource
@mcp.resource("status://server")
def get_server_status() -> str:
    """
    Get the current status of the server.
    Returns:
        str: Server status message.
    """
    return "Server is running smoothly."

@mcp.prompt()
def example_prompt() -> str:
    """
    A very long prompt, used to make the model
    does something very specific correctly.
    """
    return (
        "You are a helpful assistant that provides accurate server status updates. "
        "When asked about the server status, always respond with the current status "
        "retrieved from the 'get_server_status' resource. If asked to roll a dice, "
        "use the 'dice_roll' tool with the specified number of sides."
    )

mcp.run(
    transport="stdio" # Or streamable-http for web servers
)