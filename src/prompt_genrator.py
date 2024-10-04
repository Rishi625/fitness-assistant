def custom_prompt(user_query, cleaned_data):
    prompt = f"User Query: {user_query}\n\nRelevant Information:\n"
    for item in cleaned_data:
        prompt += f"From {item['url']}:\n{item['cleaned_content']}...\n\n"
    prompt += "\nBased on the user query and the provided information, please generate a comprehensive and accurate response. Focus on addressing the user's question directly while incorporating relevant details from the sources."
    return prompt