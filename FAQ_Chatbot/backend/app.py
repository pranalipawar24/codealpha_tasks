from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import string

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can access backend

# Load FAQs from JSON file
FAQ_FILE = os.path.join(os.path.dirname(__file__), "faqs.json")

with open(FAQ_FILE, "r", encoding="utf-8") as file:
    faqs = json.load(file)


def find_best_answer(user_message):
    """
    Matches user message with FAQ keywords
    and returns the best matching answer.
    """
    import string

    user_message = user_message.lower()
    words = user_message.translate(
        str.maketrans("", "", string.punctuation)
    ).split()

    # Greeting handling
    greetings = ["hi", "hello", "hey", "morning", "evening"]
    for greet in greetings:
        if greet in words:
            return "Hello! I’m the Internship Assistant FAQ Bot. How can I help you?"

    best_match_score = 0
    best_answer = None

    for faq in faqs:
        score = 0
        for keyword in faq["keywords"]:
            if keyword in words:
                score += 1

        if score > best_match_score:
            best_match_score = score
            best_answer = faq["answer"]

    if best_match_score == 0:
        return (
            "I’m designed to answer internship-related questions. "
            "Please ask about tasks, submission, certificates, or duration."
        )

    return best_answer


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({
            "response": "Invalid request. Please send a message."
        }), 400

    user_message = data["message"]
    bot_response = find_best_answer(user_message)

    return jsonify({
        "response": bot_response
    })


if __name__ == "__main__":
    app.run(debug=True)
