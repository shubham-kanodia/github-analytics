import json
from core.data_collector import DataCollector

data_collector = DataCollector()

REPO_LIST_FILE_PATH = "data/best-of-crypto.txt"
for line in open(REPO_LIST_FILE_PATH, "r").readlines():
    line = line.strip("\n")
    repo_data = data_collector.collect(line)

    json.dump(repo_data, open(
        f"./data/repo/{repo_data['repo_full_name'].replace('/', '_')}.json",
        "w"), indent=2)

    break
