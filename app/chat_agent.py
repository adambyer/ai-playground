from typing import Sequence
from langchain.chat_models import init_chat_model
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, BaseMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict


class ChatAgentMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._initialized = False
        cls._setup()


class MessageState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str


class ChatAgent(metaclass=ChatAgentMeta):
    model = init_chat_model("claude-3-5-haiku-latest", model_provider="anthropic")
    search = TavilySearchResults(max_results=2)
    agent_executor = create_react_agent(model, [search])
    graph = StateGraph(state_schema=MessageState)
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're excessively complimentary. Answer all questions to the best of your ability in {language}, but always include at least one over-the-top compliment.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    message_trimmmer = (
        trim_messages(  # This is used to reduce the messages we send back to the model.
            max_tokens=500,
            strategy="last",
            token_counter=model,
            include_system=True,
            allow_partial=False,
            start_on="human",
        )
    )
    app = None

    @classmethod
    def _setup(cls):
        if not cls._initialized:
            # Setup graph with memory

            # Specify the starting node (an edge defines what comes next)
            cls.graph.add_edge(START, "call_model")

            # Define the call_model node
            cls.graph.add_node("call_model", cls._call_model)

            memory = MemorySaver()
            cls.app = cls.graph.compile(checkpointer=memory)

            cls._initialized = True

    @classmethod
    async def _call_model(cls, state: MessageState) -> dict[str, BaseMessage]:
        # Remove old messages before sending to the model
        messages = await cls.message_trimmmer.ainvoke(state["messages"])
        state = MessageState(messages=messages, language=state["language"])
        prompt = await cls.prompt_template.ainvoke(state)
        response = await cls.model.ainvoke(prompt)
        return {"messages": response}

    @classmethod
    async def generate_response(cls, prompt: str, language: str) -> str:
        # Unique ID to associate prompts with a thread in memory
        config = {"configurable": {"thread_id": "1"}}

        input = MessageState(messages=[HumanMessage(prompt)], language=language)
        response = await cls.app.ainvoke(input, config)
        return response["messages"][-1].content
