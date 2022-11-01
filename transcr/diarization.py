from pyannote.audio import Pipeline
from scipy.io import wavfile

import glob
import os

import record as r

class Diarization:
    def __init__(self):
        self.pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token='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')
        self.audio = f'{r.PATH}{r.FNAME}'

    def print_timestamps(self):
        diarization = self.pipeline(self.audio)
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
    
    def diarize(self):
        for filename in glob.glob(f'{r.SPATH}*'):
            os.remove(filename)

        diarization = self.pipeline(self.audio,  max_speakers=2)

        diarization_dict = {'speaker':[], 'timestamps':[]}
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            diarization_dict['speaker'].append(speaker)
            diarization_dict['timestamps'].append((turn.start, turn.end))

        for i, (start, end) in enumerate(diarization_dict['timestamps']):
            start = int(start * r.RATE)
            end = int(end * r.RATE)
            rate, data = wavfile.read(self.audio)
            wavfile.write(f'{r.SPATH}{i}-{diarization_dict["speaker"][i]}.wav', rate, data[start:end])
        
        return diarization_dict