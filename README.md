# Image-to-Video LipSync PoC

This project generates a lip-synced video from a face image and a text script. It uses gTTS for text-to-speech and Wav2Lip for video generation.

## Project Structure

```
Video Gen/
├── assets/                     # Static input/output files
│   ├── input.jpg               # INPUT: Your face image
│   ├── script.txt              # INPUT: Your narration script
│   └── audio.mp3               # GENERATED: audio file
│
├── output/                     # Final output video
│   └── generated_video.mp4     # GENERATED: final lipsynced video
│
├── services/                   # Modular services
│   ├── tts_service.py
│   └── lipsync_service.py
│
├── utils/                      # Helpers
│   └── logger.py
│
├── wav2lip/                    # Cloned Wav2Lip repository
│   ├── checkpoints/            # Needs wav2lip_gan.pth
│   ├── face_detection/         # Needs s3fd.pth within detection/sfd/
│   ├── inference.py
│   └── ...
│
├── config.py
├── generate_video.py           # Main script to run
├── requirements.txt            # Python dependencies
├── checklist.md                # Task checklist
├── architecture.md             # System architecture
└── README.md                   # This file
```

## Setup Instructions

### 1. Clone This Repository

If you haven't already, clone this project repository to your local machine.

### 2. Set up Python Virtual Environment

It is highly recommended to use a Python virtual environment.

```bash
python -m venv venv
# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install gTTS, PyTorch (with CUDA 11.8 support by default from the specified index), and other necessary libraries for Wav2Lip.
If you do not have a CUDA-enabled GPU or a different CUDA version, you might need to adjust the PyTorch installation line in `requirements.txt` accordingly. Refer to the [PyTorch website](https://pytorch.org/get-started/locally/) for the correct command for your system (e.g., for CPU-only or a different CUDA version).

### 4. Clone Wav2Lip Repository

The Wav2Lip code is used as a submodule. Clone it into the project root if it's not already there (this step should have been done by the development assistant if you followed along, but for a fresh setup, it's needed):

```bash
git clone https://github.com/Rudrabha/Wav2Lip.git wav2lip
```

### 5. Download Wav2Lip Pre-trained Models

You need to manually download the pre-trained models for Wav2Lip and place them in the correct directories within the `wav2lip/` folder.

- **Wav2Lip GAN Model (`wav2lip_gan.pth`)**:

  - Download from: [https://huggingface.co/Nekochu/Wav2Lip/resolve/fb925b05f0d353850ee0c56810e4545e274e2b5a/wav2lip_gan.pth](https://huggingface.co/Nekochu/Wav2Lip/resolve/fb925b05f0d353850ee0c56810e4545e274e2b5a/wav2lip_gan.pth)
  - Place it in: `wav2lip/checkpoints/wav2lip_gan.pth`
  - (Create the `wav2lip/checkpoints/` directory if it doesn't exist.)

- **Face Detection Model (`s3fd.pth`)**:
  - Download from: [https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth](https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth)
  - Place it in: `wav2lip/face_detection/detection/sfd/s3fd.pth`
  - (Create the `wav2lip/face_detection/detection/sfd/` directories if they don't exist.)

### 6. Prepare Input Files

- **Face Image**: Place your input face image (e.g., a clear, front-facing JPG or PNG) into the `assets/` directory and name it `input.jpg`.
- **Script Text**: Create a text file with your narration script, save it as `assets/script.txt`.

## How to Run

Once the setup is complete and input files are in place:

1.  Ensure your virtual environment is activated.
2.  Run the main script from the project root directory:

    ```bash
    python generate_video.py
    ```

3.  Follow the console logs for progress.

## Output

The final lip-synced video will be saved to:
`output/generated_video.mp4`

Intermediate files like the generated audio (`assets/audio.mp3`) will also be present.

## Troubleshooting

- **`FileNotFoundError` for models**: Double-check that `wav2lip_gan.pth` and `s3fd.pth` are downloaded and placed in the exact paths specified within the `wav2lip/` directory.
- **PyTorch/CUDA issues**: Ensure your PyTorch installation matches your system's CUDA capabilities. If you have issues with the CUDA version specified in `requirements.txt`, install the appropriate PyTorch version for your system (CPU or a different CUDA version) manually after activating the venv, then try `pip install -r requirements.txt` again (you might need to temporarily remove torch lines from `requirements.txt` if installing manually first).
- **`ffmpeg` not found**: Wav2Lip uses `ffmpeg` for audio/video processing. Ensure `ffmpeg` is installed on your system and accessible in your PATH. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html).
