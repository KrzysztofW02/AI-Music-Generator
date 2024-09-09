import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

model_file_path = 'models/music_generation_model.h5'

def crate_model(sequence_length):
    model = Sequential()
    model.add(LSTM(128, input_shape=(sequence_length, 1), return_sequences=True))
    model.add(LSTM(128))
    model.add(Dense(1, activation = 'linear'))
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
