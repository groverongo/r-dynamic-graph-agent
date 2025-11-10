from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph.message import add_messages
from typing import Annotated, Dict, List, Sequence, TypedDict
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, END

type GraphDetails = Dict[str, List[str]]

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    graph: GraphDetails


graph = StateGraph(AgentState)

@tool
def graph_details(graph: GraphDetails):
    '''
    This is a function that will analyze the graph and return some basic information about it.
    '''

    def max_degree(graph: GraphDetails) -> int:
        max_degree = 0
        for node in graph:
            if len(graph[node]) > max_degree:
                max_degree = len(graph[node])
        return max_degree

    def min_degree(graph: GraphDetails) -> int:
        min_degree = float('inf')
        for node in graph:
            if len(graph[node]) < min_degree:
                min_degree = len(graph[node])
        return min_degree

    def num_vertices(graph: GraphDetails) -> int:
        return len(graph)

    def num_edges(graph: GraphDetails) -> int:
        return sum(len(graph[node]) for node in graph) // 2

    return {
        "max_degree": max_degree(graph),
        "min_degree": min_degree(graph),
        "num_vertices": num_vertices(graph),
        "num_edges": num_edges(graph),
    }

tools = [graph_details, ]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
).bind_tools(tools)

def should_continue(state: AgentState) -> str:
    """Determine if we should continue or end the conversation."""

    messages = state["messages"]
    
    if not messages:
        return "continue"
    
    for message in reversed(messages):
        if (isinstance(message, ToolMessage) and 
            "saved" in message.content.lower() and
            "document" in message.content.lower()):
            return "end"
    
    return "continue"

def explain_graph(state: AgentState):
    '''
    This is a function that will provide an explanation of the graph
    '''
    graph_info = f"""The current graph has the following structure (adjacency list):\n"""
    for node, neighbors in state["graph"].items():
        graph_info += f"{node}: {', '.join(neighbors)}\n"
    
    system_prompt = SystemMessage(
        f'''You are a discrete mathematics professor currently teaching graph theory. You are being asked about specific graphs.
        
            Current Graph Information:
            {graph_info}

            When analyzing the graph, you can use the available tools to get more information about its properties. The graph is already loaded in the system, so you can reference it directly in your explanations.'''
    )

    if not state["messages"]:
        user_input = "I'm ready to help you understand graphs. What would you like to know about?"
        user_message = HumanMessage(content=user_input)

    else:
        user_input = input("\nWhat else would you like to know about the graph? ")
        print(f"\n👤 USER: {user_input}")
        user_message = HumanMessage(content=user_input)

    all_messages = [system_prompt] + list(state["messages"]) + [user_message]

    response = llm.invoke(all_messages)

    print(f"\n🤖 AI: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"🔧 USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages": list(state["messages"]) + [user_message, response]}

graph = StateGraph(AgentState)

PROFESSOR_NODE = "professor"
TOOLS_NODE = "tools"

graph.add_node(PROFESSOR_NODE, explain_graph)
graph.add_node(TOOLS_NODE, ToolNode(tools))

graph.set_entry_point(PROFESSOR_NODE)

graph.add_edge(PROFESSOR_NODE, TOOLS_NODE)

graph.add_conditional_edges(
    TOOLS_NODE,
    should_continue,
    {
        "continue": PROFESSOR_NODE,
        "end": END,
    },
)

app = graph.compile()


def run_graph_agent(custom_graph: GraphDetails = None):
    """
    Run the graph analysis agent with an optional custom graph.
    If no graph is provided, uses a default triangle graph.
    
    Args:
        custom_graph: Optional dictionary representing the graph as an adjacency list
    """
    def print_messages(messages):
        """Function I made to print the messages in a more readable format"""
        if not messages:
            return
        
        for message in messages[-3:]:
            if isinstance(message, ToolMessage):
                print(f"\n🛠️ TOOL RESULT: {message.content}")

    print("\n ===== GRAPH AGENT =====")
    
    # Use custom graph if provided, otherwise use default triangle graph
    state = {"messages": [], "graph": custom_graph}
    
    print(f"\nAnalyzing graph with {len(custom_graph)} nodes...")
    
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ===== GRAPH ANALYSIS COMPLETE =====")

if __name__ == "__main__":
    # Example of using a custom graph
    custom_graph = {
        'a': ['b', 'd'],
        'b': ['a', 'c'],
        'c': ['b', 'd'],
        'd': ['a', 'c', 'e'],
        'e': ['d']
    }
    run_graph_agent(custom_graph)
    
    # Or use the default graph:
    # run_graph_agent()


