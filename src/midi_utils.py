import pretty_midi
import numpy as np

instrument_programs = {
    "Acustic Grand Piano": 0,
    "Electric Guitar": 27,
    "Violin": 40,
    "Trumpet": 56,
    "Flute": 73
}

def create_midi_from_notes(notes, output_file='generated_music.mid', instrument_name="Acoustic Grand Piano"):
    midi = pretty_midi.PrettyMIDI()
    
    program = instrument_programs.get(instrument_name, 0)  
    instrument = pretty_midi.Instrument(program=program)

    for i, note in enumerate(notes):
        midi_note = pretty_midi.Note(
            velocity=100,
            pitch=int(note), 
            start=i * 0.5,
            end=(i + 1) * 0.5
        )
        instrument.notes.append(midi_note)

    midi.instruments.append(instrument)
    midi.write(output_file)
    print(f'MIDI file saved to {output_file} with instrument: {instrument_name}')
