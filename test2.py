import os
from dotenv import find_dotenv, load_dotenv

# from newsapi import NewsApiClient

load_dotenv(find_dotenv(), override=True)

# newsapi = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))

# all_articles = newsapi.get_everything(
#     q="llm base search",
#     # sources="bbc-news,the-verge",
#     from_param="2024-06-22",
#     language="en",
#     # sort_by="relevancy",
# )

# print(all_articles)

from eventregistry import *

er = EventRegistry(apiKey=os.getenv("NEWSAPI_KEY2"))

# get the USA URI
usUri = er.getLocationUri("USA")  # = http://en.wikipedia.org/wiki/United_States

q = QueryEvents(keywords="Star Wars")
q.setRequestedResult(
    RequestEventsInfo(sortBy="date", count=50)
)  # request event details for latest 50 events

# get the full list of 50 events at once
print(er.execQuery(q))
