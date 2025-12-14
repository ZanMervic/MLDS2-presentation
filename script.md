## Slide 1 – Title

"Ok, so in this second part of the lecture we'll look at the "new" standard in the world of AI agents, the **Model Context Protocol (MCP)** and how it connects models to tools and data, when and how to use it, why it matters and finally a demo on how to connect your custom and existing MCP servers to AI applications.

---

## Slide 2 – From “Classic” Agents to Integration Headaches

"So in the first part of this lecture Sebastijan showed us how to implement simple AI agents and how to give them custom tools which they can use. These tools add additional functionalities to AI agents and give it access to things such as internal databases, APIs, search engines and so on. The mentioned approach works well for a handful of tools, but now imagine doing this at **production** scale where Agents need to talk to dozens or hundreds of systems.

The way Sebastijan showed it makes every one of those integrations its own little project where:

- You write **custom code** for each tool,
- each API you use has a **separate function schema** and different response structures,
- for each tool, we may need to implement authentication, rate limits, error handling so on.

This leads to what people sometimes call an **M×N integration problem**, where if we have M tools and N models or apps from different providers (e.g OpenAI, Anthropic, Google, ...), which all have slightly different ways of integrating tools, we end up maintaining lots of code.
MCP was proposed to address exactly this kind of fragmentation by standardizing how AI apps connect to tools and data."

---

## Slide 3 – What is MCP? A Standard, Not New Powers

“So, what exactly is MCP?

The definition provided by the creators of MCP is that, **MCP (Model Context Protocol)** is an open-source standard for connecting AI applications to external systems. 
<!-- It defines a client–server protocol so an AI app can discover and call tools / fetch resources from a system through an MCP server, without needing a custom integration for each app.  -->
It was created by Anthropic (the company behind Claude) and now adopted by others like OpenAI, Google, Microsoft, IBM and more. So basically every major player in the AI space.

The commonly used analogy, which you will se in most articles and videos about MCP is that mcp is like a **USB-C port for AI applications**.

So just like USB-C gives your devices one consistent way to connect, MCP gives AI apps one consistent way to connect to external systems.

One **Important note** here, which doesn't get mentioned enough and can thus be the source of misconception, MCP does **not** give LLMs any capabilities they didn’t have already.

- Before MCP, you could already do tool calling, access APIs, databases, filesystems, etc.
- MCP’s value is that it **standardizes and unifies** those integrations:

  - Less custom code for every tool,
  - Reusable MCP servers across assistants and platforms,
  - Easier sharing of integrations between developers.

So MCP is about **scalability and standardization**, not new functionalities.”

---

## Slide 4 - Google Trends

"To give you an idea of how MCP has been gaining traction, here is a Google Trends graph showing interest over time for 'Model Context Protocol' and related terms.

So ever since its release in November 2024, it has been slowly gaining traction, at a very similar pace to the Search term "AI Agents" and "n8n". The popularity of these terms peaked in August 2025, since then the "hype" has settled down a bit, but it's still a very useful topic to hear about at least once.

---

## Slide 5 – MCP Architecture: Host, Clients, Servers

“Now let's get a bit more technical and get a better intuition on how MCP works.

So, MCP follows a **host–client–server architecture**.

- Where the **host** is your AI application, e.g. Claude Desktop, ChatGPT, VS Code with Copilot, a workflow tool like n8n and so on.
- It does three important jobs:

  - It runs and talks to the model and manages the conversation.
  - It manages the **MCP clients** (we will hear what these are in a second)
  - It aggregates context, by collecting the outputs from different servers and feeding them back to the model.
  - And it enforcess permissions and security by deciding which servers and tools are allowed to run, which tools need user approval to be used and what data is allowed to be sent out, as we don't want to send the entire chat or sensitive information to some random server.

- Then there are **MCP clients** which are components inside the host. Each client:

  - connects to exactly one MCP server, so if we want to connect to multiple MCP servers, the host spins up multiple clients.
  - negotiates capabilities by asking the server about what it can do and provides that to the host (this step happens as soon as we connect to a new server, which needs to announce to the client which capabilities it has, their descriptions and how to use them. This than gets passed to the host, which includes it in the context of the AI agent.)
  - and handles back and forth messages when the host wants to use something.

- And finally the **MCP server** is where the integration lives:
  - It's a small service, which wraps something like a filesystem, a database, an API and exposes it in an MCP way.
  - It can run locally, on the same machine as the host or remotely as a hosted service.

---

## Slide 6 – MCP Primitives: Resources, Tools, Prompts

Cool—so what can an MCP server actually offer to the host and the model?

There are three main, so called **primitives**:

- Firstly, we have **Resources**, which are read-only data access points. These could be files, database rows, etc. The model can read them but not change them directly.

  - An important note here is that the host decides when and how to include resources as context.
  - Different hosts might preview them, summarize them, or selectively pass parts to the model.

- Then we have **Tools**, which are actions or functions the model can invoke. Tools can have side effects, like doing computations, running queries, or triggering workflows.

- Finally, we have **Prompts**, which are **structured, reusable prompt templates**. The model can ask the server for specific prompts to guide its behavior, such as:

  - “Use this ‘summarize incident’ prompt,”
  - or “Use this multi-step analysis prompt.”

  - This is useful because instead of hard-coding long instructions into every app, you can centralize them and reuse them across hosts.

The server advertises which resources, tools, and prompts it supports; the client passes that to the model. So one MCP server can be just resources, just prompts, just tools, or any combination.”

---

## Slide 7 – Transports: How Clients Talk to Servers

“Now, quick networking detail — not because you need it to use MCP, but because it helps explain how MCP works across local and remote setups.

Between an MCP client and an MCP server, the actual messages are JSON-RPC. That’s the “language” they speak.

The part that can vary is how those JSON-RPC messages get transported from client to server. MCP standardizes two transports:

1. stdio (local servers)

- stdio is the common choice when the server runs on the same machine as the host.

This is great for things like:

- local filesystem access,
- local developer tools,
- local wrappers around something you can reach from your machine.

2. Streamable HTTP (remote servers)

- Streamable HTTP is meant for servers that run remotely — on another machine, in a container, behind a URL.
- The server exposes an HTTP endpoint (often a single endpoint).
- The client sends JSON-RPC requests over HTTP.
  ”

---

## Slide 8 – MCP in Action: Example Workflow

“Let's try to imagine the whole process to get an intuition on how all of this works.

1. Let's say, the user asks, "What is the weather today in Ljubljana"

> Behind the scenes, the **host application** – think Claude Desktop or your own app – has already connected to its provided MCP servers, and from those connections, the host knows which tools are available. It then exposes those tools to the model as part of the model call.

2. This prompt goes to the AI application (the host) and than to the LLM itself, along with the context from the MCP servers.
   The LLM doesn't know the answer to this, as it wasn't trained on todays weather, but it sees in it's context, that there is a MCP server, which has a tool called `get_weather`, which requires one parameter, and that is the name of the city.

3. The LLM tells the host, that it wants to use the `get_weather` tool, with the city parameter set to "ljubljana".
4. In some cases, the host will ask the user for permission to use a specific MCP server, and after the user approves ...
5. (6. 7. 8.) The request gets sent to the server, where the needed actions are taken, and the response is sent back to the host.
6. (10.) The host then passes the response back to the LLM, which can use that information to generate a final answer for the user.

---

## Slide 7 – Why MCP Matters (Even Though Tools Existed Before)

“Before MCP, after implementing for example a "Github Integration" tool for one app, you had:

- a GitHub integration for this one app,
- and then you rewrote it again for another app,
- and again for another model/provider.

And every time you did that, you re-did the same boring but painful stuff:

- tool schemas,
- auth,
- rate limits,
- error handling,
- logging,
- retries,
- edge cases.

So as you add more tools and more hosts, the work multiplies — that’s the classic M×N integration problem.

With MCP, the integration moves into a server. So instead of writing “GitHub tool for Claude” and “GitHub tool for ChatGPT”, you build one GitHub MCP server, and any MCP-aware host can connect to it and discover:

- what it can read (resources),
- what it can do (tools),
- and what reusable templates it offers (prompts).

And just as importantly: the host stays in control.
It decides:

- which servers are enabled,
- which tools can run (and which need approval),
- and what data is allowed to leave the host.

So MCP doesn’t magically give the model new powers — it just turns integrations into something that’s portable, reusable, and governable.

---

## Slide 8 – MCP server implementation (DEMO)

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

“
Now the next step would be, to integrate the implemented MCP server into the AI agent from earlier (the one Sebastijan implemented).

This is where the drawbacks come and where we see, that MCP shouldn't be used everywhere.

So here we have our simple AI Agent using tooling from earlier:
**Here I show a screenshot of the Simple AI agent with tooling implementation**
The whole implementation (without the tool implementation) is about 25 lines of code.

**Here I show a screenshot of the more Complex AI agent with MCP**
However, to use an MCP server with our custom agent, that agent needs to behave as an MCP host and include an MCP client to connect to the server. Now I couldn't fit the entire implementation on the screen, but it's quite a bit more complex and it takes around 165 lines of code. There are tutorials on how to build your own MCP host on the official MCP site, but it's quite complex.

From this you can see that perhaps we shouldn't use MCP everywhere. For smaller projects with AI agents like the one Sebastijan showed you, it's actually easier to just use the tools like we did before instead of MCP.

However, if we plan on using dozens of tools, or functionalities for which there already exist MCP servers, it might be worth investing some time into the MCP way in order to make the AI app much more scalable and future proof.
You only need to do this process once, and there exist good documentation and loads of tutorials on how to do this.
”

---

## Slide 8.2 – MCP with existing hosts.

Now let's look at in my opinion, the most useful part of MCP ...

So the beauty of MCP being a widely used standard is, that there are already many existing MCP compatible hosts/apps, some of which I am sure you already use, which can connect to our (and other) MCP servers in order to give them extra functionalities.

Examples of existing MCP hosts are applications such as Claude Desktop, Github Copilot inside VSCode, Cursor,...

Let's see how we can add MCP servers to something like Claude Desktop.

There are different ways to add MCP servers to existing hosts, but the easiest one is to add them using Docker.
For this we first need to dockerize our MCP server, this is easily done with a simple Dockerfile, so if you are not familiar with docker, this file contains instructions on how to create a Docker Image which includes our Server.

- We start with an existing python docker image which contains python
- Than we copy our server into it and install the required packages
- Finally, we add commands which run our server when the container is ran.
- We can build this image using the following command.

From docker desktop, we can than connect to the MCP Host/app we want to use, in this case Claude Desktop, and Docker will handle everything else for us. Behind the scenes, what it does, is edits the hosts mcp_config.json file, which we can see here...
It adds the MCP_DOCKER section, when we connect for the first time and this allows the host to see and use every server that we hava in docker.

The other option, if we want to avoid Docker, is to manually edit the mcp_config.json, as you can see with the coin-local example, all we need to do is specify some parameters, these include the path to our python or virtual env. and the path to our server.

Now let's look in more detail how this process looks with docker.

**Opens Docker Desktop**

...
---

## Slide 9 - Code Execution with MCP (Anthropic Update)

“A quick heads‑up for those of you planning to build large‑scale MCP hosts. Anthropic—the creators of MCP—recently published an article titled **‘Code execution with MCP: building more efficient agents’**. They observed that as people connected agents to hundreds or thousands of MCP tools, two things happened:

1. **Tool definition overload:** Every tool’s schema is loaded into the model’s context. When you have thousands of tools, these definitions alone can consume hundreds of thousands of tokens.
2. **Intermediate result bloat:** Each tool call returns data back through the model. A two‑hour meeting transcript or a 10,000‑row spreadsheet might have to pass through the context multiple times.

Both issues cause latency and cost to skyrocket.

Anthropic proposes a solution they call **code execution with MCP**. Instead of letting the model call tools directly, you provide the agent with a _code execution environment_ (e.g. a Python or TypeScript runtime) that exposes MCP tools as imported functions. The agent writes code to:

- **Import only the tools it needs** from a virtual filesystem of servers and tools.
- **Process data inside the runtime**—filter, aggregate or transform large results—before sending a compact summary back.
- Use loops, conditionals, and reusable functions to orchestrate complex workflows in a single execution step.

In their example, this approach reduced token usage from roughly **150 k tokens to about 2 k tokens**, a ~98 % reduction. It also offers privacy benefits: sensitive data can stay in the execution environment and be tokenized before the model sees it.

The catch is that **code execution is more complex**. You need a secure sandbox, resource limits and monitoring. For simple demos and smaller projects, direct MCP tool calls are fine. If you’re building enterprise‑scale agents or connecting to thousands of tools, it’s worth exploring this pattern. For a deeper dive, check out Anthropic’s blog post and the accompanying videos.”