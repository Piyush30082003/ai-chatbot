from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import logging

app = Flask(__name__, template_folder="../templates")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


conversation_history = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "AI Chatbot"}), 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True)
        if not data or "message" not in data:
            return jsonify({"error": "Message is required"}), 400

        user_message = data["message"].strip()
        session_id = data.get("session_id", "default")

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Build conversation history for context
        if session_id not in conversation_history:
            conversation_history[session_id] = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful, friendly AI assistant. "
                        "Answer questions clearly and concisely."
                    ),
                }
            ]

        conversation_history[session_id].append(
            {"role": "user", "content": user_message}
        )

        # Keep last 10 messages to avoid token overflow
        messages = conversation_history[session_id][-10:]

        logger.info(f"Session {session_id}: Sending message to OpenAI")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )

        assistant_message = response.choices[0].message.content

        conversation_history[session_id].append(
            {"role": "assistant", "content": assistant_message}
        )

        return jsonify(
            {
                "response": assistant_message,
                "session_id": session_id,
                "tokens_used": response.usage.total_tokens,
            }
        ), 200

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route("/reset", methods=["POST"])
def reset_conversation():
    data = request.get_json()
    session_id = data.get("session_id", "default") if data else "default"
    if session_id in conversation_history:
        del conversation_history[session_id]
    return jsonify({"message": "Conversation reset successfully"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
