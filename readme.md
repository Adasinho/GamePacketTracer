# Instalacja środowiska

Przygotowanie środowiska wirtualnego
```
python -m venv venv
```

Aktywacja środowiska
```
.\venv\Scripts\activate
```

Instalacja scapy oraz pyinstaller
```
pip install scapy
pip install pyinstaller
```

## Instalacja plików wykonawczych



# Przykład uruchamiania

Opis dostosowania skryptu do poprawnego uruchamiania i śledzenia gry

## Skrypt runGame.bat

Przed pierwszym uruchomieniem należy w skrypcie dostosować zmienne nad którymi są komentarze

```bat
: Edit here server ip
SET server_ip=0.0.0.0

: Edit application to run
SET game_path=game.exe
SET game_arguments=-arg1 -arg2

: Set other directories if you want
SET packets_log_path=pcap_logs
SET ping_log_path=ping_logs
```

## Ręczne wywołanie poszczególnych skryptów

packetWatcher.py
```
python packetWatcher.py --address <ip_address> --logPath <log_path>
```

pingWatcher.py
```
pingWatcher.py --address <ip_address> --logPath <log_path>
```

