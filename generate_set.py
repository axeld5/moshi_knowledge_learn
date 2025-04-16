import json
import os
import sphn
import soundfile as sf
from pathlib import Path
from kokoro import KPipeline
from pydub import AudioSegment

def load_text_data(json_path):
    """
    Load and prepare text data from a JSON file.
    
    Args:
        json_path (str): Path to the JSON file containing QA pairs
        
    Returns:
        list: List of formatted text strings
    """
    with open(json_path, 'r') as f:
        dataset = json.load(f)
    
    # Format each QA pair into a single string
    text_list = [f"Question: {item['question']} Answer: {item['answer']}" 
                 for item in dataset]
    
    return text_list

def generate_audio_files(text_list, output_dir, voice='af_heart', sample_rate=24000):
    """
    Generate audio files from text using Kokoro pipeline.
    
    Args:
        text_list (list): List of text strings to convert to audio
        output_dir (str): Directory to save audio files
        voice (str): Voice to use for generation
        sample_rate (int): Sample rate for audio files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize the pipeline
    pipeline = KPipeline(lang_code='a')
    
    # Generate audio for each text
    for i, text in enumerate(text_list):
        generator = pipeline(text, voice=voice)
        for j, (gs, ps, audio) in enumerate(generator):
            print(f"Generating audio {i}_{j}: {gs} {ps}")
            output_path = os.path.join(output_dir, f'{i}_{j}.wav')
            sf.write(output_path, audio, sample_rate)

def upsample_audio_files(input_dir, output_dir):
    """
    Upsample audio files to 44100 Hz and stereo.
    
    Args:
        input_dir (str): Directory containing the audio files
        output_dir (str): Directory to save the upsampled audio files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for file_path in os.listdir(input_dir):
        if file_path.endswith(".wav"):
            # Use os.path.join for better path handling
            input_file = os.path.join(input_dir, file_path)
            output_file = os.path.join(output_dir, file_path)
            try:
                # Load the audio file
                audio = AudioSegment.from_wav(input_file)
                # Set channels to stereo (duplicates mono)
                stereo_audio = audio.set_channels(2)
                # Set frame rate (sample rate)
                resampled_audio = stereo_audio.set_frame_rate(44100)
                # Export the result
                resampled_audio.export(output_file, format="wav")
                print(f"Successfully converted '{input_file}' to '{output_file}'")
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Make sure ffmpeg is installed and in your PATH if you encounter issues.")

def generate_data_jsonl(output_file, audio_dir):
    """
    Generate a JSONL file containing audio paths and durations.

    Args:
        output_file (str): Path to the output JSONL file
        output_dir (str): Directory containing the audio files
    """
    audio_dir = Path(audio_dir)
    path_objects = list(audio_dir.glob("*.wav"))
    # sphn.durations likely needs the actual file paths to read them
    full_paths_str = [str(p) for p in path_objects]
    durations = sphn.durations(full_paths_str)
    with open(output_file, "w") as fobj:
        # Iterate through the original Path objects and durations
        for p, d in zip(path_objects, durations):
            if d is None:
                continue
            # Construct the relative path: 'audios/filename.wav'
            # Using os.path.join ensures '/' is used as separator
            relative_path = os.path.join(p.parent.name, p.name).replace("\\", "/")
            json.dump({"path": relative_path, "duration": d}, fobj)
            fobj.write("\n")

def generate_set(json_path, output_dir, jsonl_path):
    text_list = load_text_data(json_path=json_path)
    generate_audio_files(text_list, output_dir=output_dir)
    upsample_audio_files(input_dir=output_dir, output_dir=f"upsampled_{output_dir}")
    generate_data_jsonl(output_file=jsonl_path, audio_dir=f"upsampled_{output_dir}")

if __name__ == "__main__":
    generate_set(json_path='files/qa_pairs.json', output_dir='audios', jsonl_path='data.jsonl')
    generate_set(json_path='files/eval_pairs.json', output_dir='eval_audios', jsonl_path='eval_data.jsonl')