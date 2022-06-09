import json
from core.data_collector import DataCollector

data_collector = DataCollector()

REPO_LIST_FILE_PATH = "data/best-of-crypto.txt"
COMPLETED_LIST_FILE_PATH = "data/completed.txt"
completed_repos = [_.strip("\n") for _ in open(COMPLETED_LIST_FILE_PATH, "r").readlines()]

for line in open(REPO_LIST_FILE_PATH, "r").readlines():
    line = line.strip("\n")

    if line in completed_repos:
        continue
    else:
        repo_data = data_collector.collect(line)

        json.dump(repo_data, open(
            f"./data/repo/{repo_data['repo_full_name'].replace('/', '_')}.json",
            "w"), indent=2)

        print(f"Added repo - {repo_data['repo_full_name']}")
        open(COMPLETED_LIST_FILE_PATH, "a").write(line + "\n")
        break
