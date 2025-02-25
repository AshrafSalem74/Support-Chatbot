import streamlit as st
import os
from mistralai import Mistral, UserMessage

# Set API key
os.environ["MISTRAL_API_KEY"] = "tlcYsUNSS1iVHZ6lWnUw8KKW2f8AoVJf"  # Replace with your actual API key
api_key = os.getenv("MISTRAL_API_KEY")

# Initialize Mistral client
def mistral(user_message, model="mistral-large-latest"):
    client = Mistral(api_key=api_key)
    messages = [UserMessage(content=user_message)]
    chat_response = client.chat.complete(model=model, messages=messages)
    return chat_response.choices[0].message.content

# Streamlit UI
st.title("Mistral AI Chatbot")
st.write("Interact with Mistral AI for text processing tasks.")

# User input
query = st.text_area("Enter your query:")

# Select task
option = st.selectbox(
    "Select a task:",
    [
        "General Chatbot",
        "Classify Bank Inquiry",
        "Extract Medical Data",
        "Generate Mortgage Email Response",
        "Analyze Newsletter",
    ]
)

# Define prompts based on selected task
if option == "Classify Bank Inquiry":
    prompt = f"""
    You are a bank customer service bot.
    Categorize the following inquiry into one of these categories:
    card arrival, change pin, exchange rate, country support,
    cancel transfer, charge dispute, or customer service.
    Inquiry: {query}
    Category:
    """
elif option == "Extract Medical Data":
    prompt = f"""
    Extract information from the following medical notes:
    {query}
    Return JSON format with this schema:
    {{"age": int, "gender": str, "diagnosis": str, "weight": int, "smoking": str}}
    """
elif option == "Generate Mortgage Email Response":
    prompt = f"""
    You are a mortgage lender bot. Generate a personalized response
    to the customer's email using provided mortgage facts.
    Email:
    {query}
    """
elif option == "Analyze Newsletter":
    prompt = f"""
    Summarize and analyze the following newsletter. Generate key
    questions and provide insights.
    Newsletter:
    {query}
    """
else:
    prompt = query  # General chatbot mode

# Process query
if st.button("Submit"):
    response = mistral(prompt)
    st.write("### Response:")
    st.write(response)
