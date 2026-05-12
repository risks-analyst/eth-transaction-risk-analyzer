import threading
import webbrowser
from app import app

def run():
    app.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    threading.Thread(target=run).start()

    # Open as system-style interface
    webbrowser.open("http://127.0.0.1:5000")
