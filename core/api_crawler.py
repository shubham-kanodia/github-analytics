import os
import requests
from time import sleep


class ApiCrawler:
    HEADERS = {
        "Accept": "application / vnd.github.v3 + json",
        "Authorization": f"token {os.environ['PAT']}"
    }
    BASE_URL = "https://api.github.com/repos/"
    COUNT = 0

    def shall_wait(self):
        if self.COUNT % 20 == 0:
            sleep(5)

    def made_request(self):
        self.COUNT += 1
        self.shall_wait()

    def get_repo_data(self, repo_url: str):
        endpoint = self.BASE_URL + "/".join(repo_url.split("/")[-2:])
        resp = requests.get(endpoint, headers=self.HEADERS)
        self.made_request()

        if resp.ok:
            return resp.json()
        else:
            print(resp.json())
            raise Exception("Request Failed")

    def call_url(self, url: str):
        resp = requests.get(url, headers=self.HEADERS)
        self.made_request()

        if resp.ok:
            return resp.json()
        else:
            print(resp.json())
            raise Exception("Request Failed")
