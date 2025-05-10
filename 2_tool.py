import os
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool, Tool
import wikipediaapi
from datetime import datetime
import pytz

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

class WikipediaSearchTool(Tool):
    name = "wikipedia"
    description = "Searches Wikipedia for a given query and returns a summary."
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to search Wikipedia for."
        }
    }
    output_type = "string"
    def forward(self, query: str) -> str:
        wiki = wikipediaapi.Wikipedia('en')
        page = wiki.page(query)
        if page.exists():
            return page.summary[:500]  # Limit summary length
        else:
            return "No Wikipedia page found for your query."
class CurrentDateTimeTool(Tool):
    name = "current_datetime"
    description = "Returns the current date and time in UTC."
    inputs = {}
    output_type = "string"

    def forward(self) -> str:
        now = datetime.now(pytz.utc)
        return now.strftime("%Y-%m-%d %H:%M:%S %Z")

wiki_tool = WikipediaSearchTool()
datetime_tool = CurrentDateTimeTool()
search_tool = DuckDuckGoSearchTool()

model=LiteLLMModel(model_id="ollama/llama3.2", api_key="ollama")

model.flatten_messages_as_text = True

agent = CodeAgent(
    tools=[search_tool, wiki_tool, datetime_tool],
    model=model,
    add_base_tools=False,
    verbosity_level=2
)

response = agent.run("How many days ago did Germany last win the FIFA World Cup?")
print(response)