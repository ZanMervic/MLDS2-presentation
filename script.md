## Slide 1 – Title

**Title:**
**MCP - Model Context Protocol**

**On-slide content:**

- Big title: **“MCP - Model Context Protocol”**
- Subtitle: **“A new standard for AI integration”**
- Your name, affiliation
- Visual: AI brain/robot icon in the center connected with thin lines to icons for DB, API, cloud, email, etc.

**Script:**

“In this second part of the lecture we’ll look at what the "new" standard in the world of AI agents, the **Model Context Protocol (MCP)** and how it connects models to tools and data. MCP was all the rage a couple of months back, as you can see, it has dropped off a bit since then but it's still an important topic to hear about at least once. Unless, you also compare it to ChatGPT, in that case, MCP was old news before it even started.

---

## Slide 2 – From “Classic” Agents to Integration Headaches

**Title on slide:**
**“From tools to integration chaos”**

**On-slide content:**

Left side:

- Small text at top: **“What we saw in Part 1”**
- Simple diagram:

  - A “LLM Agent” bubble in the middle
  - 3–4 icons around it: **database**, **REST API**, **internal service**, **web search**
  - Arrows showing tool calls (like `get_users`, `http_get`, `db_query`)

Right side:

- Heading: **“Before MCP”**
- 2–3 short bullets:

  - “Each tool = custom function / plugin”
  - “Every system has its own schema, auth, error handling”
  - “Hard to scale to dozens of tools”

**Script:**

“Let’s connect this to what you saw in the **agent** part of the lecture.

In Part 1, you saw how to implement simple agents that could call tools: maybe an HTTP request tool, a database tool, a calculator, web search… That works nicely for a handful of tools. But now imagine doing this at **production** scale where Agents need to talk to **many** (dozens/hundreds) systems:

- internal databases,
- SaaS APIs (Slack, GitHub, Notion, CRM),
- search engines, file stores, and so on.

**Before MCP**, every one of those integrations was its own little project:

- You write **custom code** for each tool,
- define a **separate function schema** or plugin,
- handle auth, rate limits, error formats, prompts… all differently.

<!-- (TODO: Perhaps show an example of "messy" code for this.) -->

This leads to what people sometimes call an **M×N integration problem**: for M tools and N models, you end up maintaining lots of bespoke glue code. MCP was proposed to address exactly this kind of fragmentation by standardizing how AI apps connect to tools and data.

So the question is:

> _How do we move from ‘one-off tools everywhere’ to a **standard way** of wiring agents to systems?_

That’s where MCP comes in.”

---

## Slide 3 – What is MCP? A Standard, Not New Powers

**Title on slide:**
**“What is MCP?”**

**On-slide text:**

- One short definition:

  > “A standardized protocol for connecting AI applications to external tools, data and services.”

- A **single** analogy:

  > “Think of MCP like a USB-C port for AI applications.”

- Small caption at bottom:

  - “Standardization layer – _not_ new model abilities”

Visual:

- On the left: **AI app / Agent** icon with a small “USB-C port” symbol.
- On the right: 3–4 boxes: “DB server”, “GitHub server”, “Notion server”, “Zapier MCP server” connected via identical “MCP cable” icons.

**Script:**

“So, what exactly is MCP?

Formally, **MCP (Model Context Protocol)** is an _open-source standard_ for connecting AI applications to external systems—databases, tools, services. It’s essentially a **standardization layer** between models and the outside world, defined originally by Anthropic (the company behind Claude) and now adopted by others like OpenAI, Google, Microsoft, IBM and more.

The commonly used analogy is:

<!-- (TODO: Perhaps use the Rest API analogy instead) -->

> MCP is like a **USB-C port for AI applications**.

Just like USB-C gives your laptop one consistent way to plug into many devices, MCP gives AI apps one consistent way to plug into many tools and data sources.

**Important point:** MCP does **not** give LLMs any capabilities they didn’t have already.

- Before MCP, you could already do tool calling, plugins, RAG, etc.
- MCP’s value is that it **standardizes and unifies** those integrations:

  - Less custom glue for every tool,
  - Reusable MCP servers across assistants and platforms,
  - Easier sharing of integrations between developers.

So you can think of MCP as a **standard integration layer** that sits under whatever agent framework you’re using.”

---

## Slide 4 – MCP Architecture: Host, Clients, Servers

**Title on slide:**
**“MCP architecture: host, clients, servers”**

**On-slide diagram:**

- Big box labeled **“Host”** (e.g. ChatGPT Desktop, Claude Desktop, VS Code, n8n, custom app).

  - Inside: several small **“client”** boxes, each labeled “MCP client (GitHub)”, “MCP client (DB)”, etc.

- On the right: multiple **“MCP Server”** boxes:

  - “MCP server: GitHub”
  - “MCP server: Internal DB”
  - “MCP server: Zapier MCP”

- Arrows:

  - Host ↔ Clients (labeled “create/manage clients, coordinate LLM”)
  - Each Client ↔ its Server (1:1, labeled “MCP session”)

Minimal text (small bullet list in a corner):

- Host: runs the LLM / agent, manages clients, enforces security.
- Client: 1:1 connection to a server, handles protocol & capabilities.
- Server: exposes resources, tools, prompts.

**Script:**

“MCP follows a **host–client–server architecture**.

- The **host** is your AI application, e.g. Claude Desktop, ChatGPT Desktop, VS Code with Copilot, an IDE, or even a workflow tool like n8n in principle. The host:

  - runs or connects to the model,
  - creates **MCP clients**,
  - enforces permissions and security,
  - aggregates context from many servers.

- An **MCP client** is a component inside the host. Each client:

  - connects to _exactly one_ MCP server,
  - negotiates capabilities (which tools/resources/prompts are available),
  - routes messages back and forth.

- An **MCP server** is where the integration lives:

  - It wraps a specific data source or service,
  - exposes **resources, tools and prompts** in a standard way,
  - can be local (e.g. your filesystem) or remote (e.g. a SaaS MCP server).

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

   - “Read-only data or files (no side effects).”
   - Example on slide:

     - `customer://12345` → customer JSON
     - `file://reports/2025-Q1.pdf` → PDF content

2. **Tools**

   - “Operations with side effects or active logic.”
   - Example:

     - `create_jira_ticket(...)`
     - `send_email(to, subject, body)`

3. **Prompts**

   - “Reusable prompt templates / workflows.”
   - Example:

     - `summarize_support_ticket`
     - `generate_sales_email`

**Script:**

“Concretely, what can an MCP server provide to the model? There are three main, so called **primitives**:

<!-- TODO: Write some better examples here -->

- **Resources**: think of these as **read-only data access**:

  > That could be files, database rows, dashboards, etc. The model can read them but not change them directly.

- **Tools**: these are **actions or computations**. A tool might:

  - call an API,
  - run a query,
  - trigger a workflow.
  - any other operation with some side effects.
    For example: `create_ticket`, `list_events`, `run_sql`.

- **Prompts**: these are **structured, reusable prompt templates or flows**. Instead of hard-coding a long system prompt into your application, you can host it behind MCP:

  - “Use this ‘summarize incident’ prompt,”
  - or “Use this multi-step analysis prompt.”

The server advertises which resources, tools, and prompts it supports; the client passes that to the model in a standard way. So one MCP server can be _just_ resources, _just_ prompts, _just_ tools, or any combination.”

---

## Slide 5.1 – Transports: How Clients Talk to Servers

**Title on slide:**
**“How MCP messages travel: transports”**

**On-slide content:**
Two boxes in a row:

1. **stdio**

   - Caption: “Local processes (CLI tools, local DB, filesystem).”

2. **Streamable HTTP**

   - Caption: “Newer, single HTTP endpoint, bidirectional streaming.”

Small note at bottom:

- “All transports wrap **JSON-RPC 2.0** messages.”

<!-- (TODO: Educate yourself what any of this means ...) -->

**Script:**

“For completeness, here’s a quick overview for the networking enthusiasts...
Between an MCP client and server, all communication is via **JSON-RPC** messages, but the actual **transport** can differ.

There are two standardized transports:

1. **stdio** which is used for **local** servers.

   - Great when you run a server on the same machine: e.g. a filesystem or local database wrapper.
   - Simple: messages go over stdin/stdout.

2. **Streamable HTTP** – for **remote** servers.
   - Replaces an older **SSE** transport.
   - Don't know much about this...

As a server author you choose which transports to support; as a host you pick whatever your environment can reach. But the **MCP layer** stays the same.”

---

## Slide 6 – MCP in Action: Example Workflow

**Title on slide:**
**“MCP in action – same agent, less custom glue”**

**On-slide visual:**
A 5-step horizontal comic:

**Host app** (Claude Desktop / your app)
↓ connects to:

- **MCP server: CRM** (exposes tools like `find_customer`)
- **MCP server: Sales DB** (exposes tools like `get_monthly_sales`)

1. User: “Summarize our top customer and this month’s sales.”
2. Agent bubble: “Need CRM + sales DB.”
3. Arrow to CRM server: `crm.find_customer("Acme")` (MCP tool).
4. Arrow to DB server: `sales.get_monthly_sales("2025-10")`.
5. Agent returns a short combined report.

Minimal labels only (“MCP call: …”, “CRM MCP server”, etc.).

**Script:**

“Let's try to imagine the whole process to get an intuition on how all of this works.

User asks:

> ‘Give me a summary of our top customer and this month’s sales.’

> Behind the scenes, the **host application** – think Claude Desktop or your own app – has already:
>
> - connected to a **CRM MCP server**, and
> - connected to a **Sales DB MCP server**,
>
> From those connections, the host knows which tools are available – things like:
>
> - `find_customer(...)` from the CRM server
> - `get_monthly_sales(...)` from the Sales DB server
>
> It then exposes those tools to the model as part of the model call.

The agent decides it needs two things:

- customer details from the **CRM**,
- numbers from the **sales DB**.

With MCP, that might look like:

- Call a tool on the **CRM MCP server**:
  `find_customer("Acme Corp")` <- Here the agent chose which tool to call and which parameters to use.
  → returns structured customer info.

- Call a tool on the **Sales DB MCP server**:
  `get_monthly_sales("2025-10")`
  → returns metrics.

Then the model writes a short report from these results.

<!-- You’re right that this *pattern*—model calls tools, gets results, then reasons—also existed **before** MCP. The key difference is **where the complexity lives**:

* Pre-MCP: you bespoke-implemented every integration (CRM plugin, DB plugin, custom code, ad-hoc prompts).
* With MCP: CRM and sales DB are each just **MCP servers**. The host and MCP client already know how to talk to them in a standardized way, and those same servers can be reused by *other* agents and hosts.

So conceptually the agent loop is the same; MCP just gives you a **cleaner, reusable interface** for that loop.” -->

---

## Slide 7 – Why MCP Matters (Even Though Tools Existed Before)

**Title on slide:**
**“Why MCP matters (even though tools existed before)”**

**On-slide content:**
Two-column “Before / With MCP” graphic.

Left: **Before MCP**

- “Each tool = ad-hoc integration” <!-- (TODO: Show/explain what this means) -->
- “Different schemas, auth, error handling”
- “Hard to share integrations between apps”
- “Tool definitions often duplicated across agents”

Right: **With MCP**

- “One **standard protocol** for tools/data”
- “Servers reusable across hosts (Claude, ChatGPT, VS Code, IDEs, …)”
- “Growing ecosystem: many open-source servers (GitHub, AWS docs, DBs, Zapier, n8n MCP, …)”
- “Easier enterprise governance & security boundaries”

Small note at bottom:

> “LLMs already had tool calling; MCP standardizes it.”

**Script:**

<!--
TODO: This part is really important so it should be perfected
Reference the two following sources:
- https://www.youtube.com/watch?v=7j1t3UZA1TY (from 10min ->)
- https://www.youtube.com/watch?v=5xqFjh56AwM (whole video is a banger)
- https://medium.com/@tahirbalarabe2/model-context-protocol-mcp-vs-apis-the-new-standard-for-ai-integration-d6b9a7665ea7
- https://www.freecodecamp.org/news/mcp-vs-apis-whats-the-real-difference/
 -->

“Let’s be careful about _what_ MCP changes.

**First, an important note:** LLMs could call tools **before** MCP. We had function-calling, plugins, RAG, custom frameworks, etc. MCP does **not** bring any new functionalities.

What MCP does is:

- Turn tool & data access into a **standard protocol**, similar to how REST or OpenAPI standardized web APIs.
- Make integrations **reusable**:

  - The same “GitHub MCP server” or “filesystem server” can be used by Claude, ChatGPT Desktop, VS Code Copilot Chat, Cursor, Zed, and so on.

- Encourage an ecosystem:

  - There’s already a catalog of MCP servers for things like MongoDB, Apify, Elasticsearch, Windows features, n8n, and more.

- Help with **security and governance**:

  - The host controls which servers are available, what capabilities they expose, and how much context each server sees, which is important for enterprise deployments.

So the value proposition is not ‘new capabilities’, but **scalable, interoperable, governed integration**. That’s why major players like Anthropic, OpenAI, Google, Microsoft and IBM frame it as a standardization layer rather than yet another agent framework.”

---

## Slide 8 – MCP server implementation (DEMO)

**On-slide visual:**

<!-- (TODO: show that these tools each needed to be implemented separately) -->

```python
from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("Demo Server")

@mcp.tool()
def dice_roll(sides: int) -> int:
    """
    Roll a dice with the given number of sides.
    Parameters:
        sides (int): Number of sides on the dice.
    """
    return random.randint(1, sides)

@mcp.resource("file:///example/resource")
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
        "..."
    )

mcp.run(
    transport="stdio" # Or streamable-http for web servers
)
```

**Script:**

“Now that we know the basics of what MCP is, and what it offers, let's try to see it in action.
I will show you a minimal MCP server implementation in Python, using the official `mcp` SDK.
Note that there are also official SDKs for other popular languages like TypeScript, C#, Java, ...

Ok, so here on the slide I have the python code for a MCP server, which includes a tool (`dice_roll`), a resource (`get_server_status`) and a prompt (`example_prompt`).

1. So starting from the top, we first import the `FastMCP` Class from the `mcp` library.
2. Right under, we can instantiate it with `mcp = FastMCP("Demo Server")`.
3. All we then need to do is add functionality to the server in the form of tools, resources, and prompts.
4. We do that by defining functions, in which we implement our logic and than return the result. All we than need to do, to transform these functions to a MCP tool/resource/prompt, is add the corresponding decorators.
5. At the end we can run the server, where we define the transport we mentioned before, so `stdio` for local usage or `streamable-http` when we want to deploy it as a web service.

And that’s it — this is a complete MCP server.

In a real production server, most of your effort goes into implementing the actual logic behind these tools and resources. But the beauty of MCP is that you only have to do that once. After you’ve built and hosted this server, any MCP-compatible client or agent can reuse these capabilities without needing custom integration code every time.

From the users perspective, most of the integration complexity — error handling, auth, calling external APIs, etc. — lives in the server implementation. As a user, you just connect to it and start using its tools.
”

---

## Slide 8.1 – MCP - Not all bells and whistles

**On-slide content:**

TODO

**Script:**

“
Now you are probably asking, how can we use our MCP server with the Agent we implemented earlier.

This is where the drawbacks come and where we see, that MCP shouldn't be used everywhere.
To use an MCP server from our custom agent, that agent needs to behave as an MCP host and include an MCP client to connect to the server. For multiple servers, the host creates one client per server and manages them. There are tutorials on how to build your own MCP host on the official MCP site, but it's quite complex.

**Here is show a screenshot of the Host and Client implementations?**

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

<!-- At the top, we use the **Python MCP SDK** to connect to a local MCP server over stdio:

- `StdioServerParameters` describes how to start the server (`python server.py`).
- `stdio_client` gives us read/write streams.
- `ClientSession` handles the MCP protocol.
- We call `session.initialize()` and then `session.list_tools()` to see what the server exposes. -->

From this you can see, that for smaller projects with AI agents like the one Sebastijan showed you, it's actually easier to just use the tools like we did before instead of MCP.

However, if we plan on using dozens of tools, or functionalities for which there already exist MCP servers, it might be worth investing some time into the MCP way in order to make the AI app much more scalable and future proof.
”

---

## Slide 8.2 – MCP with existing hosts.

Even if in the previous slide, we saw, that building your own MCP hosts for our AI Agents to use our MCP server is hard and may not always be worth it, it's not over for our MCP server.

The beauty of MCP being a widely used standard is, that there are already many existing MCP hosts, some of which I am sure you already use, which can connect to our (and other) MCP servers in order to give them extra functionalities.

Examples of existing MCP hosts are applications such as Claude Desktop, Github Copilot inside VSCode, Cursor,...

Let's see how we can add MCP servers to something like Claude Desktop.

So if we open up claude code, and click here `search and tools` we can see there are some tools already added (this is from when I as testing), under this, we can see `Add connectors` where if we click, we can see some MCP servers Claude lists for us to include (this is a payed feature). But we can also add our own MCP servers and there are two ways of doing so, the easier one being with Docker.

So let's open up docker, and here on the side we can see `MCP toolkit`, where docker has a big catalog of MCP servers <!-- Show servers, comment on it --> and also Clients <!-- Show clients, comment on it -->.

Here we can select some MCP servers, I have picked the Openweather, if we click on it we see the tools it offers (just one in this case), and also any configuration we can do. In this case I needed to get an Openweather API key, but that is all I needed to do as a user, everything else is handled by the Openweather developers.

Here in my images, we can also see my dice-mcp-server. Now I won't show how to dockerize your MCP server because we don't have time, but it's very simple and there are many tutorials on it.

Now let's see this in action in the Claude Desktop.

Let's first ask it for the weather in London. So here we see that Claude asks us if it can use the Openweather MCP with the city parameter set to London. And here is the information. We can also see what the response from the MCP server was.

Now let's ask it to roll a 12 sided dice. Again it asks us for permission, and here we can see that the MCP call contains the sides parameter set to 12, which corresponds to the parameter of our function <!-- Show code -->. And we get a response!

<!--
TODO: Depending on the time, I can also show: 
- how to dockerize our server (Dockerfile + where to add our image to the registry - the commands)
- how Docker edits the `claude_desktop_config.json` and how we can manually edit it to add local servers. Explain the file.
-->
---


<!-- ### Demo script

**Intro (tie-in to Slides 8.1 & 8.2):**

> “We just saw how an MCP server looks in Python, and how a client might connect to it.
> For the **live** demo, I won’t make you watch me write Python. Instead, we’ll use MCP servers that are already packaged for us—mostly via Docker—and see how to plug them into real tools like Claude Desktop, VS Code, and n8n.”

---

### Part 1 – Docker MCP Toolkit → Claude Desktop

**Steps you show:**

1. **Open Docker Desktop (MCP Toolkit / Catalog).**

   - Go to the MCP section / MCP Toolkit.
   - Show a **catalog of MCP servers** (e.g. GitHub Official, Firecrawl, Filesystem, n8n MCP, etc.).

   **Narration:**
   “Docker Desktop has a **MCP Toolkit** that lets you spin up many MCP servers in one click—GitHub, Docker CLI, Kubernetes, Firecrawl, n8n MCP, and so on.”

2. **Select one or two servers and add them.**

   - Click “Add” / “Install” on e.g. **GitHub Official** and **n8n MCP**.
   - Docker pulls and starts the containers.

   **Narration:**
   “I’ll enable the GitHub MCP server and the n8n MCP server from this catalog. Under the hood, these are just **Docker images** that expose an MCP endpoint, very similar to how our Python `server.py` could be containerized.”

3. **Connect to Claude Desktop.**

   - In the Docker MCP Toolkit UI, click “Connect to Claude Desktop” (or show the step where it writes into `claude_desktop_config.json`).

   **Narration:**
   “With one click, Docker writes the MCP configuration into Claude Desktop’s MPC config JSON. That tells Claude:

   > ‘When you start, also start these MCP servers and connect to them.’”

4. **Switch to Claude Desktop.**

   - Open Claude Desktop, start a new chat.
   - Show that the GitHub server and n8n MCP server appear in the tools/resources panel.

   **Narration:**
   “When Claude Desktop boots up, it reads that config and starts these MCP servers as part of the host. Now Claude can use tools from GitHub and from n8n MCP.”

5. **Ask Claude a question that uses one of the servers.**

   - Example prompt:

     - “List the open issues in repository X that mention ‘MCP’ and summarize them.”
     - Or, if using n8n MCP: “Create an n8n workflow that watches a GitHub repo and posts to Slack when new PRs are opened.”

   **Narration (while it runs):**
   “Claude decides which MCP tools to call. For GitHub, that might be `list_issues`, `get_repo`, etc. For the n8n MCP server, it can ask for available nodes and then propose a workflow.
   Note that **we did not write any integration code here**:

   - Docker handles running the servers,
   - Claude acts as host+client,
   - MCP defines the contract between them.”

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

- install an MCP server like any extension,
- configure it via a `.vscode/mcp.json` file,
- and then Copilot Chat can call those tools when you’re working in a repository.

Again, the pattern is the same:

- host = VS Code / Copilot Chat,
- client = Copilot’s MCP client,
- servers = Dockerized or remote MCP servers that expose tools/data.”
 -->

---

## Slide 9 - Code Execution with MCP (Anthropic Update)

**On-slide content:**

A simple “Problem → Solution” graphic.

- **Problem:**  
  - *Tool soup*: thousands of tool definitions load into the model’s context.  
  - *Result bloat*: large intermediate results (e.g. long transcripts or spreadsheets) flow through the model.  
  - These patterns increase latency and token costs.

- **Proposed solution (Anthropic)**: *Code execution with MCP*.  
  - Treat MCP servers as code libraries; let the agent write code that imports only the tools it needs.  
  - Process large data inside the execution environment and return only summaries or filtered results.  
  - Reduces token usage dramatically (e.g. from ~150,000 tokens to ~2,000 tokens).  
  - Keeps sensitive data within the code runtime; results are tokenized before being exposed.

- **Trade‑offs:**  
  - Requires a secure sandbox and careful resource limits.  
  - More complex to implement than direct tool calls.

Include a link or footnote: *“See Anthropic’s blog for details.”*

**Script:**

“A quick heads‑up for those of you planning to build large‑scale MCP hosts.  Anthropic—the creators of MCP—recently published an article titled **‘Code execution with MCP: building more efficient agents’**.  They observed that as people connected agents to hundreds or thousands of MCP tools, two things happened:

1. **Tool definition overload:**  Every tool’s schema is loaded into the model’s context.  When you have thousands of tools, these definitions alone can consume hundreds of thousands of tokens.
2. **Intermediate result bloat:**  Each tool call returns data back through the model.  A two‑hour meeting transcript or a 10,000‑row spreadsheet might have to pass through the context multiple times.

Both issues cause latency and cost to skyrocket.

Anthropic proposes a solution they call **code execution with MCP**. Instead of letting the model call tools directly, you provide the agent with a *code execution environment* (e.g. a Python or TypeScript runtime) that exposes MCP tools as imported functions.  The agent writes code to:

- **Import only the tools it needs** from a virtual filesystem of servers and tools.
- **Process data inside the runtime**—filter, aggregate or transform large results—before sending a compact summary back.  
- Use loops, conditionals, and reusable functions to orchestrate complex workflows in a single execution step.

In their example, this approach reduced token usage from roughly **150 k tokens to about 2 k tokens**, a ~98 % reduction.  It also offers privacy benefits: sensitive data can stay in the execution environment and be tokenized before the model sees it.

The catch is that **code execution is more complex**.  You need a secure sandbox, resource limits and monitoring.  For simple demos and smaller projects, direct MCP tool calls are fine.  If you’re building enterprise‑scale agents or connecting to thousands of tools, it’s worth exploring this pattern.  For a deeper dive, check out Anthropic’s blog post and the accompanying videos.”