"""Graph Agent implementation."""
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from ..config.settings import settings
from ..models.schemas import AgentState

class GraphAgent:
    """Agent for analyzing and explaining graphs."""
    
    def __init__(self, tools: List[Any]):
        """Initialize the GraphAgent with tools."""
        self.llm = self._setup_llm(tools)
    
    def _setup_llm(self, tools: List[Any]):
        """Configure the language model with tools."""
        return ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            timeout=settings.TIMEOUT,
            max_retries=settings.MAX_RETRIES,
        ).bind_tools(tools)
    
    def process_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Process a node in the agent's state graph.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with new messages
        """
        graph_info = self._format_graph_info(state["graph"])
        system_prompt = self._create_system_prompt(graph_info)
        
        if not state["messages"]:
            user_input = "I'm ready to help you understand graphs. What would you like to know about?"
            user_message = HumanMessage(content=user_input)
        else:
            user_input = input("\nWhat else would you like to know about the graph? ")
            print(f"\n👤 USER: {user_input}")
            user_message = HumanMessage(content=user_input)
        
        all_messages = [system_prompt] + list(state["messages"]) + [user_message]
        response = self.llm.invoke(all_messages)
        
        print(f"\n🤖 AI: {response.content}")
        if hasattr(response, "tool_calls") and response.tool_calls:
            print(f"🔧 USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")
        
        return {"messages": list(state["messages"]) + [user_message, response]}
    
    def _format_graph_info(self, graph: Dict[str, List[str]]) -> str:
        """Format graph information for the system prompt."""
        if not graph:
            return "No graph data available."            
        graph_info = "The current graph has the following structure (adjacency list):\n"
        for node, neighbors in graph.items():
            graph_info += f"{node}: {', '.join(neighbors)}\n"
        return graph_info
    
    def _create_system_prompt(self, graph_info: str) -> SystemMessage:
        """Create the system prompt with graph context."""
        return SystemMessage(
            f"""You are a discrete mathematics professor currently teaching graph theory. 
            You are being asked about specific graphs.
            
            Current Graph Information:
            {graph_info}

            When analyzing the graph, you can use the available tools to get more information 
            about its properties. The graph is already loaded in the system, so you can 
            reference it directly in your explanations."""
        )
