import json
import os

# Settings
INPUT_ALIGNED_JSON = "output/aligned_words.json"
INPUT_LYRICS_TXT = "input/lyrics.txt"
OUTPUT_CORRECTED_JSON = "output/corrected_aligned_words.json"
OUTPUT_SRT_FILE = "output/corrected_lyrics.srt"

def load_whisper_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_lyrics_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # Basic clean
    text = text.replace("\n", " ").replace("\r", " ").strip()
    words = text.split()
    return words

def save_corrected_json(corrected_words, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(corrected_words, f, ensure_ascii=False, indent=2)

def save_as_srt(corrected_words, path):
    def format_timestamp(seconds):
        ms = int(seconds * 1000)
        h = ms // (3600 * 1000)
        m = (ms % (3600 * 1000)) // (60 * 1000)
        s = (ms % (60 * 1000)) // 1000
        ms = ms % 1000
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    with open(path, "w", encoding="utf-8") as f:
        for idx, word in enumerate(corrected_words, start=1):
            start = format_timestamp(word['start'])
            end = format_timestamp(word['end'])
            text = word['word']
            f.write(f"{idx}\n{start} --> {end}\n{text}\n\n")

def main():
    # Load files
    whisper_words = load_whisper_json(INPUT_ALIGNED_JSON)
    lyrics_words = load_lyrics_txt(INPUT_LYRICS_TXT)

    corrected_words = []

    print(f"[*] Matching {len(whisper_words)} whisper words to {len(lyrics_words)} lyrics words...")

    for i in range(max(len(whisper_words), len(lyrics_words))):
        if i < len(whisper_words):
            corrected_word = whisper_words[i].copy()
            if i < len(lyrics_words):
                corrected_word['word'] = lyrics_words[i]  # Force lyrics word
            corrected_words.append(corrected_word)
        else:
        # Insert missing lyrics words
            last_end = corrected_words[-1]['end'] if corrected_words else 0
            fake_start = last_end + 0.3  # 300ms gap
            fake_end = fake_start + 0.5  # 500ms duration
            corrected_word = {
                "start": fake_start,
                "end": fake_end,
                "word": lyrics_words[i]
            }
            corrected_words.append(corrected_word)

    print(f"[+] Matched {len(corrected_words)} words.")


    # LOAD LYRICS AS LINES
    def load_lyrics_lines(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        lines = [line.strip() for line in lines if line.strip()]
        return lines

    #Save line-by-Line SRT: 
    def save_lines_as_srt(corrected_words, lyrics_lines, path):
        def format_timestamp(seconds):
            ms = int(seconds * 1000)
            h = ms // (3600 * 1000)
            m = (ms % (3600 * 1000)) // (60 * 1000)
            s = (ms % (60 * 1000)) // 1000
            ms = ms % 1000
            return f"{h:02}:{m:02}:{s:02},{ms:03}"

        idx = 1
        word_idx = 0
        with open(path, "w", encoding="utf-8") as f:
            for line in lyrics_lines:
                line_words = line.split()
                if word_idx + len(line_words) <= len(corrected_words):
                    start = corrected_words[word_idx]['start']
                    end = corrected_words[word_idx + len(line_words) - 1]['end']
                    text = line
                    f.write(f"{idx}\n{format_timestamp(start)} --> {format_timestamp(end)}\n{text}\n\n")
                    idx += 1
                    word_idx += len(line_words)

    # Save word-by-word SRT
    save_as_srt(corrected_words, "output/corrected_lyrics_word.srt")
    print(f"[+] Word-by-word SRT saved.")

# Save line-by-line SRT
    lyrics_lines = load_lyrics_lines(INPUT_LYRICS_TXT)
    save_lines_as_srt(corrected_words, lyrics_lines, "output/corrected_lyrics_line.srt")
    print(f"[+] Line-by-line SRT saved.")

if __name__ == "__main__":
    main()
