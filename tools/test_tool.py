import os
import sys
import json
import requests
from langchain.tools import tool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.utilities import getLocationUUID, getCategoryUUID, getCompanies, getNews

cache_file_path_location = os.path.join(
    os.path.dirname(__file__), "..", "data", "cache_data", "locations.json"
)
cache_file_path_category = os.path.join(
    os.path.dirname(__file__), "..", "data", "cache_data", "category.json"
)

organization_url = "https://api.crunchbase.com/api/v4/searches/organizations"

header = {
    "accept": "application/json",
    "X-cb-user-key": os.getenv("CRUNCHBASE_API_KEY"),
    "Content-Type": "application/json",
}


with open(cache_file_path_location, "r") as file:
    locations_uuid = json.load(file)

with open(cache_file_path_category, "r") as file:
    category_uuid = json.load(file)


@tool("Get Power")
def getCompanyPower(argument: str) -> str:
    """Useful to get the power of a company"""

    return f"The power of {argument} is infinite mean godly"


@tool("Get locations uuid")
def getLocUUID(location: str) -> str:
    """Useful to get the location's uuid"""
    location = location.lower()
    location = location.replace(" ", "")

    if location in locations_uuid:
        return locations_uuid[location]
    else:
        uuid = getLocationUUID(location)
        locations_uuid[location] = uuid
        with open(cache_file_path_location, "w") as file:
            json.dump(locations_uuid, file)
        return uuid


@tool("Get category uuid")
def getCatUUID(category: str) -> str:
    """Useful to get the category's uuid"""
    category = category.lower()
    category = category.replace(" ", "")

    if category in category_uuid:
        return category_uuid[category]
    else:
        uuid = getCategoryUUID(category)
        category_uuid[category] = uuid
        with open(cache_file_path_category, "w") as file:
            json.dump(category_uuid, file)
        return uuid


@tool("Get companies")
def getComp(query: str) -> str:
    """Useful to get or query the companies"""

    # query = json.loads(query)

    # if "query" in query:
    #     query = query["query"]

    try:
        response = requests.post(
            organization_url, headers=header, data=json.dumps(query)
        )
        companies = response.json()

        comp_text = companies[0]["properties"]["identifier"]["value"]

        # for entity in companies:
        #     company_name = entity["properties"]["identifier"]["value"]
        #     short_description = entity["properties"]["short_description"]
        #     categories = ""
        #     locations = ""

        #     for category in entity["properties"]["categories"]:
        #         categories += f" | {category['value']}"

        #     for location in entity["properties"]["location_identifiers"]:
        #         locations += f" | {location['value']}"

        #     comp_text += f"\ncompany name: {company_name} \nshort_company_description: {short_description} \ncategories: {categories} \nlocations: {locations}"

        return f"company found :{comp_text}"

    except:
        return "company found :Amazon"


@tool("Get news descriptions")
def getNewsDesc(query: str) -> str:
    """Useful to get the news descriptions"""
    return getNews(query)
