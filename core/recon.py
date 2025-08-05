from scapy.all import Ether, IP, TCP, UDP, ARP

def scan_packet(packet):
    data = {}

    if Ether in packet:
        data["src_mac"] = packet[Ether].src
        data["dst_mac"] = packet[Ether].dst

    if ARP in packet:
        data['protocol'] = 'ARP'
        data['src_ip'] = packet[ARP].psrc
        data['dst_ip'] = packet[ARP].pdst
        return data

    if IP in packet:
        data['src_ip'] = packet[IP].src
        data['dst_ip'] = packet[IP].dst

        if TCP in packet:
            data['protocol'] = 'TCP'
            data['src_port'] = packet[TCP].sport
            data['dst_port'] = packet[TCP].dport

        elif UDP in packet:
            data['protocol'] = 'UDP'
            data['src_port'] = packet[UDP].sport
            data['dst_port'] = packet[UDP].dport

        else:
            data['protocol'] = packet[IP].proto  # Safe: Only accessed if IP is present

    return data  # Always return something, even partial
