# NetVision - Lightweight Network Security Monitor

<p align="center">
  <b>Real-time Network Threat Detection</b>
</p>

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-v2.1.0-green.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/6lackRaven/NetVision?style=social)](https://github.com/6lackRaven/GhostEyes)

> **Author:** 6lackRaven
> **Status:** Active • Stable • Async-first
> **Docs:** See [`DOCUMENTATION.md`](DOCUMENTATION.md)
---

**NetVision** is a lightweight, high-performance network security monitoring tool designed for real-time threat detection. Combining a C-based packet sniffer with Python analysis, it provides immediate identification of suspicious network activity.

Created by **6lackRaven**

---
## 🚀 Features

- **High-Performance Sniffing**: C-based packet capture for maximum efficiency
- **Real-time Threat Detection**: Port scans, blacklisted IPs, suspicious ports, ARP storms
- **Comprehensive Alerting**: Colorized console output with JSON logging
- **Flexible Monitoring**: Interface selection and capture duration control
- **Minimal Dependencies**: Lightweight and easy to deploy

## 📦 Installation

### Prerequisites
- Linux OS (tested on Ubuntu 20.04+)
- Python 3.8+
- Root privileges for packet capture

```bash
# Install dependencies
sudo apt update
sudo apt install gcc libpcap-dev libjansson-dev python3-pip
```

### Setup
```bash
# Clone repository
git clone https://github.com/6lackRaven/NetVision.git
cd NetVisionLite

# Install Python requirements
pip install -r requirements.txt

# Compile C sniffer (will be done automatically on first run)
cd sniffer
gcc -o sniffer sniffer.c -lpcap -ljansson
cd ..
```

## 🛠 Quick Start

```bash
# Basic monitoring (default interface)
sudo ./netvision.py

# Monitor specific interface
sudo ./netvision.py -i eth0

# Verbose mode (debug output)
sudo ./netvision.py -vv

# Time-limited capture (60 seconds)
sudo ./netvision.py -t 60

# Save alerts to custom logfile
sudo ./netvision.py -l my_alerts.json
```

## 📊 Sample Output
```
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                                                            ▓
▓  ███╗   ██╗███████╗████████╗██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗  ▓
▓  ████╗  ██║██╔════╝╚══██╔══╝██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║  ▓
▓  ██╔██╗ ██║█████╗     ██║   ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║  ▓
▓  ██║╚██╗██║██╔══╝     ██║   ╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║  ▓
▓  ██║ ╚████║███████╗   ██║    ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║  ▓
▓  ╚═╝  ╚═══╝╚══════╝   ╚═╝     ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝  ▓
▓                                                            ▓
▓  »»——⧋ Real-time Network Threat Detection ⧋——««  ▓
▓  »»——⧋ Created by 6lackRaven ⧋——««  ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

[2023-08-05 14:32:15] 📡 Starting C sniffer on eth0
[2023-08-05 14:32:16] [!] Port scan detected from 192.168.1.15
[2023-08-05 14:32:18] [!] Suspicious port access (4444 from 192.168.1.22)
[2023-08-05 14:32:20] [!] Blacklisted IP 10.0.0.99 is active
```

## 📂 Project Structure
```
NetVisionLite/
├── netvision.py          # Main CLI runner
├── sniffer/              # C-based packet capture
│   └── sniffer.c         # Raw packet capture
├── core/                 # Analysis modules
│   ├── recon.py          # Device/protocol discovery
│   ├── detect.py         # Rule-based alerts
│   └── logger.py         # Alert logging
├── utils/                # Helpers
│   └── format.py         # Formatting utilities
├── data/                 # Log storage
│   └── session.json      # Alert logs
├── requirements.txt      # Dependencies
├── LICENSE               # MIT License
└── README.md             # This file
```

---

## ⚠️ Disclaimer

NetVision is intended strictly for authorized security testing and educational use.
By using this tool, you accept full responsibility for your actions.

Only scan targets you own or have explicit written permission to test.

Comply with applicable laws (e.g., CFAA, GDPR).
                                                                                                     The author(s) are not liable for misuse or damage.

                                                                                                                                                                                                          ---

#$ 📜 License

MIT — see the LICENSE file.


---

💬 Contact
                                                                                                     - Author: 6lackRaven
- Email:  harleystanislas.raven@gmail.com
- Telegram: Thereal6lackRaven
- Facebook: Harley Stanislas


---

## 🤝 Contributing
Contributions are welcome! 

1. Fork the repo


2. Create a feature branch: git checkout -b feature/your-feature


3. Commit clean, tested code


4. Open a PR with a clear description



Please follow the established code style & be respectful.


#3 ❤️ Support / Donations

If you’d like to support continued open-source development:
```
- Bitcoin (BTC):   bc1qvc8y7z2jguzr7e3fvwyf09l3me94mqk06nz3hj
- Ethereum (ETH):  0x58bC732d4279321F1E4A8cA57eD2Ad16ed5A2e15
- USDT (ERC20):    0x58bC732d4279321F1E4A8cA57eD2Ad16ed5A2e15
- BNB (BEP20):     0x58bC732d4279321F1E4A8cA57eD2Ad16ed5A2e15
- Solana (SOL):    E7x7ak3H6ob2eHbgsbfgVXpEJyVqMPUFPBtkuEUKj2cq
```
Thank you for supporting independent security tooling 🙏
