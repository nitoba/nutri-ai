from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import tools_condition

from agents.nutritionist import NutritionistAgent
from llms.main import llm
from prompts.nutritionist_agent import prompt
from tools.calorie_calculator import calculate_calories
from tools.generate_meal_plan_pdf import generate_meal_plan_pdf
from tools.user_info_extractor import extract_user_info
from utils.state import State
from utils.tools import create_tool_node_with_fallback

safe_tools = [calculate_calories, extract_user_info]
generate_tools = [generate_meal_plan_pdf]

generate_tool_names = {t.name for t in generate_tools}

assistant_runnable = prompt | llm.bind_tools(safe_tools)

graph_builder = StateGraph(State)
memory = MemorySaver()


graph_builder.add_node('assistant', NutritionistAgent(assistant_runnable))
graph_builder.add_node(
    'safe_tools', create_tool_node_with_fallback(safe_tools)
)
graph_builder.add_node(
    'generate_tools', create_tool_node_with_fallback(generate_tools)
)

graph_builder.add_edge(START, 'assistant')


def route_tools(state: State):
    next_node = tools_condition(state)
    # If no tools are invoked, return to the user
    if next_node == END:
        return END
    ai_message = state['messages'][-1]
    # This assumes single tool calls. To handle parallel tool calling, you'd want to
    # use an ANY condition
    first_tool_call = ai_message.tool_calls[0]
    if first_tool_call['name'] in generate_tool_names:
        return 'generate_tools'
    return 'safe_tools'


graph_builder.add_conditional_edges(
    'assistant', route_tools, ['safe_tools', 'generate_tools', END]
)

graph_builder.add_edge('safe_tools', 'assistant')

agent_graph = graph_builder.compile(checkpointer=memory)


if __name__ == '__main__':
    from IPython.display import Image, display

    try:
        display(Image(agent_graph.get_graph(xray=True).draw_mermaid_png()))
    except Exception:
        # This requires some extra dependencies and is optional
        pass
