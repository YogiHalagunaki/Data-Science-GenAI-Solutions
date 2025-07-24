
# 🌍 LLM LANG TRANSLATOR

**LLM LANG TRANSLATOR** is a powerful multi-model app that uses state-of-the-art language models to extract and translate text from either raw input or images into English. It compares translations across **GPT-4**, **Claude Sonnet**, and **Gemini 1.5 Pro** side-by-side.

---

## 🚀 Features

- 🔤 **Text Translation**: Input any text in any language and get English translations from 3 different LLMs.
- 🖼️ **Image Translation**: Upload an image, and the app will extract visible text and translate it to English.
- 📊 **LLM Comparison**: Compare outputs from **GPT-4**, **Claude Sonnet**, and **Gemini 1.5 Pro** in parallel.
- 📥 **Export Results**: Download the results as a `.json` file.
- 🎨 **Responsive UI**: Clean and user-friendly layout with side-by-side output display.

---
## 🧠 Model Behavior
The models follow a shared system prompt that:

* Translates any language to English.

* Extracts text from images.

* Maintains structure and formatting.

* Handles multi-language inputs.

* Ignores input already in English.

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/)
- [litellm](https://github.com/BerriAI/litellm)
- [Google Generative AI](https://ai.google.dev/)
- [Pillow](https://pillow.readthedocs.io/)
- [dotenv](https://pypi.org/project/python-dotenv/)

---

## 📁 Project Structure
```bash 
├── streamlit_app.py                 # Main Streamlit app
├── UI_items.py            # UI styling and header
├── requirements.txt
├── .env                   # Your environment variables (not tracked)
└── README.md

```

---
## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YogiHalagunaki/Data-Science-GenAI-Solutions.git
cd Language Translator Streamlit App  # or the correct path to your health app

```

### 2. Install Dependencies
```bash 
pip install -r requirements.txt

```
### 3. Set Up .env
```env
AZURE_API_KEY=your_azure_key
AZURE_API_BASE=your_azure_endpoint
AZURE_API_VERSION=2023-12-01-preview
GEMINI_API_KEY=your_gemini_key

```
## ▶️ Run the App
```bash 
streamlit run streamlit_app.py

```

## 🙋 Author

**Yogi Halagunaki**  
GitHub: [@YogiHalagunaki](https://github.com/YogiHalagunaki)  
Email: halagunakiyogi@gmil.com  
Location: India 
