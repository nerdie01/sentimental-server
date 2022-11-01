import os
import speech_recognition

import record as r

class Transcription:
    def __init__(self):
        self.filenames = [f'{r.SPATH}{filename}' for filename in os.listdir(r.SPATH)]
    def transcribe_to_dict(self):
        transcription_dict = {'speaker':[], 'transcription':[]}

        for filename in self.filenames:
            try:
                r = speech_recognition.Recognizer()
                with speech_recognition.AudioFile(filename) as source:
                    audio = r.record(source)
                transcription_dict['transcription'].append(r.recognize_google(audio))
                transcription_dict['speaker'].append(filename.split('-')[1].split('.')[0])

                print(f'Transcribed {filename} successfully.')
            
            except speech_recognition.UnknownValueError:
                print(f'Could not transcribe {filename}! Skipping...')
                continue
        
        self.transcription = transcription_dict
        return transcription_dict

    def stringify(self):
        string = ''
        for i, speaker in enumerate(self.transcription['speaker']):
            string += f'Person {chr(65 + int(speaker[len(speaker)-2:]))}: {self.transcription["transcription"][i]}\n'
        return string