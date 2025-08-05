### DOCUMENTATION.md
```markdown
# NetVision Documentation

## Overview
NetVisionLite is a lightweight network security monitor that combines:
1. High-performance C-based packet sniffer
2. Python-based real-time threat analysis
3. Comprehensive alerting and logging system

## Core Components

### Packet Capture (`sniffer/sniffer.c`)
- Raw socket implementation for maximum performance
- Filters for IP packets (TCP, UDP, ICMP)
- Outputs JSON-formatted packet metadata
- Automatic interface binding

### Threat Detection (`core/detect.py`)
- **Port Scan Detection**: >10 unique ports in 5 seconds
- **Suspicious Port Access**: 4444, 31337, 6667
- **Blacklisted IP Monitoring**: Custom IP blocklist
- **ARP Storm Detection**: Broadcast ARP floods

### Alert Logging (`core/logger.py`)
- Colorized console output
- JSON logfile storage
- Timestamped entries
- Packet metadata preservation

### Helper Utilities (`utils/format.py`)
- Terminal colorization
- Timestamp formatting
- Data size humanization
- Text truncation for cleaner output

## Command Reference
```bash
usage: netvision.py [-h] [-i INTERFACE] [-v] [-t TIMEOUT] [-l LOGFILE] [-f {text,json}]

options:
  -h, --help            show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        Network interface to monitor (default: system default)
  -v, --verbose         Increase verbosity (-v: INFO, -vv: DEBUG)
  -t TIMEOUT, --timeout TIMEOUT
                        Capture duration in seconds (0 = infinite)
  -l LOGFILE, --logfile LOGFILE
                        Alert logfile path (default: netvision.log)
  -f {text,json}, --format {text,json}
                        Alert output format (default: text)
```

## Configuration

### Blacklisted IPs
Edit `core/detect.py`:
```python
BLACKLISTED_IPS = {
    "192.168.1.66",
    "10.0.0.99",
    "172.16.0.15",
    # Add your custom IPs here
}
```

### Suspicious Ports
Edit `core/detect.py`:
```python
SUSPICIOUS_PORTS = {
    4444,    # Metasploit default
    31337,   # Back Orifice
    6667,    # IRC
    1337,    # Elite hacker port
    # Add your custom ports here
}
```

### Alert Thresholds
Adjust detection sensitivity in `core/detect.py`:
```python
# Port scan threshold (ports per second)
PORT_SCAN_THRESHOLD = 10  
SCAN_TIME_WINDOW = timedelta(seconds=5)
```

## Advanced Usage

### Running as Service
```bash
# Create systemd service file
sudo nano /etc/systemd/system/netvision.service

[Unit]
Description=NetVisionLite Network Monitor
After=network.target

[Service]
User=root
ExecStart=/path/to/NetVisionLite/netvision.py -i eth0 -l /var/log/netvision.json
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable netvision
sudo systemctl start netvision
```

### Log Analysis
Use jq to analyze JSON logs:
```bash
# Count alerts by type
jq '.[].alert' data/session.json | sort | uniq -c

# Extract source IPs of alerts
jq '.[] | select(.alert) | .packet.src_ip' data/session.json | sort | uniq
```

### Performance Tuning
For high-traffic networks:
1. Increase sniffer buffer size in `sniffer.c`
2. Adjust kernel network parameters:
```bash
sudo sysctl -w net.core.rmem_max=26214400
sudo sysctl -w net.core.netdev_max_backlog=50000
```

## Troubleshooting

### Common Issues
**Sniffer fails to start:**
- Verify libpcap and libjansson are installed
- Check interface exists with `ip link show`
- Ensure running with root privileges

**No alerts detected:**
- Confirm network traffic exists
- Check detection thresholds
- Run with `-vv` for debug output

**High CPU usage:**
- Reduce verbosity level
- Filter unnecessary traffic in sniffer
- Consider hardware limitations

## Development
```bash
# Set up development environment
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black .
flake8
```
```
