from smolagents import CodeAgent, HfApiModel
from sql_engine_tool import SqlEngineTool

agent = CodeAgent(
    tools=[SqlEngineTool],
    model=HfApiModel("meta-llama/Meta-Llama-3.1-8B-Instruct"),
)
response = agent.run("Can you design employee and department tables with some sample data?")
print(response)