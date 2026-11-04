"""
Talks to a model running locally in LM Studio (nothing goes to the cloud).

Before running:
  1. Open LM Studio, load a chat model (e.g. Qwen3 14B).
  2. Developer tab -> Start Server (it listens on http://localhost:1234).
  3. Run:  python openai_example.py
"""
import time

from openai import APIConnectionError, OpenAI

BASE_URL = "http://localhost:1234/v1"  # Ollama would be http://localhost:11434/v1
MODEL = None  # None = pick the first chat model LM Studio lists; or set e.g. "qwen3-14b"

# The key is ignored by LM Studio, but the library requires some value.
client = OpenAI(base_url=BASE_URL, api_key="not-needed")


def pick_model():
    models = [m.id for m in client.models.list().data]
    print("Models available:", ", ".join(models) or "(none)")
    if MODEL:
        return MODEL
    chat_models = [m for m in models if "embed" not in m.lower()]
    return chat_models[0] if chat_models else None


def main():
    try:
        model = pick_model()
    except APIConnectionError:
        print(f"Could not reach {BASE_URL}.")
        print("Is the LM Studio server running? (Developer tab -> Start Server)")
        return
    if not model:
        print("LM Studio is running but lists no chat models. Download or load one first.")
        return
    print(f"Using model: {model}\n")

    start = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "Explain what a Python decorator is in 3 sentences."},
        ],
        temperature=0.7,
    )
    elapsed = time.perf_counter() - start

    print(response.choices[0].message.content)
    usage = response.usage
    if usage:
        print(f"\n[{usage.completion_tokens} tokens in {elapsed:.1f}s, "
              f"{usage.completion_tokens / elapsed:.1f} tok/s including load and prompt time]")


if __name__ == "__main__":
    main()