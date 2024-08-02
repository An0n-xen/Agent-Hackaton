import json
from utils.utilities import latestNews

# save_data = latestNews()
# news_data = []

# for idx, article in enumerate(save_data["articles"]):
#     if article["description"]:
#         news_data.append(f"{idx + 1}. {article["description"]}")
#     else:
#         news_data.append(f"{idx + 1}. {article["title"]}")

# with open("./test_data/test1.json", "w") as f:
#     json.dump(news_data, f)

with open("./test_data/test1.json", "r") as f:
    data = json.load(f)

data_string = json.dumps(data, indent=4)
print(data_string)
