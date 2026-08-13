"""Entry point to launch the Castle Chess Tournament Application."""

# ==========================================
# IMPORTS & MAIN LAUNCHER
# ==========================================
from controllers.main_controller import MainController


def main() -> None:
    """Instantiates and launches the main application controller."""
    app = MainController()
    app.run()


if __name__ == "__main__":
    main()
