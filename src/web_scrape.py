import requests
from bs4 import BeautifulSoup

def web_scraper(urls):
    scraped_data = []
    for url in urls:
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