import os

ASSETS_DIR = "assets/"
SCRIPT_FILE = os.path.join(ASSETS_DIR, "script.txt")
AUDIO_FILE = os.path.join(ASSETS_DIR, "audio.mp3")

# Wav2Lip specific paths
WAV2LIP_MODEL_PATH = "wav2lip/checkpoints/wav2lip_gan.pth"

# TTS Configuration
TTS_LANGUAGE = "fi" # Default language for Text-to-Speech

# Input/Output files
FACE_IMAGE_FILE = ASSETS_DIR + "input.jpg"
OUTPUT_DIR = "output"
OUTPUT_VIDEO_FILE = os.path.join(OUTPUT_DIR, "generated_video.mp4")

# OUTPUT_DIR, FACE_IMAGE, OUTPUT_VIDEO will be added later 