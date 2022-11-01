import matplotlib.pyplot as plot

import asyncio
import base64
import socket
import websockets
import json
import sys
import os

from pydub import AudioSegment

HEADER = 64
FORMAT = 'utf-8'
PORT = 25566
WPORT = 25565
IP = '169.254.92.79'
WIP = '192.168.86.28'
DISCONNECT = '$$DISCONNECT'
CLOSE = '$$CLOSE'

FNAME = 'audio'
FFORMAT = 'caf'

import record as r, diarization as d, transcription as t

async def echo(websocket):
    decodedBytes = b''
    async for message in websocket:
        print(message)

start = websockets.serve(echo, WIP, WPORT, max_size=sys.maxsize)
print(f'Started websockets server at {WIP}:{WPORT}.')

asyncio.get_event_loop().run_until_complete(start)
asyncio.get_event_loop().run_forever()