import json
from core.data_collector import DataCollector
from core.repositories_collector import RepositoriesCollector

repos_collector = RepositoriesCollector()

topics = ["solidity", "ethereum", "solana", "cosmos", "polkadot", "bitcoin"]
for topic in topics:
    data = repos_collector.collect(topic)
    json.dump(data, open(
        f"./data/repositories/{topic}.json",
        "w"), indent=2)
