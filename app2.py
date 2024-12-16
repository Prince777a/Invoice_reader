from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure the Generative AI client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the updated Gemini model (e.g., Gemini 1.5 Flash)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input_prompt, image, user_query):
    """
    Generate a response using the Gemini model.
    
    Args:
        input_prompt (str): The initial input context.
        image (list): A list containing the image details.
        user_query (str): The user's specific query.

    Returns:
        str: The model's response text.
    """
    response = model.generate_content([input_prompt, image[0], user_query])
    return response.text

def input_image_details(uploaded_file):
    """
    Process the uploaded file and prepare it for the model.

    Args:
        uploaded_file: The uploaded file object.

    Returns:
        list: A list of dictionaries containing the image details.
    """
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize the Streamlit app
st.set_page_config(page_title="MultiLanguage Invoice Extractor")

st.header("MultiLanguage Invoice Extractor")
input_query = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the invoice")

# Define the initial context for the model
input_prompt = """
You are an expert in understanding invoices. We will upload an image as an invoice,
and you will have to answer any questions based on the uploaded invoice image.
"""

# Handle the submit button click
if submit:
    if uploaded_file is None:
        st.error("Please upload an invoice image first.")
    else:
        try:
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, input_query)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
