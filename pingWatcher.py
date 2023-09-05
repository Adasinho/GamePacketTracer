import subprocess
import time
import platform
import os
import argparse
import signal
from datetime import datetime

def handler(signum, frame):
    print("Zatrzymanie pingowania")
    exit(0)

def get_os_type():
    os_name = platform.system()
    if os_name == "Linux":
        return "Linux"
    elif os_name == "Windows":
        return "Windows"
    else:
        return "Other"

def ping_and_log(server_ip, save_directory):
    
    # Generuj unikalną nazwę pliku na podstawie aktualnej daty i czasu
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    save_file = f"{save_directory}/ping_history_{timestamp}.txt"
    
    # Sprawdź, czy folder istnieje; jeśli nie, utwórz go
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    while True:
        result = None
        
        os_type = get_os_type()
        if os_type == "Linux":
            # Polecenia dla Linuxa
            # Wykonaj ping i przechwytaj wynik
            result = subprocess.run(["ping", "-c", "1", server_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        elif os_type == "Windows":
            # Polecenia dla Windows
            # Wykonaj ping i przechwytaj wynik
            result = subprocess.run(["ping", "-n", "1", server_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            # Dla innych systemów operacyjnych
            print("Nieobsługiwany system")
            return
        
        # Ekstraktuj czas odpowiedzi
        response_time = None
        for line in result.stdout.splitlines():
            if "time=" in line:
                response_time = line.split("time=")[1].split()[0]  # format "time=XX.X ms"

        # Zapisz do pliku z datą i czasem
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(save_file, 'a') as log_file:
            if response_time:
                log_file.write(f"{timestamp} - {response_time}\n")
            else:
                log_file.write(f"{timestamp} - Brak odpowiedzi\n")

        # Czekaj sekundę przed następnym pingiem
        time.sleep(1)

signal.signal(signal.SIGINT, handler)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skrypt zbierający pakiety pod danym adresem IP")
    parser.add_argument("--address", type=str, required=True, help="IP address")
    parser.add_argument("--logPath", type=str, required=True, help="Logs location")
    
    args = parser.parse_args()
    
    # SERVER_IP = "139.59.147.201"  # Na przykład Google DNS; możesz zmienić na inny adres IP
    # SAVE_DIRECTORY = "pings"
    
    print("Rozpoczęcie pingowania adresu:", args.address, "... Naciśnij Ctrl+C, aby zakończyć.")
    
    ping_and_log(args.address, args.logPath)
