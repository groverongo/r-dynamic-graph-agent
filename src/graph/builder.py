"""Graph builder for the agent's state machine."""
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import Callable, Dict, Any, List
from ..models.schemas import AgentState

def should_continue(state: AgentState) -> str:
    """
    Determine if the conversation should continue or end.
    
    Args:
        state: Current agent state
        
    Returns:
        str: Next node to transition to or END
    """
    messages = state["messages"]
    
    if not messages:
        return "continue"
    
    for message in reversed(messages):
        if (hasattr(message, 'content') and 
            isinstance(message.content, str) and
            "saved" in message.content.lower() and
            "document" in message.content.lower()):
            return "end"
    
    return "continue"

def build_graph(
    tools: List[Any],
    process_node: Callable[[Dict[str, Any]], Dict[str, Any]]
) -> StateGraph:
    """
    Build and configure the agent's state graph.
    
    Args:
        tools: List of tools available to the agent
        process_node: Function to process nodes in the graph
        
    Returns:
        Configured StateGraph instance
    """
    graph = StateGraph(AgentState)
    
    # Define node names as constants
    PROFESSOR_NODE = "professor"
    TOOLS_NODE = "tools"
    
    # Add nodes
    graph.add_node(PROFESSOR_NODE, process_node)
    graph.add_node(TOOLS_NODE, ToolNode(tools))
    
    # Set entry point
    graph.set_entry_point(PROFESSOR_NODE)
    
    # Add edges
    graph.add_edge(PROFESSOR_NODE, TOOLS_NODE)
    
    # Add conditional edges
    graph.add_conditional_edges(
        TOOLS_NODE,
        should_continue,
        {
            "continue": PROFESSOR_NODE,
            "end": END,
        },
    )
    
    return graph
