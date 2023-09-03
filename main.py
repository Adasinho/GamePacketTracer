import threading
import signal
import platform
import multiprocessing
import time

from packetWatcher import capture_to_pcap
from pingWatcher import ping_and_log

SERVER_IP = "139.59.147.201"  # Na przykład Google DNS; możesz zmienić na inny adres IP
PACKETS_SAVE_DIRECTORY = "pcap_files"  # Zmień na żądany folder
PINGS_SAVE_DIRECTORY = "pings"

# Tworzenie wątków
#thread1 = threading.Thread(target=ping_and_log, args=(SERVER_IP, PINGS_SAVE_DIRECTORY))
#thread2 = threading.Thread(target=capture_to_pcap, args=(SERVER_IP, PACKETS_SAVE_DIRECTORY))  # Zamień `twoja_druga_funkcja` na nazwę funkcji lub kod drugiego skryptu

#thread1.daemon = True
#thread2.daemon = True

def funkcja1(stop_event):
    while not stop_event.is_set():
        ping_and_log(SERVER_IP, PINGS_SAVE_DIRECTORY)
        print("Proces 1 działa...")
        time.sleep(1)
        
def funkcja2(stop_event):
    while not stop_event.is_set():
        capture_to_pcap(SERVER_IP, PACKETS_SAVE_DIRECTORY)
        print("Proces 2 działa...")
        time.sleep(1)

if __name__ == "__main__":
    stop_event = multiprocessing.Event()
    
    # Utwórz procesy
    #process1 = multiprocessing.Process(target=ping_and_log, args=(SERVER_IP, PINGS_SAVE_DIRECTORY))
    #process2 = multiprocessing.Process(target=capture_to_pcap, args=(SERVER_IP, PACKETS_SAVE_DIRECTORY))
    process1 = multiprocessing.Process(target=funkcja1, args=(stop_event,))
    process2 = multiprocessing.Process(target=funkcja2, args=(stop_event,))

    # uruchom procesy
    process1.start()
    process2.start()

    # Funkcja do zatrzymywania wątków
    #def signal_handler(sig, frame):
    #    print("Zamykanie skryptu...")
    #    exit(0)

    # Funkcja obsługi sygnału
    def signal_handler(sig, frame):
        print("Zamykanie skryptu...")
        
        #process1.terminate()
        #process2.terminate()
        
        stop_event.set()
        
        process1.join()
        process2.join()
        exit(0)

    # Ustawienie sygnału przerwania
    signal.signal(signal.SIGINT, signal_handler)

    # Czekaj na zakończenie procesów (choć w tym przypadku nigdy się to nie stanie)
    process1.join()
    process2.join()

    # Uruchomienie wątków
    #thread1.start()
    #thread2.start()

    # Utrzymuj skrypt w działaniu
    #try:
    #    while True:
    #        pass
    #except KeyboardInterrupt:
    #    pass