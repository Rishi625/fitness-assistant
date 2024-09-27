from typing import List, Any

import requests
from bs4 import BeautifulSoup

def web_scraper(urls):
    print("This is the original url:",urls)
    url_data = []
    url_data.append(urls)
    scraped_data = []
    for url in url_data:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.find_all(['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            content = ' '.join([element.get_text() for element in elements if element.get_text().strip()])
            scraped_data.append({"url": url, "content": content})
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while scraping {url}: {e}")
    return scraped_data