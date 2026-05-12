from flask import Flask, request, jsonify, render_template
from web3 import Web3

app = Flask(__name__)

# 🌐 Web3 connection
RPC_URL = "https://mainnet.infura.io/v3/4d271f5642ca493d9300cb49f8f560df"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# ---------------- WEB3 LOGIC ----------------

def decode_transfer(data):
    data = data[2:]
    params = data[8:]
    to_raw = params[0:64]
    amount_raw = params[64:128]

    to_address = "0x" + to_raw[-40:]
    amount_int = int(amount_raw, 16)

    return to_address, amount_int


def analyze_transaction(tx_hash):
    tx = w3.eth.get_transaction(tx_hash)

    return {
        "from": tx["from"],
        "to": tx["to"],
        "value_eth": str(w3.from_wei(tx["value"], "ether")),
        "gas": tx["gas"]
    }

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return "🔥 Crypto Bot is running correctly"

@app.route("/analyze", methods=["POST"])
def analyze():
    tx_hash = request.json.get("hash")

    try:
        result = analyze_transaction(tx_hash)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------------- START ----------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)


import threading
import webbrowser
from app import app

def run():
    app.run(port=5000, debug=False)

if __name__ == "__main__":
    threading.Thread(target=run).start()
    webbrowser.open("http://127.0.0.1:5000")
