"""Interactive command-line menu for HaikuForge AI."""

from .haiku_utils import Haiku
from .input_utils import InputValidator


class Menu:
    """Display and route the HaikuForge AI command-line menu.

    The Menu class provides static methods to:
        - Display the welcome screen.
        - Present the available feature options.
        - Validate menu choices.
        - Route the user to the relevant ``Haiku`` workflow.
        - Exit cleanly when requested.
    """

    @staticmethod
    def welcome() -> None:
        """Display the welcome screen in the assignment style.

        This method prints a decorative bordered welcome message that includes:
            - Module and application name.
            - Author and class details.
            - School and coursework context.
        """
        border = "*" * 58

        print("\n" + border)
        print("* {:<55}*".format("ST1507 DSAA: Welcome to:"))
        print("* {:<55}*".format(""))
        print("* {:<55}*".format("~ HaikuForge AI - Haiku Generator Application ~"))
        print("* {:<55}*".format("-" * 55))
        print("* {:<55}*".format(""))
        print("* {:<55}*".format("- Done by: Goh Kun Ming(2415691)"))
        print("* {:<55}*".format("- Class DAAA/FT/2A/02"))
        print("* {:<55}*".format("- Singapore Polytechnic, School of Computing"))
        print(border)

        InputValidator.wait_for_enter()

    @staticmethod
    def display_menu(options: dict[int, str]) -> None:
        """Display the list of available menu options.

        The menu is rendered in a readable format where each option is shown
        with its corresponding number and description.

        Args:
            options: Dictionary mapping option numbers to their descriptions.
        """
        choices = ",".join(str(key) for key in options)
        print(f"\n\nPlease select your choice: ({choices})")
        for key, label in options.items():
            print(f"\t{key}. {label}")

    @staticmethod
    def get_valid_choice(options: dict[int, str]) -> int:
        """Prompt the user until a valid menu choice is entered.

        This method ensures robust input handling by:
            - Accepting only digits.
            - Converting input to an integer.
            - Verifying the integer is one of the allowed menu keys.

        Args:
            options: Dictionary mapping valid menu choices to descriptions.

        Returns:
            A validated menu choice selected by the user.
        """
        while True:
            choice = input("Enter Choice: ").strip()

            if choice.isdigit() and int(choice) in options:
                return int(choice)

            print("Please enter a valid number from the menu.")

    @staticmethod
    def menu() -> None:
        """Run the main loop for the HaikuForge AI menu system.

        This static method:
            - Displays the menu to the user.
            - Validates the user's menu selection.
            - Maps the selection to the corresponding ``Haiku`` method.
            - Continues running until the user chooses to exit.
        """
        haiku = Haiku()

        options = {
            1: "Synonymize Haiku",
            2: "Zen-ize Haiku",
            3: "Antonymize Haiku",
            4: "Batch Processing",
            5: "AI Modified Haiku",
            6: "Narrate Haiku",
            7: "Exit",
        }

        action_map = {
            1: haiku.synonymize_haiku,
            2: haiku.zen_ize_haiku,
            3: haiku.antonymize_haiku,
            4: haiku.batch_processing,
            5: haiku.ai_modified_haiku,
            6: haiku.haiku_narrate,
            7: Menu.exit_program,
        }

        while True:
            Menu.display_menu(options)
            choice = Menu.get_valid_choice(options)

            try:
                result = action_map[choice]()

                if result:
                    print(result)
                    InputValidator.wait_for_enter()

            except Exception as e:
                print(f"An error occurred: {e}")
                InputValidator.wait_for_enter()

    @staticmethod
    def exit_program() -> None:
        """Print the exit message and terminate the program.

        This method is typically called when the user selects the "Exit" option
        from the menu. It cleanly ends the session with a farewell message.
        """
        print("\n\nBye, thanks for using ST1507 DSAA: HaikuForge AI\n\n")
        raise SystemExit(0)
