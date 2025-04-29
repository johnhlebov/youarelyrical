# 🎵 YouAreLyrical - Precise Ukrainian Lyric Alignment Tool

This project aligns Ukrainian song lyrics word-by-word based on provided audio and lyrics text.  
It outputs both detailed word-level subtitles and clean line-level subtitles for professional lyric video production.

---

## ✨ Features
- Word-by-word forced alignment using WhisperX
- Strict correction to match the official `lyrics.txt`
- No artificial stretching of timings (preserves model precision)
- Handles missing or extra words gracefully
- Dual export:
  - Word-by-word `.srt` for karaoke-style highlighting
  - Line-by-line `.srt` matching original lyrics
  - JSON output for future editing or animations
- Git-tracked clean project structure

---

## 🛠 How It Works

1. **Input:**  
   - `input/song.wav` — the song audio
   - `input/lyrics.txt` — the clean text version of lyrics

2. **Process:**  
   - Preprocesses audio to mono, 16kHz
   - Transcribes and aligns using WhisperX
   - Forces matched words according to lyrics.txt
   - Exports corrected word and line SRT files

3. **Output:**  
   - `output/corrected_aligned_words.json`
   - `output/corrected_lyrics_word.srt`
   - `output/corrected_lyrics_line.srt`

---

## 📦 Project Structure

```plaintext
youarelyrical/
├── input/
│   ├── song.wav
│   ├── lyrics.txt
├── output/
│   ├── aligned_words.json           (raw WhisperX output)
│   ├── corrected_aligned_words.json (final corrected JSON)
│   ├── corrected_lyrics_word.srt    (word-by-word SRT)
│   ├── corrected_lyrics_line.srt    (line-by-line SRT)
├── scripts/
│   ├── script.py                    (audio preprocessing and WhisperX alignment)
│   ├── match_and_export.py          (correction, word and line SRT export)
├── .gitignore
├── README.md


⚡ Quickstart

# Setup Python environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install required packages
pip install -r requirements.txt

# Preprocess and align
python scripts/script.py

# Correct alignments and export subtitles
python scripts/match_and_export.py


🔥 Requirements
Python 3.9+
ffmpeg installed on system
Python packages:
 whisperx
 torch
 soundfile

pip install git+https://github.com/m-bain/whisperx.git
pip install torch soundfile

📢 Important Notes
.wav input must be high quality and properly normalized for best results.
Ensure lyrics.txt matches what is actually sung (small differences will still be corrected, but big gaps cause trouble).
No stretch applied — lyrics timing reflects actual model output.
For clean videos, word-by-word and line-by-line files are generated separately.

🚀 Future Upgrades
Web UI for uploading songs and auto-generating lyric videos
After Effects export JSON for direct text layer creation
Advanced fuzzy matching and manual correction interface
Multilingual support (English/Ukrainian)

Made with 💻 and 🎵 by [Johny Hlebov @ Orange Music Production 🍊]
