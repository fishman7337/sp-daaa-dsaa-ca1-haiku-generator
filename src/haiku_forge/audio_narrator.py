"""Audio narration support for haiku lines."""

import time
import wave
from pathlib import Path

from .paths import DEFAULT_AUDIO_DIR

try:
    import winsound
except ImportError:  # pragma: no cover - exercised on non-Windows CI runners.
    winsound = None


class HaikuAudioNarrator:
    """Narrate haiku using pre-recorded word-level WAV files.

    The class can play clips on Windows and can stitch available clips into a
    single ``.wav`` file on any platform supported by Python's ``wave`` module.
    Missing clips are reported and skipped.
    """

    def __init__(self, audio_folder: str | Path = DEFAULT_AUDIO_DIR) -> None:
        """Initialise the narrator.

        Args:
            audio_folder: Folder containing one ``.wav`` file per supported word.

        """
        self.audio_folder = Path(audio_folder)

    def _get_wav_path(self, word: str) -> Path:
        """Build the expected WAV path for a word.

        Args:
            word: Word to map to a WAV filename.

        Returns:
            Full path to the expected ``.wav`` file.

        """
        clean_word = word.lower().strip(".,!?;:\"'")
        return self.audio_folder / f"{clean_word}.wav"

    def _play_word(self, word: str) -> None:
        """Play the WAV file for a word when playback is available.

        Args:
            word: Word to play as audio.

        """
        filepath = self._get_wav_path(word)

        if not filepath.exists():
            print(f"[Missing: {word}] ", end="")
            return

        if winsound is None:
            print(f"[Playback unavailable: {word}] ", end="")
            return

        winsound.PlaySound(str(filepath), winsound.SND_FILENAME)
        time.sleep(0.05)

    def narrate(self, haiku_lines: list[str]) -> None:
        """Narrate a haiku line by line.

        Args:
            haiku_lines: Haiku lines to narrate audibly.

        """
        for index, line in enumerate(haiku_lines, start=1):
            print(f"\nLine {index}: {line}")

            for word in line.strip().split():
                self._play_word(word)

            time.sleep(0.2)

    def save_to_audio_file(self, haiku_lines: list[str], output_filename: str | Path) -> None:
        """Save the haiku as one stitched WAV file.

        Args:
            haiku_lines: Haiku lines to narrate and save.
            output_filename: Desired output filename, with or without ``.wav``.

        """
        output_path = Path(output_filename)
        if output_path.suffix.lower() != ".wav":
            output_path = output_path.with_suffix(".wav")

        word_paths = self._collect_existing_word_paths(haiku_lines)
        if not word_paths:
            print("No matching audio clips were found. Audio file was not created.")
            return

        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with wave.open(str(output_path), "wb") as output:
                params_set = False

                for word_path in word_paths:
                    with wave.open(str(word_path), "rb") as word_audio:
                        if not params_set:
                            output.setparams(word_audio.getparams())
                            params_set = True

                        output.writeframes(word_audio.readframes(word_audio.getnframes()))

            print(f"Haiku audio saved to '{output_path}'")

        except (OSError, wave.Error) as exc:
            print(f"Failed to save audio: {exc}")

    def _collect_existing_word_paths(self, haiku_lines: list[str]) -> list[Path]:
        """Collect audio clip paths for words that have matching WAV files.

        Args:
            haiku_lines: Haiku lines to inspect.

        Returns:
            Paths to existing word-level audio clips, in narration order.

        """
        word_paths = []

        for line in haiku_lines:
            for word in line.strip().split():
                word_path = self._get_wav_path(word)
                if word_path.exists():
                    word_paths.append(word_path)
                else:
                    print(f"[Missing: {word}] - skipping")

        return word_paths
