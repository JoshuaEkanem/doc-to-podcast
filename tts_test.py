import wave
from pathlib import Path
from piper.voice import PiperVoice

MODEL_PATH = Path("voices/en_US-lessac-medium.onnx")
OUTPUT_PATH = Path("output/test.wav")
OUTPUT_PATH.parent.mkdir(exist_ok=True)

TEXT = """
Welcome to DocCast — your document, turned into a podcast.
Today we're exploring an exciting topic pulled straight from your files.
Let's dive in.
"""

voice = PiperVoice.load(MODEL_PATH)

with wave.open(str(OUTPUT_PATH), "wb") as wav_file:
    voice.synthesize_wav(TEXT, wav_file)

print(f"Audio saved to {OUTPUT_PATH}")