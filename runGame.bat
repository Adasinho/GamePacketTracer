@echo off

: Edit here server ip
SET server_ip=0.0.0.0

: Edit application to run
SET game_path=game.exe
SET game_arguments=-arg1 -arg2

: Set other directories if you want
SET packets_log_path=pcap_logs
SET ping_log_path=ping_logs

SET ping_watcher_path=pingWatcher.exe
SET packet_watcher_path=packetWatcher.exe

start "" "%game_path%" %game_arguments%
start "" "%ping_watcher_path%" --address %server_ip% --logPath %ping_log_path%
start "" "%packet_watcher_path%" --address %server_ip% --logPath %packets_log_path%

:loop
timeout /t 5 >nul
tasklist | find /i "%game_path%" >nul
if errorlevel 1 goto end
goto loop

:end
taskkill /IM %packet_watcher_path%
taskkill /IM %ping_watcher_path%