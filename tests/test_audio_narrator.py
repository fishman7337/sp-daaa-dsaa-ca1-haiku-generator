import wave
from pathlib import Path

from haiku_forge.audio_narrator import HaikuAudioNarrator


def _write_tiny_wav(path: Path) -> None:
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(1)
        wav_file.setframerate(8000)
        wav_file.writeframes(b"\x80" * 8)


def test_save_to_audio_file_stitches_existing_word_clips(tmp_path: Path) -> None:
    audio_dir = tmp_path / "audio"
    audio_dir.mkdir()
    _write_tiny_wav(audio_dir / "sun.wav")
    _write_tiny_wav(audio_dir / "moon.wav")

    output_file = tmp_path / "out" / "narration"
    narrator = HaikuAudioNarrator(audio_folder=audio_dir)

    narrator.save_to_audio_file(["Sun moon", "missing"], output_file)

    assert output_file.with_suffix(".wav").is_file()
