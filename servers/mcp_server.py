from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP()

# Simple tool
@mcp.tool()
def dice_roll(sides: int) -> int:
    """
    Roll a dice with the given number of sides.
    Parameters:
        sides (int): Number of sides on the dice.
    """
    return random.randint(1, sides)

mcp.run(
    transport="stdio" # Or streamable-http for web servers
)