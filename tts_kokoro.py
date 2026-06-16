import soundfile as sf
from kokoro_onnx import Kokoro
from pathlib import Path

KOKORO_MODEL = Path("voices/kokoro-v1.0.onnx")
KOKORO_VOICES = Path("voices/voices-v1.0.bin")
OUTPUT_PATH = Path("output/kokoro_test.wav")
OUTPUT_PATH.parent.mkdir(exist_ok=True)

TEXT = """
Welcome to DocCast — your document, turned into a podcast.
Today we're exploring an exciting topic pulled straight from your files.
Let's dive in.
"""

kokoro = Kokoro(str(KOKORO_MODEL), str(KOKORO_VOICES))

samples, sample_rate = kokoro.create(
    TEXT,
    voice="af_heart",
    speed=1.0,
    lang="en-us"
)

sf.write(str(OUTPUT_PATH), samples, sample_rate)
print(f"Audio saved to {OUTPUT_PATH}")