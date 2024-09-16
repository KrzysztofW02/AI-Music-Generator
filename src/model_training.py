import numpy as np
import tensorflow as tf
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Bidirectional, Dense, LSTM, Dropout, BatchNormalization

model_file_path = 'models/music_generation_model.h5'

def create_model(sequence_length):
    model = Sequential()
    model.add(Bidirectional(LSTM(256, input_shape=(sequence_length, 1), return_sequences=True)))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(256, return_sequences=True)))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(128)))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(4, activation='linear'))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(model, inputs, targets, epochs=20, batch_size=64):
    history = model.fit(inputs, targets, epochs=epochs, batch_size=batch_size)
    return history

def save_model(model, model_file_path):
    model.save(model_file_path)

def load_model(model_file_path):
    model = tf.keras.models.load_model(model_file_path)
    return model

def sample_with_temperature(predictions, temperature=1.0):
    note = predictions[0][0] 
    note_with_noise = note + np.random.normal(0, temperature * 5) 
    note_with_noise = np.clip(note_with_noise, 0, 127)

    return note_with_noise

C_major_scale = [60, 62, 64, 65, 67, 69, 71, 72]
G_major_scale = [59, 62, 64, 66, 67, 69, 71, 72]
F_major_scale = [60, 62, 63, 65, 67, 69, 70, 72] 

def constrain_to_scale(note):
    chosen_scale = random.choice([C_major_scale, G_major_scale, F_major_scale])
    closest_note = min(chosen_scale, key=lambda x: abs(x - note))
    return closest_note

def generate_notes(model, seed_sequence, num_notes=100, temperature=1.0):
    generated_notes = []
    current_sequence = seed_sequence

    for _ in range(num_notes):
        prediction = model.predict(current_sequence)
        prediction = np.clip(prediction, 0, 127)
        next_note = sample_with_temperature(prediction, temperature=temperature)
        next_note_constrained = constrain_to_scale(next_note)
        generated_notes.append(next_note_constrained)
        next_note_constrained = np.reshape(next_note_constrained, (1, 1, 1))
        current_sequence = np.append(current_sequence[:, 1:, :], next_note_constrained, axis=1)

    return generated_notes





