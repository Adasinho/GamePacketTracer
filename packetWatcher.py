"""

import subprocess
import time
import re

from scapy.all import sniff, TCP, UDP

class GamePacketTracer:
    def __init__(self):
        self.__connections = []
    
    def check_game_ports(self, process_name):
        try:
            result = subprocess.check_output(f"netstat -abn", shell=True, text=True, stderr=subprocess.STDOUT)
            #print(result)
            lines = result.split('\n')

            for index, line in enumerate(lines):
                if process_name in line:
                    prev_line = lines[index - 1].strip()  # Poprzednia linia zawiera informacje o protokole, adresie IP i porcie
                    combined_line = prev_line + " " + line.strip()  # Połącz obie linie
                    print(combined_line)
                    ports = re.findall(r":(\d+)", combined_line)
                    
                    for port in ports:
                        if port not in self.__connections:
                            self.__connections.append(port)

            return self.__connections

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None
        
    def packet_callback(self, packet):
        # Sprawdzanie, czy pakiet zawiera warstwę TCP lub UDP
        if packet.haslayer(TCP) or packet.haslayer(UDP):
            sport = packet.sport if packet.haslayer(TCP) else packet[UDP].sport
            dport = packet.dport if packet.haslayer(TCP) else packet[UDP].dport
            #print("sport: " + str(sport) + ", dport: " + str(dport))
            for connection in self.__connections:
                if sport == connection or dport == connection:
                    print(packet.summary())
    
    def update(self):
        sniff(prn=self.packet_callback, store=0)

if __name__ == "__main__":
    #process_name = "TestMPShooter.exe"
    process_name = "steam.exe"
    
    packetTracer = GamePacketTracer()
    
    #time.sleep(10)
    connections = packetTracer.check_game_ports(process_name)
    if connections:
        for connection in connections:
            print(connection)
    else:
        print(f"No ports found for the game {process_name}.")
        
    # Możesz dodać filtr do sniff() w celu optymalizacji przechwytywania, ale poniżej przykład bez filtru
    packetTracer.update()

"""

from scapy.all import sniff, IP, wrpcap
from datetime import datetime
import os

save_directory = None
save_file = None

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
    print(f"Przechwytywanie pakietów dla {target_ip}... Naciśnij Ctrl+C, aby zakończyć.")
    sniff(lfilter=filter_packet, store=True, prn=packet_callback)

if __name__ == "__main__":
    #target_ip = "139.59.147.201"  # Zmień na adres IP serwera, który chcesz monitorować
    #print(f"Monitorowanie ruchu w kierunku: {target_ip}")
    #sniff(prn=packet_callback, filter=f"ip host {target_ip}", store=0)
    
    #capture_packets(100, "captured_packets.pcap", f"ip host {target_ip}")
    
    TARGET_IP = "139.59.147.201"
    SAVE_DIRECTORY = "pcap_files"  # Zmień na żądany folder
    capture_to_pcap(TARGET_IP, SAVE_DIRECTORY)
    
