import pickle
import numpy as np
from pathlib import Path

data_path = base_dir = Path(__file__).resolve().parent.parent / 'data' / 'processed_midi_data.pkl'
processed_data_path = base_dir = Path(__file__).resolve().parent.parent / 'data' / 'preprocessed_data.pkl'

def load_midi_data(data_path):
    all_midi_notes = []
    with open(data_path, 'rb') as f:
        while True:
            try:
                chunk = pickle.load(f)
                all_midi_notes.extend(chunk)
            except EOFError:
                break
    return all_midi_notes

def preprocess_data_chunked(all_midi_notes, sequence_length=50, chunk_size=1000):
    inputs = []
    targets = []
    
    for song in all_midi_notes:
        pitches = [note['pitch'] for note in song]

        for i in range(0, len(pitches) - sequence_length):
            inputs.append(pitches[i:i+sequence_length])
            targets.append(pitches[i+sequence_length])
        
        if len(inputs) >= chunk_size:
            save_preprocessed_chunk(inputs, targets)
            inputs = []
            targets = []
    
    if inputs:
        save_preprocessed_chunk(inputs, targets)

def save_preprocessed_chunk(inputs, targets):
    with open(processed_data_path, 'ab') as f:
        pickle.dump((inputs, targets), f)
    print("Saved a chunk of preprocessed data")


all_midi_notes = load_midi_data(data_path)

preprocess_data_chunked(all_midi_notes)
