import os
import yt_dlp
import shlex
import subprocess
import re

# Function to merge video and audio
def merge_video_audio(video_path, audio_path, output_path):
    print("MERGING")
    cmd = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac -strict experimental "{output_path}"'
    result = subprocess.call(cmd, shell=True)
    if result != 0:
        raise RuntimeError("FFmpeg failed to merge video and audio.")


# Unified download function
def download_media(choice, file_path, video_url, resolution="best"):
    def download_with_retry(options):
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([video_url])
        except yt_dlp.utils.DownloadError as e:
            raise RuntimeError(f"Download failed: {e}")

    # Ensure file name is valid
    file_name = os.path.basename(file_path)

    # Determine download directory and temporary paths
    download_dir = os.path.dirname(file_path)
    os.makedirs(download_dir, exist_ok=True)
    video_file = os.path.join(download_dir, f"{file_name}_video.mp4")
    audio_file = os.path.join(download_dir, f"{file_name}_audio.webm")
    final_output = file_path + ".mp4"

    # Process choice
    if choice == 1:  # Download video only
        video_download_options = {'format': resolution, 'outtmpl': video_file}
        download_with_retry(video_download_options)
        print(f"Video file saved: {video_file}")
        return video_file, "_video.mp4"

    elif choice == 2:  # Download audio only
        audio_download_options = {'format': 'bestaudio', 'outtmpl': audio_file}
        download_with_retry(audio_download_options)
        print(f"Audio file saved: {audio_file}")
        return audio_file, "_audio.webm"

    elif choice == 3:  # Download and merge both
        video_download_options = {'format': resolution, 'outtmpl': video_file}
        audio_download_options = {'format': 'bestaudio', 'outtmpl': audio_file}

        # Download video and audio
        download_with_retry(video_download_options)
        download_with_retry(audio_download_options)

        # Merge video and audio
        merge_video_audio(video_file, audio_file, final_output)
        os.remove(video_file)
        os.remove(audio_file)
        print(f"Merged file saved: {final_output}")
        return final_output, ".mp4"

    else:
        raise ValueError("Invalid choice. Use 1 for video, 2 for audio, 3 for both.")
