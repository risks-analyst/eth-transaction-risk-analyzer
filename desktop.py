import threading
import webview
from app import app  # your Flask app

def run_flask():
    app.run(debug=False, port=5000)

if __name__ == "__main__":
    # Run Flask in background
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    # Open desktop window (software mode)
    webview.create_window("Crypto Analyzer Bot", "http://127.0.0.1:5000")
    webview.start()
