from scapy.all import sniff, IP, wrpcap
from datetime import datetime
import os
import argparse
import signal

save_directory = None
save_file = None

def handler(signum, frame):
    print("Zatrzymanie przechwytywania pakietów")
    exit(0)

def packet_callback(pkt):
    wrpcap(save_file, pkt, append=True)
        
def capture_to_pcap(target_ip, save_place):
    global save_directory
    global save_file
    
    save_directory = save_place
    # Funkcja filtrująca pakiety wychodzące/przychodzące z określonego adresu IP
    def filter_packet(packet):
        return packet.haslayer(IP) and (packet[IP].src == target_ip or packet[IP].dst == target_ip)
    
    # Generuj unikalną nazwę pliku na podstawie aktualnej daty i czasu
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    save_file = f"{save_directory}/captured_packets_{timestamp}.pcap"
    
    # Sprawdź, czy folder istnieje; jeśli nie, utwórz go
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Przechwytuj pakiety
    sniff(lfilter=filter_packet, store=True, prn=packet_callback)

signal.signal(signal.SIGINT, handler)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skrypt zbierający pakiety pod danym adresem IP")
    parser.add_argument("--address", type=str, required=True, help="IP address")
    parser.add_argument("--logPath", type=str, required=True, help="Logs location")
    
    args = parser.parse_args()
    
    # TARGET_IP = "139.59.147.201"
    # SAVE_DIRECTORY = "pcap_files"  # Zmień na żądany folder
    
    print(f"Przechwytywanie pakietów dla {args.address}... Naciśnij Ctrl+C, aby zakończyć.")
    
    capture_to_pcap(args.address, args.logPath)
    
