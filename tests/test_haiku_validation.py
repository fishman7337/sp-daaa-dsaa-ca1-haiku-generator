from pathlib import Path

from haiku_forge.haiku_utils import Haiku


def test_haiku_and_thesaurus_file_detection(tmp_path: Path) -> None:
    haiku_file = tmp_path / "haiku.txt"
    thesaurus_file = tmp_path / "synonyms.txt"
    haiku_file.write_text("line one\nline two\nline three\n", encoding="utf-8")
    thesaurus_file.write_text("line: one, two\n", encoding="utf-8")

    haiku = Haiku()

    assert haiku._is_haiku_file(haiku_file) is True
    assert haiku._is_haiku_file(thesaurus_file) is False
    assert haiku._is_thesaurus_file(thesaurus_file) is True
    assert haiku._is_thesaurus_file(haiku_file) is False
    assert haiku._is_haiku_file(tmp_path / "missing.txt") is False
