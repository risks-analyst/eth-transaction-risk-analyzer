from web3 import Web3

RPC_URL = "https://mainnet.infura.io/v3/4d271f5642ca493d9300cb49f8f560df"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    print("Connection failed. Check your RPC.")
    exit()

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
        return (
            "High 🔴",
            "This contract may be requesting unlimited access to your tokens. "
            "Unlimited approvals are rarely necessary for normal operations. "
            "Consider whether you fully trust this contract before proceeding."
        )

    if tipo == "Approve":
        return (
            "Medium 🟡",
            "You may be authorizing an external contract to move tokens on your behalf. "
            "This is common in DeFi, but it is worth verifying that the contract "
            "is well-known and has been audited."
        )

    eth_val = w3.from_wei(tx["value"], "ether")
    if eth_val > 1:
        return (
            "Medium 🟡",
            f"This transaction involves approximately {eth_val} ETH. "
            "Higher amounts increase the potential impact of any mistake. "
            "It is advisable to double-check the destination address before signing."
        )

    if tipo == "Desconocido":
        return (
            "Medium 🟡",
            "The type of operation could not be identified with certainty. "
            "This is likely an interaction with a specific smart contract. "
            "If you do not recognize this contract, it may be worth researching it first."
        )

    if tipo == "Token Transfer":
        return (
            "Low 🟢",
            "This appears to be a standard token transfer. "
            "It is likely low risk, as long as the destination address is correct."
        )

    return (
        "Low 🟢",
        "This appears to be a direct ETH transfer. "
        "It is likely low risk if the destination address is known and trusted."
    )

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

tx_hash   = input("Enter transaction hash: ")
tx        = w3.eth.get_transaction(tx_hash)
resultado = interpretar_tx(tx)
eth_val   = w3.from_wei(tx["value"], "ether")
riesgo, motivo = evaluar_riesgo(tx, resultado["tipo"], resultado["cantidad"])

print("\n===============================")
print("   TRANSACTION RISK ANALYSIS")
print("===============================")
print(f"Type:     {resultado['tipo']}")
print(f"Action:   {resultado['accion']}")
print(f"ETH:      {eth_val}")
print(f"Amount:   {resultado['cantidad']}")
print(f"Risk:     {riesgo}")
print(f"Details:  {motivo}")
print("===============================")
