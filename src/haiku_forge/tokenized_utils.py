"""Tokenisation helpers that preserve word punctuation."""

PUNCTUATION = ".,;:?!\"'"


class TokenizedLine:
    """Represent a haiku line as editable ``(prefix, core, suffix)`` tokens.

    This makes word replacement safe because punctuation around a word can be
    preserved while only the core word is substituted.
    """

    def __init__(self, raw_line: str) -> None:
        """Tokenise a raw line.

        Args:
            raw_line: Single haiku line to tokenise.

        """
        self.raw_line = raw_line
        self.tokens: list[tuple[str, str, str]] = []

        for word in raw_line.split():
            self.tokens.append(self._split_token(word))

    @staticmethod
    def _split_token(word: str) -> tuple[str, str, str]:
        """Split a word into leading punctuation, core text, and trailing punctuation.

        Args:
            word: Word-like token from a haiku line.

        Returns:
            A tuple of ``(prefix, core, suffix)``.

        """
        prefix = ""
        core = word
        suffix = ""

        while core and core[0] in PUNCTUATION:
            prefix += core[0]
            core = core[1:]

        while core and core[-1] in PUNCTUATION:
            suffix = core[-1] + suffix
            core = core[:-1]

        return prefix, core, suffix

    def reconstruct(self) -> str:
        """Reconstruct the line from its tokenized components.

        Returns:
            Reconstructed line with spacing and punctuation preserved.

        """
        return " ".join(f"{prefix}{core}{suffix}" for prefix, core, suffix in self.tokens)

    def copy(self) -> "TokenizedLine":
        """Create a copy with an independent token list.

        Returns:
            A new ``TokenizedLine`` with the same raw line and token data.

        """
        clone = TokenizedLine(self.raw_line)
        clone.tokens = self.tokens.copy()
        return clone
