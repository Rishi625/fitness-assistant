from src.web_scrape import scrapper
import streamlit as st

st.title("Fitness Assistant")

query = st.text_input("Enter Your Query")
url = st.text_input("Enter Your URL")

button = st.button("Search")

if button:
    if query:
        st.write(query)
    if url:
        result = scrapper(url)
        st.write(result)


