import re
from tkinter import E
from core.api_crawler import ApiCrawler
from core.dependency_crawler import DependencyCrawler


class RepositoriesCollector:
    def __init__(self):
        self.api_crawler = ApiCrawler()

    @staticmethod
    def filterItems(items):
        invalidTopics = ["awesome-list", "documentation", "tutorial", "book"]
        filteredItems = []
        for item in items:
            countOfInvalidTopics = len(
                set(item["topics"]).intersection(invalidTopics))
            if countOfInvalidTopics > 0:
                continue
            else:
                filteredItems.append(item)
        return filteredItems

    def collect(self, topic):
        allItems = []
        for pageNo in range(1, 3):
            response = self.api_crawler.call_url(
                f"https://api.github.com/search/repositories?q=topic:{topic}&sort=stars&order=desc&per_page=100&page={pageNo}")
            items = response["items"]
            filteredItems = self.filterItems(items)
            allItems = allItems + filteredItems
            print(f"Fetched page {pageNo} for {topic} topic")

        return allItems
