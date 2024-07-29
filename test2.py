import os
import requests
import json
from dotenv import find_dotenv, load_dotenv

from newsapi import NewsApiClient

load_dotenv(find_dotenv(), override=True)


def search_internet(query):
    """Useful to search the internet
    about a a given topic and return relevant results"""
    top_result_to_return = 4
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        "X-API-KEY": os.environ["SERPER_API_KEY"],
        "content-type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()["organic"]
    string = []

    for result in results[:top_result_to_return]:
        try:
            string.append(
                "\n".join(
                    [
                        f"Title: {result['title']}",
                        f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}",
                        "\n-----------------",
                    ]
                )
            )
        except KeyError:
            next

    return "\n".join(string)


data = search_internet("startups that offer llm based search")
print(data)
# results = ""

# newsapi = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))
# all_articles = newsapi.get_everything(
#     q="Tech event about AI",
#     # sources="bbc-news,the-verge",
#     language="en",
#     # sort_by="relevancy",
# )

# for idx, article in enumerate(all_articles["articles"], start=1):
#     results += f"{idx}. {article['description']}\n"

# print(results)

# from eventregistry import *

# er = EventRegistry(apiKey=os.getenv("NEWSAPI_KEY2"))

# # get the USA URI
# usUri = er.getLocationUri("USA")  # = http://en.wikipedia.org/wiki/United_States

# q = QueryEvents(keywords="Star Wars")
# q.setRequestedResult(
#     RequestEventsInfo(sortBy="date", count=50)
# )  # request event details for latest 50 events

# # get the full list of 50 events at once
# print(er.execQuery(q))
