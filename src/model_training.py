import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Bidirectional, Dense, LSTM

model_file_path = 'models/music_generation_model.h5'


def create_model(sequence_length):
    model = Sequential()
    model.add(Bidirectional(LSTM(128, input_shape=(sequence_length, 1), return_sequences=True)))
    model.add(Bidirectional(LSTM(128)))
    model.add(Dense(128, activation='relu')) 
    model.add(Dense(1, activation='linear'))  
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
    predictions = np.log(predictions) / temperature
    probabilities = tf.nn.softmax(predictions).numpy()

    return np.random.choice(len(probabilities), p=probabilities)

C_major_scale = [60, 62, 64, 65, 67, 69, 71, 72]  

def constrain_to_scale(note, scale):
    closest_note = min(scale, key=lambda x: abs(x - note))  
    return closest_note

def generate_notes(model, seed_sequence, num_notes=100, temperature=1.0):
    generated_notes = []
    current_sequence = seed_sequence

    for _ in range(num_notes):
        prediction = model.predict(current_sequence)[0][0]
        prediction = np.clip(prediction, 0, 127)
        next_note = sample_with_temperature(prediction, temperature=temperature)
        generated_notes.append(next_note)
        next_note = np.reshape(next_note, (1, 1, 1))
        current_sequence = np.append(current_sequence[:, 1:, :], next_note, axis=1)

    return generated_notes





