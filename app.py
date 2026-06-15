import requests as req
import re
import wave
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from extractor import extract_text
from script_generator import generate_script
from piper.voice import PiperVoice

app = Flask(__name__)

# Handle paths for both normal run and PyInstaller bundle
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).parent

UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("output")
VOICE_MODEL = BASE_DIR / "voices" / "en_US-lessac-medium.onnx"

UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

voice = PiperVoice.load(VOICE_MODEL)


def clean_script(script: str) -> str:
    # Remove any LLM preamble like "Here's the converted script:"
    script = re.sub(r"^.*?:\s*\n", "", script, count=1)
    return script.strip()


def text_to_audio(script: str, output_path: Path):
    with wave.open(str(output_path), "wb") as wav_file:
        voice.synthesize_wav(script, wav_file)


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
        audio_path = OUTPUT_FOLDER / "podcast.wav"
        text_to_audio(script, audio_path)

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
    app.run(debug=True)