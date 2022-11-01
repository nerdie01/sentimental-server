from pathlib import Path
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, DataCollatorWithPadding
import tensorflow as tf
import math

import base_model

checkpoint = 'distilbert-base-uncased'
weights_path = 'ec_weights/'

batch_size = 16
num_epochs = 5

_labels = [
    'admiration',
    'amusement',
    'anger',
    'annoyance',
    'approval',
    'caring',
    'confusion',
    'curiosity',
    'desire',
    'disappointment',
    'disagreement',
    'disgust',
    'embarrassment',
    'excitement',
    'fear',
    'gratitude',
    'grief',
    'joy',
    'love',
    'nervousness',
    'optimism',
    'pride',
    'realization',
    'relief',
    'remorse',
    'sadness',
    'surprise',
    'neutral',
]

class EmotionClassifier(base_model.BasicModel):
    def load_model(self):
        '''Loads the model into an EmotionClassifier class object.'''
        self.model = TFAutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=28)
        if Path(f'{weights_path}checkpoint').is_file():
            self.model.load_weights(weights_path)

            opt = tf.keras.optimizers.Adam(learning_rate=5e-5)
            self.model.compile(
                optimizer=opt,
                loss=self.model.hf_compute_loss,
                metrics=['accuracy']
            )
            print(f'Loaded model weights from {weights_path}')
            return True
        print("Model could not be loaded! Make sure ec_train.py is present in the project file and not altered.")
        return False
    
    def predict(self, text):
        '''Returns a dictionary containing emotional states and their likelihood of being associated with the text.'''
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)

        prediction = tokenizer.encode(text,
            truncation=True,
            padding=True,
            return_tensors='tf'
        )

        probabilities = [(1 / (1 + math.exp(-i))) for i in self.model.predict(prediction)[0][0].tolist()]
        return dict(map(lambda x,y : (x,y), _labels, probabilities))