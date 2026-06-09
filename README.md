# 📊 AI Data Analyst Copilot

A production-ready multi-agent analytics system that lets users query business data in plain English — no SQL knowledge required. Built with LangGraph, DuckDB, FastMCP, and a Streamlit frontend, it automatically routes questions, generates SQL, executes queries, and returns charts with narrative insights.

---

## 🚀 How It Works

> Upload a CSV → Ask a question in plain English → Get instant charts and insights

Users can type questions like:

- *"Show me the top 10 customers by revenue"*
- *"What are the monthly sales trends?"*
- *"Which products are most profitable?"*

The system handles everything: understanding intent, generating and validating SQL, executing it against the dataset, and returning a chart with a narrative insight — all automatically.

---

## 🏗️ Architecture

```
User Question (Streamlit UI)
        │
        ▼
┌─────────────────┐
│  Router Agent   │  ── Classifies: SQL / Insight / Visualization
└─────────────────┘
        │
        ▼
┌─────────────────┐
│ Tool Selector   │  ── Picks: sql_tool / chart_tool / stats_tool / forecast_tool
└─────────────────┘
        │
        ▼
┌─────────────────┐
│  Context Agent  │  ── Rewrites follow-up questions into standalone queries
└─────────────────┘
        │
        ▼
┌─────────────────┐
│  Intent Agent   │  ── Extracts entity, metric, operation
└─────────────────┘
        │
        ▼
┌─────────────────┐
│  Planner Agent  │  ── Creates execution plan (chart type, aggregation)
└─────────────────┘
        │
        ▼
┌─────────────────┐
│   SQL Agent     │  ── Generates DuckDB SQL (LLM + rule-based shortcuts)
└─────────────────┘
        │
        ▼
┌─────────────────┐    ┌─────────────────┐
│ SQL Review Agent│ ──►│  Critic Agent   │  ── Two-pass SQL validation
└─────────────────┘    └─────────────────┘
        │
        ▼
┌─────────────────┐
│Validation Agent │  ── Security check (blocks destructive SQL)
└─────────────────┘
        │
        ▼
┌─────────────────┐
│ Execution Agent │  ── Runs SQL via DuckDB
└─────────────────┘
        │
        ▼
┌─────────────────┐    ┌─────────────────┐
│  Insight Agent  │    │   Chart Agent   │  ── Results + Visualization
└─────────────────┘    └─────────────────┘
```

---

## 🤖 Agent Breakdown

| Agent | Responsibility |
|---|---|
| **RouterAgent** | Classifies the question as SQL, insight, or visualization task |
| **ToolSelectorAgent** | Selects the best tool (sql, chart, stats, forecast) |
| **ContextAgent** | Rewrites follow-up questions into complete standalone queries |
| **IntentAgent** | Extracts entity, metric, and operation from the question |
| **PlannerAgent** | Creates the execution plan (chart type, aggregation method) |
| **SQLAgent** | Generates DuckDB-compatible SQL using LLM + rule-based fast paths |
| **SQLReviewAgent** | First-pass SQL cleanup — date functions, column names, comments |
| **CriticAgent** | Second-pass validation — blocks JOINs, fixes table/column names |
| **ValidationAgent** | Security guard — blocks DROP, DELETE, UPDATE, INSERT |
| **SQLFixAgent** | Error recovery — repairs failed SQL using the error message as context |
| **ExecutionAgent** | Runs the final validated SQL against the DataFrame via DuckDB |
| **InsightAgent** | Generates human-readable bullet-point insights from query results |
| **ChartAgent** | Recommends and builds the best chart type (bar/line/pie/scatter) |
| **CleaningAgent** | Preprocesses uploaded data — deduplication, null handling |
| **VisualizationAgent** | Rule-based chart type suggestion for simple queries |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit (20 KB app) |
| **Agent Orchestration** | LangGraph (StateGraph) |
| **LLM** | LangChain LLM wrapper (pluggable — OpenAI, Anthropic, etc.) |
| **Query Engine** | DuckDB (in-process SQL on Pandas DataFrames) |
| **Visualization** | Plotly Express |
| **MCP Server** | FastMCP (Model Context Protocol) |
| **Conversation Memory** | Custom in-memory module |
| **Language** | Python 3.10+ |

---

## 📁 Project Structure

```
ai-data-analyst-copilot/
│
├── app/
│   ├── agents/                      # 15 specialized AI agents
│   │   ├── router_agent.py          # Question classification
│   │   ├── tool_selector_agent.py   # Tool routing
│   │   ├── context_agent.py         # Conversation context rewriting
│   │   ├── intent_agent.py          # Intent extraction
│   │   ├── planner_agent.py         # Execution planning
│   │   ├── sql_agent.py             # SQL generation (LLM + rules)
│   │   ├── sql_review_agent.py      # SQL cleanup — pass 1
│   │   ├── critic_agent.py          # SQL validation — pass 2
│   │   ├── sql_fix_agent.py         # Error recovery
│   │   ├── validation_agent.py      # Security validation
│   │   ├── execution_agent.py       # SQL execution
│   │   ├── insight_agent.py         # Insight generation
│   │   ├── chart_agent.py           # Chart recommendation
│   │   ├── cleaning_agent.py        # Data preprocessing
│   │   └── visualization_agent.py   # Rule-based chart suggestion
│   │
│   ├── graph/
│   │   ├── workflow.py              # LangGraph StateGraph pipeline
│   │   └── nodes.py                 # Node definitions
│   │
│   ├── mcp_tools/
│   │   ├── server.py                # FastMCP server
│   │   ├── sql_tool.py              # DuckDB query wrapper
│   │   └── chart_tool.py            # Plotly chart builder
│   │
│   ├── memory/
│   │   └── memory.py                # Conversation memory management
│   │
│   ├── utils/
│   │   ├── llm.py                   # LLM client setup
│   │   ├── execution_logger.py      # Step-by-step execution logging
│   │   ├── context_builder.py       # Conversation context builder
│   │   ├── schema_builder.py        # Dataset schema extraction
│   │   └── sql_validator.py         # SQL safety validation
│   │
│   └── api/                         # API layer
│
├── frontend/
│   └── streamlit_app.py             # Main Streamlit UI (20 KB)
│
├── data/                            # Sample datasets
├── logs/                            # Execution logs
├── reports/                         # Generated reports
├── requirements.txt
├── .gitignore
└── test_llm.py                      # LLM connectivity test
```

---

## ⚙️ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-data-analyst-copilot.git
cd ai-data-analyst-copilot
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

```bash
# Windows
set OPENAI_API_KEY=your_key_here

# Mac/Linux
export OPENAI_API_KEY=your_key_here
```

### 5. Run the Streamlit app

```bash
streamlit run frontend/streamlit_app.py
```

### 6. (Optional) Start the MCP server

```bash
python app/mcp_tools/server.py
```

---

## 💡 Key Design Decisions

**Two-pass SQL validation** — `SQLReviewAgent` handles syntax cleanup while `CriticAgent` enforces business rules (no JOINs on single-table datasets, correct column names). Separating concerns keeps each agent focused and independently debuggable.

**Intent-first routing** — Before generating any SQL, the system extracts intent (entity + metric + operation). This enables hardcoded fast paths for high-confidence queries (e.g. "top customers") while the LLM handles the long tail — reducing unnecessary API calls.

**Context-aware rewriting** — `ContextAgent` rewrites follow-up questions ("only for California") into standalone queries before SQL generation, enabling natural multi-turn conversations without re-engineering downstream agents.

**LLM-optional design** — Common queries (top customers, top products, monthly trends) are resolved with rule-based shortcuts, bypassing the LLM entirely for speed and cost savings. The LLM is only invoked when rules don't match.

**MCP integration** — The system exposes analytics capabilities (health check, SQL execution, dataset stats, top products) as MCP tools via FastMCP, making it compatible with Claude and other MCP-aware clients.

**Execution logging** — Every agent step is logged via `ExecutionLogger`, making it easy to trace exactly which agent produced which output — critical for debugging multi-agent pipelines.

---

## 📈 Example Queries

```
"Who are the top 10 customers by revenue?"
"Show me monthly sales trends for last year"
"Which product categories are most profitable?"
"Compare sales across regions"
"What's the average order value?"
"Show me profit by sub-category"
```

---

## 🔒 Security

All SQL queries pass through `ValidationAgent` before execution, blocking any destructive operations (`DROP`, `DELETE`, `UPDATE`, `INSERT`). The system only runs `SELECT` queries against in-memory DataFrames — your source data is never modified.

---

## 📄 License

MIT License — free to use, modify, and distribute.
