from pathlib import Path

SUPPORTED_FORMATS = {".wav", ".mp3", ".m4a"}


def accept_audio_file(file_path: str):
    file = Path(file_path)

    if not file.exists():
        raise FileNotFoundError("Audio file not found")

    if file.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(
            "Unsupported format. Please provide WAV, MP3, or M4A."
        )

    return {
        "filename": file.name,
        "format": file.suffix.lower(),
        "path": str(file)
    }


if __name__ == "__main__":
    audio = accept_audio_file("sample.mp3")
    print(audio)
