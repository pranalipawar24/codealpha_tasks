"""
app.py
A simple web interface for the music generation system.
Built with Streamlit because it's quick to set up and looks clean.
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Page config
st.set_page_config(
    page_title="AI Music Generator",
    page_icon="🎵",
    layout="centered"
)

# Title and description
st.title("🎵 AI Music Generator")
st.markdown("---")

st.markdown("""
### About This Project
This is a deep learning system that generates original music using LSTM neural networks.
The model learns patterns from MIDI files and creates new compositions.

**How it works:**
1. The system analyzes musical patterns from training data
2. An LSTM network learns sequences of notes and chords
3. The model generates new note sequences based on learned patterns
4. Generated sequences are converted back into playable MIDI files

**Tech Stack:** Python, TensorFlow/Keras, music21, Streamlit
""")

st.markdown("---")

# Check if model exists
model_exists = os.path.exists('models/music_model.h5')
vocab_exists = os.path.exists('models/notes_vocab.pkl')

if not model_exists or not vocab_exists:
    st.warning("⚠️ Model not found! Please train the model first.")
    st.info("""
    **Training Instructions:**
    1. Add MIDI files to `data/midi_files/` folder
    2. Run: `python train_model.py`
    3. Wait for training to complete
    4. Come back here to generate music!
    """)
else:
    st.success("✅ Model loaded and ready!")
    
    # Generation settings
    st.markdown("### Generation Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_notes = st.slider(
            "Number of notes to generate",
            min_value=100,
            max_value=1000,
            value=500,
            step=50,
            help="More notes = longer music piece"
        )
    
    with col2:
        output_name = st.text_input(
            "Output filename",
            value="generated_music.mid",
            help="Name for the generated MIDI file"
        )
    
    st.markdown("---")
    
    # Generate button
    if st.button("🎼 Generate Music", type="primary", use_container_width=True):
        
        with st.spinner("🎵 Generating music... This may take a minute..."):
            try:
                # Import and run generation
                from generate_music import generate_music
                
                output_path = f"output/{output_name}"
                result_path = generate_music(num_notes=num_notes, output_file=output_path)
                
                st.success("✅ Music generated successfully!")
                
                # Download button
                with open(result_path, 'rb') as file:
                    st.download_button(
                        label="📥 Download MIDI File",
                        data=file,
                        file_name=output_name,
                        mime="audio/midi",
                        use_container_width=True
                    )
                
                st.info(f"💾 File saved to: `{result_path}`")
                
            except Exception as e:
                st.error(f"❌ Error during generation: {str(e)}")
                st.info("Make sure the model is trained properly and all dependencies are installed.")

# Sidebar with info
with st.sidebar:
    st.markdown("### 📊 Project Info")
    
    st.markdown("""
    **Model Architecture:**
    - 3 LSTM layers (256 units each)
    - Dropout layers (0.3) for regularization
    - Softmax output layer
    
    **Training Data:**
    - MIDI files from `data/midi_files/`
    - Extracted notes and chords
    - Sequence length: 50
    
    **Output:**
    - MIDI format
    - Piano instrument
    - Variable length composition
    """)
    
    st.markdown("---")
    
    st.markdown("### 🛠️ Quick Commands")
    st.code("python train_model.py", language="bash")
    st.code("python generate_music.py", language="bash")
    st.code("streamlit run app.py", language="bash")
    
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit")