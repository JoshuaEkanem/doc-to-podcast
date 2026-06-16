# 🎙️ DocCast — Document to Podcast Converter

An offline, zero-cost tool that converts PDF, DOCX, and TXT documents into 
two-host podcast-style audio using a local LLM and neural TTS — no internet 
required after setup.

Built with Flask, Ollama, and Kokoro TTS.

---

## Features

- 📄 Supports PDF, DOCX, and TXT input
- 🤖 Uses Ollama (llama3.2:3b) to generate a natural two-host podcast script
- 🎙️ Two distinct voices (male + female) via Kokoro TTS
- 🌐 Clean web UI served locally in your browser
- 📦 Available as a standalone Windows `.exe` — no Python needed
- 🔒 Fully offline after initial setup

---

## Requirements

### 1. Ollama
Download and install Ollama from [https://ollama.com](https://ollama.com), then pull the model:

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running before launching DocCast.

### 2. Voice Model Files
Download these two files and place them in the `voices/` folder:

| File | Link | Size |
|------|------|------|
| `kokoro-v1.0.onnx` | [Download](https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx) | 310MB |
| `voices-v1.0.bin` | [Download](https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin) | 27MB |

---

## Running from Source

### 1. Clone the repo
```bash
git clone https://github.com/JoshuaEkanem/doc-to-podcast.git
cd doc-to-podcast
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download voice model files
Place `kokoro-v1.0.onnx` and `voices-v1.0.bin` in the `voices/` folder as described above.

### 5. Start Ollama
Make sure Ollama is running:
```bash
ollama serve
```

### 6. Run the app
```bash
python app.py
```

Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Running the Standalone Executable

1. Download the latest release from the [Releases](https://github.com/JoshuaEkanem/doc-to-podcast/releases) page
2. Place `kokoro-v1.0.onnx` and `voices-v1.0.bin` in the `voices/` folder next to `DocCast.exe`
3. Make sure Ollama is installed and running
4. Double-click `DocCast.exe` or run it from the terminal
5. Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## How It Works
Document (PDF/DOCX/TXT)

↓

Text Extraction

(PyMuPDF / python-docx)

↓

Script Generation

(Ollama — llama3.2:3b)

↓

Two-Host TTS Synthesis

(Kokoro TTS — af_heart + am_michael)

↓

Audio Output (.wav)

---

## Project Structure
doc-to-podcast/

├── app.py               # Flask server and pipeline orchestration

├── extractor.py         # PDF / DOCX / TXT text extraction

├── script_generator.py  # Ollama podcast script generation

├── launcher.py          # Entry point for the .exe

├── doccast.spec         # PyInstaller build spec

├── requirements.txt     # Python dependencies

├── templates/

│   └── index.html       # Web UI

├── voices/              # Voice model files (not tracked in git)

│   ├── kokoro-v1.0.onnx

│   └── voices-v1.0.bin

└── output/              # Generated audio and scripts

---

## Built With

- [Flask](https://flask.palletsprojects.com/) — Web framework
- [Ollama](https://ollama.com/) — Local LLM runner
- [Kokoro TTS](https://github.com/thewh1teagle/kokoro-onnx) — Neural text-to-speech
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF extraction
- [python-docx](https://python-docx.readthedocs.io/) — DOCX extraction
- [PyInstaller](https://pyinstaller.org/) — Windows executable packaging

---

## Author

**Joshua Ekanem**  
[GitHub](https://github.com/JoshuaEkanem)

---

*Powered by Ollama & Piper TTS*