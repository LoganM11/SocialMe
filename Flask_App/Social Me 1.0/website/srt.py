import whisper_timestamped as whisper
import os

def format_time(seconds):
    millis = int(seconds * 1000)
    hours = millis // 3600000
    minutes = (millis // 60000) % 60
    seconds = (millis // 1000) % 60
    millis = millis % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

def transcribe(filename, model_path):
    audio = whisper.load_audio(filename)
    model = whisper.load_model(model_path, device="cpu")
    result = whisper.transcribe(model, audio, language="en")
    return result

def generate_srt(file_path, caption_type_number, max_value):
    max_value = int(max_value)
    """
    Generate captions based on input parameters and return the path to the SRT file.
    :param file_path: Path to the input audio file.
    :param caption_type_number: 1 = words, 2 = characters, 3 = vowels.
    :param max_value: Maximum number of the caption type per caption.
    :return: Path to the generated SRT file.
    """
    # Define the caption type based on the input number
    caption_types = {1: "words", 5: "characters", 2: "vowels"}
    caption_type = caption_types[int(caption_type_number)]

    if not caption_type:
        raise ValueError(f"{caption_type_number} Invalid caption type number. Use 1 (words), 2 (characters), or 3 (vowels).")

    # Path to the Whisper model (adjust as needed)
    model_path = os.path.join(os.getcwd(), "website\whisper_model\small", "pytorch_model.bin")

    # Transcribe the audio
    transcription_result = transcribe(file_path, model_path)

    # Generate the SRT content
    srt_file_content = ""
    segments = transcription_result["segments"]
    index = 1

    for segment in segments:
        words = segment["words"]
        caption = []
        current_count = 0

        for word in words:
            if caption_type == "words":
                current_count += 1
            elif caption_type == "characters":
                current_count += len(word["text"])
            elif caption_type == "vowels":
                current_count += sum(1 for c in word["text"].lower() if c in "aeiou")

            caption.append(word)

            if current_count >= max_value:
                start_time = format_time(caption[0]["start"])
                end_time = format_time(caption[-1]["end"])
                caption_text = ' '.join([w["text"] for w in caption])
                srt_file_content += f"{index}\n"
                srt_file_content += f"{start_time} --> {end_time}\n"
                srt_file_content += f"{caption_text}\n\n"
                caption = []
                current_count = 0
                index += 1

        # Handle remaining items in the last caption
        if caption:
            start_time = format_time(caption[0]["start"])
            end_time = format_time(caption[-1]["end"])
            caption_text = ' '.join([w["text"] for w in caption])
            srt_file_content += f"{index}\n"
            srt_file_content += f"{start_time} --> {end_time}\n"
            srt_file_content += f"{caption_text}\n\n"
            index += 1
    print(file_path)
    # Save the SRT content to a file
    output_dir = os.path.join(os.path.dirname(file_path), "srt_files")
    print(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    srt_file_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(file_path))[0]}.srt")

    with open(srt_file_path, "w", encoding="utf-8") as f:
        f.write(srt_file_content)
    print(srt_file_path)
    return srt_file_path
