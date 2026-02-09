"""
train_model.py
This script builds and trains an LSTM neural network
to learn musical patterns from MIDI note sequences.
"""

import os
import pickle
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense, Activation
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

from preprocess import load_midi_files, extract_notes, prepare_sequences


def create_model(network_input, n_vocab):
    """
    Build the LSTM neural network.
    """
    print("Building the model...")

    model = Sequential()

    model.add(LSTM(
        256,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        return_sequences=True
    ))
    model.add(Dropout(0.3))

    model.add(LSTM(256, return_sequences=True))
    model.add(Dropout(0.3))

    model.add(LSTM(256))
    model.add(Dropout(0.3))

    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))

    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    model.summary()
    return model


def train(model, network_input, network_output, epochs=20, batch_size=64):
    """
    Train the LSTM model and save the best version.
    """
    os.makedirs('models', exist_ok=True)

    checkpoint = ModelCheckpoint(
        'models/music_model.h5',
        monitor='loss',
        verbose=1,
        save_best_only=True,
        mode='min'
    )

    early_stop = EarlyStopping(
        monitor='loss',
        patience=5,
        verbose=1
    )

    print("\nStarting training...")
    print(f"Epochs: {epochs}, Batch size: {batch_size}\n")

    history = model.fit(
        network_input,
        network_output,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[checkpoint, early_stop],
        shuffle=True,
        verbose=1
    )

    return history


if __name__ == "__main__":
    print("=" * 50)
    print("Music Generation Model Training")
    print("=" * 50 + "\n")

    print("Step 1: Loading data...")
    songs = load_midi_files()

    if not songs:
        print("No MIDI files found. Exiting.")
        exit()

    print("\nStep 2: Extracting notes...")
    notes = extract_notes(songs)

    print("\nStep 3: Preparing sequences...")
    network_input, network_output, pitchnames = prepare_sequences(notes)

    with open('models/notes_vocab.pkl', 'wb') as f:
        pickle.dump(pitchnames, f)

    n_vocab = len(pitchnames)

    print("\nStep 4: Building model...")
    model = create_model(network_input, n_vocab)

    print("\nStep 5: Training model...")
    train(model, network_input, network_output, epochs=20, batch_size=64)

    print("\n" + "=" * 50)
    print("Training complete! Model saved to models/music_model.h5")
    print("=" * 50)
