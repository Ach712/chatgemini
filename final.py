# Q&A Chatbot

from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input:
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

def get_gemini_response1(input):
    model1 = genai.GenerativeModel('gemini-pro')
    response = model1.generate_content(input)
    return response.text

# Initialize session state if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to simulate chatbot response (replace with actual chatbot logic)
def chatbot_response(user_input, image):
    if image != '':
        return get_gemini_response(user_input, image)
    else:
        return get_gemini_response1(user_input)

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Image Demo")

# Title of the app
st.title("Gemini Image Chatbot")

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Chat history container
chat_history = st.container()

# Function to calculate dynamic height based on text length
def calculate_text_area_height(text):
    # 50px can occupy 270 characters, so we calculate the height accordingly
    char_count = len(text)
    height = (char_count // 270 + 1) * 50
    return max(int(height * 2.4), 100)

# Display chat messages with role and color
with chat_history:
    for message in st.session_state.messages:
        height = calculate_text_area_height(message['content'])
        if message['role'] == 'user':
            st.markdown(
                f'<div class="user-textarea" style="height: {height}px;">'
                f'<b style="color: blue;">User:</b><br>{message["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chatbot-textarea" style="height: {height}px;">'
                f'<b style="color: green;">Chatbot:</b><br>{message["content"]}</div>',
                unsafe_allow_html=True
            )

# Image upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Form for user input and submission
with st.form(key='input_form', clear_on_submit=True):
    input_prompt = st.text_input("Input Prompt: ", key="input")
    submit_button = st.form_submit_button(label="Send")

# Handle form submission
if submit_button:
    if input_prompt or uploaded_file:
        # Append user's message to session state
        st.session_state.messages.append({"role": "user", "content": input_prompt, "id": len(st.session_state.messages)})
        # Get chatbot response
        response = chatbot_response(input_prompt, image)
        # Append chatbot's response to session state
        st.session_state.messages.append({"role": "chatbot", "content": response, "id": len(st.session_state.messages)})
        # Rerun to refresh the display
        st.experimental_rerun()
