import requests as req
import re
import soundfile as sf
import sys
import numpy as np
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from extractor import extract_text
from script_generator import generate_script
from kokoro_onnx import Kokoro

app = Flask(__name__)

# Handle paths for both normal run and PyInstaller bundle
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).parent

if getattr(sys, 'frozen', False):
    # Running as exe — put uploads and output next to the exe
    EXE_DIR = Path(sys.executable).parent
else:
    EXE_DIR = Path(__file__).parent

UPLOAD_FOLDER = EXE_DIR / "uploads"
OUTPUT_FOLDER = EXE_DIR / "output"

KOKORO_MODEL = BASE_DIR / "voices" / "kokoro-v1.0.onnx"
KOKORO_VOICES = BASE_DIR / "voices" / "voices-v1.0.bin"

UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

kokoro = Kokoro(str(KOKORO_MODEL), str(KOKORO_VOICES))


def clean_script(script: str) -> str:
    # Remove any LLM preamble like "Here's the converted script:"
    script = re.sub(r"^.*?:\s*\n", "", script, count=1)
    return script.strip()


def text_to_audio(script: str, output_path: Path):
    samples, sample_rate = kokoro.create(
        script,
        voice="af_heart",
        speed=1.0,
        lang="en-us"
    )
    sf.write(str(output_path), samples, sample_rate)


def parse_script(script: str) -> list:
    lines = []
    for line in script.strip().split("\n"):
        line = line.strip()
        if line.startswith("Host A:"):
            text = line.replace("Host A:", "").strip()
            if text:
                lines.append(("A", text))
        elif line.startswith("Host B:"):
            text = line.replace("Host B:", "").strip()
            if text:
                lines.append(("B", text))
    return lines


def two_host_audio(script: str, output_path: Path, voice_a: str = "af_heart", voice_b: str = "am_michael"):
    lines = parse_script(script)

    if not lines:
        # Fallback to single host if parsing fails
        text_to_audio(script, output_path)
        return

    all_samples = []
    sample_rate = None
    silence = None

    for host, text in lines:
        voice = voice_a if host == "A" else voice_b
        samples, sr = kokoro.create(
            text,
            voice=voice,
            speed=1.0,
            lang="en-us"
        )

        if sample_rate is None:
            sample_rate = sr
            # 0.4 second silence between speakers
            silence = np.zeros(int(sr * 0.4), dtype=samples.dtype)

        all_samples.append(samples)
        all_samples.append(silence)

    final_audio = np.concatenate(all_samples)
    sf.write(str(output_path), final_audio, sample_rate)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if "document" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["document"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save uploaded file
    file_path = UPLOAD_FOLDER / file.filename
    file.save(str(file_path))

    try:
        # Step 1: Extract text
        text = extract_text(str(file_path))
        if not text:
            return jsonify({"error": "Could not extract text from file"}), 400

        # Step 2: Generate script
        script = generate_script(text)
        script = clean_script(script)

        # Save script
        script_path = OUTPUT_FOLDER / "podcast_script.txt"
        script_path.write_text(script, encoding="utf-8")

        # Step 3: Convert to audio
        voice_a = request.form.get("voice_a", "af_heart")
        voice_b = request.form.get("voice_b", "am_michael")
        audio_path = OUTPUT_FOLDER / "podcast.wav"
        two_host_audio(script, audio_path, voice_a, voice_b)

        return jsonify({
            "success": True,
            "script": script,
            "audio_url": "/audio"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/audio")
def serve_audio():
    audio_path = OUTPUT_FOLDER / "podcast.wav"
    if not audio_path.exists():
        return jsonify({"error": "Audio not found"}), 404
    return send_file(str(audio_path), mimetype="audio/wav")

@app.route("/health")
def health():
    try:
        req.get("http://127.0.0.1:11434", timeout=2)
        ollama_ok = True
    except Exception:
        ollama_ok = False

    return jsonify({
        "status": "running",
        "ollama": "connected" if ollama_ok else "not running"
    })

if __name__ == "__main__":
    app.run(debug=False)