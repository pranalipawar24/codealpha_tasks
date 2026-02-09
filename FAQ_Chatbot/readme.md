🤖 Internship Assistant FAQ Chatbot
📌 Project Overview
The Internship Assistant FAQ Chatbot is a domain-specific chatbot designed to answer frequently asked questions related to an internship program.
It provides instant, accurate responses to common queries about internship details, tasks, submissions, certificates, and support.
This project is developed as part of CodeAlpha Internship – Task.
________________________________________
🎯 Objectives
•	Provide quick answers to internship-related FAQs
•	Reduce manual effort in answering repetitive questions
•	Demonstrate basic NLP logic using keyword matching
•	Build a full-stack chatbot with frontend and backend integration
________________________________________
🛠️ Tech Stack
Frontend
•	HTML
•	CSS
•	JavaScript
Backend
•	Python
•	Flask
•	Flask-CORS
Data
•	JSON-based FAQ knowledge base
________________________________________
⚙️ Features
•	Friendly greeting responses (Hi, Hello, Good Morning, etc.)
•	Domain-specific FAQ handling
•	Keyword-based matching for user questions
•	JSON-driven knowledge base (easy to update)
•	Clean and responsive UI
•	Backend API integration using Flask
•	Cross-origin support using CORS
________________________________________
📂 Project Structure
FAQ_Chatbot/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── app.py
│   ├── faqs.json
│   └── requirements.txt
│
└── README.md
________________________________________
🚀 How It Works
1.	User enters a question in the chatbot UI
2.	The frontend sends the message to the Flask backend
3.	The backend processes the input:
o	Handles greetings
o	Matches keywords with the FAQ dataset
4.	The best-matched answer is returned to the frontend
5.	The chatbot displays the response instantly
________________________________________
▶️ How to Run the Project
Step 1: Clone the Repository
git clone https://github.com/pranalipawar24/codealpha_tasks.git
Step 2: Navigate to Backend
cd FAQ_Chatbot/backend
Step 3: Install Dependencies
pip install -r requirements.txt
Step 4: Run Flask Server
python app.py
Step 5: Open Frontend
Open frontend/index.html in your browser.
________________________________________
🧪 Sample Questions
•	What is this internship about?
•	How many tasks do I need to complete?
•	How do I submit my project?
•	Will I get a certificate?
•	Is this internship paid?
________________________________________
✅ Output
•	A functional FAQ chatbot that answers internship-related queries
•	Clean UI with smooth interaction
•	Accurate responses based on predefined knowledge base
________________________________________
📌 Future Enhancements
•	Use NLP libraries for smarter matching
•	Add database support instead of JSON
•	Implement machine learning–based intent detection
•	Add admin panel to manage FAQs
________________________________________
👩‍💻 Author
Pranali Pawar
CodeAlpha Intern
________________________________________
📅 Internship Task
CodeAlpha – Internship Task: FAQ Chatbot

