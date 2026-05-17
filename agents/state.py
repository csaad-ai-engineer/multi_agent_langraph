from typing import TypedDict, Optional

class AgentState(TypedDict):
    topic: str
    research: Optional[str]
    draft: Optional[str]
    feedback: Optional[str]
    approved: bool
    iterations: int