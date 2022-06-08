import re

import requests
from bs4 import BeautifulSoup


class DependencyCrawler:
    @staticmethod
    def crawl_dependencies(repo_url):
        url = f"{repo_url.rstrip('/')}/network/dependents"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "html.parser")

        dependent_repos_text = soup.select_one("a[href*='dependent_type=REPOSITORY']").text
        dependent_packages_text = soup.select_one("a[href*='dependent_type=PACKAGE']").text

        repos = int(re.findall("[0-9]+", dependent_repos_text.replace(",", ""))[0])
        packages = int(re.findall("[0-9]+", dependent_packages_text.replace(",", ""))[0])

        return {
            "repos": repos,
            "packages": packages
        }
