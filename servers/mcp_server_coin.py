from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP()


# Simple tool
@mcp.tool()
def unfair_coin_toss(p_heads: float) -> int:
    """
    Toss an unfair coin that lands on heads with probability p_heads.
    Returns 1 for heads and 0 for tails.

    Parameters:
        p_heads (float): Probability of landing on heads (between 0 and 1).
    """
    return random.choices([0, 1], weights=[1 - p_heads, p_heads])[0]


mcp.run(transport="stdio")  # Or streamable-http for web servers
