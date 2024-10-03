import streamlit as st
from src.web_scrape import web_scraper
from src.data_clean import data_cleaning
from src.brave_search import brave_search
from src.prompt_genrator import custom_prompt
from src.gemini_api import GeminiApi
from src.fitness_level import calculate_bmi, determine_fitness_level
from src.query_followup_handler import FollowUpHandler, format_follow_up_response

# Initialize Gemini API
gemini_api = GeminiApi()

# Set page title and configuration
st.set_page_config(page_title="Fitness Assistant", layout="wide")
st.title("Fitness Assistant")

# Initialize session states
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'initial_response' not in st.session_state:
    st.session_state.initial_response = None
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}

# Sidebar for user information
with st.sidebar:
    st.header("Your Information")
    name = st.text_input("Enter Your Name", key="name_input")
    age = st.number_input("Enter Your Age", min_value=1, max_value=120, key="age_input")
    height = st.number_input("Enter Your Height (cm)", min_value=50, max_value=300, key="height_input")
    weight = st.number_input("Enter Your Weight (kg)", min_value=20, max_value=500, key="weight_input")

# Main content area
query = st.text_input("Enter Your Fitness Query", key="query_input")
submit_button = st.button("Submit")

# Process the initial query
if submit_button:
    if name and age and height and weight and query:
        # Update user info in session state
        st.session_state.user_info = {
            "name": name,
            "age": age,
            "height": height,
            "weight": weight,
            "query": query
        }
        st.session_state.step = 1
    else:
        st.error("Please fill in all the fields before submitting.")

# Display content based on the current step
if st.session_state.step >= 1 and st.session_state.user_info:
    user_info = st.session_state.user_info

    # Display user information
    st.write(f"Hello, {user_info['name']}!")
    try:
        bmi = calculate_bmi(user_info['weight'], user_info['height'])
        st.write(f"Your BMI is: {bmi:.1f}")
        st.write(f"Your current fitness level is estimated to be: {determine_fitness_level(bmi, user_info['age'])}")
    except Exception as e:
        st.error(f"Error calculating fitness metrics: {str(e)}")

    if st.session_state.step == 1:
        try:
            with st.spinner("Processing your query..."):
                # Search and process query
                search_results = brave_search(user_info['query'])
                search_urls = [res['url'] for res in search_results]
                scraped_data = web_scraper(search_urls)
                cleaned_data = data_cleaning(scraped_data)

                # Generate initial response
                prompt = custom_prompt(user_info['query'], cleaned_data)
                initial_response = gemini_api.generate_response(prompt)

                if initial_response and initial_response.strip():
                    # Store results in session state
                    st.session_state.initial_response = initial_response
                    st.session_state.search_results = search_urls
                    st.session_state.step = 2
                else:
                    st.error("Unable to generate an initial response. Please try rephrasing your query.")
        except Exception as e:
            st.error(f"An error occurred while processing your query: {str(e)}")

    # Handle follow-up questions and responses
    if st.session_state.step >= 2:
        st.subheader("Initial Assessment")
        st.write(st.session_state.initial_response)

        try:
            follow_up_handler = FollowUpHandler()
            additional_inputs = follow_up_handler.process_follow_up(st.session_state.initial_response)

            if additional_inputs:
                get_plan_button = st.button("Get Personalized Plan")
                if get_plan_button:
                    with st.spinner("Generating your personalized plan..."):
                        formatted_query = format_follow_up_response(user_info['query'], additional_inputs)

                        # Debug information
                        with st.expander("Debug Information"):
                            st.write("Query sent to Gemini:")
                            st.code(formatted_query)

                        try:
                            final_response = gemini_api.generate_response(formatted_query)

                            if final_response and final_response.strip():
                                st.subheader("Your Personalized Fitness Plan")
                                st.write(final_response)
                                st.session_state.step = 3
                            else:
                                st.error("Sorry, we couldn't generate a personalized plan. Please try again.")
                        except Exception as e:
                            st.error(f"An error occurred while generating the plan: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred while processing follow-up questions: {str(e)}")

# Display relevant links
if st.session_state.search_results:
    st.subheader("Relevant Resources")
    for i, url in enumerate(st.session_state.search_results[:3], 1):
        st.write(f"{i}. {url}")

# Footer with reset button
st.markdown("---")
if st.button("Start Over"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()