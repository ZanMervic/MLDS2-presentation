# MCP Lecture – Key Phrases & Anchors (Slide by Slide)

## Slide 1 – Title / Framing
- “Second part of the lecture: **Model Context Protocol (MCP)**”
- What we’ll cover:
  - what MCP is
  - why it matters
  - when to use it
  - how it works
  - demo: connecting MCP servers to AI apps

---

## Slide 2 – From Classic Agents to Integration Headaches
**Transition:** “In the first part, you saw how to build simple agents with tools.”

- Tools give agents access to:
  - APIs, databases, search, internal systems
- Works fine for a few tools
- Problem at **production scale**
- Each integration requires:
  - custom code
  - different schemas
  - auth, rate limits, error handling
- Leads to **M × N integration problem**
- Motivation for MCP: **reduce fragmentation**

---

## Slide 3 – What is MCP? (Definition + Analogy)
**Definition (memorize):**
- “**MCP is an open-source standard for connecting AI applications to external systems.**”
- Client–server protocol
- Created by Anthropic, adopted by OpenAI, Google, Microsoft, IBM, etc.

**Analogy (memorize):**
- “MCP is like **USB-C for AI applications**”

**Important clarification (memorize):**
- MCP does **not** give models new powers
- Tool calling already existed
- MCP provides:
  - standardization
  - reuse
  - scalability
- Value: **integration, not intelligence**

---

## Slide 4 – MCP Adoption / Google Trends
**Transition:** “Let’s quickly look at adoption.”

- Released November 2024
- Growing interest over time
- Similar trend to:
  - “AI Agents”
  - “n8n”
- Hype peaked, but relevance remains
- Worth knowing even if not used everywhere

---

## Slide 5 – MCP Architecture: Host, Client, Server
**Core idea:** Host–client–server model

### Host
- The AI application (Claude Desktop, ChatGPT, VS Code, n8n, etc.)
- Responsibilities:
  - run the model
  - manage MCP clients
  - aggregate context
  - enforce permissions & security

### MCP Client
- One client per server
- Negotiates capabilities
- Handles communication

### MCP Server
- Where integration logic lives
- Wraps:
  - APIs
  - databases
  - filesystem
- Can be local or remote

**Flow (memorize):**
- LLM → host → MCP client → MCP server → real system → back

---

## Slide 6 – MCP Primitives
**Transition:** “What can an MCP server actually expose?”

### Resources
- Read-only data
- Host decides how to include them

### Tools
- Actions with side effects
- Model can invoke them

### Prompts
- Reusable prompt templates
- Centralized instructions
- Shared across hosts

**Key idea:**
- Server advertises capabilities
- Host exposes them to the model
- Any combination possible

---

## Slide 7 – Transports
**Purpose:** How clients talk to servers

- Protocol: **JSON-RPC**
- Two transports:

### stdio
- Local servers
- Filesystem, local tools

### Streamable HTTP
- Remote servers
- Single HTTP endpoint
- Used for hosted services

---

## Slide 8 – MCP in Action (Workflow Example)
**Scenario:** “What’s the weather in Ljubljana?”

Steps:
1. Host already knows available tools
2. LLM sees `get_weather` tool in context
3. LLM requests tool with parameter
4. Host may ask user for permission
5. Server executes request
6. Result sent back
7. LLM generates final answer

**Key intuition:**
- Model decides *what* to call
- Host controls *whether* it’s allowed

---

## Slide 7 (Why MCP Matters)
**Problem before MCP:**
- One integration per app
- Rewriting same logic repeatedly

Repeated work:
- schemas
- auth
- retries
- logging
- edge cases

**With MCP:**
- One server, many hosts
- Discoverable capabilities
- Host remains in control

**Core message (memorize):**
- MCP makes integrations **portable, reusable, governable**

---

## Slide 8 – MCP Server Implementation (Demo)
**Transition:** “Let’s see a minimal MCP server.”

Key points:
- Python example using official SDK
- Components:
  - tool
  - resource
  - prompt
- Steps:
  1. Import `FastMCP`
  2. Instantiate server
  3. Define functions
  4. Decorators turn them into MCP primitives
  5. Choose transport

**Takeaway:**
- Complete MCP server with minimal code
- Logic written once, reused everywhere

---

## Slide 8.1 – When MCP Is Overkill
**Transition:** “MCP is not always the right choice.”

- Simple agent:
  - ~25 lines of code
- MCP host:
  - ~165 lines of code
- Building a host is complex

**Guideline (memorize):**
- Small projects → classic tools
- Large-scale, many tools → MCP

---

## Slide 8.2 – MCP with Existing Hosts
**Key benefit:** Ecosystem reuse

- Existing MCP hosts:
  - Claude Desktop
  - GitHub Copilot
  - Cursor

### Adding servers
- Docker-based (easiest)
- Or manual `mcp_config.json`

**Key idea:**
- You don’t need to build your own host
- Plug servers into existing apps

---

## Slide 9 – Code Execution with MCP
**Context:** Scaling problems

Problems:
- Tool definitions bloat context
- Large tool outputs increase cost

**Anthropic solution:**
- Code execution environment
- Tools imported as functions

Benefits:
- Huge token reduction (~98%)
- Better privacy
- More efficient workflows

**Tradeoff:**
- More complexity
- Requires sandboxing

**Guideline:**
- Simple agents → direct tools
- Enterprise scale → code execution

---

## Final Closing Anchor
- MCP is about **scaling integrations**
- Not required everywhere
- Extremely powerful when complexity grows
