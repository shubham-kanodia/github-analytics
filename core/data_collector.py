from core.api_crawler import ApiCrawler


class DataCollector:
    def __init__(self):
        self.api_crawler = ApiCrawler()

    def collect(self, repo_url):
        response = self.api_crawler.get_repo_data(repo_url)
        return {
            "repo_full_name": response["full_name"],
            "license": response["license"]["name"],
            "open_issues_count": response["open_issues_count"],
            "forks": response["forks"],
            "stars": response["stargazers_count"],
            "watchers": response["watchers"],
            "topics": response["topics"],
            "updated_at": response["updated_at"]
        }
