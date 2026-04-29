from web3 import Web3

rpc_url = "https://ethereum.publicnode.com"

w3 = Web3(Web3.HTTPProvider(rpc_url))

print("Conectado:", w3.is_connected())

if w3.is_connected():
    print("Bloque actual:", w3.eth.block_number)
