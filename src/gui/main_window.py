import tkinter as tk
from utils.version_utils import check_for_update
from gui.update_window import show_update_window
from src import __version__


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title(f"Crypt CVA App {__version__}")

        # Add title
        self.label = tk.Label(self, text="Welcome to My Application!")
        self.label.pack(pady=20)

        # Check for updates when the application starts
        self.check_for_updates()

    def close_app(self):
        self.destroy()

    def check_for_updates(self):
        """Check for updates and show the update window if available."""
        latest_version, release_url = check_for_update()
        if latest_version:
            show_update_window(self, latest_version, release_url)
        else:
            print("No update available.")


# Run the main application
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
