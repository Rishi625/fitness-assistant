## Bing Search API

import os
import requests
import json

class BingSearch:
    def __init__(self):
        self.subscription_key = os.environ.get("BING_SEARCH_API_KEY")
        self.url = "https://api.bing.microsoft.com/v7.0/search"
        self.headers = {"Ocp-Apim-Subscription-Key": self.subscription_key}

    def search(self, search_term):
        params = {"q": search_term}
        response = requests.get(self.url, headers=self.headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        return search_results

    
