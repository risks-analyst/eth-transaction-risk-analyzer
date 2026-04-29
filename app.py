from flask import Flask, render_template, request, jsonify
from web3 import Web3

app = Flask(__name__)

RPC_URL = "https://mainnet.infura.io/v3/4d271f5642ca493d9300cb49f8f560df"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def decode_transfer(data):
    data       = data[2:]
    params     = data[8:]
    to_raw     = params[0:64]
    amount_raw = params[64:128]
    to_address = "0x" + to_raw[-40:]
    amount_int = int(amount_raw, 16)
    return to_address, amount_int

def evaluar_riesgo(tx, tipo, cantidad=0):
    MAX_UINT256 = 2**256 - 1
    if tipo == "Approve" and cantidad >= MAX_UINT256:
        return "High 🔴", "This contract may be requesting unlimited access to your tokens. Unlimited approvals are rarely necessary. Consider whether you fully trust this contract."
    if tipo == "Approve":
        return "Medium 🟡", "You may be authorizing an external contract to move tokens on your behalf. Verify the contract is well-known and audited."
    eth_val = w3.from_wei(tx["value"], "ether")
    if eth_val > 1:
        return "Medium 🟡", f"This transaction involves approximately {eth_val} ETH. Double-check the destination address before signing."
    if tipo == "Desconocido":
        return "Medium 🟡", "The operation type could not be identified. If you do not recognize this contract, research it before proceeding."
    if tipo == "Token Transfer":
        return "Low 🟢", "This appears to be a standard token transfer. Likely low risk if the destination address is correct."
    return "Low 🟢", "This appears to be a direct ETH transfer. Likely low risk if the destination is known and trusted."

def interpretar_tx(tx):
    value = tx["value"]
    data  = tx["input"].hex()
    if value > 0 and data == "0x":
        return {"tipo": "ETH Transfer", "accion": "Direct ETH transfer", "cantidad": 0}
    elif data.startswith("0xa9059cbb"):
        to, amount = decode_transfer(data)
        return {"tipo": "Token Transfer", "accion": f"Sending tokens to {to}", "cantidad": amount}
    elif data.startswith("0x095ea7b3"):
        to, amount = decode_transfer(data)
        return {"tipo": "Approve", "accion": f"Granting permission to {to}", "cantidad": amount}
    else:
        return {"tipo": "Desconocido", "accion": "Smart contract interaction", "cantidad": 0}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analizar", methods=["POST"])
def analizar():
    tx_hash = request.json.get("hash")
    try:
        tx        = w3.eth.get_transaction(tx_hash)
        resultado = interpretar_tx(tx)
        eth_val   = w3.from_wei(tx["value"], "ether")
        riesgo, motivo = evaluar_riesgo(tx, resultado["tipo"], resultado["cantidad"])
        return jsonify({
            "tipo":    resultado["tipo"],
            "accion":  resultado["accion"],
            "eth":     str(eth_val),
            "cantidad": str(resultado["cantidad"]),
            "riesgo":  riesgo,
            "motivo":  motivo
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
