import requests


class GHApi:
    HEADERS = {
        "Accept": "application / vnd.github.v3 + json"
    }
    BASE_URL = "https://api.github.com/repos/"

    def get_repo_data(self, repo_url: str):
        endpoint = self.BASE_URL + "/".join(repo_url.split("/")[-2:])
        resp = requests.get(endpoint, headers=self.HEADERS).json()
        return resp
