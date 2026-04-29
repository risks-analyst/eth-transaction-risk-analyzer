 freb3 import Web3
 
# Tu URL de conexión al nodo RPC
RPC_URL = "http://127.0.0.1:8545"
 
# Crear el objeto de conexión
w3 = Web3(Web3.HTTPProvider(RPC_URL))
 # ── Conexión ────────────────────────────────────
RPC_URL = = "http://127.0.0.1:8545"  # sin API key

 
if not w3.is_connected():
    print("Sin conexión. Verifica tu RPC.")
    exit()
 
# ── Intérprete ───────────────────────────────────
def interpretar_tx(tx):
    value = tx["value"]
    data  = tx["input"]
 
    if value > 0 and data == "0x":
        return {"tipo": "ETH Transfer", "accion": "Envío directo de ETH", "riesgo": "Bajo"}
 
    elif data.startswith("0xa9059cbb"):
        return {"tipo": "Token Transfer", "accion": "Envío de tokens ERC-20", "riesgo": "Bajo"}
 
    elif data.startswith("0x095ea7b3"):
        return {"tipo": "Approve", "accion": "Permiso a contrato para gastar tokens", "riesgo": "Alto"}
 
    else:
        return {"tipo": "Desconocido", "accion": "Interacción con contrato", "riesgo": "Medio"}
 
# ── Ejecución ────────────────────────────────────
tx_hash = input("Pega el hash de la transacción: ")
 
tx        = w3.eth.get_transaction(tx_hash)
resultado = interpretar_tx(tx)
eth_val   = w3.from_wei(tx["value"], "ether")
 
print("\n===============================")
print("  ANÁLISIS DE TRANSACCIÓN")
print("===============================")
print(f"Tipo:     {resultado[\"tipo\"]}")
print(f"Acción:   {resultado[\"accion\"]}")
print(f"ETH:      {eth_val}")
print(f"Riesgo:   {resultado[\"riesgo\"]}")
print("===============================")
