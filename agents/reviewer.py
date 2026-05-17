from langchain_anthropic import ChatAnthropic
from .state import AgentState

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

def reviewer_node(state: AgentState) -> AgentState:
    prompt = (
        f"Évalue ce texte sur '{state['topic']}'. "
        "Réponds UNIQUEMENT par 'APPROUVÉ' si c'est bien, "
        "ou par 'RÉVISION: <critique courte>' si besoin d'amélioration.\n\n"
        f"Texte :\n{state['draft']}"
    )
    response = llm.invoke(prompt)
    content = response.content.strip()

    if content.startswith("APPROUVÉ") or state.get("iterations", 0) >= 2:
        return {**state, "approved": True, "iterations": state.get("iterations", 0) + 1}
    else:
        feedback = content.replace("RÉVISION:", "").strip()
        return {**state, "approved": False, "feedback": feedback,
                "iterations": state.get("iterations", 0) + 1}