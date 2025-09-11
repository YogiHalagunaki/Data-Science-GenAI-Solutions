import requests
from bson.objectid import ObjectId

doc_id=ObjectId()

doc_id=str(doc_id)

url = "http://127.0.0.1:5000/skense/insurance_finance_doc_processing"

filepath = ""

# Example data to send in the request body
data = { "filepath": filepath }

# Make the POST request to the API
response = requests.post(url, json=data, verify=False)

# Check the response
if response.status_code == 200:
    print("Response:", response.json())
else:
    print(f"Error {response.status_code}: {response.text}")
