import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
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

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about Nutritional Values")

input_prompt = """
You are an expert nutritionist where you need to see the food items from the image
and calculate the total calories. Also, provide the details of
every food item with calorie intake in the tabular format given below:

1. Item 1 - number of calories
2. Item 2 - number of calories
....

Finally, you can also mention whether the food is healthy or unhealthy and also mention the
percentage split of the ratio of carbohydrates, fats, fibers, sugar, and other important 
things required in our diet in tabular format.

Tell recipe of the food item that is mentioned in the image.

"""

if submit:

    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    
    st.header("The Response is")
    st.write(response)




# import streamlit as st
# import openai
# import os
# from dotenv import load_dotenv
# from PIL import Image

# # Load environment variables
# load_dotenv()

# # Configure Azure OpenAI API
# openai.api_type = "azure"
# openai.api_base = os.getenv("AZURE_OPENAI_CHAT_ENDPOINT")
# openai.api_version = os.getenv("AZURE_API_VERSION")
# openai.api_key = os.getenv("AZURE_OPENAI_CHAT_KEY")

# def get_gemini_response(input_prompt, image_url):
#     response = openai.ChatCompletion.create(
#         engine=os.getenv("gpt-35-turbo"), # Replace with your Azure OpenAI Chat deployment name
#         messages=[
#             {"role": "system", "content": "You are an expert nutritionist."},
#             {"role": "user", "content": f"{input_prompt} Image URL: {image_url}"}
#         ]
#     )
#     return response.choices[0].message.content


# def input_image_setup(uploaded_file):
#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)
#         image_url = st.image(image, caption="Uploaded Image.", use_column_width=True, output_format="URL")
#         return image_url
#     else:
#         raise FileNotFoundError("No file uploaded")


# st.set_page_config(page_title="Gemini Health App")
# st.header("Gemini Health App")
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# if uploaded_file:
#     image = Image.open(uploaded_file)
    

# submit = st.button("Tell me about the total calories")
# input_prompt = """Analyze the food in the image and calculate total calories.  Provide details for each food item in the format below:

# 1. Item 1 - number of calories
# 2. Item 2 - number of calories
# ....

# Finally, mention whether the food is healthy or not and provide the percentage split of carbohydrates, fats, fibers, sugar, and other important dietary components.
# """

# if submit:
#     image_url = input_image_setup(uploaded_file)
#     response = get_gemini_response(input_prompt, image_url)
#     st.header("The Response is")
#     st.write(response)
