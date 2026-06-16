============================================================
  DOCCAST — Document to Podcast Converter
  Powered by Ollama & Kokoro TTS
============================================================

DocCast converts your PDF, DOCX, or TXT documents into a
two-host podcast using AI — fully offline after setup.

------------------------------------------------------------
  BEFORE YOU RUN
------------------------------------------------------------

You need to install two things before DocCast will work:

1. OLLAMA (the AI engine)
   - Download from: https://ollama.com
   - Install it like any normal program
   - Then open a terminal (Command Prompt or PowerShell)
     and run this command:

       ollama pull llama3.2:3b

   - Wait for it to finish downloading (~2GB)
   - After that, Ollama will run automatically in the
     background whenever your computer starts

2. VOICE MODEL FILES (for text-to-speech)
   - Download these two files:

     kokoro-v1.0.onnx (310MB)
     https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx

     voices-v1.0.bin (27MB)
     https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

   - Place both files inside the "voices" folder that
     is next to DocCast.exe

     Your folder should look like this:
     
       DocCast/
       ├── DocCast.exe
       ├── voices/
       │   ├── kokoro-v1.0.onnx
       │   └── voices-v1.0.bin
       └── (everything else)

------------------------------------------------------------
  HOW TO RUN
------------------------------------------------------------

1. Make sure Ollama is installed and running
   (it runs in the background automatically after install)

2. Double-click DocCast.exe
   OR open a terminal in this folder and run:
     .\DocCast.exe

3. A terminal window will open — leave it running

4. Open your browser and go to:
     http://127.0.0.1:5000

5. Upload a PDF, DOCX, or TXT file

6. Choose voices for Host A and Host B

7. Click "Generate Podcast" and wait
   (it takes 1-3 minutes depending on document length)

8. Listen to your podcast in the browser or download the
   audio file using the Download button

------------------------------------------------------------
  TO STOP DOCCAST
------------------------------------------------------------

Close the terminal window that opened when you ran
DocCast.exe, or press Ctrl+C inside it.

------------------------------------------------------------
  TROUBLESHOOTING
------------------------------------------------------------

"No audio generated" or pipeline error:
  - Make sure Ollama is running
  - Open a terminal and run: ollama serve
  - If it says "address already in use" Ollama is already
    running — that is fine

"voices not found" error:
  - Make sure kokoro-v1.0.onnx and voices-v1.0.bin are
    inside the voices/ folder next to DocCast.exe

Audio sounds robotic or wrong:
  - Try a different voice combination in the dropdowns

------------------------------------------------------------
  SYSTEM REQUIREMENTS
------------------------------------------------------------

  - Windows 10 or 11 (64-bit)
  - At least 8GB RAM recommended
  - At least 5GB free disk space
  - Internet not required after setup

------------------------------------------------------------
  BUILT BY
------------------------------------------------------------

  Yehoshua Ekanem
  github.com/JoshuaEkanem

  Powered by Afang Soup

============================================================