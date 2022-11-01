from lib2to3.pgen2 import token
from tabnanny import check
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from pathlib import Path

import tensorflow as tf
import datasets as ds
import pandas as pd
import math

import ec_model as data

dataset = ds.load_dataset('go_emotions', 'simplified')

def generate_split(split):
    text = dataset[split].to_pandas()['text'].to_list()
    labels = [int(a[0]) for a in dataset[split].to_pandas()['labels'].to_list()]
    return (text, labels)

(x_text, x_labels) = generate_split('train')
(y_text, y_labels) = generate_split('test')

tokenizer = AutoTokenizer.from_pretrained(data.checkpoint)

def generate_dataset(text, labels):
    tokenized_text = tokenizer(text, padding=True, truncation=True)
    return tf.data.Dataset.from_tensor_slices((
        dict(tokenized_text),
        labels
    ))

x_dataset = generate_dataset(x_text, x_labels)
y_dataset = generate_dataset(y_text, y_labels)

model = TFAutoModelForSequenceClassification.from_pretrained(data.checkpoint, num_labels=28)

if Path(f'{data.weights_path}checkpoint').is_file():
    model.load_weights(data.weights_path)
    print(f'Loaded model weights from {data.weights_path}')

class SaveWeights(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        model.save_weights(data.weights_path)
        print(f'Saved weights for epoch {epoch} at {data.weights_path}')

opt = tf.keras.optimizers.Adam(learning_rate=5e-5)

model.compile(
    optimizer=opt,
    loss=model.hf_compute_loss,
    metrics=['accuracy']
)

model.fit(
    x_dataset.shuffle(1000).batch(data.batch_size),
    validation_data=y_dataset.shuffle(1000).batch(data.batch_size),
    batch_size=data.batch_size,
    epochs=data.num_epochs,
    callbacks=[SaveWeights()]
)