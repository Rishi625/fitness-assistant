import streamlit as st
import os
from src.brave_search import brave_search
from src.web_scrape import web_scraper
from src.data_clean import data_cleaning
from src.prompt_genrator import custom_prompt
from src.gemini_api import GeminiApi

# Initialize Gemini API
gemini = GeminiApi()


def main():
    st.title("Fitness Assistant")

    query = st.text_input("Enter Your Query")
    url = st.text_input("Enter Your URL (optional)")

    if st.button("Search"):
        if query:
            st.subheader("Processing...")

            # Web Search
            st.write("Performing web search...")
            search_results = brave_search(query)
            if search_results:
                urls = [result['url'] for result in search_results[:3]]  # Take top 3 results
                if url:
                    urls.append(url)  # Add user-provided URL if any
            elif url:
                urls = [url]
            else:
                st.error("No search results found and no URL provided.")
                return

            # Web Scraper
            st.write("Scraping web content...")
            scraped_data = web_scraper(urls)

            # Data Cleaning
            st.write("Cleaning scraped data...")
            cleaned_data = data_cleaning(scraped_data)

            # Custom Prompt
            st.write("Generating custom prompt...")
            prompt = custom_prompt(query, cleaned_data)

            # Gemini API
            st.write("Generating response using Gemini API...")
            response = gemini.generate_response(prompt)

            # Final Response
            st.subheader("Final Response")
            st.write(response)

        else:
            st.warning("Please enter a query.")


if __name__ == "__main__":
    main()