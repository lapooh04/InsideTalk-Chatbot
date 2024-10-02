from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

app = Flask(__name__)

emotions = {
    "joy": {
        "name": "Joy",
        "response_style": "uplifting",
        "emoji": "😊",
        "validation_message": "It's great to feel joy! 😊 Let's keep that positive vibe going."
    },
    "sadness": {
        "name": "Sadness",
        "response_style": "empathetic",
        "emoji": "😢",
        "validation_message": "I understand that sadness can be heavy. 😢 I'm here for you."
    },
    "anger": {
        "name": "Anger",
        "response_style": "frustrated",
        "emoji": "😠",
        "validation_message": "It's okay to feel angry. 😠 Your feelings are valid and important."
    },
    "fear": {
        "name": "Fear",
        "response_style": "cautious",
        "emoji": "😨",
        "validation_message": "Fear can be overwhelming. 😨 Let's talk about what's on your mind."
    },
    "disgust": {
        "name": "Disgust",
        "response_style": "sarcastic",
        "emoji": "🤢",
        "validation_message": "Feeling disgust is normal. 🤢 Let's work through it together."
    },
}

conversation_history = []

def get_emotion_response(emotion, user_message):
    """Generate a response from the selected emotion character, including conversation history."""

    validation_message = emotion['validation_message']
    history_prompt = "\n".join(conversation_history)
    prompt = f"{history_prompt}\n{validation_message}: {user_message}."
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

@app.route('/')
def home():
    
    global conversation_history
    conversation_history = [] 
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    selected_emotions = request.form['selected_emotions'].split(',')
    selected_emotions = [emotion.strip() for emotion in selected_emotions if emotion.strip() in emotions]
    
    if selected_emotions:
        responses = []
        for emotion_key in selected_emotions:
            emotion = emotions[emotion_key]
            conversation_history.append(f"You: {user_input}")
            response_text = get_emotion_response(emotion, user_input)
            response_data = {
                'name': emotion['name'],
                'emoji': emotion['emoji'],
                'response': response_text,
                'emotionClass': emotion_key 
            }
            conversation_history.append(f"{emotion['name']} ({emotion['emoji']}): {response_text}")
            responses.append(response_data)

        return jsonify({'responses': responses})
    else:
        return jsonify({'response': "No valid emotions selected."})

if __name__ == '__main__':
    app.run(debug=True)
