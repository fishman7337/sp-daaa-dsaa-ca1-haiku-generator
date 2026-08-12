"""Synonym and antonym lookup utilities for haiku transformations."""

import random
from pathlib import Path

from .file_handler import FileHandler


class Thesaurus:
    """Manage synonyms and antonyms loaded from text files.

    The expected file format is one mapping per line:
        ``keyword: word1, word2, word3``

    Dictionaries are stored in lowercase to make lookups stable regardless of
    the input haiku capitalisation.
    """

    def __init__(self) -> None:
        """Initialise an empty thesaurus."""
        self.synonyms: dict[str, list[str]] = {}
        self.antonyms: dict[str, list[str]] = {}

    def load_synonyms(self, file_path: str | Path) -> None:
        """Load synonym data from a thesaurus file.

        Args:
            file_path: Path to the synonym thesaurus text file.

        """
        self.synonyms = FileHandler.load_thesaurus(file_path)

    def load_antonyms(self, file_path: str | Path) -> None:
        """Load antonym data from a thesaurus file.

        Args:
            file_path: Path to the antonym thesaurus text file.

        """
        self.antonyms = FileHandler.load_thesaurus(file_path)

    def get_random_synonym(self, word: str) -> str | None:
        """Return a random synonym for a keyword.

        Args:
            word: Keyword to look up.

        Returns:
            A randomly selected synonym, or ``None`` if the keyword is missing.

        """
        synonym_list = self.synonyms.get(word.lower())
        if not synonym_list:
            return None

        return random.choice(synonym_list)

    def get_shortest_synonym(self, word: str) -> str | None:
        """Return one of the shortest synonyms for a keyword.

        Args:
            word: Keyword to look up.

        Returns:
            A randomly selected shortest synonym, or ``None`` if the keyword is
            missing.

        """
        synonym_list = self.synonyms.get(word.lower())
        if not synonym_list:
            return None

        min_length = min(len(synonym) for synonym in synonym_list)
        shortest_synonyms = [synonym for synonym in synonym_list if len(synonym) == min_length]
        return random.choice(shortest_synonyms)

    def get_random_antonym(self, word_or_synonym: str) -> str | None:
        """Return a random antonym for a keyword or known synonym.

        Lookup is direct when ``word_or_synonym`` is an antonym key. If the input
        is one of the loaded synonyms, the method finds the original keyword and
        returns one of that keyword's antonyms.

        Args:
            word_or_synonym: Keyword or synonym to look up.

        Returns:
            A randomly selected antonym, or ``None`` if no match is found.

        """
        lookup_word = word_or_synonym.lower()

        direct_antonyms = self.antonyms.get(lookup_word)
        if direct_antonyms:
            return random.choice(direct_antonyms)

        for keyword, synonym_list in self.synonyms.items():
            if lookup_word in synonym_list and keyword in self.antonyms:
                return random.choice(self.antonyms[keyword])

        return None
