from langchain_anthropic import ChatAnthropic
from .state import AgentState

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

def writer_node(state: AgentState) -> AgentState:
    feedback_section = (
        f"\nFeedback du reviewer : {state['feedback']}\nCorrige le draft en conséquence."
        if state.get("feedback") else ""
    )
    prompt = (
        f"Rédige un paragraphe clair sur '{state['topic']}' "
        f"en t'appuyant sur ces recherches :\n{state['research']}"
        f"{feedback_section}"
    )
    response = llm.invoke(prompt)
    return {**state, "draft": response.content, "feedback": None}