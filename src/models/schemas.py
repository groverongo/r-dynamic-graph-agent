from typing import Dict, List, Sequence, TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

GraphDetails = Dict[str, List[str]]

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    graph: GraphDetails
