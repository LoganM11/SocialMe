import yt_dlp
import re

def list_formats(url):
    formats_list = []
    seen_resolutions = set()

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
            for fmt in formats:
                format_id = fmt.get('format_id', '')
                file_type = fmt.get('ext', '')
                resolution = fmt.get('format_note', '')

                # Check if the format is mp4 and the resolution is a number followed by 'p'
                if file_type == 'mp4' and re.match(r'^\d+p$', resolution):
                    if resolution not in seen_resolutions:
                        formats_list.append({
                            'id': format_id,
                            'format': f"{resolution} .{file_type}"
                        })
                        seen_resolutions.add(resolution)
    except Exception as e:
        print(f"Error: {str(e)}")

    return formats_list

# Get URL from user input
url = input("Enter the video URL: ")
formats = list_formats(url)

# Print the list of formats
for fmt in formats:
    print(f"ID: {fmt['id']}, Format: {fmt['format']}")
