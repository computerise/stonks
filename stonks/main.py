"""Application entry point."""
import time
from configure import ApplicationData


def intro(version, authors):
    print(f"Launching 'stonks' version {version}.\n")
    print(f"Authored by:\n")
    print(*authors, sep=", ")


def main():
    """Launch application."""
    app_data = ApplicationData()
    intro(app_data.version, app_data.authors)
    time.sleep(5)


if __name__ == "__main__":
    main()
