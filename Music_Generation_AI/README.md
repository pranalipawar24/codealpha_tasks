# 🎵 AI Music Generation System

An AI-powered music generation system that uses LSTM neural networks to create original musical compositions. This project was developed as part of my internship to explore the intersection of deep learning and creative AI.

## 📖 Overview

This system learns musical patterns from MIDI files and generates new, original compositions. It uses a deep LSTM (Long Short-Term Memory) network to understand sequences of notes and chords, then creates novel musical pieces based on learned patterns.

## 🧠 How It Works

### The AI Model

The system uses **LSTM (Long Short-Term Memory)** networks, a type of Recurrent Neural Network (RNN) that's particularly good at learning sequential patterns. Here's why LSTM works well for music:

1. **Sequential Learning**: Music is inherently sequential - each note depends on what came before it. LSTMs are designed to remember patterns over time.

2. **Memory Cells**: Unlike simple neural networks, LSTMs have "memory" that helps them understand long-term dependencies in music (like themes that repeat after many measures).

3. **Pattern Recognition**: The model learns:
   - Which notes commonly follow others
   - Chord progressions
   - Rhythmic patterns
   - Musical structure

### Training Process

1. **Data Preparation**:
   - Load MIDI files from the dataset
   - Extract notes and chords using music21 library
   - Create sequences of 50 notes (input) with the next note as output

2. **Model Architecture**:
```
   Input (50 notes)
      ↓
   LSTM Layer (256 units) + Dropout (0.3)
      ↓
   LSTM Layer (256 units) + Dropout (0.3)
      ↓
   LSTM Layer (256 units) + Dropout (0.3)
      ↓
   Dense Layer (softmax activation)
      ↓
   Output (predicted next note)
```

3. **Training**:
   - The model learns by trying to predict the next note in sequences
   - It adjusts its internal weights to minimize prediction errors
   - Dropout layers prevent overfitting (memorizing instead of learning)

4. **Generation**:
   - Start with a random sequence from training data
   - Predict the next note
   - Add predicted note to sequence
   - Repeat to generate full composition

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- At least 4GB RAM (8GB recommended)
- Some MIDI files for training

### Installation

1. **Clone or download this project**

2. **Create a virtual environment** (recommended):
```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
```

3. **Install dependencies**:
```bash
   pip install -r requirements.txt
```

### Prepare Training Data

1. Collect MIDI files (royalty-free sources):
   - [Classical Piano MIDI](http://www.piano-midi.de/)
   - [Free MIDI Database](https://freemidi.org/)
   - Your own MIDI files

2. Place MIDI files in the `data/midi_files/` folder
   - Aim for at least 15-20 MIDI files
   - More data = better results

### Training the Model

Run the training script:
```bash
python train_model.py
```

This will:
- Load and process your MIDI files
- Extract notes and chords
- Build the LSTM model
- Train for 50 epochs (takes 30-60 minutes depending on your hardware)
- Save the trained model to `models/music_model.h5`

**Note**: Training can take a while! On a decent laptop, expect 30-60 minutes. You'll see progress updates as it trains.

### Generating Music

**Option 1 - Web Interface** (Recommended):
```bash
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

**Option 2 - Command Line**:
```bash
python generate_music.py
```

Generated music will be saved to `output/generated_music.mid`

## 📊 Project Structure
```
Music_Generation_AI/
│
├── data/
│   └── midi_files/          # Your training MIDI files go here
│
├── output/
│   └── generated_music.mid  # Generated music is saved here
│
├── models/
│   ├── music_model.h5       # Trained model weights
│   └── notes_vocab.pkl      # Vocabulary of notes/chords
│
├── preprocess.py            # Data preprocessing (MIDI → notes)
├── train_model.py           # Model training pipeline
├── generate_music.py        # Music generation script
├── app.py                   # Streamlit web interface
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🎓 Technical Concepts Explained

### Why LSTM Instead of Simple RNN?

Simple RNNs suffer from the "vanishing gradient problem" - they forget long-term patterns. LSTMs solve this with:
- **Forget Gate**: Decides what to forget from previous notes
- **Input Gate**: Decides what new information to store
- **Output Gate**: Decides what to output based on current state

### Sequence Length (Why 50?)

We use sequences of 50 notes because:
- Long enough to capture musical phrases (typically 2-4 measures)
- Short enough to train efficiently
- Based on experimentation - you can adjust this!

### Dropout (Why 0.3?)

Dropout randomly "turns off" 30% of neurons during training:
- Prevents the model from memorizing the training data
- Forces it to learn robust, generalizable patterns
- 0.3 is a common value that works well

### Softmax Activation

The output layer uses softmax because:
- Converts raw scores into probabilities
- Each possible note gets a probability
- We pick the most likely next note

## 🎨 Customization Ideas

### Adjust Generation Parameters

In `generate_music.py`:
```python
# Generate longer pieces
generate_music(num_notes=1000)

# Generate shorter pieces
generate_music(num_notes=200)
```

### Modify Model Architecture

In `train_model.py`:
```python
# More complex model (may need more training data)
model.add(LSTM(512, return_sequences=True))

# Simpler model (faster training)
model.add(LSTM(128, return_sequences=True))
```

### Different Training Approaches
```python
# More epochs for better learning (if you have time)
train(model, network_input, network_output, epochs=100)

# Larger batch size for faster training
train(model, network_input, network_output, batch_size=128)
```

## 🐛 Troubleshooting

### "No MIDI files found"
- Make sure MIDI files are in `data/midi_files/`
- Check file extensions (.mid or .midi)

### "Model not found"
- Run `train_model.py` first
- Check that `models/music_model.h5` exists

### Training is too slow
- Reduce number of epochs (try 30 instead of 50)
- Use fewer MIDI files for initial testing
- Consider using Google Colab for free GPU access

### Generated music sounds random
- Train with more MIDI files (aim for 30+)
- Train for more epochs
- Use MIDI files with similar style/genre

## 🔮 Future Improvements

Some ideas I'd like to explore:

1. **Multi-Instrument Support**: Currently only piano, could add other instruments

2. **Style Transfer**: Train different models on different genres, let users pick style

3. **Rhythm Control**: Add explicit rhythm/tempo control instead of fixed 0.5 offset

4. **Conditional Generation**: Allow users to specify key, tempo, or mood

5. **GAN-Based Approach**: Experiment with Generative Adversarial Networks for more variety

6. **Real-Time Generation**: Stream notes as they're generated instead of batch processing

7. **Interactive Composition**: Let users provide a starting melody

## 📚 Learning Resources

If you want to learn more about the concepts used:

- **LSTMs**: [Understanding LSTM Networks](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- **Music Theory**: [musictheory.net](https://www.musictheory.net/)
- **music21**: [Official Documentation](https://web.mit.edu/music21/doc/)
- **TensorFlow**: [TensorFlow Tutorials](https://www.tensorflow.org/tutorials)

## 🙏 Acknowledgments

- **music21** library for making MIDI processing accessible
- **TensorFlow** team for the excellent deep learning framework
- Various online tutorials and papers that inspired this project
- The open-source community for MIDI datasets

## 📝 License

This project is open source and available for educational purposes. Feel free to use, modify, and learn from it!

## 💬 Questions?

If you're having trouble or want to discuss the project:
- Check the troubleshooting section above
- Review the code comments - I tried to explain everything
- Research specific error messages online

---

**Developed as an internship project exploring AI and creative applications**

*Note: This is a learning project. Generated music quality depends heavily on training data quality and quantity.*
