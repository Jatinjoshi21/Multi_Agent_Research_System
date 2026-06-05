# 🔬 Multi-Agent Research System

A modular, multi-agent pipeline that automates end-to-end research on any topic — from web search and content scraping to report writing and critical evaluation — with a polished Streamlit UI.

---

## ✨ Features

- **4-Stage Agentic Pipeline** — Search → Scrape → Write → Critique, each handled by a dedicated agent or chain
- **Streamlit UI** — Live pipeline visualizer with per-step status, tabbed results, and a final report card
- **Downloadable Reports** — Export the generated report as a `.txt` file directly from the UI
- **Modular Architecture** — Agents and chains are independently defined in `agents.py`, making them easy to swap or extend

---

## 🗂️ Project Structure

```
MULTIAGENTSYSTEM/
├── agents.py          # Agent & chain definitions (search, reader, writer, critic)
├── pipeline.py        # Core pipeline logic (CLI entry point)
├── app.py             # Streamlit UI
├── tools.py           # Custom tools used by agents
├── requirements.txt   # Python dependencies
├── .env               # API keys and environment variables (not committed)
└── .gitignore
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd MULTIAGENTSYSTEM
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key     # or whichever search API you use
```

---

## 🖥️ Running the App

### Streamlit UI (recommended)

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser, enter a research topic, and click **Run →**.

### CLI (headless)

```bash
python pipeline.py
```

You'll be prompted to enter a research topic. Results are printed to the terminal.

---

## 🔄 Pipeline Overview

```
User Input (topic)
      │
      ▼
┌─────────────┐
│ Search Agent │  ← Searches the web for recent information on the topic
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Reader Agent │  ← Picks the most relevant URL and scrapes it for deep content
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Writer Chain │  ← Synthesizes search + scraped content into a structured report
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Critic Chain │  ← Reviews the report and provides actionable feedback
└─────────────┘
```

| Step | Component | Role |
|------|-----------|------|
| 1 | `build_search_agent()` | Queries the web for up-to-date information |
| 2 | `build_reader_agent()` | Scrapes the most relevant source URL |
| 3 | `writer_chain` | Drafts a comprehensive research report |
| 4 | `critic_chain` | Evaluates quality and suggests improvements |

---

## 📦 Dependencies

Key packages (see `requirements.txt` for full list):

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI |
| `langchain` | Agent and chain orchestration |
| `langchain-anthropic` | Claude LLM integration |
| `tavily-python` | Web search tool |
| `beautifulsoup4` / `requests` | Web scraping |
| `python-dotenv` | Environment variable management |

---
