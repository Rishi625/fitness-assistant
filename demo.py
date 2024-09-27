import streamlit as st
from src.web_scrape import web_scraper
from src.data_clean import data_cleaning
from src.brave_search import brave_search
from src.prompt_genrator import custom_prompt
from src.gemini_api import GeminiApi

gemini_api = GeminiApi()

st.title("Fitness Assistant")

query = st.text_input("Enter Your Query")
url = st.text_input("Enter Your URL")

button = st.button("Search")

if button:
    if query:
        st.write(query)
        search_results = brave_search(query)
        search_results = [res['url'] for res in search_results]
        scraped_data = web_scraper(search_results)
        output = data_cleaning(scraped_data)
        output_final = custom_prompt(query, output)
        response = gemini_api.generate_response(output_final)
        st.write(response)
    #if url:
    #    result = web_scraper(url)
    #    output = data_cleaning(result)
    #    st.write(output)

