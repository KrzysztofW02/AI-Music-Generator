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

    for i, chord in enumerate(notes):
        start_time = i * 0.5 + np.random.uniform(-0.03, 0.03)
        duration = 0.5 + np.random.uniform(-0.05, 0.05)
        velocity = np.random.randint(80, 110)
        
        for note in chord:
            midi_note = pretty_midi.Note(
                velocity=velocity,
                pitch=int(note),
                start=start_time,
                end=start_time + duration
            )
            instrument.notes.append(midi_note)

    midi.instruments.append(instrument)
    midi.write(output_file)
    print(f'MIDI file saved to {output_file} with instrument: {instrument_name}')


