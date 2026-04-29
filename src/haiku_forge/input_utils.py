"""Reusable validation helpers for interactive command-line prompts."""

from pathlib import Path


class InputValidator:
    """Utility class for common user input validation tasks.

    This class provides static methods to:
        - Prompt for valid existing files or folders.
        - Prompt for a new filename with overwrite confirmation.
        - Prompt for yes/no answers with strict validation.
        - Pause execution until Enter is pressed.
    """

    @staticmethod
    def wait_for_enter() -> None:
        """Prompt the user to press only the Enter key to continue.

        The prompt repeats if the user types anything else, keeping pauses explicit
        during demonstrations and marking workflows.
        """
        while True:
            confirm = input("\n\nPress Enter to continue....")
            if confirm == "":
                break

    @staticmethod
    def get_yes_or_no(prompt: str) -> str:
        """Prompt the user for a yes/no response until ``y`` or ``n`` is entered.

        Args:
            prompt: Prompt message shown to the user.

        Returns:
            The validated response, either ``"y"`` or ``"n"``.
        """
        while True:
            response = input(f"\n\n{prompt}").strip().lower()
            if response in ("y", "n"):
                return response

            print("Please enter 'y' or 'n'.")

    @staticmethod
    def prompt_for_existing_file(prompt_message: str) -> str:
        """Prompt the user until a valid existing file is provided.

        Args:
            prompt_message: Message displayed when requesting a file path.

        Returns:
            A valid file path that exists on the system.
        """
        while True:
            path = input(f"\n\n{prompt_message}").strip()

            if not path:
                print("No file name entered. Please try again.")
                continue

            if not Path(path).is_file():
                print("File not found. Please try again.")
                continue

            return path

    @staticmethod
    def prompt_for_existing_folder(prompt_message: str) -> str:
        """Prompt the user until a valid existing directory is entered.

        Args:
            prompt_message: Message displayed when requesting the folder path.

        Returns:
            A valid folder path that exists on the system.
        """
        while True:
            path = input(f"\n\n{prompt_message}").strip()

            if not path:
                print("No folder name entered. Please try again.")
                continue

            if not Path(path).is_dir():
                print("Folder not found. Please try again.")
                continue

            return path

    @staticmethod
    def prompt_for_new_filename(prompt_message: str) -> str:
        """Prompt the user to enter a writable filename.

        If the specified file already exists, the user is asked whether to overwrite it.

        Args:
            prompt_message: Message displayed when prompting the user for input.

        Returns:
            A valid filename for writing output.
        """
        while True:
            output_file = input(f"{prompt_message}").strip()

            if not output_file:
                print("No file name entered. Please try again.")
                continue

            if Path(output_file).exists():
                overwrite = InputValidator.get_yes_or_no(
                    f"'{output_file}' already exists. Overwrite? y/n: "
                )
                if overwrite == "n":
                    continue

            return output_file
