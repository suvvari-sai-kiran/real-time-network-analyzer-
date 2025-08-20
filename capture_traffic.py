from scapy.all import sniff, IP, get_if_list
import mysql.connector
from datetime import datetime
import socket
import subprocess

INTERFACE = "Wi-Fi"  # Change as per your system (use get_if_list() to see available ones)

# Optional: Map protocol numbers to names
protocol_map = {
    1: "ICMP",
    6: "TCP",
    17: "UDP",
    2: "IGMP",
    89: "OSPF"
}


# --- Function to insert captured data into MySQL ---
def insert_to_db(timestamp, src_ip, dst_ip, protocol, length, src_hostname):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="SAIKIRAN",
            database="network_logs"
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO traffic_logs (timestamp, src_ip, src_hostname, dst_ip, protocol, length)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (timestamp, src_ip, src_hostname, dst_ip, protocol, length))
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        print("❌ DB Error:", err)


# --- Try to get hostname using nbtscan (for Windows devices in LAN) ---
def try_nbtscan(ip):
    try:
        output = subprocess.check_output(['nbtscan', ip], stderr=subprocess.DEVNULL, timeout=2)
        lines = output.decode().split('\n')
        for line in lines:
            if ip in line and '<' in line:
                parts = line.split()
                if len(parts) >= 2:
                    return parts[1]  # Hostname from nbtscan
        return None
    except Exception:
        return None


# --- Master hostname resolution function ---
def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return try_nbtscan(ip) or "Unknown"


# --- Packet handler function ---
def process_packet(packet):
    if IP in packet:
        ip_layer = packet[IP]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        protocol_num = ip_layer.proto
        length = len(packet)

        # Convert protocol number to readable name
        protocol = protocol_map.get(protocol_num, str(protocol_num))

        src_hostname = get_hostname(src_ip)

        print(f"📦 {src_ip} ({src_hostname}) → {dst_ip} | {protocol} | {length} bytes")
        insert_to_db(timestamp, src_ip, dst_ip, protocol, length, src_hostname)


# --- Start sniffing ---
if __name__ == "__main__":
    print(f"🚀 Capturing traffic on interface: {INTERFACE} (Press Ctrl+C to stop)")
    try:
        sniff(prn=process_packet, store=False, iface=INTERFACE)
    except Exception as e:
        print(f"❌ Error starting sniffing: {e}")
