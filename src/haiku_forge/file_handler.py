"""File loading and saving helpers for haiku and thesaurus text files."""

from collections.abc import Iterable
from pathlib import Path


class FileHandler:
    """Utility class for handling project file operations.

    This class provides static methods to:
        - Read haiku lines from text files.
        - Write haiku lines to output text files.
        - Load thesaurus mappings into dictionaries.
        - Ensure output folders exist before saving files.
    """

    @staticmethod
    def read_haiku(filepath: str | Path) -> list[str]:
        """Read haiku lines from a text file.

        Each line in the file is stripped of leading/trailing whitespace.

        Args:
            filepath: Path to the haiku file.

        Returns:
            A list of haiku lines, each as a separate string.

        """
        with Path(filepath).open("r", encoding="utf-8") as file:
            return [line.strip() for line in file]

    @staticmethod
    def write_haiku(filepath: str | Path, haiku_lines: Iterable[str]) -> None:
        """Write haiku lines to a text file.

        Parent folders are created automatically so batch workflows can save into
        a newly prepared output directory.

        Args:
            filepath: Destination path where the haiku will be saved.
            haiku_lines: Lines to write.

        """
        path = Path(filepath)
        if path.parent != Path("."):
            path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8", newline="\n") as file:
            for line in haiku_lines:
                file.write(f"{line}\n")

    @staticmethod
    def load_thesaurus(filepath: str | Path) -> dict[str, list[str]]:
        """Load a thesaurus file into a dictionary mapping keywords to word lists.

        Each line in the file must be formatted as:
            keyword: word1, word2, word3, ...

        Args:
            filepath: Path to the thesaurus text file.

        Returns:
            A dictionary where each key is a keyword and each value is a list of
            associated words.

        """
        thesaurus = {}

        with Path(filepath).open("r", encoding="utf-8") as file:
            for line in file:
                if ":" not in line:
                    continue

                keyword, values = line.strip().split(":", maxsplit=1)
                clean_values = [
                    value.strip().lower() for value in values.split(",") if value.strip()
                ]

                if keyword.strip() and clean_values:
                    thesaurus[keyword.strip().lower()] = clean_values

        return thesaurus

    @staticmethod
    def ensure_folder_exists(folder_path: str | Path) -> None:
        """Ensure that the specified folder exists.

        Args:
            folder_path: Folder path to check or create.

        """
        Path(folder_path).mkdir(parents=True, exist_ok=True)
