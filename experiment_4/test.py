from smolagents import CodeAgent, HfApiModel
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float, insert, inspect, text
from sql_engine_tool import sql_engine

engine = create_engine("sqlite:///experiment_4/courses.db:")
agent = CodeAgent(
    tools=[sql_engine],
    model=HfApiModel("meta-llama/Meta-Llama-3.1-8B-Instruct"),
)
agent.run("Can you give me the name of the client who got the most expensive receipt?")