from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition

from agents.nutritionist import NutritionistAgent
from llms.main import llm
from prompts.nutritionist_agent import prompt
from tools.calorie_calculator import calculate_calories
from tools.user_info_extractor import extract_user_info
from utils.state import State
from utils.tools import create_tool_node_with_fallback

tools = [calculate_calories, extract_user_info]

assistant_runnable = prompt | llm.bind_tools(tools)

graph_builder = StateGraph(State)
memory = MemorySaver()


graph_builder.add_node('assistant', NutritionistAgent(assistant_runnable))
graph_builder.add_node('tools', create_tool_node_with_fallback(tools))

graph_builder.add_edge(START, 'assistant')

graph_builder.add_conditional_edges(
    'assistant',
    tools_condition,
)
graph_builder.add_edge('tools', 'assistant')

agent_graph = graph_builder.compile(checkpointer=memory)


if __name__ == '__main__':
    from IPython.display import Image, display

    try:
        display(Image(agent_graph.get_graph(xray=True).draw_mermaid_png()))
    except Exception:
        # This requires some extra dependencies and is optional
        pass
