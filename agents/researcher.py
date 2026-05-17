from langchain_anthropic import ChatAnthropic
from .state import AgentState

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

def researcher_node(state: AgentState) -> AgentState:
    prompt = f"Recherche des faits clés et concis sur : {state['topic']}"
    response = llm.invoke(prompt)
    return {**state, "research": response.content}