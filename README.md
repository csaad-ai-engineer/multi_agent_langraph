# Multi-Agent LangGraph Demo

A multi-agent content generation pipeline built with [LangGraph](https://github.com/langchain-ai/langgraph). Given a topic, three specialized agents collaborate in a loop to research, write, and review a paragraph until the output is approved.

## How it works

```
                        ┌─────────────────────────────────────────────────┐
                        │                  AgentState                     │
                        │  topic · research · draft · feedback · approved │
                        └─────────────────────────────────────────────────┘

        ┌───────────────────┐     research     ┌───────────────────┐
 START ─►                   ├─────────────────►│                   │
        │    Researcher     │                  │      Writer       │◄──────────┐
        │                   │                  │                   │           │
        └───────────────────┘                  └────────┬──────────┘           │
          Gathers key facts                             │ draft                │
          about the topic                              ▼                      │
                                             ┌───────────────────┐  feedback  │
                                             │                   ├────────────┘
                                             │     Reviewer      │  (revision requested,
                                             │                   │   max 2 iterations)
                                             └────────┬──────────┘
                                                      │ approved
                                                      ▼
                                                    END
```

| Agent | Role |
|-------|------|
| **Researcher** | Gathers key facts about the topic |
| **Writer** | Drafts a paragraph using the research (incorporates reviewer feedback on retry) |
| **Reviewer** | Approves the draft or requests a revision with brief feedback |

The loop exits when the reviewer approves or after 2 iterations.

## Prerequisites

- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

1. Clone the repo and install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your API key in `.env`:

```
ANTHROPIC_API_KEY=your_key_here
```

## Usage

### CLI

Run the pipeline directly on a hardcoded topic:

```bash
python main.py
```

The script prints the graph structure, research output, final draft, and number of iterations used.

To change the topic, edit the `topic` variable in `main.py`:

```python
topic = "The benefits of solar energy"
```

### REST API

Start the FastAPI server:

```bash
uvicorn api:api --reload
```

The API is available at `http://localhost:8000`.

**POST /generate**

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "The benefits of solar energy"}'
```

Response:

```json
{
  "topic": "The benefits of solar energy",
  "research": "...",
  "draft": "...",
  "iterations": 1,
  "approved": true
}
```

**GET /health**

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

Interactive docs are available at `http://localhost:8000/docs`.

### Docker

Build and run with Docker:

```bash
docker build -t multi-agent-demo .
docker run -p 8000:8000 --env-file .env multi-agent-demo
```

The API will be accessible at `http://localhost:8000`.

## Project structure

```
.
├── agents/
│   ├── state.py        # Shared AgentState TypedDict
│   ├── researcher.py   # Researcher agent node
│   ├── writer.py       # Writer agent node
│   └── reviewer.py     # Reviewer agent node
├── main.py             # LangGraph workflow definition and CLI entry point
├── api.py              # FastAPI wrapper
├── Dockerfile
└── requirements.txt
```
