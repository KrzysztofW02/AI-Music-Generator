import os
import pretty_midi
import numpy as np

dataset_path = r"lmd_full\lmd_full"  

def is_valid_midi(file_path):
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            return header == b'MThd'  
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        return False

def midi_to_note_sequence(midi_file_path):
    try:
        midi_data = pretty_midi.PrettyMIDI(midi_file_path)
        notes = []
        for instrument in midi_data.instruments:
            if not instrument.is_drum:
                for note in instrument.notes:
                    notes.append({
                        'start': note.start,
                        'end': note.end,
                        'pitch': note.pitch,
                        'velocity': note.velocity
                    })
        return notes
    except Exception as e:
        print(f"Error processing {midi_file_path}: {e}")
        return None

def process_midi_dataset(dataset_path, save_to):
    all_midi_notes = []
    total_files = 0
    skipped_files = 0
    processed_files = 0

    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.mid') or file.endswith('.midi'):
                total_files += 1
                midi_file_path = os.path.join(root, file)  
                if is_valid_midi(midi_file_path):
                    note_sequence = midi_to_note_sequence(midi_file_path)  
                    if note_sequence:
                        all_midi_notes.append(note_sequence)
                        processed_files += 1
                    else:
                        skipped_files += 1
                        print(f"Skipped (could not process): {midi_file_path}")
                else:
                    skipped_files += 1
                    print(f"Skipping invalid MIDI file: {midi_file_path}")

    np.save(save_to, all_midi_notes)
    print(f"Processed data saved to {save_to}")
    print(f"Total files: {total_files}, Processed files: {processed_files}, Skipped files: {skipped_files}")

save_to = r'processed_midi_data.npy'
process_midi_dataset(dataset_path, save_to)
