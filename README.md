# Moshi Knowledge Learning Project

This project tries to verify if Moshi can learn out of distribution data through finetuning on generated samples. It uses Kokoro for text-to-speech. It generates question-answer pairs from a text corpus, converts them to audio, and prepares them for fine-tuning.

## Project Overview

The workflow consists of three main steps:
1. **Generate QA Pairs**: Creates question-answer pairs from a text corpus using Google's Gemini API
2. **Generate Audio Dataset**: Converts the QA pairs to audio files using Kokoro, then upsamples them to 44.1kHz stereo
3. **Validate Dataset**: Ensures all audio files meet the required specifications (44.1kHz, stereo)

Once this is all done, hop on the [moshi-finetune repository](https://github.com/kyutai-labs/moshi-finetune/tree/main) and follow the steps here to finetune the model.

## Setup and Installation

### Using Docker (Recommended)

The easiest way to run this project is using Docker:

1. Build the Docker image:
   ```bash
   docker build -t moshi-rag .
   ```

2. Run the container with your API key:
   ```bash
   docker run -it --env-file .env moshi-rag
   ```

### Manual Setup

1. Install Python 3.10 or higher
2. Install system dependencies:
   ```bash
   # On Ubuntu/Debian
   apt-get update && apt-get install -y ffmpeg
   
   # On macOS
   brew install ffmpeg
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

Run the complete workflow:

```bash
python generate_qa.py
python generate_set.py
python validate_set.py
```

Or run individual steps as needed.

## Project Structure

- `generate_qa.py`: Generates QA pairs from text using Gemini API
- `generate_set.py`: Converts QA pairs to audio and prepares the dataset
- `validate_set.py`: Validates the audio files
- `files/`: Contains input text and generated QA pairs
- `audios/`: Contains generated audio files
- `upsampled_audios/`: Contains upsampled audio files (44.1kHz, stereo)
- `eval_audios/`: Contains evaluation audio files
- `upsampled_eval_audios/`: Contains upsampled evaluation audio files

## Fine-tuning Configuration

The project uses the configuration in `moshi_7B.yaml` for fine-tuning. Key parameters:

- LoRA rank: 128
- Learning rate: 2e-6
- Batch size: 4
- Max steps: 500
- Gradient checkpointing: enabled

## Experience Feedback

### Voice Generation
- Moshiko voice was turned female as was the Kokoro voice
- The voice generation process worked well for creating consistent audio samples, as it was still possible to have a conversation with the finetuned Moshiko

### Fine-tuning Results
- While losses were gradually reduced, it failed to learn in 500 steps (even 2000) about the data that was sent in the qa_pairs
- Eval loss turned to NaN very quickly

### Assessment
Over 100 QA pair voicelines, the finetuning library seems really good for voice cloning, but further experiments (likely with further compute) could be required to check if it learned latent knowledge.

## Acknowledgements

- [Moshi](https://github.com/kyutai/moshi) for the voice generation model
- [Kokoro](https://github.com/hexgrad/kokoro) for the text-to-speech pipeline
- [Google Gemini](https://ai.google.dev/) for the QA generation
