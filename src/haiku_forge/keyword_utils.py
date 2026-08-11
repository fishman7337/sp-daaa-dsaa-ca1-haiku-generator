"""Index keyword positions inside tokenised haiku lines."""

from collections.abc import Iterator


class KeywordIndex:
    """Track token positions that should be replaced during batch generation."""

    def __init__(self) -> None:
        """Initialise an empty keyword index."""
        self._positions: dict[tuple[int, int], list[str]] = {}

    def add(self, line_idx: int, token_idx: int, synonyms_list: list[str]) -> None:
        """Record a token position and its possible replacement words.

        Args:
            line_idx: Zero-based line index.
            token_idx: Zero-based token index within the line.
            synonyms_list: Replacement words for the token.

        """
        self._positions[(line_idx, token_idx)] = synonyms_list

    def items(self) -> Iterator[tuple[tuple[int, int], list[str]]]:
        """Iterate over stored token positions and replacement lists.

        Yields:
            Tuples in the form ``((line_idx, token_idx), replacement_words)``.

        """
        yield from self._positions.items()
