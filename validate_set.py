import soundfile as sf
import os

def validate_audio_files(input_dir='data/data/audios'):
    """
    Validate audio files in the given directory.
    
    Args:
        input_dir (str): Directory containing the audio files
    """
    is_valid = True
    for file_path in os.listdir(input_dir):
        if file_path.endswith(".wav"):
            file_path = input_dir + "/" + file_path
            try:
                info = sf.info(file_path)
                Channels = info.channels
                SampleRate = info.samplerate
                if SampleRate != 44100:
                    print(f"WARNING: {file_path} has {SampleRate} Hz sample rate")
                    is_valid = False
                if Channels != 2:
                    print(f"WARNING: {file_path} has {info.channels} channels")
                    is_valid = False
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                is_valid = False
    return is_valid