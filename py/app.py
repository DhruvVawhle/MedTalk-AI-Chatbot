from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from api.env file in the same directory
load_dotenv('api.env')

# Get API key securely from environment variables
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    logging.error("ERROR: GEMINI_API_KEY not found in api.env file!")
    raise ValueError("GEMINI_API_KEY environment variable is not set")

logging.info(f"API Key loaded: {api_key[:20]}...")  # Log first 20 chars for debugging

# Configure Gemini API
genai.configure(api_key=api_key)

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize the generative model
model = genai.GenerativeModel('gemini-2.0-flash')  # Use the latest stable version

# Serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/favicon.ico")
def favicon():
    """Return a 204 No Content response for favicon requests"""
    return "", 204

# API endpoint to handle chat requests
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('query')

        if not user_input:
            return jsonify({'error': 'No input provided'}), 400
        
        # Generate response using Gemini API
        response = model.generate_content(user_input)
        
        # Handle response safely
        if response and hasattr(response, 'candidates') and response.candidates:
            reply_text = response.candidates[0].content.parts[0].text
        elif response and hasattr(response, 'text'):
            reply_text = response.text
        else:
            reply_text = "Sorry, I couldn't generate a response."
        
        return jsonify({'reply': reply_text})
    
    except Exception as e:
        error_msg = str(e)
        logging.error(f"API error: {error_msg}")
        
        # Handle quota errors gracefully
        if "429" in error_msg or "quota" in error_msg.lower():
            return jsonify({'error': 'API quota exceeded. Please wait a moment and try again.'}), 429
        else:
            return jsonify({'error': 'Failed to get response from the server.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
