import re

def data_cleaning(scraped_data):
    cleaned_data = []
    for item in scraped_data:
        cleaned_content = re.sub(r'\s+', ' ', item['content'])  # Remove extra whitespace
        cleaned_content = re.sub(r'<[^>]+>', '', cleaned_content)  # Remove HTML tags
        cleaned_content = cleaned_content.strip()
        cleaned_data.append({"url": item['url'], "cleaned_content": cleaned_content})
    return cleaned_data