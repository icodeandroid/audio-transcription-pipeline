import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def transcribe_with_timestamps(audio_file: str):
    with open(audio_file, "rb") as file:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )

    return {
        "text": result.text,
        "segments": [
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            }
            for segment in result.segments
        ]
    }


if __name__ == "__main__":
    result = transcribe_with_timestamps("sample.mp3")
    print(result)
