from typing import Annotated, Optional, TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    pdf_path: Optional[str]
    pdf_sent: bool = False
