from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


class ChatAgentService:
    memory = MemorySaver()
    model = ChatAnthropic(model_name="claude-3-7-sonnet-latest")
    search = TavilySearchResults(max_results=2)
    tools = [search]
    agent_executor = create_react_agent(model, tools, checkpointer=memory)

    def __init__(self):
        raise TypeError(
            "ChatAgentService is a utility class and cannot be instantiated."
        )

    @classmethod
    async def generate_response(cls, prompt: str) -> str:
        # Unique ID to associate prompts with a thread in memory
        config = {"configurable": {"thread_id": "1"}}
        input = {
            "messages": [HumanMessage(content=prompt)],
        }
        async for step in cls.agent_executor.astream(
            input,
            config,
            stream_mode="values",
        ):
            response = step["messages"][-1].content

        return response
