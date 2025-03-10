import os
import re
from pydub import AudioSegment
from pydub.silence import split_on_silence
import noisereduce as nr
import numpy as np

def process_audio_file(input_file, settings):
    """
    Processes an audio file by removing background noise and silences.

    Args:
        input_file (str): Path to the input audio file.
        settings (dict): Dictionary with processing settings:
            - "silence_thresh": Silence threshold in dBFS.
            - "min_silence_len": Minimum silence length in ms.
            - "padding": Padding in ms.
            - "leeway": Silence leeway in ms.
            - "prop_decrease": Proportion of noise reduction (0 to skip noise removal).
    
    Returns:
        str: Path to the processed audio file.
    """
    # Extract file name and directory
    file_name, _ = os.path.splitext(os.path.basename(input_file))
    original_dir = os.path.dirname(input_file)

    # Create "enhanced" folder parallel to the original directory
    enhanced_dir = os.path.join(original_dir, "enhanced")
    os.makedirs(enhanced_dir, exist_ok=True)

    # New output path
    output_file = os.path.join(enhanced_dir, f"{file_name}.mp3")

    # Load audio file
    print("Loading audio file...")
    audio = AudioSegment.from_file(input_file)

    # Step 1: Remove background noise (if prop_decrease > 0)
    if settings["prop_decrease"] > 0:
        print("Removing background noise...")
        samples = np.array(audio.get_array_of_samples())
        reduced_noise_samples = nr.reduce_noise(
            y=samples,
            sr=audio.frame_rate,
            prop_decrease=settings["prop_decrease"]
        )
        audio = AudioSegment(
            reduced_noise_samples.tobytes(),
            frame_rate=audio.frame_rate,
            sample_width=audio.sample_width,
            channels=audio.channels
        )
        print("Background noise removed.")
    else:
        print("Skipping background noise removal...")

    # Step 2: Remove silences
    print("Removing silences...")
    chunks = split_on_silence(
        audio,
        min_silence_len=settings["min_silence_len"],
        silence_thresh=settings["silence_thresh"]
    )
    processed_audio = AudioSegment.silent(duration=0)

    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        processed_audio += chunk
        if i < len(chunks) - 1:
            processed_audio += AudioSegment.silent(duration=settings["leeway"])

    print("Silences removed.")

    # Step 3: Export processed audio
    print("Exporting processed audio...")
    processed_audio.export(output_file, format="mp3")
    print(f"Processed audio saved at: {output_file}")

    return output_file


