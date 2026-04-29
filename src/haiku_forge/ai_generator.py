"""Syllable-aware Markov haiku generator."""

from .ai_markov import MarkovChainModel
from .ai_syllables import SyllableCounter
from .file_handler import FileHandler
from .input_utils import InputValidator


class AIHaikuGenerator:
    """Generate haiku using a Markov chain and syllable-aware constraints.

    The generator trains on user-selected haiku lines and creates three-line
    output with 5, 7, and 5 syllable targets.
    """

    def __init__(self) -> None:
        """Initialise the generator with model, syllable, and input helpers."""
        self.markov_model = MarkovChainModel()
        self.syllable_counter = SyllableCounter()
        self.validator = InputValidator()

    def train_model(self, haiku_lines: list[str]) -> None:
        """Train the internal Markov chain model.

        Args:
            haiku_lines: Haiku lines used as training data.
        """
        self.markov_model.train(haiku_lines)

    def generate_haiku(self) -> list[str]:
        """Generate a three-line haiku with a 5-7-5 syllable target.

        Returns:
            The generated haiku lines.
        """
        first = self.markov_model.generate_line(5, self.syllable_counter)
        second = self.markov_model.generate_line(7, self.syllable_counter)

        attempts = 0
        while True:
            third = self.markov_model.generate_line(5, self.syllable_counter)
            if third != first or attempts >= 3:
                break
            attempts += 1

        return [
            first.rstrip(".") + ".",
            second.rstrip(".") + ".",
            third.rstrip("."),
        ]

    def run_extra_feature_six(self) -> None:
        """Run the interactive AI haiku generation workflow."""
        print("\n\n=== AI Haiku Generator ===")

        path = self.validator.prompt_for_existing_file("Please enter the training haiku file: ")
        haiku_lines = FileHandler.read_haiku(path)
        self.train_model(haiku_lines)

        try:
            result = self.generate_haiku()
            print("\nAI-Generated Haiku")
            print("-" * 30)
            for line in result:
                print(line)

            self.validator.wait_for_enter()
            if self.validator.get_yes_or_no("Would you like to save the haiku? y/n: ") == "y":
                filename = self.validator.prompt_for_new_filename("Enter filename to save: ")
                FileHandler.write_haiku(filename, result)
                print(f"Haiku saved to '{filename}'.")

            self.validator.wait_for_enter()
            if self.validator.get_yes_or_no("Generate another haiku? y/n: ") == "y":
                self.run_extra_feature_six()

        except Exception as exc:
            print(f"Failed to generate haiku: {exc}")
