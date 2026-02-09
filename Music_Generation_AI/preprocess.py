"""
preprocess.py
This script handles loading MIDI files and extracting musical notes/chords.
I'm using music21 library which makes working with MIDI pretty straightforward.
"""

import os
import pickle
from music21 import converter, note, chord
import numpy as np


def load_midi_files(data_dir='data/midi_files'):
    """
    Load all MIDI files from the data directory.
    Returns a list of parsed music21 streams.
    """
    songs = []
    print(f"Loading MIDI files from {data_dir}...")

    midi_files = [f for f in os.listdir(data_dir)
                  if f.endswith('.mid') or f.endswith('.midi')]

    if not midi_files:
        print("Warning: No MIDI files found!")
        return []

    for file in midi_files:
        try:
            filepath = os.path.join(data_dir, file)
            print(f"  Loading: {file}")
            song = converter.parse(filepath)
            songs.append(song)
        except Exception as e:
            print(f"  Error loading {file}: {e}")

    print(f"Successfully loaded {len(songs)} MIDI files.\n")
    return songs


def extract_notes(songs):
    """
    Extract notes and chords from the parsed MIDI files.
    Uses a flattened stream to support most MIDI formats.
    """
    notes = []
    print("Extracting notes and chords from songs...")

    for song in songs:
        for element in song.recurse():
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    print(f"Extracted {len(notes)} notes/chords.")
    print(f"Unique notes/chords: {len(set(notes))}\n")
    return notes


def prepare_sequences(notes, sequence_length=50):
    """
    Convert notes into input-output sequences for LSTM training.
    """
    pitchnames = sorted(set(notes))
    note_to_int = {note: number for number, note in enumerate(pitchnames)}

    network_input = []
    network_output = []

    for i in range(len(notes) - sequence_length):
        seq_in = notes[i:i + sequence_length]
        seq_out = notes[i + sequence_length]

        network_input.append([note_to_int[n] for n in seq_in])
        network_output.append(note_to_int[seq_out])

    n_patterns = len(network_input)
    n_vocab = len(pitchnames)

    # Convert to NumPy arrays (CRITICAL FIX)
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    network_input = network_input / float(n_vocab)
    network_output = np.array(network_output)

    print(f"Created {n_patterns} training sequences.")
    print(f"Vocabulary size: {n_vocab}\n")

    return network_input, network_output, pitchnames


def save_data(notes, pitchnames):
    """Save notes and vocabulary for later music generation."""
    os.makedirs('models', exist_ok=True)

    with open('models/notes.pkl', 'wb') as f:
        pickle.dump(notes, f)

    with open('models/notes_vocab.pkl', 'wb') as f:
        pickle.dump(pitchnames, f)

    print("Saved notes and vocabulary.\n")


if __name__ == "__main__":
    print("=" * 50)
    print("MIDI Preprocessing Pipeline")
    print("=" * 50 + "\n")

    songs = load_midi_files()
    if not songs:
        exit()

    notes = extract_notes(songs)

    network_input, network_output, pitchnames = prepare_sequences(notes)

    save_data(notes, pitchnames)

    print("Preprocessing complete!")
    print(f"Input shape: {network_input.shape}")
    print(f"Output length: {len(network_output)}")
