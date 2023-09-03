import os
import signal
import subprocess
import time

"""
if __name__ == "__main__":
    # Uruchamianie procesu
    proc1 = subprocess.Popen(["./dist/packetWatcher.exe"])
    proc2 = subprocess.Popen(["./dist/pingWatcher.exe"])

    # ... tutaj możesz czekać lub robić inne rzeczy ...
    time.sleep(5)

    # Wysyłanie sygnału SIGINT do procesu
    os.kill(proc1.pid, signal.SIGINT)

    time.sleep(5)

    os.kill(proc2.pid, signal.SIGINT)

    # Czekanie na zakończenie procesu po wysłaniu sygnału
    proc1.wait()
    proc2.wait()
"""
    
# Lista procesów podtrzymywanych
processes = []

def handle_sigint(sig, frame):
    print("\nOtrzymano sygnał SIGINT. Zamykanie procesów...")
    processes[0].send_signal(signal.CTRL_C_EVENT)
    
    time.sleep(3)
    
    processes[1].send_signal(signal.CTRL_C_EVENT)
    
    #for p in processes:
        #p.send_signal(signal.CTRL_C_EVENT)  # Wysyłanie sygnału CTRL+C do procesu
    #exit(0)

# Rejestracja funkcji obsługi dla sygnału SIGINT
signal.signal(signal.SIGINT, handle_sigint)

# Uruchamianie programów exe
prog1 = subprocess.Popen(["./packetWatcher.exe"])
prog2 = subprocess.Popen(["./pingWatcher.exe"])
prog3 = subprocess.Popen(["./TestMPShooterClient.exe", "139.59.147.201:7777", "-WINDOWED"])

# Dodawanie procesów do listy
processes.extend([prog1, prog2])

# Czekanie na zakończenie procesów (opcjonalnie)
try:
    while True:
        if prog3.poll() is not None:
            print("Gra została zamknięta")
            handle_sigint(None, None)
        
        time.sleep(1)
            
except KeyboardInterrupt:
    handle_sigint(None, None)