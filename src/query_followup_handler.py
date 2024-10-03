import streamlit as st
from typing import Dict, List
import re


class FollowUpHandler:
    def __init__(self):
        self.common_fitness_attributes = {
            'weight_loss_goal': ['1-5 kg', '5-10 kg', '10-15 kg', '15-20 kg', 'more than 20 kg'],
            'target_timeline': ['1 month', '3 months', '6 months', '1 year', 'ongoing'],
            'current_lifestyle': ['sedentary', 'lightly active', 'moderately active', 'very active'],
            'exercise_frequency': ['never', '1-2 times per week', '3-4 times per week', '5+ times per week'],
            'eating_habits': ['regular meals', 'irregular meals', 'frequent snacking', 'restricted eating'],
            'health_conditions': ['none', 'diabetes', 'hypertension', 'thyroid issues', 'other'],
            'stress_level': ['low', 'moderate', 'high'],
            'sleep_quality': ['poor', 'fair', 'good', 'excellent']
        }

        # Add more complex patterns for natural language questions
        self.question_patterns = [
            (r"(?i)what (?:is|are) your (\w+(?:\s+\w+)*)", "general"),
            (r"(?i)how much (\w+(?:\s+\w+)*) would you like", "goal"),
            (r"(?i)do you (\w+(?:\s+\w+)*)", "yes_no"),
            (r"(?i)are there any (\w+(?:\s+\w+)*)", "existence"),
            (r"(?i)tell me (?:more )?about your (\w+(?:\s+\w+)*)", "description"),
            (r"(?i)what('s| is) your current (\w+(?:\s+\w+)*)", "current_state")
        ]

    def extract_required_info(self, gemini_response: str) -> List[str]:
        required_info = []

        # Split the response into sentences for better analysis
        sentences = re.split(r'[.!?]+', gemini_response)

        for sentence in sentences:
            # Check for specific keywords that might indicate needed information
            if re.search(r'(?i)weight.*loss.*goal', sentence):
                required_info.extend(['weight_loss_goal', 'target_timeline'])

            if re.search(r'(?i)current lifestyle|exercise.*regular|eating habits', sentence):
                required_info.extend(['current_lifestyle', 'exercise_frequency', 'eating_habits'])

            if re.search(r'(?i)health condition|medication', sentence):
                required_info.append('health_conditions')

            # Add stress and sleep if mental health or overall wellness is mentioned
            if re.search(r'(?i)stress|emotional eating|mental health', sentence):
                required_info.extend(['stress_level', 'sleep_quality'])

        return list(set(required_info))  # Remove duplicates

    def get_follow_up_inputs(self, required_info: List[str]) -> Dict[str, str]:
        user_inputs = {}

        for info in required_info:
            if info in self.common_fitness_attributes:
                options = self.common_fitness_attributes[info]
                display_name = ' '.join(info.split('_')).title()

                # Create a more user-friendly label
                if info == 'weight_loss_goal':
                    label = "How much weight would you like to lose?"
                elif info == 'target_timeline':
                    label = "What is your target timeline for weight loss?"
                elif info == 'current_lifestyle':
                    label = "How would you describe your current lifestyle?"
                elif info == 'exercise_frequency':
                    label = "How often do you currently exercise?"
                elif info == 'eating_habits':
                    label = "What are your current eating habits?"
                elif info == 'health_conditions':
                    label = "Do you have any health conditions to consider?"
                elif info == 'stress_level':
                    label = "How would you rate your current stress level?"
                elif info == 'sleep_quality':
                    label = "How would you rate your sleep quality?"
                else:
                    label = f"Select your {display_name}:"

                user_inputs[info] = st.selectbox(label, options)

        return user_inputs

    def process_follow_up(self, gemini_response: str) -> Dict[str, str]:
        required_info = self.extract_required_info(gemini_response)

        if required_info:
            st.write("To provide you with a personalized weight loss plan, please answer the following questions:")
            return self.get_follow_up_inputs(required_info)

        return {}


def format_follow_up_response(original_query: str, user_inputs: Dict[str, str]) -> str:
    formatted_response = f"""
Based on the user's fitness query: "{original_query}"

User Profile:
"""

    for key, value in user_inputs.items():
        formatted_key = ' '.join(key.split('_')).title()
        formatted_response += f"- {formatted_key}: {value}\n"

    formatted_response += """
Please provide a comprehensive, personalized fitness plan that addresses:
1. Specific exercise recommendations based on their current fitness level and goals
2. Dietary suggestions that align with their fitness goals
3. A weekly schedule that incorporates both exercise and meal planning
4. Tips for overcoming potential challenges they might face
5. Metrics they can use to track their progress

The plan should be detailed, actionable, and tailored to their specific situation.
"""

    return formatted_response