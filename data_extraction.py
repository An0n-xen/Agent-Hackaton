import os
import json
from utils.utilities import getStories, getItem, parseItem


def runPulling(
    Stories: list[int],
    data: dict[list],
    n_collected: int,
    story_type: str,
    is_start: bool = False,
):
    if is_start:
        n_collected = 0

    print(f"Data pulling started")

    count = 0
    for idx in range(n_collected, len(Stories)):
        # Checkpoint
        if count > 0 and count % 3 == 0:
            with open(f"./data/{story_type}_stories.json", "w") as file:
                json.dump(data, file)

            print("Check point reached")

        # Get story data
        items = parseItem(getItem(Stories[idx]))

        kids = items.get("kids")

        if kids:
            p_kids = []
            for kid in kids:
                item = getItem(kid)
                p_kids.append(parseItem(item))

            items["kids"] = p_kids

        data.append(items)

        print(f"{idx + 1} of {len(Stories)} done..")
        count += 1

    # Final checkpoint
    with open(f"./data/{story_type}_stories.json", "w") as file:
        json.dump(data, file)


def pullStoryData(story_type: str):
    user_input = input("Continue data collection (y/n): ")

    # loading data
    data = []

    if user_input == "y":
        is_start = False

        if os.path.isfile():
            with open(f"./data/{story_type}_stories.json", "r") as file:
                data = json.load(file)
        else:
            print("No existing data \n Creating new data")

            with open(f"./data/{story_type}_stories.json", "w") as file:
                json.dump([], file)
    else:
        is_start = True
        with open(f"./data/{story_type}_stories.json", "w") as file:
            json.dump([], file)

    Stories = getStories(story_type)

    runPulling(
        Stories=Stories,
        data=data,
        n_collected=len(data),
        story_type=story_type,
        is_start=is_start,
    )

    print("Data collection completed")


pullStoryData(story_type="new")
