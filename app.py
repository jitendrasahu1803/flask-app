from flask import Flask, jsonify, request
import random
from datetime import datetime

app = Flask(__name__)

# Sample quotes
quotes = [
    "Believe you can and you're halfway there.",
    "Don’t watch the clock; do what it does. Keep going.",
    "Success is what happens after you survive all your mistakes.",
    "The harder you work for something, the greater you’ll feel when you achieve it.",
    "Dream it. Wish it. Do it.",
    "Push yourself, because no one else is going to do it for you."
]

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Motivational Quote Generator API!",
        "endpoints": ["/quote", "/quote/add"]
    })

@app.route('/quote', methods=['GET'])
def get_quote():
    return jsonify({
        "quote": random.choice(quotes),
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/quote/add', methods=['POST'])
def add_quote():
    data = request.get_json()
    quote = data.get('quote')
    if quote:
        quotes.append(quote)
        return jsonify({"message": "Quote added!", "total_quotes": len(quotes)}), 201
    return jsonify({"error": "No quote provided"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

