# 📄 PDF Translation Service

A simple web app built with [Streamlit](https://streamlit.io/) that allows users to upload a PDF file and translate the text content into a selected target language. The app uses **PyMuPDF** for PDF parsing and manipulation and **Google Translate** (via `googletrans`) for text translation.

## 🚀 Features

- Upload any PDF document.
- Select from multiple target languages (English, French, German, Spanish).
- Automatically extracts, translates, and overlays translated text on the original PDF layout.
- Download the fully translated PDF.
- Clean and easy-to-use web interface powered by Streamlit.

---

## 🌍 Supported Languages

* English (en)

* French (fr)

* German (de)

* Spanish (es)

More languages can be added by extending the list in the selectbox.
---
## 🛠️ Requirements

- Python 3.8+
- googletrans (text translation)
---

## 📦 Installation

### 1. Clone the Repository

```bash
git lone https://github.com/YogiHalagunaki/Data-Science-GenAI-Solutions.git
cd Document Translation
```
### 2. Python Packages

Install all dependencies using:

```bash
pip install -r requirements.txt
```
### 3. Running the App
``` bash
streamlit run translatorgpt.py

Note :  Replace app.py with the actual filename of your script if different.
```

---

## 🙋 Author

**Yogi Halagunaki**  
GitHub: [@YogiHalagunaki](https://github.com/YogiHalagunaki)  
Email: halagunakiyogi@gmil.com  
Location: India 
