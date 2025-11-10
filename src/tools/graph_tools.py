from typing import Dict, List
from langchain_core.tools import tool

@tool
def graph_details(graph: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Analyze the graph and return basic information about it.
    
    Args:
        graph: Dictionary representing the graph as an adjacency list
        
    Returns:
        Dictionary containing graph metrics
    """
    def max_degree(g: Dict[str, List[str]]) -> int:
        return max((len(neighbors) for neighbors in g.values()), default=0)

    def min_degree(g: Dict[str, List[str]]) -> int:
        return min((len(neighbors) for neighbors in g.values()), default=0)

    def num_vertices(g: Dict[str, List[str]]) -> int:
        return len(g)

    def num_edges(g: Dict[str, List[str]]) -> int:
        return sum(len(neighbors) for neighbors in g.values()) // 2

    if not graph:
        return {
            "max_degree": 0,
            "min_degree": 0,
            "num_vertices": 0,
            "num_edges": 0,
        }
        
    return {
        "max_degree": max_degree(graph),
        "min_degree": min_degree(graph),
        "num_vertices": num_vertices(graph),
        "num_edges": num_edges(graph),
    }

def get_tools():
    return [graph_details]
