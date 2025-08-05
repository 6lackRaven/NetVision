# NetVision - Lightweight Network Security Monitor

<p align="center">
  <img src="https://i.imgur.com/your_logo.png" alt="NetVisionLite Banner" width="600">
</p>

<p align="center">
  <b>Real-time Network Threat Detection</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0-blue">
  <img src="https://img.shields.io/badge/License-MIT-green">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow">
  <img src="https://img.shields.io/badge/Platform-Linux-lightgrey">
</p>

---

**NetVision** is a lightweight, high-performance network security monitoring tool designed for real-time threat detection. Combining a C-based packet sniffer with Python analysis, it provides immediate identification of suspicious network activity.

Created by **6lackRaven**

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
git clone https://github.com/yourusername/NetVisionLite.git
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

## 🤝 Contributing
Contributions are welcome! Please open an issue first to discuss proposed changes.

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
```
