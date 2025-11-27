## Slide 1 – Title

**Title:**
**MCP - Model Context Protocol**

**On-slide content:**

* Big title: **“MCP - Model Context Protocol”**
* Subtitle: **“A new standard for AI integration”**
* Your name, affiliation
* Visual: AI brain/robot icon in the center connected with thin lines to icons for DB, API, cloud, email, etc.

**Script:**

“Welcome everyone. In this second part of the lecture we’ll look at what the "new" standard of connecting AI models to tools and data looks like and how to use it.
Specifically, we’ll talk about the **Model Context Protocol (MCP)** and how it connects models to tools and data, and then if we have the time we will see that plays with automation platforms like **n8n**.
---

## Slide 2 – From “Classic” Agents to Integration Headaches

**Title on slide:**
**“From tools to integration chaos”**

**On-slide content:**

Left side:

* Small text at top: **“What we saw in Part 1”**
* Simple diagram:

  * A “LLM Agent” bubble in the middle
  * 3–4 icons around it: **database**, **REST API**, **internal service**, **web search**
  * Arrows showing tool calls (like `get_users`, `http_get`, `db_query`)

Right side:

* Heading: **“Before MCP”**
* 2–3 short bullets:

  * “Each tool = custom function / plugin”
  * “Every system has its own schema, auth, error handling”
  * “Hard to scale to dozens of tools”

**Script:**

“Let’s connect this to what you saw in the **agent** part of the lecture.

In Part 1, we built agents that could call tools: maybe an HTTP request tool, a database tool, a calculator, web search… That works nicely for a handful of tools. But now imagine doing this at **production** scale.

Real agents need to talk to **many** systems:

* internal databases,
* SaaS APIs (Slack, GitHub, Notion, CRM),
* search engines, file stores, and so on.

**Before MCP**, every one of those integrations was its own little project:

* You write **custom code** for each tool,
* define a **separate function schema** or plugin,
* handle auth, rate limits, error formats, prompts… all differently.

<!-- (TODO: Perhaps show an example of "messy" code for this.) -->

This leads to what people sometimes call an **M×N integration problem**: for M tools and N models, you end up maintaining lots of bespoke glue code. MCP was proposed to address exactly this kind of fragmentation by standardizing how AI apps connect to tools and data.

So the question is:

> *How do we move from ‘one-off tools everywhere’ to a **standard way** of wiring agents to systems?*

That’s where MCP comes in.”

---

## Slide 3 – What is MCP? A Standard, Not New Powers

**Title on slide:**
**“What is MCP?”**

**On-slide text:**

* One short definition:

  > “A standardized protocol for connecting AI applications to external tools, data and services.”
* A **single** analogy:

  > “Think of MCP like a USB-C port for AI applications.”
* Small caption at bottom:

  * “Standardization layer – *not* new model abilities”

Visual:

* On the left: **AI app / Agent** icon with a small “USB-C port” symbol.
* On the right: 3–4 boxes: “DB server”, “GitHub server”, “Notion server”, “Zapier MCP server” connected via identical “MCP cable” icons.

**Script:**

“So, what exactly is MCP?

Formally, **MCP (Model Context Protocol)** is an *open-source standard* for connecting AI applications to external systems—databases, tools, services. It’s essentially a **standardization layer** between models and the outside world, defined originally by Anthropic (the company behind Claude) and now adopted by others like OpenAI, Google, Microsoft, IBM and more.

The commonly used analogy is:

> MCP is like a **USB-C port for AI applications**.

Just like USB-C gives your laptop one consistent way to plug into many devices, MCP gives AI apps one consistent way to plug into many tools and data sources.

**Important point:** MCP does **not** give LLMs any capabilities they didn’t have already.

* Before MCP, you could already do tool calling, plugins, RAG, etc.
* MCP’s value is that it **standardizes and unifies** those integrations:

  * Less custom glue for every tool,
  * Reusable MCP servers across assistants and platforms,
  * Easier sharing of integrations between developers.

So you can think of MCP as a **standard integration layer** that sits under whatever agent framework you’re using.”

---

## Slide 4 – MCP Architecture: Host, Clients, Servers

**Title on slide:**
**“MCP architecture: host, clients, servers”**

**On-slide diagram:**

* Big box labeled **“Host”** (e.g. ChatGPT Desktop, Claude Desktop, VS Code, n8n, custom app).

  * Inside: several small **“client”** boxes, each labeled “MCP client (GitHub)”, “MCP client (DB)”, etc.
* On the right: multiple **“MCP Server”** boxes:

  * “MCP server: GitHub”
  * “MCP server: Internal DB”
  * “MCP server: Zapier MCP”
* Arrows:

  * Host ↔ Clients (labeled “create/manage clients, coordinate LLM”)
  * Each Client ↔ its Server (1:1, labeled “MCP session”)

Minimal text (small bullet list in a corner):

* Host: runs the LLM / agent, manages clients, enforces security.
* Client: 1:1 connection to a server, handles protocol & capabilities.
* Server: exposes resources, tools, prompts.

**Script:**

“MCP follows a **host–client–server architecture**.

* The **host** is your AI application, e.g. Claude Desktop, ChatGPT Desktop, VS Code with Copilot, an IDE, or even a workflow tool like n8n in principle. The host:

  * runs or connects to the model,
  * creates **MCP clients**,
  * enforces permissions and security,
  * aggregates context from many servers.

* An **MCP client** is a component inside the host. Each client:

  * connects to *exactly one* MCP server,
  * negotiates capabilities (which tools/resources/prompts are available),
  * routes messages back and forth.

* An **MCP server** is where the integration lives:

  * It wraps a specific data source or service,
  * exposes **resources, tools and prompts** in a standard way,
  * can be local (e.g. your filesystem) or remote (e.g. a SaaS MCP server).

So when the model ‘calls a tool’, it’s actually going:
**LLM inside host → MCP client → MCP server → real system**,
and back again. The host never exposes the full conversation to the server; it only sends what’s needed.”

---

## Slide 5 – MCP Primitives: Resources, Tools, Prompts

**Title on slide:**
**“What can an MCP server expose?”**

**On-slide layout:**
A 3-column table (or 3 cards) with **name, definition, and a concrete example**:

1. **Resources**

   * “Read-only data or files (no side effects).”
   * Example on slide:

     * `customer://12345` → customer JSON
     * `file://reports/2025-Q1.pdf` → PDF content

2. **Tools**

   * “Operations with side effects or active logic.”
   * Example:

     * `create_jira_ticket(...)`
     * `send_email(to, subject, body)`

3. **Prompts**

   * “Reusable prompt templates / workflows.”
   * Example:

     * `summarize_support_ticket`
     * `generate_sales_email`

**Script:**

“Concretely, what can an MCP server provide to the model?

* **Resources**: think of these as **read-only data access**. The server says:

  > “Here’s a list of resources you can browse or fetch.”
  > That could be files, database rows, dashboards, etc. The model can read them but not change them directly.

* **Tools**: these are **actions or computations**. A tool might:

  * call an API,
  * run a query,
  * trigger a workflow.
    For example: `create_ticket`, `list_events`, `run_sql`.

* **Prompts**: these are **structured, reusable prompt templates or flows**. Instead of hard-coding a long system prompt into your application, you can host it behind MCP:

  * “Use this ‘summarize incident’ prompt,”
  * or “Use this multi-step analysis prompt.”

The server advertises which resources, tools, and prompts it supports; the client passes that to the model in a standard way. So one MCP server can be *just* resources, *just* prompts, *just* tools, or any combination.”

---

## Slide 5.1 – Transports: How Clients Talk to Servers

**Title on slide:**
**“How MCP messages travel: transports”**

**On-slide content:**
Two boxes in a row:

1. **stdio**

   * Caption: “Local processes (CLI tools, local DB, filesystem).”

2. **Streamable HTTP**

   * Caption: “Newer, single HTTP endpoint, bidirectional streaming.”

Small note at bottom:

* “All transports wrap **JSON-RPC 2.0** messages.”

<!-- (TODO: Educate yourself what any of this means ...) -->

**Script:**

“Between an MCP client and server, all communication is via **JSON-RPC** messages, but the actual **transport** can differ.

There are two standardized transports:

1. **stdio** – for **local** servers.

   * Great when you run a server on the same machine: e.g. a filesystem or local database wrapper.
   * Simple: messages go over stdin/stdout.

2. **Streamable HTTP** – for **remote** servers.
   * Replaces an older **SSE** transport.
   * Single HTTP endpoint for bidirectional streaming, easier to deploy and reason about.
   * The ecosystem is gradually shifting towards this as the default remote transport.

As a server author you choose which transports to support; as a host you pick whatever your environment can reach. But the **MCP layer** stays the same.”

---

## Slide 6 – MCP in Action: Example Workflow

<!-- (TODO: This slide might be obsolete, it shows nothing new compared to basic tool usage.) -->

**Title on slide:**
**“MCP in action – same agent, less custom glue”**

**On-slide visual:**
A 5-step horizontal comic:

1. User: “Summarize our top customer and this month’s sales.”
2. Agent bubble: “Need CRM + sales DB.”
3. Arrow to CRM server: `crm.find_customer("Acme")` (MCP tool).
4. Arrow to DB server: `sales.get_monthly_sales("2025-10")`.
5. Agent returns a short combined report.

Minimal labels only (“MCP call: …”, “CRM MCP server”, etc.).

**Script:**

“Let’s see this in story form.

User asks:

> ‘Give me a summary of our top customer and this month’s sales.’

The agent decides it needs two things:

* customer details from the **CRM**,
* numbers from the **sales DB**.

With MCP, that might look like:

* Call a tool on the **CRM MCP server**:
  `find_customer("Acme Corp")`
  → returns structured customer info.

* Call a tool on the **Sales DB MCP server**:
  `get_monthly_sales("2025-10")`
  → returns metrics.

Then the model writes a short report from these results.

You’re right that this *pattern*—model calls tools, gets results, then reasons—also existed **before** MCP. The key difference is **where the complexity lives**:

* Pre-MCP: you bespoke-implemented every integration (CRM plugin, DB plugin, custom code, ad-hoc prompts).
* With MCP: CRM and sales DB are each just **MCP servers**. The host and MCP client already know how to talk to them in a standardized way, and those same servers can be reused by *other* agents and hosts.

So conceptually the agent loop is the same; MCP just gives you a **cleaner, reusable interface** for that loop.”

---

## Slide 7 – Why MCP Matters (Even Though Tools Existed Before)

**Title on slide:**
**“Why MCP matters (even though tools existed before)”**

**On-slide content:**
Two-column “Before / With MCP” graphic.

Left: **Before MCP**

* “Each tool = ad-hoc integration” <!-- (TODO: Show/explain what this means) -->
* “Different schemas, auth, error handling”
* “Hard to share integrations between apps”
* “Tool definitions often duplicated across agents”

Right: **With MCP**

* “One **standard protocol** for tools/data”
* “Servers reusable across hosts (Claude, ChatGPT, VS Code, IDEs, …)”
* “Growing ecosystem: many open-source servers (GitHub, AWS docs, DBs, Zapier, n8n MCP, …)”
* “Easier enterprise governance & security boundaries”

Small note at bottom:

> “LLMs already had tool calling; MCP standardizes it.”

**Script:**

“Let’s be careful about *what* MCP changes.

**First, an important note:** LLMs could call tools **before** MCP. We had function-calling, plugins, RAG, custom frameworks, etc. MCP does **not** bring any new functionalities.

What MCP does is:

* Turn tool & data access into a **standard protocol**, similar to how REST or OpenAPI standardized web APIs.
* Make integrations **reusable**:

  * The same “GitHub MCP server” or “filesystem server” can be used by Claude, ChatGPT Desktop, VS Code Copilot Chat, Cursor, Zed, and so on.
* Encourage an ecosystem:

  * There’s already a catalog of MCP servers for things like MongoDB, Apify, Elasticsearch, Windows features, n8n, and more.
* Help with **security and governance**:

  * The host controls which servers are available, what capabilities they expose, and how much context each server sees, which is important for enterprise deployments.

So the value proposition is not ‘new capabilities’, but **scalable, interoperable, governed integration**. That’s why major players like Anthropic, OpenAI, Google, Microsoft and IBM frame it as a standardization layer rather than yet another agent framework.”

---

## Slide 8 – Using MCP in Practice (e.g. with Agents / SDKs)

**Title on slide:**
**“Using MCP in practice (e.g. with OpenAI / other Agents)”**

**On-slide visual:**
Left side: tiny pseudo-code snippet (Python-ish) showing **before**:

<!-- (TODO: show that these tools each needed to be implemented separately) -->

```python
agent = Agent(
    model="gpt-4.1",
    tools=[
        http_get_tool,
        db_query_tool,
    ],
)
```

Right side: **after** (conceptual example):

```python
agent = Agent(
    model="gpt-4.1",
    tools=[ /* maybe some built-ins */ ],
    mcp_servers={
        "internal_db": local_mcp_server("db.json"),
        "github": remote_mcp_server("https://example.com/github"),
    },
)
```

Underneath: small bullets:

* “Add MCP servers alongside or instead of bespoke tools.”
* “Reuse servers across agents & apps.”
* “Same agent logic, different integration layer.”

**Script:**

“Let’s connect this back to the type of agent you built in Part 1.

There, we did something like:

* define a few tools (HTTP, DB query, etc.),
* pass them to your agent as `tools=[…]`,
* let the model call them.

With MCP-aware frameworks—like OpenAI’s Agents SDK, VS Code’s GitHub Copilot Chat, Google’s ADK, and others—the pattern becomes:

* you still *can* keep some ‘classic’ tools,
* but you also pass a set of **MCP servers**,
* each server exposes multiple tools/resources/prompts.

So it’s **not literally** just `tools=` replaced with `mcp=`; it’s more like:

> “Here are some built-in tools, **plus** these MCP servers you can use as additional tool sources.”

Your agent logic barely changes:

* it still reasons, plans, and calls tools,
* but the inventory of tools now comes from **standard MCP servers**, not just your own handcrafted specs.

If you want to MCP-ify a tool and agent from part 1 you'd:

1. Wrap your existing API/DB logic into an MCP server (there are Python SDKs and templates for that).
2. Point the agent or host to that MCP server via its MCP config.
3. Remove the bespoke tool definitions you no longer need.

The agent’s behavior is similar, but the integration becomes cleaner and reusable.”

---

## Slide 8.1 – Minimal MCP Server in Python (for completeness)

**Title on slide:**
**“(Optional) Minimal MCP server in Python”**

**On-slide content:**

```python
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo Server", json_response=True)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

if __name__ == "__main__":
    # Serve over stdio (for local hosts like Claude Desktop)
    mcp.run(transport="stdio")
```

Small bullet list on the side:

* “`FastMCP` from the official Python MCP SDK”
* “Tools defined as normal Python functions”
* “Can also expose resources & prompts in the same server”

At the bottom, one tiny line:

* “To containerize: wrap this in a small Dockerfile that installs `mcp` and runs `server.py`.”

**Script:**

“For completeness, here’s how a **tiny MCP server in Python** might look, using the official `mcp` SDK.

* We create a `FastMCP` instance called `Demo Server`.
* We define a single tool, `add`, using the `@mcp.tool()` decorator.
* And we run the server with `transport="stdio"`, which makes it usable by local hosts like Claude Desktop or any other MCP client that wants to connect over stdio.

In a real project you would normally also expose:

* **resources** (for read-only data access),
* **prompts** (for reusable instruction templates),

all from the same Python file.

We’re *not* going to focus on coding servers live in the demo—most of you will primarily be **users** of MCP servers. But I want you to see that the implementation is relatively short and uses normal Python functions.

If you wanted to package this as a Docker image, you could:

* write a tiny `Dockerfile` that:

  * starts from `python:3.11-slim`,
  * installs `mcp[server]`,
  * copies `server.py`,
  * and sets `CMD ["python", "server.py"]`.

Then this custom server could appear in the same catalogs as other Dockerized MCP servers and be used by any host that knows how to talk to Docker-based MCP servers.”

---

## Slide 8.2 – Python: Using an MCP Server from an Agent / Client

<!-- (TODO: Understand this ...)
(TODO: Perhaps clarify, when to and when not to use MCP and instead import functions? https://www.youtube.com/watch?v=5xqFjh56AwM&t=116s&pp=ygUDTUNQ) -->

**Title on slide:**
**“(Optional) Python: connecting to an MCP server”**

**On-slide content (two-part code snippet):**

Top: **MCP client connection with stdio**

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def connect_to_server():
    params = StdioServerParameters(
        command="python",
        args=["server.py"],  # our demo server
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Available tools:", [t.name for t in tools])

asyncio.run(connect_to_server())
```

Bottom: **Conceptual “agent config” using those tools**

```python
# Pseudo-code: passing MCP tools into an agent
agent = Agent(
    model="gpt-4.1",
    tools=tools_from_mcp_session,  # tools discovered via MCP
)
```

**Script:**

“This slide is just to close the loop for those of you who *do* like seeing code.

At the top, we use the **Python MCP SDK** to connect to a local MCP server over stdio:

* `StdioServerParameters` describes how to start the server (`python server.py`).
* `stdio_client` gives us read/write streams.
* `ClientSession` handles the MCP protocol.
* We call `session.initialize()` and then `session.list_tools()` to see what the server exposes.

Once we have that list of tools, a framework-specific agent (OpenAI Agents, Google ADK, custom code, etc.) can **treat them as normal tools**:

* they’re just tool definitions with names, parameters, and descriptions—only now they came from a **standard MCP server**, not from hand-written JSON.

In practice, you won’t usually write this MCP client code yourself if you’re using a desktop app or IDE:

* Claude Desktop, VS Code, GitHub Copilot, n8n and others **implement this “client+host” logic for you**.

So think of this slide as: *“Under the hood, this is what your host does when it connects to an MCP server.”*”

---

## Demo – Using Existing MCP Servers (Docker, Claude/VS Code, n8n)

<!-- (TODO: https://www.youtube.com/watch?v=GuTcle5edjk&t=2152s&pp=ygUDbWNw) -->

**No dedicated slide required, or you can reuse Slide 8 as a backdrop.**

### Demo goals

1. Show how **ordinary users** can connect to **existing MCP servers**:

   * From Docker Desktop MCP Toolkit to Claude Desktop (or ChatGPT Desktop).
   * From VS Code via the MCP marketplace/settings.
2. Show that **your own server**, if containerized, would appear in these flows the same way.
3. Use n8n as a bridge:

   * show how n8n can use external MCP servers in a workflow,
   * and tease that we’ll dive into n8n more in the second section.

---

### Demo script

**Intro (tie-in to Slides 8.1 & 8.2):**

> “We just saw how an MCP server looks in Python, and how a client might connect to it.
> For the **live** demo, I won’t make you watch me write Python. Instead, we’ll use MCP servers that are already packaged for us—mostly via Docker—and see how to plug them into real tools like Claude Desktop, VS Code, and n8n.”

---

### Part 1 – Docker MCP Toolkit → Claude Desktop

**Steps you show:**

1. **Open Docker Desktop (MCP Toolkit / Catalog).**

   * Go to the MCP section / MCP Toolkit.
   * Show a **catalog of MCP servers** (e.g. GitHub Official, Firecrawl, Filesystem, n8n MCP, etc.).

   **Narration:**
   “Docker Desktop has a **MCP Toolkit** that lets you spin up many MCP servers in one click—GitHub, Docker CLI, Kubernetes, Firecrawl, n8n MCP, and so on.”

2. **Select one or two servers and add them.**

   * Click “Add” / “Install” on e.g. **GitHub Official** and **n8n MCP**.
   * Docker pulls and starts the containers.

   **Narration:**
   “I’ll enable the GitHub MCP server and the n8n MCP server from this catalog. Under the hood, these are just **Docker images** that expose an MCP endpoint, very similar to how our Python `server.py` could be containerized.”

3. **Connect to Claude Desktop.**

   * In the Docker MCP Toolkit UI, click “Connect to Claude Desktop” (or show the step where it writes into `claude_desktop_config.json`).

   **Narration:**
   “With one click, Docker writes the MCP configuration into Claude Desktop’s MPC config JSON. That tells Claude:

   > ‘When you start, also start these MCP servers and connect to them.’”

4. **Switch to Claude Desktop.**

   * Open Claude Desktop, start a new chat.
   * Show that the GitHub server and n8n MCP server appear in the tools/resources panel.

   **Narration:**
   “When Claude Desktop boots up, it reads that config and starts these MCP servers as part of the host. Now Claude can use tools from GitHub and from n8n MCP.”

5. **Ask Claude a question that uses one of the servers.**

   * Example prompt:

     * “List the open issues in repository X that mention ‘MCP’ and summarize them.”
     * Or, if using n8n MCP: “Create an n8n workflow that watches a GitHub repo and posts to Slack when new PRs are opened.”

   **Narration (while it runs):**
   “Claude decides which MCP tools to call. For GitHub, that might be `list_issues`, `get_repo`, etc. For the n8n MCP server, it can ask for available nodes and then propose a workflow.
   Note that **we did not write any integration code here**:

   * Docker handles running the servers,
   * Claude acts as host+client,
   * MCP defines the contract between them.”

6. **Tie back to your custom Python server:**

   **Narration:**
   “If we wanted to use **our own Python MCP server** from Slide 8.1, we’d package it as a Docker image and register it here in the same way. To Claude, it’s just another MCP server with tools, resources and prompts.”

---

### Part 2 – VS Code as an MCP Host (brief mention)

You don’t have to do a full VS Code demo, just a quick glance:

1. Open VS Code’s **MCP servers** view / documentation (e.g. `https://code.visualstudio.com/mcp`).
2. Show the list of installable MCP servers (MongoDB, Apify, Elasticsearch, etc.).

**Narration:**

“VS Code with GitHub Copilot also supports MCP.

Here you can see a marketplace of MCP servers—MongoDB, Apify, Elasticsearch and many others. You can:

* install an MCP server like any extension,
* configure it via a `.vscode/mcp.json` file,
* and then Copilot Chat can call those tools when you’re working in a repository.

Again, the pattern is the same:

* host = VS Code / Copilot Chat,
* client = Copilot’s MCP client,
* servers = Dockerized or remote MCP servers that expose tools/data.”

---

### Part 3 – n8n + MCP (segue into n8n section)

Now do a **very short** n8n demo, since the detailed n8n slides will come later.

**Visual:** open n8n, show a simple workflow with MCP nodes.

**Narration + structure:**

> “Finally, let’s look at how MCP and **n8n** play together, because that’s our segue into the automation part of the talk.”

1. **Show n8n’s MCP nodes.**

   * `MCP Client Tool` node: n8n acting as an MCP client to *external* MCP servers.
   * `MCP Server Trigger` node: n8n exposing its workflows as MCP tools to *other* hosts.

   **Narration:**
   “n8n supports MCP with two node types:

   * **MCP Client Tool** – n8n calls tools from *external* MCP servers (for example the GitHub MCP server we just used with Claude, or a custom Python MCP server).
   * **MCP Server Trigger** – n8n itself acts as an MCP server, letting AI assistants call n8n workflows as tools.”

2. **Show a simple workflow:**

   * Trigger: HTTP/Webhook or Cron.
   * Node: `MCP Client Tool` configured to call GitHub MCP server or some other Docker MCP server.
   * Node: send results to Slack or email.

   **Narration:**
   “Here’s a simple example:

   * The workflow is triggered once a day.
   * It uses the **MCP Client Tool** node to call the GitHub MCP server and get open issues.
   * It then formats a report and sends it to Slack.

The important part is: we didn’t write a GitHub integration in n8n; we just pointed n8n at an existing MCP server. MCP becomes a **shared connector layer** between Claude, VS Code, n8n, and any other host that knows how to talk MCP.”

3. **Tease the next section:**

   **Narration:**
   “In the next part of the lecture, we’ll stay in n8n and design an actual workflow that uses agents and MCP together. For now, the key idea is:

> MCP gives us reusable, standard servers, and tools like Claude, VS Code and n8n can all **consume the same servers** without bespoke integrations.”

---

## Slide 9 – Code Execution with MCP (Anthropic Update)

**Title on slide:**
**“Scaling MCP: code execution instead of ‘tool soup’”**

**On-slide content:**
A simple “Before / After” diagram:

* **Before (classic MCP tool-calling)**:

  * Model context contains:

    * thousands of tool definitions,
    * many large tool results.
  * Caption: “Tool schemas + intermediate data bloat context → high token cost.”

* **After (code execution + MCP)**:

  * A box labeled **“Code execution env (Python/TS)”** sitting between model and MCP servers.
  * The model writes code that:

    * loads only the tools it needs from MCP,
    * processes data **inside the runtime**,
    * passes only summaries back to the model.

Small bullets:

* “Load **tool definitions on demand**.”
* “Process large results in code, not in the context window.”
* “Better privacy & state (results don’t have to go through the model).”

**Script:**

“There’s one more interesting, slightly advanced update from Anthropic (creators of MCP): **code execution with MCP**.

As MCP adoption has grown, people started connecting agents to **hundreds or thousands of tools**. That led to two problems:

1. **Tool definition overload** – if you dump thousands of tool schemas into the prompt, you blow up the context and latency.
2. **Result bloat** – every intermediate result has to pass through the model (e.g. a 10,000-row spreadsheet), again consuming tons of tokens.

Anthropic’s suggested pattern is to combine **MCP with a code execution environment**:

* Present MCP servers as a kind of **code API**.
* Let the agent write code that does things like:

  * import only the specific MCP tools it needs,
  * filter and aggregate large results inside the runtime,
  * log or return just compact summaries.

In their example, this reduced token usage from about **150,000 tokens to ~2,000 tokens**—roughly a 98% reduction—by moving orchestration and filtering into code.

There are also **privacy benefits**: sensitive data can stay inside the execution environment, never entering the model context.

The trade-off is complexity: you need a secure sandbox, resource limits, monitoring, etc. So for a **teaching demo**, I’d keep our example simple—direct MCP tool calls. Then use this slide as a **“heads up”**:

> *‘In production, people increasingly combine MCP with code execution to make agents cheaper, faster and safer.’*”

---

## Slide 10 – (Transition to n8n – MCP → Automation)

**Title on slide:**
**“From MCP to automation: n8n”**

**On-slide content (simple):**

* Diagram showing:

  * **MCP servers** on the left (GitHub, DB, n8n MCP, etc.)
  * **AI host** in the middle (Claude, VS Code, ChatGPT)
  * **n8n** on the right as:

    * an **MCP client** (calling external servers), and
    * an **MCP server** (exposing workflows)

**Script:**

“To wrap up the MCP part:

* MCP standardizes how agents talk to tools and data.
* Many tools—Claude Desktop, VS Code, GitHub Copilot, Windows, n8n—either already support MCP or are adding support.

In the **second part**, we’ll zoom in on **n8n**:

* how to use MCP servers *inside* n8n workflows, and
* how to expose n8n workflows *as* MCP tools to other agents.

The goal is to show how everything you saw here with MCP plugs directly into practical automation.”
