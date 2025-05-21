import subprocess
import os
import sys
from utils.logger import log

def run_lipsync(image_path: str, audio_path: str, output_path: str, wav2lip_model_path: str):
    log(f"Starting lipsync process for image: {image_path} and audio: {audio_path}")

    # Ensure paths are absolute or correctly relative to the Wav2Lip script's execution directory
    # Wav2Lip's inference.py expects paths relative to its own location if not absolute.
    # For simplicity, we'll try to use paths relative to the project root and adjust as needed.

    wav2lip_root = "wav2lip"
    # Construct paths relative to the wav2lip_root where inference.py is located
    # inference.py is in wav2lip/, so paths to assets/ and output/ need to be ..\assets and ..\output
    # However, image_path, audio_path, output_path, and wav2lip_model_path are already relative to project root.

    # Convert paths to be relative to the wav2lip directory for the script
    # The script will be run from the 'wav2lip' directory.
    rel_image_path = os.path.join("..", image_path)
    rel_audio_path = os.path.join("..", audio_path)
    rel_output_path = os.path.join("..", output_path)
    model_path_in_wav2lip_dir = os.path.relpath(wav2lip_model_path, wav2lip_root)

    python_executable = sys.executable

    command = [
        python_executable,
        "inference.py",
        "--checkpoint_path", model_path_in_wav2lip_dir,
        "--face", rel_image_path,
        "--audio", rel_audio_path,
        "--outfile", rel_output_path,
        "--static", "True" # Provide a value for static
    ]

    log(f"Executing Wav2Lip command: {' '.join(command)}")

    try:
        # Wav2Lip inference script needs to be run from its own directory
        process = subprocess.Popen(command, cwd=wav2lip_root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            log(f"Lipsync process completed successfully. Output: {output_path}")
        else:
            log(f"Lipsync process failed. Return code: {process.returncode}")
            log(f"STDERR: {stderr.decode()}")
            log(f"STDOUT: {stdout.decode()}")
            raise Exception(f"Wav2Lip inference failed: {stderr.decode()}")
        
        # Check if the output file was created
        if not os.path.exists(output_path):
            log(f"Error: Output file {output_path} was not created by Wav2Lip.")
            log(f"STDOUT from Wav2Lip: {stdout.decode()}")
            log(f"STDERR from Wav2Lip: {stderr.decode()}")
            # This might indicate an issue even if Wav2Lip returned 0, like wrong paths in ffmpeg post-processing.
            # The inference script itself creates temp/result.avi and then uses ffmpeg to combine with audio.
            # If output_path (e.g. ../output/generated_video.mp4) is not created, ffmpeg might have failed.
            
            # For debugging, let's check if the intermediate temp/result.avi was created
            temp_avi = os.path.join(wav2lip_root, "temp", "result.avi")
            if os.path.exists(temp_avi):
                log(f"Intermediate video {temp_avi} was created.")
            else:
                log(f"Intermediate video {temp_avi} was NOT created.")
            raise Exception(f"Wav2Lip did not produce the final output file: {output_path}. Check logs.")

    except FileNotFoundError as e:
        log(f"Error running Wav2Lip: {e}. Ensure Wav2Lip and its dependencies (like python in venv) are correctly set up.")
        raise
    except Exception as e:
        log(f"An unexpected error occurred during lipsync: {e}")
        raise 