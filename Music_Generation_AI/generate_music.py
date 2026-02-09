"""
generate_music.py
This script uses the trained model to generate new music.
It starts with a random seed sequence and predicts future notes.
"""

import os
import pickle
import numpy as np
from music21 import instrument, note, chord, stream, tempo
from tensorflow.keras.models import load_model


def load_model_and_vocab():
    """Load the trained model and vocabulary."""
    print("Loading trained model and vocabulary...")

    model = load_model('models/music_model.h5')

    with open('models/notes_vocab.pkl', 'rb') as f:
        pitchnames = pickle.load(f)

    print(f"Model loaded. Vocabulary size: {len(pitchnames)}\n")
    return model, pitchnames


def prepare_seed_sequence(notes, pitchnames, sequence_length=50):
    """Pick a random starting sequence from training data."""
    note_to_int = {note: number for number, note in enumerate(pitchnames)}

    start = np.random.randint(0, len(notes) - sequence_length - 1)
    seed_sequence = notes[start:start + sequence_length]

    pattern = [note_to_int[n] for n in seed_sequence]
    return pattern


def sample_with_temperature(prediction, temperature=0.8):
    """Apply temperature sampling to add controlled randomness."""
    prediction = np.asarray(prediction).astype('float64')
    prediction = np.log(prediction + 1e-9) / temperature
    exp_preds = np.exp(prediction)
    prediction = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(prediction), p=prediction)


def generate_notes(model, pattern, pitchnames, n_vocab, num_notes=400):
    """Generate a sequence of notes using the trained model."""
    int_to_note = {number: note for number, note in enumerate(pitchnames)}
    prediction_output = []

    print(f"Generating {num_notes} notes...")

    for i in range(num_notes):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)[0]
      # Gradually vary creativity to avoid repetition
        dynamic_temperature = 0.7 + (i % 100) / 300
        index = sample_with_temperature(prediction, temperature=dynamic_temperature)


        result = int_to_note[index]
        prediction_output.append(result)

        pattern.append(index)
        pattern = pattern[1:]

        if (i + 1) % 100 == 0:
            print(f"  Generated {i + 1}/{num_notes} notes...")

    print("Note generation complete!\n")
    return prediction_output


def create_midi(prediction_output, output_file='output/generated_music.mid'):
    """Convert generated notes into a MIDI file."""
    print("Creating MIDI file...")

    os.makedirs('output', exist_ok=True)

    midi_stream = stream.Stream()
    midi_stream.append(tempo.MetronomeMark(number=100))  # faster tempo

    offset = 0.0

    for pattern in prediction_output:
        if pattern is None or pattern == "":
            continue

        try:
            if '.' in pattern:
                notes_in_chord = pattern.split('.')
                chord_notes = []

                for n in notes_in_chord:
                    new_note = note.Note(int(n))
                    new_note.storedInstrument = instrument.Piano()
                    chord_notes.append(new_note)

                new_chord = chord.Chord(chord_notes)
                new_chord.offset = offset
                midi_stream.append(new_chord)
            else:
                new_note = note.Note(pattern)
                new_note.offset = offset
                new_note.storedInstrument = instrument.Piano()
                midi_stream.append(new_note)

            offset += 0.5  # PERFECT timing

        except Exception:
            continue

    midi_stream.write('midi', fp=output_file)
    print(f"MIDI file saved to: {output_file}\n")

    return output_file


def generate_music(num_notes=400, output_file='output/generated_music.mid'):
    """Main function to generate music."""
    print("=" * 50)
    print("AI Music Generation")
    print("=" * 50 + "\n")

    model, pitchnames = load_model_and_vocab()
    n_vocab = len(pitchnames)

    with open('models/notes.pkl', 'rb') as f:
        notes = pickle.load(f)

    pattern = prepare_seed_sequence(notes, pitchnames)
    prediction_output = generate_notes(model, pattern, pitchnames, n_vocab, num_notes)

    output_path = create_midi(prediction_output, output_file)

    print("=" * 50)
    print("Music generation complete!")
    print("=" * 50)

    return output_path


if __name__ == "__main__":
    generate_music(num_notes=400)
