import re
from core.api_crawler import ApiCrawler


class DataCollector:
    def __init__(self):
        self.api_crawler = ApiCrawler()

    @staticmethod
    def clean_url(url):
        return re.sub(r"\{(.*?)\}", "", url)

    @staticmethod
    def get_contributors_from_response(contributors_response):
        contributors = []
        for elem in contributors_response:
            contributors.append(
                {
                    "username": elem["login"],
                    "contributions": elem["contributions"]
                }
            )
        return contributors

    @staticmethod
    def get_commits_from_response(commits_response):
        commits = []
        for elem in commits_response:
            commits.append(
                {
                    "author": elem["commit"]["author"],
                    "message": elem["commit"]["message"],
                    "pushed_at": elem["commit"]["committer"]["date"]
                }
            )
        return commits

    @staticmethod
    def get_releases_from_response(releases_response):
        releases = []
        for elem in releases_response:
            releases.append(
                {
                    "name": elem["name"],
                    "published_at": elem["published_at"],
                    "message": elem.get("body"),
                    "author_username": elem["author"]["login"]
                }
            )
        return releases

    @staticmethod
    def get_comments_from_response(comments_response):
        comments = []
        for elem in comments_response:
            comments.append(
                {
                    "user": elem["user"]["login"],
                    "created_at": elem["created_at"],
                    "author_association": elem["author_association"],
                    "body": elem["body"]
                }
            )
        return comments

    def get_issues_from_response(self, issues_response):
        issues = []
        for elem in issues_response:
            comments_url = elem["comments_url"]
            comments_response = self.api_crawler.call_url(comments_url)

            comments = self.get_comments_from_response(comments_response)
            issues.append(
                {
                    "title": elem["title"],
                    "pull_request": elem.get("pull_request", {}).get("url"),
                    "state": elem["state"],
                    "created_at": elem["created_at"],
                    "closed_at": elem["closed_at"],
                    "comments": comments
                }
            )
        return issues

    def collect(self, repo_url):
        repo_response = self.api_crawler.get_repo_data(repo_url)

        issues_response = self.api_crawler.call_url(
            self.clean_url(repo_response["issues_url"])
        )
        issues = self.get_issues_from_response(issues_response)

        contributors_response = self.api_crawler.call_url(
            self.clean_url(repo_response["contributors_url"])
        )
        contributors = self.get_contributors_from_response(contributors_response)

        commits_response = self.api_crawler.call_url(
            self.clean_url(repo_response["commits_url"])
        )
        commits = self.get_commits_from_response(commits_response)

        releases_response = self.api_crawler.call_url(
            self.clean_url(repo_response["releases_url"])
        )
        releases = self.get_releases_from_response(releases_response)

        return {
            "repo_full_name": repo_response["full_name"],
            "license": repo_response["license"]["name"],
            "open_issues_count": repo_response["open_issues_count"],
            "forks": repo_response["forks"],
            "stars": repo_response["stargazers_count"],
            "watchers": repo_response["watchers"],
            "topics": repo_response["topics"],
            "pushed_at": repo_response["pushed_at"],
            "organization": repo_response["organization"]["login"],
            "contributors": contributors,
            "contributors_count": len(contributors),
            "commits": commits,
            "releases": releases,
            "issues": issues
        }
