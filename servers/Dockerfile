# Use a small official Python image
FROM python:3.11-slim

# Work inside /app in the container
WORKDIR /app

# Copy your MCP server into the image
COPY mcp_server.py /app/mcp_server.py

# Install the MCP Python SDK (provides mcp.server.fastmcp)
RUN pip install --no-cache-dir "mcp"

# Make sure Python doesn't buffer stdout/stderr,
# which can otherwise delay communication over stdio.
ENV PYTHONUNBUFFERED=1

# When the container starts, run your MCP server
ENTRYPOINT ["python", "/app/mcp_server.py"]

# To build the Docker image, run the following command in the terminal:
# docker build -t dice-mcp-server .

# Than there are two options, to use it with a MCP host:

# 1) Add a new entry in the mcp_config.json file of your MCP host:

# {
#   "mcpServers": {
#     "dice-docker": {
#       "command": "docker",
#       "args": [
#         "run",
#         "--rm",
#         "-i",
#         "dice-mcp-server"
#       ],
#       "env": {}
#     }
#   }
# }

# 2) Create a custom catalog in Docker
# This way, the server will be accessible just like any other MCP server in the catalog.

# Create a new catalog (if you don't have one already):
# docker mcp catalog create custom-servers

# Create a new entry for your server in the custom catalog:
# dice-mcp-server:
#     dateAdded: "2025-11-27T00:00:00Z"
#     description: "Local dice rolling MCP server"
#     image: dice-mcp-server:latest
#     metadata:
#       category: utilities
#       license: MIT
#       owner: local
#       tags:
#         - dice
#         - random
#     prompts: 0
#     readme: ""
#     ref: ""
#     resources: {}
#     source: ""
#     title: "Dice MCP Server"
#     type: server
# Store this as a temporary YAML file and then run:
# docker mcp catalog add custom-servers dice-mcp-server temp.yaml

# Enable the server:
# docker mcp server enable dice-mcp-server