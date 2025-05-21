from utils.logger import log
from gtts import gTTS
import os

def load_script(path: str) -> str:
    log(f"Loading script from: {path}")
    try:
        with open(path, 'r') as f:
            content = f.read()
        log(f"Script loaded successfully. Length: {len(content)} characters.")
        return content
    except FileNotFoundError:
        log(f"Error: Script file not found at {path}")
        raise
    except Exception as e:
        log(f"Error loading script from {path}: {e}")
        raise

def generate_audio(text: str, out_path: str, lang: str = 'en'):
    log(f"Generating audio for text (first 50 chars): '{text[:50]}...' to {out_path} in language: {lang}")
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(out_path)
        log(f"Audio successfully generated and saved to {out_path}")
    except Exception as e:
        log(f"Error generating audio: {e}")
        # Optionally, clean up partially created file if any
        if os.path.exists(out_path):
            try:
                os.remove(out_path)
                log(f"Cleaned up partially created audio file: {out_path}")
            except Exception as clean_e:
                log(f"Error cleaning up audio file {out_path}: {clean_e}")
        raise 