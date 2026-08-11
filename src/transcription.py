import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def transcribe_audio(audio_file: str) -> str:
    with open(audio_file, "rb") as file:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=file
        )

    return result.text.strip()


if __name__ == "__main__":
    text = transcribe_audio("sample.mp3")
    print(text)
