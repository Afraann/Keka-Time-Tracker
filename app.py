import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini API
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        # Manual CORS handling
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        if not GENAI_API_KEY:
             return jsonify({"error": "Server configuration error: GEMINI_API_KEY not set"}), 500

        img = Image.open(file.stream)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = (
            "Analyze this Keka attendance timeline screenshot. "
            "1. Check if there is an 'OUT missing' log indicating an active session. "
            "2. If active, extract the exact time of the punch-in immediately above 'OUT missing'. "
            "3. Extract the already completed 'Effective hours' shown at the top of the screen. "
            "4. Output ONLY a raw JSON object with this exact structure (do not include markdown tags): "
            "{\"lastPunchIn\": \"HH:MM:SS AM/PM\", \"syncedEffectiveHours\": \"Hh Mm\", \"isActiveSession\": true}"
        )

        response = model.generate_content([prompt, img])
        
        # Clean up response text to ensure it's valid JSON
        response_text = response.text.replace('```json', '').replace('```', '').strip()
        
        return response_text, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method Not Allowed. Ensure you are sending a POST request."}), 405

if __name__ == '__main__':
    app.run(debug=True)
