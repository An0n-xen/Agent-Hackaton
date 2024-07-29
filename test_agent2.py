import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from utils.config import functions_description, news_trend_sentiment
from utils.utilities import getNews

load_dotenv(find_dotenv(), override=True)

client = OpenAI()


def getNewsDesc(query: str) -> str:
    """Useful to get the news descriptions"""
    return getNews(query)


def RunAgentFunction(func_name: str, func_arguments: dict):
    """
    Runs the specified agent function with the given arguments.

    Args:
        func_name (str): The name of the agent function to run.
        func_arguments: The arguments to pass to the agent function.

    Returns:
        The result from the agent function.
    """

    # Getting required function
    function = eval(func_name)

    # Running function and storing results
    result_from_function = function(func_arguments)
    return result_from_function


def run(messages: list) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0,
    )

    res = response.choices[0]

    # if res.finish_reason == "function_call":
    #     func_name = res.message.function_call.name
    #     func_args = json.loads(res.message.function_call.arguments)

    #     results = RunAgentFunction(func_name, func_args)

    #     messages = [{"role": "function", "name": func_name, "content": results}]

    #     print("fun")
    #     agent_response = run(messages)

    #     return agent_response

    agent_response = res.message.content
    return agent_response


if __name__ == "__main__":
    user_input = input("Enter a new topic: ")

    news_descriptions = getNewsDesc(user_input)

    messages = [
        {
            "role": "assistant",
            "content": news_trend_sentiment,
        },
        {"role": "user", "content": news_descriptions},
    ]

    results = run(messages=messages)

    print(results)
