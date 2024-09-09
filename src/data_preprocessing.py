import pickle
import numpy as np

data_path = r"lmd_full\processed_midi_data.pkl" 

def load_midi_data(data_path):
    with open(data_path, 'rb') as f:
        all_midi_notes = []
        while True:
            try:
                chunk = pickle.load(f)
                all_midi_notes.extend(chunk)
            except EOFError:
                break
    return all_midi_notes

def preprocess_data(all_midi_notes, sequence_length=50):
    inputs = []
    targets = []
    
    for song in all_midi_notes:
        pitches = [note['pitch'] for note in song]

        for i in range(0, len(pitches) - sequence_length):
            inputs.append(pitches[i:i+sequence_length])
            targets.append(pitches[i+sequence_length])

    inputs = np.array(inputs) / 127.0
    targets = np.array(targets) / 127.0

    return inputs, targets

