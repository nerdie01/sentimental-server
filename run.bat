@echo off
start cmd /k call bin/stec.bat
echo first file opened 
echo websocket will start in ten seconds
echo.
timeout /t 10
start cmd /k call bin/transcr.bat