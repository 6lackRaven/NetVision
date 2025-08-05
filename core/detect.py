from datetime import datetime, timedelta
from collections import defaultdict

port_tracker = defaultdict(list)
BLACKLISTED_IPS = {"192.168.1.66", "10.0.0.99"}
SUSPICIOUS_PORTS = {4444, 31337, 6667}

def analyze_packet(pkt_data):
    alerts = []

    src_ip = pkt_data.get("src_ip")
    dst_port = pkt_data.get("dst_port")
    protocol = pkt_data.get("protocol")

    if src_ip and dst_port:
        now = datetime.now()

        port_tracker[src_ip].append((dst_port, now))
        port_tracker[src_ip] = [
            (port, t) for port, t in port_tracker[src_ip]
            if now - t < timedelta(seconds=5)
        ]

        if len(set(p for p, _ in port_tracker[src_ip])) > 10:
            alerts.append(f"Port scan detected from {src_ip}")

        if dst_port in SUSPICIOUS_PORTS:
            alerts.append(f"Suspicious port access ({dst_port} from {src_ip})")

        if src_ip in BLACKLISTED_IPS:
            alerts.append(f"Blacklisted IP {src_ip} is active")

        if protocol == "ARP" and pkt_data.get("dst_mac") == "ff:ff:ff:ff:ff:ff":
            alerts.append(f"Possible ARP storm from {src_ip}")

    return alerts
