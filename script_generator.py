import ollama
from pathlib import Path


SYSTEM_PROMPT = """
You are a podcast script writer. Your job is to convert document text into 
a natural, engaging two-host podcast script between Host A and Host B.

Rules:
- Write in a conversational, friendly tone
- Alternate between Host A and Host B naturally
- Each line must start with either "Host A:" or "Host B:" exactly
- Host A leads the conversation and introduces topics
- Host B asks questions, adds insight, and reacts naturally
- Start with Host A's intro and end with both hosts signing off
- Avoid bullet points or lists — write it as spoken word only
- Keep it concise — aim for a 2 to 3 minute read total
- Do not include stage directions or sound effects
"""


def generate_script(text: str, model: str = "llama3.2:3b") -> str:
    prompt = f"""
Here is the document content:

{text[:3000]}

Convert this into a natural podcast script following the rules you were given.
"""

    print(f"Generating script using {model}...")

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    import sys
    from extractor import extract_text

    if len(sys.argv) < 2:
        print("Usage: python script_generator.py <path_to_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    print("Extracting text...")
    text = extract_text(file_path)
    print(f"Extracted {len(text)} characters\n")

    script = generate_script(text)

    print("\n--- Generated Podcast Script ---\n")
    print(script)
    print("\n--- End of Script ---")

    # Save script to file
    output_path = Path("output/podcast_script.txt")
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(script, encoding="utf-8")
    print(f"\nScript saved to {output_path}")