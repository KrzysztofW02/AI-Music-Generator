import pickle
import numpy as np
from model_training import create_model, train_model, save_model

data_path = r"lmd_full\processed_midi_data.pkl"

with open(data_path, 'rb') as f:
    inputs, targets = pickle.load(f)

inputs = np.expand_dims(inputs, axis=-1)

model = create_model(sequence_length=50)
train_model(model, inputs, targets, epochs=20)

save_model(model, 'models/music_generation_model.h5')
