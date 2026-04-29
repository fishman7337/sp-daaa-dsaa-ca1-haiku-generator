"""Bigram Markov model used by the haiku generator."""

import random
from typing import Protocol


class SupportsSyllableCount(Protocol):
    """Protocol for objects that can return a syllable count for a word."""

    def get_syllable_count(self, word: str) -> int:
        """Return the syllable count for ``word``."""


class MarkovChainModel:
    """Bigram-based Markov chain model with syllable constraints.

    The model trains on haiku lines, learns word transitions, and uses a small
    fallback vocabulary when the learned chain reaches a dead end. Generated
    lines avoid ending on weak grammar words such as ``the`` or ``in``.
    """

    def __init__(self) -> None:
        """Initialise the transition map and fallback vocabulary."""
        self.model: dict[str, list[str]] = {}
        self.fallback_words = [
            "the",
            "sun",
            "moon",
            "river",
            "mist",
            "breeze",
            "echo",
            "sky",
            "cloud",
            "light",
            "stone",
            "dream",
            "leaf",
            "wind",
            "dew",
            "dawn",
            "peace",
            "still",
            "stream",
            "glow",
            "twilight",
            "longing",
            "drift",
            "dance",
            "fade",
            "forest",
            "shade",
            "petal",
            "whisper",
            "soft",
            "bloom",
            "air",
            "space",
            "dust",
            "shimmer",
        ]
        self.disallowed_endings = {
            "the",
            "a",
            "an",
            "of",
            "and",
            "in",
            "on",
            "at",
            "by",
            "to",
            "for",
            "with",
            "from",
            "as",
        }

    def train(self, corpus: list[str]) -> None:
        """Train the Markov chain model using a corpus of haiku lines.

        Args:
            corpus: Haiku lines used to train the model.
        """
        for line in corpus:
            words = line.strip().split()

            for index in range(len(words) - 1):
                current = self._clean_word(words[index])
                next_word = words[index + 1]

                if current:
                    self.model.setdefault(current, []).append(next_word)

    def generate_line(
        self,
        max_syllables: int,
        syllable_counter: SupportsSyllableCount,
    ) -> str:
        """Generate a haiku line with a syllable limit.

        Args:
            max_syllables: Maximum number of syllables allowed in the line.
            syllable_counter: Object that can return syllable counts.

        Returns:
            A generated line, or a failure message if generation is unsuccessful.
        """
        for _ in range(15):
            line = self._attempt_line(max_syllables, syllable_counter)
            if line:
                return line

        return "[Failed to generate haiku line]"

    def _attempt_line(
        self,
        max_syllables: int,
        syllable_counter: SupportsSyllableCount,
    ) -> str:
        """Attempt to generate a haiku line within the syllable limit.

        Args:
            max_syllables: Maximum allowed syllables for the line.
            syllable_counter: Object that can return syllable counts.

        Returns:
            A generated line that fits the syllable constraint, or an empty string.
        """
        word = random.choice(list(self.model.keys()) + self.fallback_words)
        words = [word]
        syllable_total = syllable_counter.get_syllable_count(word)

        while syllable_total < max_syllables:
            next_candidates = self.model.get(self._clean_word(word), []) + self.fallback_words
            random.shuffle(next_candidates)

            for candidate in next_candidates:
                clean_candidate = self._clean_word(candidate)
                next_syllables = syllable_counter.get_syllable_count(clean_candidate)

                if syllable_total + next_syllables <= max_syllables:
                    words.append(candidate)
                    syllable_total += next_syllables
                    word = candidate
                    break
            else:
                break

        while self._clean_word(words[-1]) in self.disallowed_endings and len(words) > 1:
            words.pop()

        return self._final_format(words)

    @staticmethod
    def _clean_word(word: str) -> str:
        """Clean a word for consistent Markov and syllable lookups.

        Args:
            word: Word to clean.

        Returns:
            Lowercase word with common punctuation removed.
        """
        return word.lower().strip(".,!?;:\"'")

    @staticmethod
    def _final_format(words: list[str]) -> str:
        """Format the final haiku line.

        Args:
            words: Words forming the haiku line.

        Returns:
            A capitalised line, or an empty string if no words were given.
        """
        if not words:
            return ""

        formatted_words = words.copy()
        formatted_words[0] = formatted_words[0].capitalize()
        return " ".join(formatted_words)
