from pathlib import Path

from haiku_forge.thesaurus import Thesaurus


def test_thesaurus_loads_synonyms_and_antonyms(tmp_path: Path) -> None:
    synonyms = tmp_path / "synonyms.txt"
    antonyms = tmp_path / "antonyms.txt"
    synonyms.write_text("red: crimson, rust\n", encoding="utf-8")
    antonyms.write_text("red: green, blue\n", encoding="utf-8")

    thesaurus = Thesaurus()
    thesaurus.load_synonyms(synonyms)
    thesaurus.load_antonyms(antonyms)

    assert thesaurus.synonyms == {"red": ["crimson", "rust"]}
    assert thesaurus.antonyms == {"red": ["green", "blue"]}


def test_thesaurus_returns_direct_and_reverse_antonyms() -> None:
    thesaurus = Thesaurus()
    thesaurus.synonyms = {"red": ["crimson"]}
    thesaurus.antonyms = {"red": ["green"]}

    assert thesaurus.get_random_antonym("red") == "green"
    assert thesaurus.get_random_antonym("crimson") == "green"
    assert thesaurus.get_random_antonym("unknown") is None


def test_thesaurus_returns_random_and_shortest_synonyms() -> None:
    thesaurus = Thesaurus()
    thesaurus.synonyms = {"autumn": ["fall", "equinox"]}

    assert thesaurus.get_random_synonym("autumn") in {"fall", "equinox"}
    assert thesaurus.get_shortest_synonym("autumn") == "fall"
    assert thesaurus.get_random_synonym("missing") is None
    assert thesaurus.get_shortest_synonym("missing") is None
