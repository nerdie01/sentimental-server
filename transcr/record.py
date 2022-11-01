import pyaudio
import wave

from diarization import Diarization

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

PATH = 'clips/'
SPATH = 'clips/sliced/'
FNAME = 'clip.wav'

class Recorder:
    def record(time):
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        frames = []

        print('Recording...')
        for i in range(0, int(RATE / CHUNK * time)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(f'{PATH}{FNAME}', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()