"""Core haiku transformation workflows used by the interactive menu."""

from collections.abc import Callable
from itertools import product
from pathlib import Path

from .ai_generator import AIHaikuGenerator
from .audio_narrator import HaikuAudioNarrator
from .file_handler import FileHandler
from .input_utils import InputValidator
from .keyword_utils import KeywordIndex
from .paths import DEFAULT_AUDIO_DIR
from .thesaurus import Thesaurus
from .tokenized_utils import TokenizedLine

ReplacementFunction = Callable[[str], str | None]
RedoFunction = Callable[[], object | None]


class Haiku:
    """Processing engine for haiku transformation, generation, and narration."""

    def __init__(self) -> None:
        """Initialise the processing engine and shared input validator."""
        self.validator = InputValidator()

    def _is_haiku_file(self, path: str | Path) -> bool:
        """Return whether a file appears to contain a haiku rather than a thesaurus.

        Args:
            path: File path to inspect.

        Returns:
            ``True`` when no line contains a colon; otherwise ``False``.

        """
        try:
            with Path(path).open("r", encoding="utf-8") as file:
                return not any(":" in line for line in file)
        except OSError:
            return False

    def _is_thesaurus_file(self, path: str | Path) -> bool:
        """Return whether a file appears to contain thesaurus mappings.

        Args:
            path: File path to inspect.

        Returns:
            ``True`` when at least one line contains a colon; otherwise ``False``.

        """
        try:
            with Path(path).open("r", encoding="utf-8") as file:
                return any(":" in line for line in file)
        except OSError:
            return False

    def _prompt_haiku_file(self, prompt: str) -> str:
        """Prompt until the user provides a valid haiku file.

        Args:
            prompt: Prompt message shown to the user.

        Returns:
            Valid haiku file path.

        """
        while True:
            path = self.validator.prompt_for_existing_file(prompt)
            if self._is_haiku_file(path):
                return path

            print("That isn't a haiku file. Please select a haiku.")

    def _prompt_thesaurus_file(self, prompt: str) -> str:
        """Prompt until the user provides a valid thesaurus file.

        Args:
            prompt: Prompt message shown to the user.

        Returns:
            Valid thesaurus file path.

        """
        while True:
            path = self.validator.prompt_for_existing_file(prompt)
            if self._is_thesaurus_file(path):
                return path

            print("That isn't a thesaurus file. Please select a thesaurus.")

    def save_and_redo(self, haiku_lines: list[str], redo_function: RedoFunction) -> None:
        """Offer to save generated text and repeat the current workflow.

        Args:
            haiku_lines: Generated or transformed haiku lines.
            redo_function: Function to call if the user wants another attempt.

        """
        self.validator.wait_for_enter()

        save_choice = self.validator.get_yes_or_no("Do you want to save the text file? y/n: ")
        if save_choice == "y":
            new_filename = self.validator.prompt_for_new_filename("Please enter new filename: ")
            try:
                FileHandler.write_haiku(new_filename, haiku_lines)
                print(f'The text has been saved in "{new_filename}"')
            except OSError as exc:
                print(f"Failed to save. Error: {exc}")

        self.validator.wait_for_enter()

        redo_choice = self.validator.get_yes_or_no("Do you want to give this another try? y/n: ")
        if redo_choice == "y":
            redo_function()

    def display_haiku(self, title: str, haiku_lines: list[str]) -> None:
        """Display a titled haiku block.

        Args:
            title: Banner text shown above the haiku.
            haiku_lines: Lines to display.

        """
        print(f"\n\n{title}")
        print("-" * 30)
        for line in haiku_lines:
            print(line)

    def _load_haiku_and_synonyms(self) -> tuple[list[str], Thesaurus]:
        """Load a haiku file and synonym thesaurus selected by the user.

        Returns:
            Loaded haiku lines and a thesaurus containing synonyms.

        """
        haiku_file = self._prompt_haiku_file(
            "Select the Haiku you want to process\nPlease enter input file: "
        )
        synonyms_file = self._prompt_thesaurus_file(
            "Select a synonym thesaurus.\nPlease enter input file: "
        )
        self.validator.wait_for_enter()

        thesaurus = Thesaurus()
        thesaurus.load_synonyms(synonyms_file)
        return FileHandler.read_haiku(haiku_file), thesaurus

    def _load_haiku_synonyms_antonyms(self) -> tuple[list[str], Thesaurus]:
        """Load a haiku file plus synonym and antonym thesauruses.

        Returns:
            Loaded haiku lines and a thesaurus containing synonyms and antonyms.

        """
        haiku_file = self._prompt_haiku_file(
            "Select the Haiku you want to process\nPlease enter input file: "
        )
        synonyms_file = self._prompt_thesaurus_file(
            "Select a synonym thesaurus.\nPlease enter input file: "
        )
        antonyms_file = self._prompt_thesaurus_file(
            "Select an antonym thesaurus.\nPlease enter input file: "
        )
        self.validator.wait_for_enter()

        thesaurus = Thesaurus()
        thesaurus.load_synonyms(synonyms_file)
        thesaurus.load_antonyms(antonyms_file)
        return FileHandler.read_haiku(haiku_file), thesaurus

    def process_haiku(
        self,
        haiku_lines: list[str],
        replacement_function: ReplacementFunction,
    ) -> list[str]:
        """Apply a replacement function to every replaceable word in a haiku.

        Args:
            haiku_lines: Original haiku lines to process.
            replacement_function: Function that receives a lowercase word and
                returns a replacement, or ``None`` to leave it unchanged.

        Returns:
            Processed haiku lines with punctuation and capitalisation preserved.

        """
        processed_lines = []

        for raw_line in haiku_lines:
            token_line = TokenizedLine(raw_line)

            for index, (prefix, core, suffix) in enumerate(token_line.tokens):
                replacement = replacement_function(core.lower())
                if replacement is None:
                    continue

                if core[:1].isupper():
                    replacement = replacement.capitalize()

                token_line.tokens[index] = (prefix, replacement, suffix)

            processed_lines.append(token_line.reconstruct())

        return processed_lines

    def synonymize_haiku(self) -> None:
        """Create a new haiku by replacing keywords with random synonyms."""
        haiku_lines, thesaurus = self._load_haiku_and_synonyms()

        def perform_synonymization() -> None:
            self.display_haiku("The Haiku before processing:", haiku_lines)
            processed = self.process_haiku(haiku_lines, thesaurus.get_random_synonym)
            self.display_haiku("The Synonymized Haiku after processing:", processed)
            self.save_and_redo(processed, perform_synonymization)

        perform_synonymization()

    def zen_ize_haiku(self) -> None:
        """Create a compact haiku by replacing keywords with shortest synonyms."""
        haiku_lines, thesaurus = self._load_haiku_and_synonyms()

        def perform_zenization() -> None:
            self.display_haiku("The Haiku before processing:", haiku_lines)
            processed = self.process_haiku(haiku_lines, thesaurus.get_shortest_synonym)
            self.display_haiku("The Zen-ized Haiku after processing:", processed)
            self.save_and_redo(processed, perform_zenization)

        perform_zenization()

    def antonymize_haiku(self) -> None:
        """Create a contrasting haiku by replacing keywords with antonyms."""
        haiku_lines, thesaurus = self._load_haiku_synonyms_antonyms()

        def perform_antonymization() -> None:
            self.display_haiku("The Haiku before processing:", haiku_lines)
            processed = self.process_haiku(haiku_lines, thesaurus.get_random_antonym)
            self.display_haiku("The Antonymized Haiku after processing:", processed)
            self.save_and_redo(processed, perform_antonymization)

        perform_antonymization()

    def batch_processing(self) -> None:
        """Generate all synonym permutations for a haiku and save them as files."""
        haiku_file = self._prompt_haiku_file(
            "Select the Haiku you want to process\nPlease enter input file: "
        )
        synonyms_file = self._prompt_thesaurus_file(
            "Select a synonym thesaurus.\nPlease enter input file: "
        )
        output_folder = self.validator.prompt_for_existing_folder(
            "Select an existing folder to store the generated haiku files\n"
            "Please enter the folder name: "
        )
        self.validator.wait_for_enter()

        raw_lines = FileHandler.read_haiku(haiku_file)
        tokenized_lines = [TokenizedLine(line) for line in raw_lines]

        thesaurus = Thesaurus()
        thesaurus.load_synonyms(synonyms_file)
        keyword_index = self._build_keyword_index(tokenized_lines, thesaurus)

        positions = list(keyword_index.items())
        if not positions:
            print("\nNo keywords found in the haiku that match the thesaurus.")
            return

        print("\nBatch processing started!")
        synonym_lists = [synonyms for _, synonyms in positions]

        for counter, combination in enumerate(product(*synonym_lists), start=1):
            output_lines = self._render_batch_combination(
                tokenized_lines,
                positions,
                combination,
            )
            FileHandler.write_haiku(Path(output_folder) / f"v{counter}.txt", output_lines)
            print(".", end="", flush=True)

        print(f"\nBatch processing completed with {counter} permutations")
        self.validator.wait_for_enter()

    @staticmethod
    def _build_keyword_index(
        tokenized_lines: list[TokenizedLine],
        thesaurus: Thesaurus,
    ) -> KeywordIndex:
        """Build an index of token positions that have synonym replacements.

        Args:
            tokenized_lines: Tokenised haiku lines.
            thesaurus: Loaded thesaurus.

        Returns:
            Keyword index used by batch processing.

        """
        keyword_index = KeywordIndex()

        for line_index, tokenized_line in enumerate(tokenized_lines):
            for token_index, (_, core, _) in enumerate(tokenized_line.tokens):
                synonyms = thesaurus.synonyms.get(core.lower())
                if synonyms:
                    keyword_index.add(line_index, token_index, synonyms)

        return keyword_index

    @staticmethod
    def _render_batch_combination(
        tokenized_lines: list[TokenizedLine],
        positions: list[tuple[tuple[int, int], list[str]]],
        combination: tuple[str, ...],
    ) -> list[str]:
        """Render one batch-processing synonym combination.

        Args:
            tokenized_lines: Original tokenised haiku lines.
            positions: Token positions that should be replaced.
            combination: Replacement words for this permutation.

        Returns:
            Rendered haiku lines for the permutation.

        """
        copied_lines = [line.copy() for line in tokenized_lines]

        for replacement_index, ((line_index, token_index), _) in enumerate(positions):
            prefix, original_word, suffix = copied_lines[line_index].tokens[token_index]
            replacement = combination[replacement_index]

            if original_word[:1].isupper():
                replacement = replacement.capitalize()

            copied_lines[line_index].tokens[token_index] = (prefix, replacement, suffix)

        return [line.reconstruct() for line in copied_lines]

    def ai_modified_haiku(self) -> None:
        """Generate a new haiku using a syllable-aware Markov model."""
        print("\n\nAI Haiku Generator")

        training_file = self._prompt_haiku_file("Enter haiku training file: ")
        self.validator.wait_for_enter()

        generator = AIHaikuGenerator()
        generator.train_model(FileHandler.read_haiku(training_file))

        def generate_once() -> None:
            haiku = generator.generate_haiku()
            self.display_haiku("AI-Modified Haiku", haiku)
            self.save_and_redo(haiku, generate_once)

        generate_once()

    def haiku_narrate(self) -> None:
        """Narrate a haiku word by word using matching WAV files."""

        def perform_narration() -> None:
            haiku_file = self._prompt_haiku_file("Enter the haiku file to narrate: ")
            self.validator.wait_for_enter()

            haiku_lines = FileHandler.read_haiku(haiku_file)
            self.display_haiku("Haiku to Narrate", haiku_lines)

            narrator = HaikuAudioNarrator(audio_folder=DEFAULT_AUDIO_DIR)
            narrator.narrate(haiku_lines)

            if self.validator.get_yes_or_no("Save audio to file? y/n: ") == "y":
                filename = self.validator.prompt_for_new_filename(
                    "Enter output audio filename (without .wav): "
                )
                narrator.save_to_audio_file(haiku_lines, filename)

            self.validator.wait_for_enter()

            if self.validator.get_yes_or_no("Narrate another haiku? y/n: ") == "y":
                perform_narration()

        perform_narration()
