from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from textblob import TextBlob
from dotenv import load_dotenv
import os

# Configure Google Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Mental Health Tips Database
MENTAL_HEALTH_TIPS = {
    "stress": "Try deep breathing exercises or meditation to manage stress.",
    "anxiety": "Practicing mindfulness can help reduce anxiety levels.",
    "depression": "Consider speaking to a therapist if you're feeling persistently low.",
    "sleep": "Good sleep hygiene includes maintaining a regular sleep schedule.",
    "exercise": "Regular exercise boosts mental health by releasing endorphins.",
}

# Simple predefined chatbot responses
CHAT_RESPONSES = {
    "hello": "Hey there! How are you feeling today?",
    "hi": "Hello! What’s on your mind?",
    "help": "I’m here for you. You can talk to me about anything that’s bothering you.",
    "bye": "Take care of yourself. I'm always here if you need to talk."
}

# Function to get response from Gemini AI
def get_gemini_response(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Using the latest model
        response = model.generate_content(text)
        
        if hasattr(response, "text"):
            return format_response(response.text)  # Format AI-generated response
        else:
            return "Sorry, I couldn't process your request."
    
    except Exception as e:
        print("Error:", e)
        return "I'm having trouble understanding right now. Try again later."

# Function to format chatbot responses for better readability
def format_response(text):
    formatted_text = text.replace("**", "").replace("*", "")  # Remove Markdown formatting
    formatted_text = formatted_text.replace("\n", "\n\n")  # Add spacing for better readability
    formatted_text = formatted_text.replace("-", "• ")
      # Convert dashes to bullet points
    return formatted_text.strip()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").lower()
    
    # Check for predefined responses
    for keyword in CHAT_RESPONSES:
        if keyword in user_message:
            return jsonify({"response": CHAT_RESPONSES[keyword]})

    # Sentiment analysis
    sentiment = TextBlob(user_message).sentiment.polarity
    
    # Handle **positive** emotions
    if sentiment > 0.3:
        positive_response = "😊 That's amazing! I'm really happy for you.\n"
        # Special handling for achievements
        if "won" in user_message or "achieved" in user_message or "first place" in user_message:
            positive_response += "🎉 Congratulations! Your hard work paid off. Keep pushing forward! 🚀"
        else:
            positive_response += "It's great to hear that you're feeling good. Want to share more about it?"
        return jsonify({"response": positive_response})

    # Handle **negative** emotions (already implemented)
    if sentiment < -0.3:
        distress_response = "I'm here for you. "
        ai_response = get_gemini_response("Provide a short, comforting message.")
        return jsonify({"response": f"{distress_response}{ai_response}"})

    # Check for mental health tips
    for keyword in MENTAL_HEALTH_TIPS:
        if keyword in user_message:
            return jsonify({"response": MENTAL_HEALTH_TIPS[keyword]})
    
    # Default AI-generated response using Gemini
    ai_response = get_gemini_response(user_message)
    return jsonify({"response": ai_response})


if __name__ == "__main__":
    app.run(debug=True)