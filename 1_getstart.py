from smolagents import CodeAgent, LiteLLMModel
from smolagents import tool
from smolagents.agents import ToolCallingAgent
from smolagents import DuckDuckGoSearchTool

model=LiteLLMModel(model_id="ollama_chat/llama3.2", api_key="ollama")

agent=CodeAgent(tools=[],model=model,
                add_base_tools=True)

agent.run("Could you give me the 118th number in the Fibonacci sequence?",
          )