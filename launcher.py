import sys
import time
import threading
import webbrowser
import requests
from app import app

HOST = "127.0.0.1"
PORT = 5000
URL = f"http://{HOST}:{PORT}"


def check_ollama():
    try:
        r = requests.get("http://127.0.0.1:11434", timeout=3)
        return True
    except Exception:
        return False


def open_server_info():
    # Wait for Flask to start
    time.sleep(2)
    # Print clear instructions to console
    print("\n" + "=" * 50)
    print("  DocCast is running!")
    print(f"  Open your browser and go to:")
    print(f"  --> {URL}")
    print("=" * 50)
    print("\n  Press Ctrl+C to stop the server.\n")

    if not check_ollama():
        print("  WARNING: Ollama is not running.")
        print("  Start Ollama before generating podcasts.")
        print("  Download it at: https://ollama.com\n")


if __name__ == "__main__":
    t = threading.Thread(target=open_server_info)
    t.daemon = True
    t.start()

    app.run(host=HOST, port=PORT, debug=False)