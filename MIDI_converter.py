import os
import pretty_midi
import pickle

dataset_path = r"lmd_full\lmd_full" 

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

def process_midi_dataset_in_chunks(dataset_path, save_to, chunk_size=100):
    all_midi_notes = []
    file_count = 0

    with open(save_to, 'ab') as f: 
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith('.mid') or file.endswith('.midi'):
                    midi_file_path = os.path.join(root, file)  
                    note_sequence = midi_to_note_sequence(midi_file_path)  

                    if note_sequence:
                        all_midi_notes.append(note_sequence)
                        file_count += 1

                    if file_count >= chunk_size:
                        pickle.dump(all_midi_notes, f)  
                        all_midi_notes = []  
                        file_count = 0
                        print(f"Saved a chunk of {chunk_size} MIDI files to {save_to}")

        if all_midi_notes:
            pickle.dump(all_midi_notes, f)
            print(f"Saved the remaining {len(all_midi_notes)} MIDI files to {save_to}")

save_to = r'processed_midi_data.pkl'

process_midi_dataset_in_chunks(dataset_path, save_to, chunk_size=100)
