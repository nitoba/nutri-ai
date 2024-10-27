from langchain_core.runnables import Runnable, RunnableConfig

from utils.state import State


class NutritionistAgent:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            # configuration = config.get('configurable', {})
            # state = {**state, 'user_info': passenger_id}
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get('text')
            ):
                messages = state['messages'] + [
                    ('user', 'Respond with a real output.')
                ]
                state = {**state, 'messages': messages}
            else:
                break
        return {'messages': result}
