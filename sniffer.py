from scapy.all import sniff, IP
import mysql.connector
from datetime import datetime

# MySQL connection setup
def insert_packet(timestamp, src_ip, dst_ip, protocol, length):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="SAIKIRAN",
            database="network"
        )
        cursor = conn.cursor()
        query = """
            INSERT INTO traffic_logs (timestamp, src_ip, dst_ip, protocol, length)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (timestamp, src_ip, dst_ip, protocol, length))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Database error:", e)

# Packet handler function
def process_packet(packet):
    if IP in packet:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet.proto
        length = len(packet)

        insert_packet(timestamp, src_ip, dst_ip, protocol, length)
        print(f"Logged: {timestamp} {src_ip} -> {dst_ip} [Proto: {protocol}] Len: {length}")

# Start sniffing (root permission might be required)
print("Starting packet capture...")
sniff(filter="ip", prn=process_packet, store=0)
