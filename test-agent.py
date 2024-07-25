import json
from openai import OpenAI
from crewai import Crew, Process, Agent, Task
from langchain_openai import ChatOpenAI
from utils.config import (
    parse_json_des,
    expected_format,
    correct_format,
    search_op,
)
from utils.utilities import getCompanies
from tools.test_tool import getLocUUID, getCatUUID, getComp
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

manager_llm = ChatOpenAI(model_name="gpt-4o")
agent_llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
client = OpenAI()

JsonParseAgent = Agent(
    role="Given a text, identify and extract the relevant information for these keys and output it in a JSON format",
    goal="convert text to json json",
    backstory="json parser",
    verbose=False,
    allow_delegation=False,
    LLM=agent_llm,
)


JsonParseAgentAgent2 = Agent(
    role="take the json data from the previous agent and re parse it and output it in a JSON format",
    goal=f"get the json data in a json format {expected_format}",
    backstory="re parsing the json data in a json format",
    verbose=False,
    allow_delegation=False,
    LLM=agent_llm,
)

JsonParseAgentAgent3 = Agent(
    role="correctly format the json string and find companies",
    goal="correctly format the json string and find companies",
    # backstory="intelligent json string formatter and company finder",
    backstory="intelligent json string formatter",
    verbose=True,
    allow_delegation=False,
    LLM=agent_llm,
    max_iter=2,
)

ParseJsonTask = Task(
    agent=JsonParseAgent,
    description=parse_json_des,
    expected_output="json",
    human_input=True,
)

ParseJsonTaskTask2 = Task(
    agent=JsonParseAgentAgent2,
    description=f"""restructure the json data, by taking the non-null parameters and then output it in a json format,
                    Please do not hallucination any values, use the provided data in the json only.
                    when restructuring the json data, pay attention to search operators {search_op} and use the appropriate one
                    find the location's uuid using the tools you have if a location is provided, and do same for category if provided
                    for the field_ids leave it as it in the {expected_format} just focus on query section,
                    """,
    expected_output=f"""result should be in json string, in the example format {expected_format} also when parse the json, Please parse the final json string correctly
                """,
    context=[ParseJsonTask],
    tools=[getLocUUID, getCatUUID],
)

ParseJsonTask3 = Task(
    agent=JsonParseAgentAgent3,
    context=[ParseJsonTaskTask2],
    # description=f"{correct_format} after use the tools you have to find companies using the json string",
    description=f"{correct_format}",
    # tools=[getComp],
    expected_output="json",
)

agent_crew = Crew(
    agents=[JsonParseAgent, JsonParseAgentAgent2],
    tasks=[ParseJsonTask, ParseJsonTaskTask2],
    process=Process.sequential,
    verbose=2,
    manager_llm=manager_llm,
)

crew_results = agent_crew.kickoff()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0,
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": correct_format},
        {"role": "user", "content": crew_results},
    ],
)

results = response.choices[0].message.content

query = json.loads(results)

companies = getCompanies(query)

print(companies)
