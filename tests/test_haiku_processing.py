from haiku_forge.haiku_utils import Haiku
from haiku_forge.thesaurus import Thesaurus
from haiku_forge.tokenized_utils import TokenizedLine


def test_tokenized_line_preserves_wrapping_punctuation() -> None:
    tokenized = TokenizedLine('"Red," leaves fall!')

    tokenized.tokens[0] = ('"', "Crimson", ',"')

    assert tokenized.reconstruct() == '"Crimson," leaves fall!'


def test_process_haiku_preserves_capitalisation_and_punctuation() -> None:
    haiku = Haiku()

    processed = haiku.process_haiku(
        ["Red, yellow leaves."],
        lambda word: {"red": "crimson", "yellow": "gold"}.get(word),
    )

    assert processed == ["Crimson, gold leaves."]


def test_batch_combination_preserves_original_capitalisation() -> None:
    tokenized_lines = [TokenizedLine("Red leaves")]
    positions = [((0, 0), ["crimson"])]

    rendered = Haiku._render_batch_combination(
        tokenized_lines,
        positions,
        ("crimson",),
    )

    assert rendered == ["Crimson leaves"]


def test_build_keyword_index_only_tracks_words_in_thesaurus() -> None:
    thesaurus = Thesaurus()
    thesaurus.synonyms = {"red": ["crimson"], "leaves": ["foliage"]}

    index = Haiku._build_keyword_index([TokenizedLine("Red leaves fall")], thesaurus)

    assert list(index.items()) == [
        ((0, 0), ["crimson"]),
        ((0, 1), ["foliage"]),
    ]
