import pretty_midi

def create_midi_from_notes(notes, output_file='generated_music.mid'):
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)

    for i, note in enumerate(notes):
        midi_note = pretty_midi.Note(
            velocity=100,
            pitch=int(note * 127),
            start = i * 0.5,
            end = (i + 1) * 0.5 
        )
        instrument.notes.append(midi_note)

    midi.instruments.append(instrument)
    midi.write(output_file)
    print(f'MIDI file saved to {output_file}')