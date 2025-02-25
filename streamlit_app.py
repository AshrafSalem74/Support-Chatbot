import streamlit as st
from mistralai import Mistral, UserMessage
import os

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
st.title("🤖 Mistral AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for task selection
with st.sidebar:
    st.header("Configuration")
    task = st.selectbox(
        "Select Task:",
        [
            "General Chatbot",
            "Classify Bank Inquiry",
            "Extract Medical Data",
            "Generate Mortgage Email Response",
            "Analyze Newsletter",
        ],
        index=0,
    )

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Construct task-specific prompt
    if task == "Classify Bank Inquiry":
        system_prompt = f"""You are a bank customer service bot. Categorize this inquiry:
        Categories: card arrival, change pin, exchange rate, country support,
        cancel transfer, charge dispute, or customer service.
        Inquiry: {prompt}
        Category:"""
    elif task == "Extract Medical Data":
        system_prompt = f"""Extract medical information as JSON:
        {prompt}
        Use schema: {{"age": int, "gender": str, "diagnosis": str, "weight": int, "smoking": str}}"""
    elif task == "Generate Mortgage Email Response":
        system_prompt = f"""As a mortgage lender bot, generate response:
        Email: {prompt}"""
    elif task == "Analyze Newsletter":
        system_prompt = f"""Analyze newsletter and provide insights:
        {prompt}"""
    else:
        system_prompt = prompt

    # Get AI response
    with st.spinner("Processing..."):
        response = mistral(system_prompt)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to display new messages
    st.rerun()