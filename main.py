"""Application entry point."""
import time
from stonks.configuration import ApplicationSettings
from stonks.manager import ApplicationManager


def intro(version, authors):
    """Introduce the application."""
    print(f"Launching 'stonks' version {version}.\nAuthored by:\n")
    print(*authors, sep=", ")


def main():
    """Launch application."""
    app_settings = ApplicationSettings().load_config()
    intro(
        app_settings.get("application").get("version"),
        app_settings.get("application").get("authors"),
    )
    manager = ApplicationManager()
    print(manager.start())
    time.sleep(5)


if __name__ == "__main__":
    main()
