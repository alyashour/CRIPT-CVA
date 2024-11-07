import tkinter as tk
from tkinter import messagebox
from utils.update_manager import perform_update  # Importing the update logic


class UpdateWindow(tk.Toplevel):
    """Popup window to notify the user about an update."""

    def __init__(self, parent, latest_version, release_url):
        super().__init__(parent)
        self.title("Update Available")
        self.geometry("300x150")

        # Message to notify the user about the new version
        message = f"A new version ({latest_version}) is available!\nDo you want to update?"

        label = tk.Label(self, text=message, wraplength=250)
        label.pack(pady=20)

        # Button to trigger the update
        update_button = tk.Button(self, text="Update", command=lambda: self.initiate_update(release_url))
        update_button.pack(pady=5)

        # Button to close the window without updating
        close_button = tk.Button(self, text="Later", command=self.destroy)
        close_button.pack(pady=5)

    def initiate_update(self, release_url):
        """Initiate the update by calling the update manager to download and apply the update."""
        perform_update(release_url)
        self.destroy()
        messagebox.showinfo("Update Completed", "The application has been updated!")


# Function to create and display the update window
def show_update_window(parent, latest_version, release_url):
    """Show the update window to notify the user about the new version."""
    update_window = UpdateWindow(parent, latest_version, release_url)
    update_window.grab_set()  # Make it modal (blocks interaction with the parent)
    update_window.wait_window()  # Wait until the user interacts with the window
