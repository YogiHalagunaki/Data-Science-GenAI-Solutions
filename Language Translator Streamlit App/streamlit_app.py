import io
import os
import json
import base64
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
from litellm import completion
from UI_items import create_header
import google.generativeai as genai

load_dotenv()

# Set up environment variables
AZURE_API_KEY = ""
AZURE_API_BASE = ""
AZURE_API_VERSION = ""
GEMINI_API_KEY = ""

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-pro-latest')

st.set_page_config(layout="wide", page_title="LLM LANG TRANSLATOR", initial_sidebar_state="auto", menu_items=None)
heading = "LLM LANG TRANSLATOR"
create_header(heading)

SYSTEM_PROMPT = """
You are an expert language translator and text extractor. Your task is to:
1. If the input is text, translate it to English if it's not already in English.
2. If the input is an image, extract all visible text from the image and translate it to English.
3. Maintain the original formatting and structure of the text as much as possible.
4. If there are multiple languages in the input, translate all of them to English.
5. If the input is already in English, simply return it as is.

Respond with the translated or extracted English text only, without any additional comments or explanations.
"""

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def process_with_model(model, input_text=None, is_image=False, image=None):
    if model == "GPT-4":
        llm_model = "azure/gpt-4-omni"
    elif model == "Sonnet":
        llm_model = "bedrock/anthropic.claude-3-sonnet-20240229-v1:0"
    else:  # Gemini
        if is_image:
            response = gemini_model.generate_content([SYSTEM_PROMPT, "Extract and translate the text from this image to English:", image])
        else:
            response = gemini_model.generate_content(f"{SYSTEM_PROMPT}\n\nInput text:\n{input_text}")
        return response.text

    if is_image:
        encoded_data = image_to_base64(image)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": [
                {"type": "text", "text": "Extract and translate the text from this image to English:"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_data}"}}
            ]}
        ]
    else:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": input_text}
        ]

    resp = completion(
        model=llm_model,
        max_tokens=4096,
        temperature=0,
        top_p=0.95,
        messages=messages
    )
    return resp.choices[0].message.content

def process_parallel(input_text=None, image=None):
    is_image = image is not None
    results = {}
    for model in ["GPT-4", "Sonnet", "Gemini 1.5 Pro"]:
        results[model] = process_with_model(model, input_text, is_image, image)
    return results

def process_parallel(input_text=None, image=None):
    is_image = image is not None
    results = {}
    for model in ["GPT-4", "Sonnet", "Gemini 1.5 Pro"]:
        results[model] = process_with_model(model, input_text, is_image, image)
    return results

def main():
    st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
    }
    .output-container {
        display: flex;
        justify-content: space-between;
    }
    .output-column {
        width: 32%;
    }
    </style>
    """, unsafe_allow_html=True)

    # st.title("LLM LANG TRANSLATOR")

    input_type = st.radio("Select input type", ["Text", "Image"], horizontal=True)
    
    if input_type == "Text":
        input_text = st.text_area("Enter text to translate", height=200)
    else:
        uploaded_file = st.file_uploader(
            "Upload image",
            type=["png", "jpg", "jpeg"],
            help="Only image files are supported",
            accept_multiple_files=False,
        )
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)

    process = st.button("Translate")

    if process:
        with st.spinner("translating..."):
            if input_type == "Text" and input_text:
                results = process_parallel(input_text=input_text)
                output = {
                    "original_text": input_text,
                    "translated_text": results
                }
                file_name = "translated_text.json"
            elif input_type == "Image" and uploaded_file:
                results = process_parallel(image=image)
                output = {
                    "image_name": uploaded_file.name,
                    "translated_text": results
                }
                file_name = f"{uploaded_file.name}_translated.json"
            else:
                st.error("Please provide input before processing.")
                return

        st.subheader("Input and Output Comparison")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.subheader("Original Input")
            if input_type == "Text":
                st.text_area("Original Text", input_text, height=300, disabled=True)
            else:
                st.image(image, caption="Uploaded Image", use_container_width=True)
        
        with col2:
            st.subheader("GPT-4 Output")
            st.text_area("GPT-4", results["GPT-4"], height=300)
        
        with col3:
            st.subheader("Sonnet Output")
            st.text_area("Sonnet", results["Sonnet"], height=300)
        
        with col4:
            st.subheader("Gemini 1.5 Pro Output")
            st.text_area("Gemini 1.5 Pro", results["Gemini 1.5 Pro"], height=300)
        
        # Save as JSON
        st.download_button(
            label="Download JSON",
            data=json.dumps(output, indent=2),
            file_name=file_name,
            mime="application/json"
        )

if __name__ == "__main__":
    main()
