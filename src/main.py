"""
Main entry point for the Graph Agent application.

This module provides the command-line interface for running the graph analysis agent.
"""
import sys
from typing import Dict, List, Optional
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.agents.graph_agent import GraphAgent
from src.tools.graph_tools import get_tools
from src.graph.builder import build_graph


def run_graph_agent(custom_graph: Optional[Dict[str, List[str]]] = None) -> None:
    """
    Run the graph analysis agent with an optional custom graph.
    
    Args:
        custom_graph: Optional dictionary representing the graph as an adjacency list.
                     If not provided, a default graph will be used.
    """
    def print_messages(messages):
        """Helper function to print messages in a readable format."""
        if not messages:
            return
        
        for message in messages[-3:]:
            if hasattr(message, 'content') and hasattr(message, 'type') and message.type == 'tool':
                print(f"\n🛠️ TOOL RESULT: {message.content}")

    # Use custom graph if provided, otherwise use default
    if custom_graph is None:
        custom_graph = {
            'a': ['b', 'd'],
            'b': ['a', 'c'],
            'c': ['b', 'd'],
            'd': ['a', 'c', 'e'],
            'e': ['d']
        }
    
    print("\n ===== GRAPH AGENT =====")
    print(f"\nAnalyzing graph with {len(custom_graph)} nodes...")
    
    # Initialize agent and tools
    tools = get_tools()
    agent = GraphAgent(tools=tools)
    
    # Build and compile the graph
    workflow = build_graph(tools=tools, process_node=agent.process_node)
    app = workflow.compile()
    
    # Initial state
    state = {"messages": [], "graph": custom_graph}
    
    # Run the agent
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ===== GRAPH ANALYSIS COMPLETE =====")


if __name__ == "__main__":
    # Example usage with a custom graph
    example_graph = {
        'a': ['b', 'd'],
        'b': ['a', 'c'],
        'c': ['b', 'd'],
        'd': ['a', 'c', 'e'],
        'e': ['d']
    }
    run_graph_agent(example_graph)
