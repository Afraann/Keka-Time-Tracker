# Keka Time Tracker

A simple Flask application to analyze Keka attendance screenshots and track your work hours.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables:**
    Create a `.env` file in the root directory (if not exists) and add your Gemini API Key:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```

## Running the Application

### Development
To run in development mode with debug enabled:
```bash
python app.py
```
Access at `http://localhost:5000`.

### Production
To run in production mode using `waitress` (a production-quality WSGI server):
```bash
python wsgi.py
```
Access at `http://localhost:8080`.

## Features
-   **Screenshot Analysis**: Upload a Keka timeline screenshot.
-   **AI Parsing**: Uses Google Gemini to extract punch-in times and effective hours.
-   **Live Timer**: Tracks your session duration and calculates "Time Remaining" to reach 7h 30m.
-   **Dark/Light Mode**: Toggle between themes.
