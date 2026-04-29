from pathlib import Path

from haiku_forge.file_handler import FileHandler


def test_read_and_write_haiku_round_trip(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "haiku.txt"
    lines = ["Last gust of autumn.", "Red, yellow, brown unite.", "Carpet under trees"]

    FileHandler.write_haiku(target, lines)

    assert FileHandler.read_haiku(target) == lines


def test_load_thesaurus_normalises_values_and_splits_first_colon(tmp_path: Path) -> None:
    thesaurus_file = tmp_path / "synonyms.txt"
    thesaurus_file.write_text(
        "Sun: glow, Light\nnote: value:with:colon, plain\ninvalid line\n",
        encoding="utf-8",
    )

    assert FileHandler.load_thesaurus(thesaurus_file) == {
        "sun": ["glow", "light"],
        "note": ["value:with:colon", "plain"],
    }
