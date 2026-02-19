import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from google import genai  # The new unified SDK
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True

# Initialize the new Gemini Client
# It automatically looks for GEMINI_API_KEY in your .env, but we pass it explicitly to be safe
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY not found. Please check your .env file.")
    client = None
else:
    client = genai.Client(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if not client:
        return jsonify({"error": "Server API key configuration error"}), 500

    if 'image' not in request.files: # Antigravity frontend sends 'image', not 'screenshot'
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Open the image stream directly with Pillow
        img = Image.open(file.stream)
        
        prompt = (
            "Analyze this Keka attendance timeline screenshot. "
            "1. Check if there is an 'OUT missing' log indicating an active session. "
            "2. If active, extract the exact time of the punch-in immediately above 'OUT missing'. "
            "3. Extract the already completed 'Effective hours' shown at the top of the screen. "
            "4. Output ONLY a raw JSON object with this exact structure (do not include markdown tags): "
            "{\"lastPunchIn\": \"HH:MM:SS AM/PM\", \"syncedEffectiveHours\": \"Hh Mm\", \"isActiveSession\": true}"
        )

        # The new SDK syntax for generating content
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, img]
        )
        
        # Clean up response text just in case
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        
        return clean_json, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        logger.exception("Error processing image")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    # app.run(port=8080, debug=True)
    # app.run(debug=True)