# 🌐 AI Language Translation Tool

## 📌 Project Overview
The **AI Language Translation Tool** is a web-based application that translates text between multiple languages using AI-powered translation APIs.  
It supports automatic language detection, text-to-speech conversion, and a clean, user-friendly interface.

This project is developed as part of the **CodeAlpha Internship – Task 1**.

---

## 🎯 Objectives
- Translate text between multiple languages accurately
- Provide a simple and intuitive user interface
- Demonstrate API integration in Python
- Implement additional features like text-to-speech and clipboard copy

---

## 🛠️ Tech Stack
**Frontend / UI**
- Streamlit
- Custom CSS

**Backend / Logic**
- Python
- Translatepy API
- gTTS (Google Text-to-Speech)

---

## ✨ Features
- Supports **100+ languages**
- Auto language detection
- Clean and responsive UI
- Text-to-speech output
- Copy translated text to clipboard
- Translation history (session-based)
- Error handling for invalid inputs

---

## 📁 Project Structure

```text
Language_Translator/
├── app.py
├── requirements.txt
└── README.md

▶️ How to Run the Project
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Run the application
streamlit run app.py

3️⃣ Open in browser
http://localhost:8501

🧪 Sample Test Inputs
Hello, how are you?
Good morning
Translate this sentence into Hindi
नमस्कार, माझं नाव प्रनाली आहे

📌 Notes
Internet connection is required for translation
Auto-detect works best with longer sentences
gTTS supports most major languages
