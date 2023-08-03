from pydub import AudioSegment

def get_audio_duration(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        duration_in_ms = len(audio)
        duration_in_seconds = duration_in_ms / 1000
        return duration_in_seconds
    except Exception as e:
        print(f"Error: {e}")
        return None
