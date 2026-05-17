from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.researcher import researcher_node
from agents.writer import writer_node
from agents.reviewer import reviewer_node

# --- Définition du graphe ---
workflow = StateGraph(AgentState)

# Ajouter les nœuds
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)

# Définir le point d'entrée
workflow.set_entry_point("researcher")

# Transitions fixes
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")

# Transition conditionnelle depuis le reviewer
def should_continue(state: AgentState):
    return END if state["approved"] else "writer"

workflow.add_conditional_edges("reviewer", should_continue)

# Compiler le graphe
app = workflow.compile()

# --- Exécution ---
if __name__ == "__main__":
    topic = "Les avantages de l'énergie solaire"
    print(f"Sujet : {topic}\n{'='*50}")
    print(app.get_graph().draw_ascii())

    initial_state: AgentState = {
        "topic": topic,
        "research": None,
        "draft": None,
        "feedback": None,
        "approved": False,
        "iterations": 0,
    }

    result = app.invoke(initial_state)

    print(f"Recherches :\n{result['research']}\n")
    print(f"Draft final :\n{result['draft']}\n")
    print(f"Approuvé en {result['iterations']} itération(s)")