import json
from langchain_openai import ChatOpenAI
from crewai import Crew, Process, Agent, Task
from tools.test_tool import getNewsDesc

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)


manager_llm = ChatOpenAI(model_name="gpt-4o-mini")
agent_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)


NewsSentimentAgent = Agent(
    role="Find the sentiment of the news",
    goal="Find the sentiment of the news",
    backstory="News Sentiment analyist to find the sentiment of the news",
    verbose=True,
    allow_delegation=False,
    LLM=agent_llm,
)

NewsSentimentTask = Task(
    agent=NewsSentimentAgent,
    description="Use the tool to get the news descriptions, before getting the news descriptions, wait for human input so you which news description you want to get, Then find the sentiment of the news descriptions, give a percentage score for each of these sections Positive, Negative, Tools building, Break throughs, Research and development",
    expected_output="""
            the output should be in this format
            
                Postive - (positive count / total count)
                Negative - (negative count / total count)
                Research development - (research development count / total count)
                Tools building - (tools building count / total count)
                Break throughs - (break throughs count / total count)
        """,
    human_input=True,
    tools=[getNewsDesc],
)

agent_crew = Crew(
    agents=[NewsSentimentAgent],
    tasks=[NewsSentimentTask],
    process=Process.sequential,
    verbose=2,
    manager_llm=manager_llm,
)

crew_results = agent_crew.kickoff()
print(crew_results)
