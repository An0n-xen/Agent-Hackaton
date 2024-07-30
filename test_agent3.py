from crewai import Crew, Process, Agent, Task
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
from tools.test_tool import getNewsDesc, search_internet

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

search_tool = SerperDevTool()

manager_llm = ChatOpenAI(model_name="gpt-4o-mini")
agent_llm = ChatOpenAI(model_name="gpt-4o", temperature=0)


SentimentAgent = Agent(
    role="Get the news descriptions on the topic {topic} and analyze various pieces of data and provide insightful reflections based on the content",
    goal="Get the news descriptions on the topic {topic} and analyze various pieces of data and provide insightful reflections based on the content",
    backstory="AI trained to analyze various pieces of data and provide insightful reflections based on the content",
    verbose=True,
    allow_delegation=False,
    LLM=agent_llm,
    tools=[search_internet],
)

CompaniesSearch = Agent(
    role="From sourcing strategies, search for startup that fit the sourcing strategies",
    goal="From sourcing strategies, search for startup that fit the sourcing strategies",
    backstory="you are an agent the find startups on the web",
    verbose=True,
    allow_delegation=False,
    LLM=agent_llm,
)

JsonParse = Agent(
    role="structure data in json format",
    goal="structure data into json format",
    backstory="you are a json formatter",
    verbose=False,
    allow_delegation=False,
    LLM=agent_llm,
)

SentimentTask = Task(
    agent=SentimentAgent,
    description="""
        Get the news descriptions on the topic {topic} and analyze various pieces of data and provide insightful reflections based on the content
        Identify the Key Information: Identify the main points or events described in each news description.

        Identify Trends and Implications: Look for any trends, patterns, or implications related to the topic.

        Generate a Reflection: Based on the key information and identified trends, provide a reflection that highlights the significance of the data. This reflection should connect the data to broader themes or trends and consider its impact .

        Filter Articles:
        Include Articles with Clear VC Trends: Based on the reflections, include only those articles that clearly indicate a trend relevant to VC investments.

        Exclude Articles without Clear Trends: Ignore articles that do not provide clear insights or trends for VC investments.
        
        Develop Sourcing Strategies: Based on the summarized reflections, develop sourcing strategies for potential investment opportunities in the AI sector

        Example
        News description: Hackers accessed OpenAI's internal systems last year and stole messages about AI design, prompting security concerns.
        Reflection: OpenAI, a tech giant, is even being hacked, so cybersecurity for AI is important. 

        News description: Wallace Shawn's Father Ignatius tangles with technology in this scene from episode 9, "How to Build a Chatbot."
        Reflection: No clear trend for a VC. 

        News description: Stay up to date on the latest AI technology advancements and learn about the challenges and opportunities AI presents now and for the future.
        Reflection: No clear trend for a VC. 

        News description: A California judge dismissed many of the claims outlined in a copyright lawsuit that accuses GitHub, Microsoft, and OpenAI of copying developers’ code.
        Reflection: Governments are getting more sensitive about AI's impact on copyright, so making data copyrightable or enabling publishers to monetize their data for AI training are getting more important.

        Note: the above is just an example do not hallucinate news descriptions from the above example
        
        The results you output should be of the format
        News description: The actual news description
        Reflection: The reflection you had on the news description
    """,
    expected_output="""
        Your output should be of the format
        
        News description: The actual news description
        Reflections: The reflection you had on the news description
        Sourcing strategies: The sourcing strategies you had on the news description
    """,
    max_iter=3,
)

CompaniesSearchTask = Task(
    agent=CompaniesSearch,
    description="""
        From each sourcing strategies you received from the previous agent, 
        from each sourcing strategy, narrow down on the category or kind of startup being described. 
        use tools available to search for startup that have less than 1 million dollars in funding and fit the sourcing strategies
    """,
    expected_output="Your output should be a list of the name of the companies and descriptions of the companies you found",
    context=[SentimentTask],
)


agent_crew = Crew(
    agents=[SentimentAgent, CompaniesSearch],
    tasks=[SentimentTask, CompaniesSearchTask],
    manager=manager_llm,
    process=Process.sequential,
)

inputs = {"topic": "llm based search"}
crew_results = agent_crew.kickoff(inputs=inputs)


print(crew_results)
