from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import random
from textblob import TextBlob

app = Flask(__name__)
CORS(app)

openings = [
    "Hello! How can I assist you today?",
    "Hi there! What can I do for you?",
    "Good day! How can I help?",
    "Hey! What would you like to know?",
    "Welcome! How can I assist you?"
]

closings = [
    "Thank you for chatting with me. Have a great day!",
    "Goodbye! If you have any more questions, feel free to ask.",
    "Take care! I'm here if you need anything else.",
    "Farewell! Don't hesitate to reach out if you have more questions.",
    "It was nice talking to you. Bye!"
]

shop_related_keywords = ["clothes", "clothing", "apparel", "fashion", "shop", "store", "purchase", "buy", "sell", "retail", "t-shirt", "dress"]


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if is_shop_related(user_input):
        response = communicate_with_llama(user_input)
        sentiment = analyze_sentiment(response)
        response = filter_response_by_sentiment(response, sentiment)
    else:
        response = "I'm sorry, I can only help with questions related to clothing or our shop."
    return jsonify({'response': response})


@app.route('/start', methods=['GET'])
def start_conversation():
    opening = random.choice(openings)
    return jsonify({'response': opening})


@app.route('/end', methods=['GET'])
def end_conversation():
    closing = random.choice(closings)
    return jsonify({'response': closing})


def is_shop_related(user_input):
    return any(keyword in user_input.lower() for keyword in shop_related_keywords)


def communicate_with_llama(user_input):
    url = "http://localhost:11434/api/generate"
    payload = {
        'model': 'llama3',
        'prompt': user_input
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers, stream=True)

    full_response = ''
    for line in response.iter_lines():
        if line:
            part = json.loads(line.decode('utf-8')).get('response', '')
            full_response += part
            if json.loads(line.decode('utf-8')).get('done', False):
                break

    return full_response


def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return 'positive'
    elif sentiment < 0:
        return 'negative'
    else:
        return 'neutral'


def filter_response_by_sentiment(response, sentiment):
    desired_sentiment = 'positive'
    if sentiment != desired_sentiment:
        return f"Response filtered for {desired_sentiment} sentiment."
    return response


if __name__ == '__main__':
    app.run(debug=True)
