import os
import requests


class ApiCrawler:
    HEADERS = {
        "Accept": "application / vnd.github.v3 + json",
        "Authorization": f"token {os.environ['PAT']}"
    }
    BASE_URL = "https://api.github.com/repos/"

    def get_repo_data(self, repo_url: str):
        endpoint = self.BASE_URL + "/".join(repo_url.split("/")[-2:])
        resp = requests.get(endpoint, headers=self.HEADERS)

        if resp.ok:
            return resp.json()
        else:
            print(resp.json())
            raise Exception("Request Failed")

    def call_url(self, url: str):
        resp = requests.get(url, headers=self.HEADERS)
        if resp.ok:
            return resp.json()
        else:
            print(resp.json())
            raise Exception("Request Failed")
