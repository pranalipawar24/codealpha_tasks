"""
AI Language Translation Tool
CodeAlpha Internship - Task 1
Author: Pranali Pawar
"""

import streamlit as st
from translatepy import Translator
from translatepy.exceptions import TranslatepyException, UnknownLanguage
from gtts import gTTS
import os
import io
import base64
from datetime import datetime
import time

st.set_page_config(
    page_title="AI Language Translation Tool",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
    }
    .title-text {
        text-align: center;
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .subtitle-text {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .translation-box {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        min-height: 200px;
    }
    .language-selector {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .stButton > button {
        width: 100%;
        background-color: #3498db;
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .feature-button {
        background-color: #2ecc71 !important;
        margin: 0.5rem 0;
    }
    .feature-button:hover {
        background-color: #27ae60 !important;
    }
    .swap-button {
        background-color: #9b59b6 !important;
    }
    .swap-button:hover {
        background-color: #8e44ad !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Translator
@st.cache_resource
def get_translator():
    """Initialize and cache the translator object"""
    try:
        return Translator()
    except Exception as e:
        st.error(f"Failed to initialize translator: {str(e)}")
        return None

def get_languages():
    """Get all supported languages"""
    languages = {
        'auto': 'Auto Detect',
        'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic',
        'hy': 'Armenian', 'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian',
        'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan',
        'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh': 'Chinese',
        'zh-CN': 'Chinese (Simplified)', 'zh-TW': 'Chinese (Traditional)',
        'co': 'Corsican', 'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish',
        'nl': 'Dutch', 'en': 'English', 'eo': 'Esperanto', 'et': 'Estonian',
        'tl': 'Filipino', 'fi': 'Finnish', 'fr': 'French', 'fy': 'Frisian',
        'gl': 'Galician', 'ka': 'Georgian', 'de': 'German', 'el': 'Greek',
        'gu': 'Gujarati', 'ht': 'Haitian Creole', 'ha': 'Hausa', 'haw': 'Hawaiian',
        'he': 'Hebrew', 'hi': 'Hindi', 'hmn': 'Hmong', 'hu': 'Hungarian',
        'is': 'Icelandic', 'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish',
        'it': 'Italian', 'ja': 'Japanese', 'jw': 'Javanese', 'kn': 'Kannada',
        'kk': 'Kazakh', 'km': 'Khmer', 'ko': 'Korean', 'ku': 'Kurdish',
        'ky': 'Kyrgyz', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian',
        'lt': 'Lithuanian', 'lb': 'Luxembourgish', 'mk': 'Macedonian',
        'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese',
        'mi': 'Maori', 'mr': 'Marathi', 'mn': 'Mongolian', 'my': 'Myanmar',
        'ne': 'Nepali', 'no': 'Norwegian', 'ps': 'Pashto', 'fa': 'Persian',
        'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi', 'ro': 'Romanian',
        'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic', 'sr': 'Serbian',
        'st': 'Sesotho', 'sn': 'Shona', 'sd': 'Sindhi', 'si': 'Sinhala',
        'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali', 'es': 'Spanish',
        'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'tg': 'Tajik',
        'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish',
        'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek', 'vi': 'Vietnamese',
        'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba',
        'zu': 'Zulu'
    }
    return languages

def get_language_code(lang_name):
    """Get language code from language name"""
    languages = get_languages()
    for code, name in languages.items():
        if name == lang_name:
            return code
    return 'en'  # Default to English

def translate_text(text, src_lang, dest_lang):
    """Translate text using translatepy"""
    try:
        translator = get_translator()
        if translator is None:
            return None, "Translator initialization failed"
        
        # Handle auto detection
        if src_lang == 'auto':
            # translatepy can auto-detect
            result = translator.translate(text, destination_language=dest_lang)
        else:
            result = translator.translate(text, source_language=src_lang, destination_language=dest_lang)
        
        return result.result, None
    except UnknownLanguage as e:
        return None, f"Unknown language: {str(e)}"
    except TranslatepyException as e:
        return None, f"Translation error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def text_to_speech(text, lang_code):
    """Convert text to speech using gTTS"""
    try:
        # Handle Chinese language codes for gTTS
        if lang_code == 'zh-CN':
            lang_code = 'zh'
        elif lang_code == 'zh-TW':
            lang_code = 'zh-tw'
        
        tts = gTTS(text=text, lang=lang_code, slow=False)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        
        # Create audio player with base64 encoding
        audio_base64 = base64.b64encode(audio_bytes.read()).decode()
        audio_html = f"""
            <audio controls autoplay style="width: 100%;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        """
        return audio_html, None
    except Exception as e:
        return None, str(e)

def copy_to_clipboard(text):
    """Copy text to clipboard using JavaScript"""
    # Escape special characters for JavaScript
    escaped_text = text.replace('`', '\\`').replace('${', '\\${')
    js_code = f"""
    <script>
    function copyToClipboard() {{
        const text = `{escaped_text}`;
        navigator.clipboard.writeText(text).then(() => {{
            // Show success message
            const successDiv = document.createElement('div');
            successDiv.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #4CAF50; color: white; padding: 10px 20px; border-radius: 5px; z-index: 1000;';
            successDiv.textContent = '✅ Text copied to clipboard!';
            document.body.appendChild(successDiv);
            setTimeout(() => successDiv.remove(), 3000);
        }}).catch(err => {{
            console.error('Copy failed:', err);
        }});
    }}
    copyToClipboard();
    </script>
    """
    return js_code

def main():
    # Header section
    st.markdown("<h1 class='title-text'>🌐 AI Language Translation Tool</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle-text'>Translate text between 100+ languages instantly with AI-powered accuracy</p>", unsafe_allow_html=True)
    
    # Initialize session state
    if 'translated_text' not in st.session_state:
        st.session_state.translated_text = ""
    if 'translation_history' not in st.session_state:
        st.session_state.translation_history = []
    if 'source_lang' not in st.session_state:
        st.session_state.source_lang = 'auto'
    if 'target_lang' not in st.session_state:
        st.session_state.target_lang = 'en'
    if 'source_text' not in st.session_state:
        st.session_state.source_text = ""
    
    # Get supported languages
    languages = get_languages()
    language_names = list(languages.values())
    
    # Main translation container
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.markdown("### 📝 Source Text")
            
            # Source text area with session state
            source_text = st.text_area(
                "Enter text to translate:",
                height=200,
                placeholder="Type or paste your text here... (Max 5000 characters)",
                value=st.session_state.source_text,
                max_chars=5000,
                key="source_text_input",
                label_visibility="collapsed"
            )
            st.session_state.source_text = source_text
            
            # Character count
            st.caption(f"Characters: {len(source_text)}/5000")
            
            # Source language selection
            st.markdown("<div class='language-selector'>", unsafe_allow_html=True)
            source_lang_name = st.selectbox(
                "Source Language:",
                options=language_names,
                index=language_names.index(languages[st.session_state.source_lang]),
                key="source_lang_select"
            )
            st.session_state.source_lang = get_language_code(source_lang_name)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            
            # Translate button
            translate_button = st.button("🔄 Translate", 
                                       use_container_width=True, 
                                       type="primary",
                                       key="translate_btn")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Language swap button
            if st.button("⇄ Swap Languages", 
                        use_container_width=True,
                        key="swap_btn",
                        help="Swap source and target languages"):
                # Swap languages
                temp = st.session_state.source_lang
                st.session_state.source_lang = st.session_state.target_lang
                st.session_state.target_lang = temp
                
                # Also swap the text if translation exists
                if st.session_state.translated_text:
                    st.session_state.source_text = st.session_state.translated_text
                    st.session_state.translated_text = ""
                
                st.rerun()
        
        with col3:
            st.markdown("### 🌍 Translated Text")
            
            # Display translation result
            translation_display = st.empty()
            
            if st.session_state.translated_text:
                translation_display.markdown(
                    f"<div class='translation-box'>{st.session_state.translated_text}</div>", 
                    unsafe_allow_html=True
                )
            else:
                translation_display.markdown(
                    "<div class='translation-box' style='color: #7f8c8d; text-align: center; padding: 3rem;'>"
                    "Translation will appear here..."
                    "</div>",
                    unsafe_allow_html=True
                )
            
            # Target language selection
            st.markdown("<div class='language-selector'>", unsafe_allow_html=True)
            target_lang_name = st.selectbox(
                "Target Language:",
                options=[name for name in language_names if name != 'Auto Detect'],
                index=[name for name in language_names if name != 'Auto Detect'].index(
                    languages[st.session_state.target_lang]
                ),
                key="target_lang_select"
            )
            st.session_state.target_lang = get_language_code(target_lang_name)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Handle translation
    if translate_button:
        # Validation
        if not source_text.strip():
            st.markdown("<div class='error-message'>⚠️ Please enter text to translate</div>", unsafe_allow_html=True)
            return
        
        if st.session_state.source_lang != 'auto' and st.session_state.source_lang == st.session_state.target_lang:
            st.markdown("<div class='error-message'>⚠️ Source and target languages are the same</div>", unsafe_allow_html=True)
            return
        
        # Show progress
        with st.spinner('Translating...'):
            time.sleep(0.3)  # Simulate processing time
            translated_text, error = translate_text(
                source_text, 
                st.session_state.source_lang, 
                st.session_state.target_lang
            )
            
            if error:
                st.markdown(f"<div class='error-message'>❌ {error}</div>", unsafe_allow_html=True)
            else:
                st.session_state.translated_text = translated_text
                st.markdown("<div class='success-message'>✅ Translation successful!</div>", unsafe_allow_html=True)
                
                # Add to history
                st.session_state.translation_history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'source': source_text[:100] + "..." if len(source_text) > 100 else source_text,
                    'translation': translated_text[:100] + "..." if len(translated_text) > 100 else translated_text,
                    'source_lang': languages[st.session_state.source_lang],
                    'target_lang': languages[st.session_state.target_lang]
                })
    
    # Additional features (only show if translation exists)
    if st.session_state.translated_text:
        st.markdown("---")
        st.markdown("### 🔧 Additional Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Copy to clipboard button
            if st.button("📋 Copy Translation", 
                        key="copy_btn", 
                        use_container_width=True,
                        help="Copy translated text to clipboard"):
                st.components.v1.html(
                    copy_to_clipboard(st.session_state.translated_text),
                    height=0
                )
        
        with col2:
            # Text-to-speech button
            if st.button("🔊 Listen to Audio", 
                        key="tts_btn", 
                        use_container_width=True,
                        help="Listen to the translated text"):
                with st.spinner('Generating audio...'):
                    audio_html, error = text_to_speech(
                        st.session_state.translated_text, 
                        st.session_state.target_lang
                    )
                    
                    if error:
                        st.error(f"Audio generation failed: {error}")
                    else:
                        st.markdown("### 🔊 Audio Player")
                        st.components.v1.html(audio_html, height=80)
        
        with col3:
            # Clear button
            if st.button("🗑️ Clear All", 
                        type="secondary", 
                        use_container_width=True,
                        help="Clear all text and translation"):
                st.session_state.translated_text = ""
                st.session_state.source_text = ""
                st.rerun()
        
        # Translation history (collapsible)
        if st.session_state.translation_history:
            with st.expander("📜 Translation History (Last 5)"):
                for i, item in enumerate(reversed(st.session_state.translation_history[-5:]), 1):
                    st.markdown(f"""
                    **Entry #{len(st.session_state.translation_history) - i + 1}** ({item['timestamp']})
                    - **From ({item['source_lang']}):** {item['source']}
                    - **To ({item['target_lang']}):** {item['translation']}
                    ---
                    """)
                
                if st.button("Clear History", key="clear_history"):
                    st.session_state.translation_history = []
                    st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #7f8c8d; font-size: 0.9rem;'>"
        "Built with ❤️ for Internship Task 1 | "
        "Used Translatepy API & Streamlit | "
        f"Supported Languages: {len(languages)}"
        "</div>",
        unsafe_allow_html=True
    )
    
    # Instructions in sidebar
    with st.sidebar:
        st.markdown("### 📖 How to Use")
        st.markdown("""
        1. **Enter text** in the left text box
        2. **Select source language** (or use Auto Detect)
        3. **Select target language**
        4. Click **🔄 Translate** button
        5. Use additional features:
           - 📋 Copy translation to clipboard
           - 🔊 Listen to audio
           - ⇄ Swap languages
           - 📜 View history
        
        **Tips:**
        - Use Auto Detect for unknown languages
        - Click ⇄ to quickly swap languages
        - History saves your last 5 translations
        """)
        
        st.markdown("---")
        st.markdown("### ⚙️ Tech Stack")
        st.markdown("""
        - **Frontend**: Streamlit
        - **Translation**: Translatepy API
        - **Text-to-Speech**: Google TTS (gTTS)
        - **Styling**: Custom CSS
        """)

if __name__ == "__main__":
    main()