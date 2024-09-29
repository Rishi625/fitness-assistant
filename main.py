import streamlit as st
import os
from src.brave_search import brave_search
from src.web_scrape import web_scraper
from src.data_clean import data_cleaning
from src.prompt_genrator import custom_prompt
from src.gemini_api import GeminiApi
from src.fitness_level import determine_fitness_level,calculate_bmi

# Initialize Gemini API
gemini_api = GeminiApi()

st.title("Fitness Assistant")

# User input fields
name = st.text_input("Enter Your Name")
age = st.number_input("Enter Your Age", min_value=1, max_value=120)
height = st.number_input("Enter Your Height (cm)", min_value=50, max_value=300)
weight = st.number_input("Enter Your Weight (kg)", min_value=20, max_value=500)
query = st.text_input("Enter Your Fitness Query")

button = st.button("Submit")

if button:
    if name and age and height and weight and query:
        st.write(f"Hello, {name}!")

        # Calculate BMI and fitness level
        bmi = calculate_bmi(weight, height)
        fitness_level = determine_fitness_level(bmi, age)

        st.write(f"Your BMI is: {bmi}")
        st.write(f"Your current fitness level is estimated to be: {fitness_level}")

        # Process the fitness query
        st.write("Processing your query:", query)
        search_results = brave_search(query)
        search_results = [res['url'] for res in search_results]
        scraped_data = web_scraper(search_results)
        output = data_cleaning(scraped_data)
        output_final = custom_prompt(query, output)
        response = gemini_api.generate_response(output_final)

        st.write("Here's a summary based on your query:")
        st.write(response)

        st.write("Relevant links:")
        for url in search_results[:3]:  # Limit to top 3 results
            st.write(url)
    else:
        st.write("Please fill in all the fields before submitting.")