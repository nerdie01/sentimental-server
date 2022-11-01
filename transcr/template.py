from pyannote.audio import Pipeline

import record as r, diarization as d, transcription as t

diarization = d.Diarization()
diarization.diarize()

transcription = t.Transcription()
transcription.transcribe_to_dict()

print(transcription.stringify())