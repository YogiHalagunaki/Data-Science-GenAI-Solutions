import requests
import json

BASE_URL = "http://localhost:8000"
MODEL_NAME = "qwen-2.5-0.5b"      # choice the model as per your requirment 

def test_root():
    print("::::::::GET::::::::")
    res = requests.get(f"{BASE_URL}/")
    print(res.status_code, res.json())

def test_download_model():
    print("::::::POST:::::::")
    payload = {
        "model_name": MODEL_NAME,
        "repo_id": "Qwen/Qwen2.5-0.5B-Instruct-GGUF",
        "filename": "qwen2.5-0.5b-instruct-fp16.gguf"
    }
    res = requests.post(f"{BASE_URL}/models/download", json=payload)
    print(res.status_code, res.json())

def test_list_models():
    print("::::::::GET:::::::::::")
    res = requests.get(f"{BASE_URL}/models")
    print(res.status_code, json.dumps(res.json(), indent=2))

def test_chatBot(que):
    print(":::::::::POST:::::::::")
    payload = {
        "model_name": MODEL_NAME,
        "messages": [{"role": "user", "content": que}],
        "temperature": 0.7,
        "max_tokens": 100,
        "stream": False
    }
    res = requests.post(f"{BASE_URL}/chat", json=payload)
    print(res.status_code)
    try:
        print(json.dumps(res.json(), indent=2))
    except Exception:
        print("Error parsing response:", res.text)

def test_unload_model():
    print("::::::::::POST::::::::::::")
    res = requests.post(f"{BASE_URL}/models/{MODEL_NAME}/unload")
    print(res.status_code, res.json())

def test_delete_model():
    print("::::::::::DELETE:::::::::::::")
    res = requests.delete(f"{BASE_URL}/models/{MODEL_NAME}")
    print(res.status_code, res.json())

if __name__ == "__main__":
    #test_root()
    #test_download_model()
    #test_list_models()
    test_chatBot("Tell me a joke.")
    test_chatBot("Tell me my name if posible")
    test_chatBot("how many states in India.")
    #test_unload_model()
    #test_delete_model()
