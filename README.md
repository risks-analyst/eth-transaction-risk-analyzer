# ETH Transaction Risk Analyzer

Real-time Ethereum transaction risk analyzer. Detects transaction types, decodes contract calls, and provides probabilistic risk assessment in plain English.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-green)
![Web3](https://img.shields.io/badge/Web3.py-7.x-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Problem

Blockchain transactions are written in raw hexadecimal data that most users cannot interpret. A single misunderstood approval can drain an entire wallet. This tool translates raw on-chain data into plain English risk assessments before you sign anything.

## Live Demo

## Demo

[![ETH Risk Analyzer Demo](https://img.youtube.com/vi/4YUZ-EINPLM/0.jpg)](https://youtu.be/4YUZ-EINPLM)

## Features

- Paste any Ethereum transaction hash and get instant analysis
- Detects transaction types: ETH Transfer, Token Transfer, Approve, Contract Interaction
- Decodes contract call data (ABI selectors, destination address, amounts)
- Probabilistic risk assessment: Low, Medium, High
- Plain English explanations — no crypto knowledge required
- Clean dark UI, runs locally in your browser

## Architecture

Ethereum Network
↓
Infura/Alchemy RPC
↓
web3.py (Python)
↓
Flask Backend → Risk Engine → JSON Response
↓
HTML/CSS/JS Frontend

## Stack

- **Python** — core logic and blockchain interaction
- **Flask** — lightweight web server
- **web3.py** — Ethereum node communication
- **HTML/CSS/JS** — frontend interface
- **Infura/Alchemy** — RPC provider

## Setup

### Requirements

- Python 3.10+
- An Ethereum RPC URL (Infura, Alchemy, or Ankr)

### Installation

```bash
# Clone the repository
git clone https://github.com/risks-analyst/eth-transaction-risk-analyzer
cd eth-transaction-risk-analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure your RPC URL
echo "RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY" > .env
```

### Run

```bash
python app.py
```

Open your browser at `http://localhost:5000`

## How It Works

1. User pastes an Ethereum transaction hash
2. Backend fetches raw transaction data via RPC
3. Risk engine decodes the `input` field using ABI selectors
4. Probabilistic risk assessment is generated
5. Results displayed in plain English

## Risk Levels

| Level | When | Action |
|-------|------|--------|
| 🟢 Low | Standard ETH or token transfer | Generally safe |
| 🟡 Medium | Unknown contract or high ETH amount | Verify before signing |
| 🔴 High | Unlimited approval detected | Do not sign unless fully trusted |

## Technical Decisions

**Why Flask over FastAPI?**
Flask is lightweight and sufficient for a synchronous request-response model. FastAPI will be used in future versions for async support.

**Why selector-based detection over full ABI decoding?**
ERC-20 selectors are universal across all contracts. This approach works without requiring the contract ABI, making it faster and more accessible.

## Roadmap

- [ ] Full ABI decoding for known contracts
- [ ] Token name resolution via Etherscan API
- [ ] Multi-chain support (Polygon, Arbitrum, Base)
- [ ] Wallet history analysis
- [ ] Browser extension version

## License

MIT License — see [LICENSE](LICENSE) for details.
