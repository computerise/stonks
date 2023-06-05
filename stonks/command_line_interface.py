"""User input and program output from the command line."""

from time import sleep


class CommandLineInterface:
    """Class for controlling the user interactions and program outputs via the command line."""

    outro_duration_seconds: int = 0

    def intro(version: str, authors: list[str]) -> None:
        """Introduce the application."""
        print(f"\nLaunching `stonks` version `{version}`.\n\nAuthored by:\n")
        print(*authors, sep=", ", end="\n\n")

    @classmethod
    def outro(cls, message: str) -> None:
        """Class method for printing exit method."""
        print(
            message,
            f"\nTerminating application in {cls.outro_duration_seconds} seconds...",
        )
        for remaining_seconds in list(range(cls.outro_duration_seconds + 1))[::-1]:
            if remaining_seconds == 0:
                print("Goodbye.")
                break
            print(remaining_seconds)
            sleep(1)
