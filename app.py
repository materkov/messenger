from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/conversations')
def get_conversations():
    data = [
        {
            'id': 12,
            'title': 'Conversation 1'
        },
        {
            'id': 14,
            'title': 'Conversation 3'
        }
    ]
    return json.dumps(data)
