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
WIP = '0.0.0.0'
DISCONNECT = '$$DISCONNECT'
CLOSE = '$$CLOSE'

FNAME = 'audio'
FFORMAT = 'caf'

import record as r, diarization as d, transcription as t

stec_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stec_client.connect((IP, PORT))

print(f'Successfully connected to STEC socket at ███.███.██.██:{PORT}.')

def send_to_stec(msg):
    message = msg.encode(FORMAT)
    length = len(message)
    send_length = str(length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    stec_client.send(send_length)
    stec_client.send(message)
    if msg == DISCONNECT or msg == CLOSE:
        sys.exit()

async def echo(websocket):
    b64encodeMode = False
    decodedBytes = b''
    async for message in websocket:
        if message == '$$B64START':
            b64encodeMode = True
            continue

        if not b64encodeMode:
            print('Recieved manual-input message from ██.██.██.███')
            output = message

        if message == '$$B64END':
            with open(f'{FNAME}.{FFORMAT}', 'wb') as f:
                print(f'Recieved message from ██.██.██.███')
                f.write(decodedBytes)
            f.close()

            decodedBytes = b''

            sound = AudioSegment.from_file(f'{FNAME}.{FFORMAT}', format=FFORMAT)
            sound.export(f'{r.PATH}{r.FNAME}', format='wav')

            diarization = d.Diarization()
            diarization.diarize()

            transcription = t.Transcription()
            transcription.transcribe_to_dict()

            output = transcription.stringify()

            print(output)
            b64encodeMode = False

        if b64encodeMode:
            decodedBytes += base64.b64decode(message)
            continue

        else:
            send_to_stec(output)

            sm_length = stec_client.recv(HEADER)
            sm = stec_client.recv(int(sm_length)).decode(FORMAT)

            ec_length = stec_client.recv(HEADER)
            ec = stec_client.recv(int(ec_length)).decode(FORMAT)

            print(sm)
            print(ec)

            await websocket.send(f'{output}&&{sm}&&{ec}')

start = websockets.serve(echo, WIP, WPORT)
print(f'Started websockets server at ██.██.██.███:{WPORT}.')

asyncio.get_event_loop().run_until_complete(start)
asyncio.get_event_loop().run_forever()