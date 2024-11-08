import logging
import os
from os.path import dirname
import subprocess
import sys
from tkinter import messagebox
from utils.release_manager import download_release

# Set up logging
logging.basicConfig(level=logging.INFO)

def perform_update(latest_version, release_url) -> bool:
    """Handles the update process: check for updates, download, and apply."""
    if latest_version and release_url:
        try:
            logging.info(f"Downloading update for version {latest_version}...")
            download_release(release_url)
            logging.info("Update downloaded successfully!")
            messagebox.showinfo("Update Successful", "The update has been downloaded successfully!")
            do_restart = messagebox.askyesno("Restart App?", "Would you like to restart immediately?")
            if do_restart:
                restart_app()
        except Exception as e:
            logging.error(f"Error during the update process: {e}")
            messagebox.showerror("Update Failed", f"There was an error updating the application.\n{e}")
            return False
    else:
        logging.info("No updates available.")

    return True

def restart_app():
    """Restarts the application after the update."""
    executable_path = os.path.join(dirname(dirname(dirname(dirname(sys.executable)))), 'main.app')
    if os.path.isdir(executable_path) and os.access(executable_path, os.X_OK):
        messagebox.showinfo("Restarting", f"Restarting the app from: {executable_path}")
        # Use subprocess to restart the app as an executable
        subprocess.Popen(["/usr/bin/open", "-a", executable_path], start_new_session=True)
    else:
        messagebox.showerror(
            "Error",
            "Could not find the app executable to restart.\n"
            "Please close and open manually."
        )