import requests
from bs4 import BeautifulSoup
import re

def scrapper(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    job_elements = soup.find_all(['div','p','h'])
    scrap_data = []
    for job_element in job_elements:
        scrap = job_element.get_text()
        if len(scrap) > 0:
           scrap_data.append(scrap)
           print("scrap dat:", scrap_data)
    scrapped_data = ' '.join(scrap_data)
    cleaned_data = clean_scrap_data(scrapped_data)
    return {"url":url,"Scrapped_content": cleaned_data}

def clean_scrap_data(scrapped_data):
    scrapped_data = scrapped_data.strip()
    scrapped_data = re.sub(r'\s+', ' ', scrapped_data)
    scrapped_data = scrapped_data.replace('\n', '').replace('\r', '').replace('\t', '')
    scrapped_data = scrapped_data.replace('<','').replace('>','')

    return scrapped_data