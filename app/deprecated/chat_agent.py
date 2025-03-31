from langchain.agents import initialize_agent
from langchain.tools import StructuredTool
from langchain.agents.agent_types import AgentType

from .ai_model_langchain import AIModelLangChain


class ChatAgent:
    tool = StructuredTool.from_function(
        name="document_qa",
        func=AIModelLangChain.generate_response,
        description="Answers questions about internal documents.",
    )
    agent_executer = initialize_agent(
        # Provide tools for the agent to pick from
        tools=[tool],
        # The agent uses this model to decide what tools to use, plan, and possibly to generate the response
        llm=AIModelLangChain.chat_model,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    @classmethod
    def generate_response(cls, prompt: str) -> str:
        return cls.agent_executer.invoke(prompt)["output"]
