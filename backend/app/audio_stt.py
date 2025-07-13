import whisper
model = whisper.load_model("base")

def transcribe_audio(audio_chunk: bytes) -> str:
    """
    Transcribe audio bytes using Whisper.
    """
    # write bytes to temp file
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".webm") as f:
        f.write(audio_chunk)
        f.flush()
        result = model.transcribe(f.name)
    return result["text"]
