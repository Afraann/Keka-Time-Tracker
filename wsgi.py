from waitress import serve
from app import app
import logging

if __name__ == "__main__":
    logging.info("Starting Waitress server on http://0.0.0.0:8080")
    serve(app, host='0.0.0.0', port=8080)
