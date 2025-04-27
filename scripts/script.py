import os
import whisperx
import ffmpeg
import json
import time
import torch

# SETTINGS
INPUT_AUDIO = "input/song.wav"    # your song file
INPUT_LYRICS = "input/lyrics.txt" # your lyrics text file
OUTPUT_JSON = "output/aligned_words.json"
DEVICE = "cpu"
LANGUAGE = "uk"  # Ukrainian

def preprocess_audio(input_audio_path, output_audio_path):
    print("[*] Preprocessing audio...")
    ffmpeg.input(input_audio_path).output(
        output_audio_path,
        ac=1,  # mono
        ar=16000  # 16kHz
    ).overwrite_output().run()
    print("[+] Audio preprocessing done.")

def load_lyrics(lyrics_path):
    print("[*] Loading lyrics...")
    with open(lyrics_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    print("[+] Lyrics loaded.")
    return text

def main():
    start_time = time.time()

    if not os.path.exists("output"):
        os.makedirs("output")

    # Preprocess audio
    preprocessed_audio = "input/song_preprocessed.wav"
    preprocess_audio(INPUT_AUDIO, preprocessed_audio)

    # Load model
    print("[*] Loading WhisperX model...")
    model = whisperx.load_model("small", language=LANGUAGE, device=DEVICE, compute_type="float32")
    print("[+] Model loaded.")

    # Load audio
    print("[*] Loading audio...")
    audio = whisperx.load_audio(preprocessed_audio)

    # Load lyrics
    lyrics_text = load_lyrics(INPUT_LYRICS)

    # Transcribe
    print("[*] Transcribing...")
    result = model.transcribe(audio)

    # Align
    print("[*] Loading alignment model...")
    align_model, metadata = whisperx.load_align_model(language_code=LANGUAGE, device="cpu")
    print("[+] Alignment model loaded.")

    print("[*] Aligning...")
    aligned = whisperx.align(
    result["segments"],  # <- transcription segments
    align_model,         # <- alignment model you just loaded
    metadata,            # <- model metadata
    audio,               # <- preprocessed audio
    device="cpu"         # <- forced CPU
)

    # Save result
    print("[*] Saving result...")
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(aligned["word_segments"], f, ensure_ascii=False, indent=2)

    print(f"[+] Done. Results saved to {OUTPUT_JSON}")
    print(f"Total time: {round(time.time() - start_time, 2)} seconds.")

if __name__ == "__main__":
    main()
