@echo off
cd transcr
call conda activate spbclient
python server.py
pause