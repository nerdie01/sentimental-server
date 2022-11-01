from pathlib import Path
from transformers import AutoTokenizer, BartForConditionalGeneration, pipeline
import tensorflow as tf
import math

import base_model

checkpoint = 'philschmid/bart-large-cnn-samsum'

class Summarizer(base_model.BasicModel):
    def load_model(self):
        self.model = BartForConditionalGeneration.from_pretrained(checkpoint)
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    
    def predict(self, text):
        tokenized_text = self.tokenizer.tokenize(text)

        summarizer = pipeline(
            "summarization",
            min_length=int(len(tokenized_text)/2),
            max_length=int(len(tokenized_text)),
            model=self.model,
            tokenizer=self.tokenizer
        )

        return summarizer(text)[0]['summary_text']