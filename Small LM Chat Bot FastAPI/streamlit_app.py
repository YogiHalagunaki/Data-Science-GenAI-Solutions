import json
import time
import requests
from UI_items import *
import streamlit as st
from typing import List, Dict

st.set_page_config(
    layout="wide",
    page_title="SLM INFERENCE",
    initial_sidebar_state="auto",
    menu_items=None,
    )

# Constants
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'selected_model' not in st.session_state:
    st.session_state.selected_model = None

def get_available_models() -> Dict[str, Dict]:
    """Fetch available models from the config"""
    response = requests.get(f"{API_BASE_URL}/models")
    if response.status_code == 200:
        return {model['name']: model for model in response.json()}
    return {}

def download_model(model_name: str):
    """Download a model"""
    payload = {
        "model_name": model_name,
        "repo_id": "",
        "filename": ""
    }
    with st.spinner(f'Downloading {model_name}...'):
        try:
            response = requests.post(f"{API_BASE_URL}/models/download", json=payload)
            st.sidebar.write("Debug - Download Response:", response.json())
            if response.status_code == 200:
                st.success(f"Successfully downloaded {model_name}")
                time.sleep(2)
                st.rerun()
            else:
                st.error(f"Error downloading model: {response.json()['detail']}")
        except Exception as e:
            st.error(f"Error during download: {str(e)}")

def chat_with_model(model_name: str, messages: List[Dict], max_tokens: int =2000, top_p: float=0.95, top_k: int =40, repeat_penalty: float=1.1, presence_penalty: float=0.0, frequency_penalty: float=0.0, temperature: float = 0.3):
    """Send a chat request to the API"""
    payload = {
        "messages": messages,
        "model_name": model_name,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "top_k": top_k,
        "repeat_penalty": repeat_penalty,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
        "stream": False
    }
    response = requests.post(f"{API_BASE_URL}/chat", json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.json()['detail']}")
        return None

def main():
    create_header(heading="SLM INFERENCE")
    st.text(" ")
    st.text(" ")
    # Sidebar for model management
    with st.sidebar:
        st.header("Model Management")
        
        # Get current models status
        available_models = get_available_models()
        
        # Display downloaded models
        st.subheader("Downloaded Models")
        if available_models:
            for model_name, model_info in available_models.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"Model Name:::{model_name}")
                    st.caption(f"Status: {model_info['status']}")
                with col2:
                    if st.button("Delete", key=f"delete_{model_name}"):
                        response = requests.delete(f"{API_BASE_URL}/models/{model_name}")
                        if response.status_code == 200:
                            st.success("Model deleted")
                            time.sleep(1)
                            st.rerun()
        else:
            st.info("No models downloaded yet")
        
        # Download new models section
        st.subheader("Download New Models")
        from_config = {
            "llama-3.2-1b": "Llama 3.2B (1B)",
            "qwen-2.5-1.5b": "Qwen 2.5 (1.5B)",
            "qwen-2.5-0.5b": "Qwen 2.5 (0.5B)",
            "gemma-2-2b": "Gemma 2 (2B)"
        }
        
        for model_id, model_name in from_config.items():
            if model_id not in available_models:
                if st.button(f"Download {model_name}", key=f"download_{model_id}"):
                    download_model(model_id)

    # Main chat interface
    st.header("Chat Interface")
    
    # Model selector and parameters
    col1,_,c1,_, col2 = st.columns([2,0.5,2.5,0.5, 2])
    
    with col2:
        st.text(" ")
        st.text(" ")
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
    with col1:
        st.text(" ")
        downloaded_models = [name for name in available_models.keys()]
        if downloaded_models:
            selected_model = st.selectbox(
                "Select a model to chat with",
                downloaded_models,
                index=0 if st.session_state.selected_model is None else downloaded_models.index(st.session_state.selected_model)
            )
            st.session_state.selected_model = selected_model
        else:
            st.warning("Please download a model first to start chatting")
            return
    
    with c1:
        st.text(" ")
        st.text(" ")
        show_params = st.checkbox("Show Advanced Parameters", value=False)
    
    # Model parameters in an expander
    if show_params:
        with st.expander("Model Parameters", expanded=True):
            col1, col2,col3,col4 = st.columns(4)
            
            with col1:
                temperature = st.slider(
                    "Temperature",
                    min_value=0.0,
                    max_value=2.0,
                    value=0.3,
                    step=0.1,
                    help="Higher values make output more random, lower values more deterministic"
                )
                
                top_p = st.slider(
                    "Top P",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.95,
                    step=0.05,
                    help="Nucleus sampling threshold"
                )
                
            with col2:              
                
                top_k = st.slider(
                    "Top K",
                    min_value=1,
                    max_value=100,
                    value=40,
                    step=1,
                    help="Limits vocabulary to top K tokens"
                )
                
                presence_penalty = st.slider(
                    "Presence Penalty",
                    min_value=-2.0,
                    max_value=2.0,
                    value=0.0,
                    step=0.1,
                    help="Penalizes tokens based on presence in history"
                )
                   
            with col3:
                max_tokens = st.slider(
                    "Max Tokens",
                    min_value=50,
                    max_value=4096,
                    value=2000,
                    step=50,
                    help="Maximum number of tokens to generate"
                )
                 
                frequency_penalty = st.slider(
                    "Frequency Penalty",
                    min_value=-2.0,
                    max_value=2.0,
                    value=0.0,
                    step=0.1,
                    help="Penalizes tokens based on frequency"
                )
                
            with col4:
                repeat_penalty = st.slider(
                    "Repeat Penalty",
                    min_value=1.0,
                    max_value=2.0,
                    value=1.1,
                    step=0.1,
                    help="Penalizes repeated tokens"
                )

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_with_model(
                    st.session_state.selected_model,
                    st.session_state.messages,
                    max_tokens,
                    top_p,
                    top_k,
                    repeat_penalty,
                    presence_penalty,
                    frequency_penalty,
                    temperature
                )
                if response:
                    assistant_response = response['choices'][0]['message']['content']
                    st.write(assistant_response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

if __name__ == "__main__":
    main()
