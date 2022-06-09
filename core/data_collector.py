import re
from core.api_crawler import ApiCrawler
from core.dependency_crawler import DependencyCrawler


class DataCollector:
    def __init__(self):
        self.api_crawler = ApiCrawler()
        self.dependency_crawler = DependencyCrawler()

    @staticmethod
    def clean_url(url):
        return re.sub(r"\{(.*?)\}", "", url)

    @staticmethod
    def get_contributors_from_response(contributors_response):
        contributors = []
        for elem in contributors_response:
            contributors.append(
                {
                    "username": elem.get("login"),
                    "contributions": elem.get("contributions")
                }
            )
        return contributors

    @staticmethod
    def get_commits_from_response(commits_response):
        commits = []
        for elem in commits_response:
            commits.append(
                {
                    "author": elem.get("commit", {}).get("author"),
                    "message": elem.get("commit", {}).get("message"),
                    "pushed_at": elem.get("commit", {}).get("committer", {}).get("date")
                }
            )
        return commits

    @staticmethod
    def get_releases_from_response(releases_response):
        releases = []
        for elem in releases_response:
            releases.append(
                {
                    "name": elem.get("name"),
                    "published_at": elem.get("published_at"),
                    "message": elem.get("body"),
                    "author_username": elem.get("author", {}).get("login")
                }
            )
        return releases

    def get_issues_response(self, url):
        page_number = 1
        per_page = 100

        start = True
        issues_collection = []
        issues_response = []

        while start or len(issues_response) >= per_page:
            try:
                issues_response = self.api_crawler.call_url(
                    f"{self.clean_url(url)}?page={page_number}&per_page={per_page}&state=all"
                )
                issues_collection.extend(issues_response)
                page_number += 1
            except Exception:
                issues_response = []

            start = False

        return issues_collection

    def get_contributors_response(self, url):
        page_number = 1
        per_page = 100

        start = True
        contributors_collection = []
        contributors_response = []

        while start or len(contributors_response) >= per_page:
            try:
                contributors_response = self.api_crawler.call_url(
                    f"{self.clean_url(url)}?page={page_number}&per_page={per_page}&state=all"
                )
                contributors_collection.extend(contributors_response)
                page_number += 1
            except Exception:
                contributors_response = []

            start = False

        return contributors_collection

    def get_releases_response(self, url):
        page_number = 1
        per_page = 100

        start = True
        releases_collection = []
        releases_response = []

        while start or len(releases_response) >= per_page:
            try:
                releases_response = self.api_crawler.call_url(
                    f"{self.clean_url(url)}?page={page_number}&per_page={per_page}&state=all"
                )
                releases_collection.extend(releases_response)
                page_number += 1
            except Exception:
                releases_response = []

            start = False

        return releases_collection

    def get_pulls_response(self, url):
        page_number = 1
        per_page = 100

        start = True
        pulls_collection = []
        pulls_response = []

        while start or len(pulls_response) >= per_page:
            try:
                pulls_response = self.api_crawler.call_url(
                    f"{self.clean_url(url)}?page={page_number}&per_page={per_page}&state=all"
                )
                pulls_collection.extend(pulls_response)
                page_number += 1
            except Exception:
                pulls_response = []

            start = False

        return pulls_collection

    def get_commits_response(self, url):
        page_number = 1
        per_page = 100

        start = True
        commits_collection = []
        commits_response = []

        while start or len(commits_response) >= per_page:
            try:
                commits_response = self.api_crawler.call_url(
                    f"{self.clean_url(url)}?page={page_number}&per_page={per_page}&state=all"
                )
                commits_collection.extend(commits_response)
                page_number += 1
            except Exception:
                commits_response = []

            start = False

        return commits_collection

    def get_issues_from_response(self, issues_response):
        issues = []
        for elem in issues_response:
            labels = [label["name"] for label in elem.get("labels", [])]
            issues.append(
                {
                    "title": elem.get("title"),
                    "state": elem.get("state"),
                    "created_at": elem.get("created_at"),
                    "closed_at": elem.get("closed_at"),
                    "labels": labels
                }
            )
        return issues

    @staticmethod
    def separate_issues_and_pulls(issues_response):
        pulls = []
        issues = []
        for issue in issues_response:
            if issue["html_url"].split("/")[-2] == "pull":
                pulls.append(issue)
            else:
                issues.append(issue)

        return pulls, issues

    @staticmethod
    def get_pulls_from_response(pulls_response):
        pulls = []
        for elem in pulls_response:
            pulls.append(
                {
                    "created_at": elem.get("created_at"),
                    "updated_at": elem.get("updated_at"),
                    "closed_at": elem.get("closed_at"),
                    "merged_at": elem.get("merged_at"),
                    "state": elem.get("state"),
                    "author_association": elem.get("author_association")
                }
            )
        return pulls

    def collect(self, repo_url):
        dependents = self.dependency_crawler.crawl_dependencies(repo_url)

        repo_response = self.api_crawler.get_repo_data(repo_url)

        issues_response = self.get_issues_response(repo_response.get("issues_url"))
        _, issues_response = self.separate_issues_and_pulls(issues_response)

        issues = self.get_issues_from_response(issues_response)

        pulls_response = self.get_pulls_response(repo_response.get("pulls_url"))
        pulls = self.get_pulls_from_response(pulls_response)

        contributors_response = self.get_contributors_response(repo_response.get("contributors_url"))
        contributors = self.get_contributors_from_response(contributors_response)

        commits_response = self.get_commits_response(repo_response.get("commits_url"))
        commits = self.get_commits_from_response(commits_response)

        releases_response = self.get_releases_response(repo_response.get("releases_url"))
        releases = self.get_releases_from_response(releases_response)

        return {
            "repo_full_name": repo_response.get("full_name"),
            "license": repo_response.get("license", {}).get("name") if repo_response.get("license") else None,
            "open_issues_count": sum([issue["state"] == "open" for issue in issues]),
            "forks": repo_response.get("forks"),
            "stars": repo_response.get("stargazers_count"),
            "watchers": repo_response.get("subscribers_count"),
            "topics": repo_response.get("topics"),
            "pushed_at": repo_response.get("pushed_at"),
            "organization": repo_response.get("organization", {}).get("login"),
            "contributors": contributors,
            "contributors_count": len(contributors),
            "commits": commits,
            "releases": releases,
            "issues": issues,
            "pulls": pulls,
            "dependent_repos": dependents.get("repos"),
            "dependent_packages": dependents.get("packages")
        }
