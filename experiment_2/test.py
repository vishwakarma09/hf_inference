from smolagents import load_tool, CodeAgent, HfApiModel, DuckDuckGoSearchTool
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("hf_token")
# Import tool from Hub
image_generation_tool = load_tool("m-ric/text-to-image", trust_remote_code=True)

search_tool = DuckDuckGoSearchTool()

agent = CodeAgent(
    tools=[search_tool],
    model=HfApiModel("Qwen/Qwen2.5-72B-Instruct", token=token),
    planning_interval=3 # This is where you activate planning!
)

# Run it!
result = agent.run(
    "How long would a cheetah at full speed take to run the length of Pont Alexandre III?",
)