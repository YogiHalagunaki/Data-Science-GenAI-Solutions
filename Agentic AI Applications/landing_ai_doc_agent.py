import requests

# Replace with the actual path to your image or PDF file
file_path = "./media/yogi/WORK_SPACE/GenAI_Solutions/Data/test.pdf"

# Choose either image or pdf depending on the file type
files = {
    #"image": open(file_path, "rb")  # For image file
    "pdf": open(file_path, "rb")  # Uncomment this line if it's a PDF file
}

# Replace with your actual API key
headers = {
    "Authorization": "ENTER_YOUR_API_KEY_HERE",
}

# Define the API endpoint
url = "https://api.va.landing.ai/v1/tools/agentic-document-analysis"

# Make the POST request
response = requests.post(url, files=files, headers=headers)

# Print the response in JSON format
print(response.json())

# Don't forget to close the file after the request is made
files["image"].close()  # Or files["pdf"].close() if using a PDF
