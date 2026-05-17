from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import app as agent_graph
from agents.state import AgentState

api = FastAPI(title="Multi-Agent API", version="1.0.0")

class TopicRequest(BaseModel):
    topic: str

class AgentResponse(BaseModel):
    topic: str
    research: str
    draft: str
    iterations: int
    approved: bool

@api.post("/generate", response_model=AgentResponse)
async def generate(request: TopicRequest):
    try:
        initial_state: AgentState = {
            "topic": request.topic,
            "research": None,
            "draft": None,
            "feedback": None,
            "approved": False,
            "iterations": 0,
        }
        result = agent_graph.invoke(initial_state)
        return AgentResponse(
            topic=result["topic"],
            research=result["research"],
            draft=result["draft"],
            iterations=result["iterations"],
            approved=result["approved"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api.get("/health")
async def health():
    return {"status": "ok"}