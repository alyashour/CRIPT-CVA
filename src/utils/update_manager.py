import logging
import os
import sys
from utils.release_manager import download_release
from tkinter import messagebox

# Set up logging
logging.basicConfig(level=logging.INFO)


def perform_update(release_url):
    """Handle the update process: check for updates, download and apply."""
    try:
        logging.info("Checking for updates...")

        # Download the release
        logging.info(f"Downloading the update from {release_url}...")
        download_release(release_url)

        # Notify the user
        logging.info("Update downloaded successfully!")

        # You might trigger a restart or any other post-update action here
        messagebox.showinfo("Update Success", "The application has been updated successfully!")

    except Exception as e:
        logging.error(f"Error during the update process: {e}")
        messagebox.showerror("Update Failed", "There was an error while updating the application.")

def restart_app():
    """Restart the application after the update."""
    print("Restarting the application...")
    python = sys.executable
    os.execv(python, ['python'] + sys.argv)  # Restart the application with the same arguments
