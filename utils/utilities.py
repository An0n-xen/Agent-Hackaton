import os
import json
import requests
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv, find_dotenv
from newsapi import NewsApiClient

load_dotenv(find_dotenv(), override=True)

autocomplete_url = "https://api.crunchbase.com/api/v4/autocompletes"
organization_url = "https://api.crunchbase.com/api/v4/searches/organizations"

newsapi = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))

header = {
    "accept": "application/json",
    "X-cb-user-key": os.getenv("CRUNCHBASE_API_KEY"),
    "Content-Type": "application/json",
}


def getStories(type: str = "new") -> List:
    """_summary_

    Args:
        type (Str, optional): _description_. Defaults to "new, top, best".

    Returns:
        List: Returns a list of stories
    """
    url = f"https://hacker-news.firebaseio.com/v0/{type}stories.json"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def getItem(id: str) -> Dict:
    """_summary_

    Args:
        id (str): id of the item you want


    Returns:
        Dict: Returns a dictionary of the item
    """

    url = f" https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def convertUtc(date: str) -> datetime:
    n_datetime = datetime.fromtimestamp(int(date))

    return n_datetime.strftime("%Y-%m-%d %H:%M:%S")


def parseItem(item: Dict) -> Dict:
    results = {
        "id": item.get("id", ""),
        "by": item.get("by", ""),
        "type": item.get("type", ""),
        "time": convertUtc(item.get("time", "")),
        "title": item.get("title", ""),
        "url": item.get("url", ""),
        "text": item.get("text", ""),
        "kids": item.get("kids", []),
        "score": item.get("score", 0),
        "parents": item.get("parents", []),
        "descendants": item.get("descendants", 0),
    }

    return results


def getLocationUUID(location: str) -> str:
    params = {"query": location, "collection_ids": "locations", "limit": 1}

    response = requests.get(autocomplete_url, params=params, headers=header)

    if response.status_code == 200:
        data = response.json()
        uuid = data.get("entities")[0].get("identifier").get("uuid")
        return uuid
    else:
        return None


def getCategoryUUID(category: str) -> str:
    params = {"query": category, "collection_ids": "categories", "limit": 1}

    response = requests.get(autocomplete_url, params=params, headers=header)

    if response.status_code == 200:
        data = response.json()
        uuid = data.get("entities")[0].get("identifier").get("uuid")
        return uuid
    else:
        return None


def getCompanies(query: dict) -> dict:

    response = requests.post(organization_url, headers=header, data=json.dumps(query))
    companies = response.json()

    return companies


def getNews(query: str) -> str:
    results = ""
    all_articles = newsapi.get_everything(
        q=query,
        language="en",
        sort_by="relevancy",
    )

    for idx, article in enumerate(all_articles["articles"], start=1):
        results += f"{idx}. {article['description']}\n"

    return results
