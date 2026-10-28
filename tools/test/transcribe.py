"""Распознать речь в файлах (скилл /comfy-test). Запускать через transcribe.sh — он освобождает VRAM и ставит LD_LIBRARY_PATH.

transcribe.py [--lang ru|en] [--words] file …
"""
import argparse
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("files", nargs="+")
ap.add_argument("--lang")
ap.add_argument("--words", action="store_true")
a = ap.parse_args()
model = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16", local_files_only=True)
for f in a.files:
    segs, info = model.transcribe(f, language=a.lang, word_timestamps=a.words)
    segs = list(segs)
    print(f"=== {f}  [{info.language} {info.language_probability:.2f}, {info.duration:.1f} с]")
    print(" ".join(s.text.strip() for s in segs))
    if a.words:
        for s in segs:
            print("  " + " ".join(f"{w.word.strip()}@{w.start:.2f}" for w in s.words))
