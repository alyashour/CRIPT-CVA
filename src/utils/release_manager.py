import os
import sys

import requests
import zipfile
from io import BytesIO
from version import version

def _is_executable():
    return getattr(sys, 'frozen', False)

def download_release(release_url):
    """
    Download the latest release from the provided URL and apply it.
    """
    try:
        # Step 1: Download the release zip file
        response = requests.get(release_url)
        response.raise_for_status()
        zip_file = BytesIO(response.content)

        # Step 2: Extract the zip contents into the parent folder
        if _is_executable():
            exe_path = sys.executable
            app_path = os.path.dirname(os.path.dirname(os.path.dirname(exe_path)))
            app_dir = os.path.dirname(app_path)
        else:
            raise Exception("Do not update source. Updater is only for executables.")

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(app_dir)

        # make sure the executable is a unix executable and not a document (extraction bug in ZipFile)
        # consider contributing to ZipFile to fix the issue
        os.chmod(os.path.join(app_dir, 'criptcva.app', 'Contents', 'MacOS', 'main'), 0o755)

        # Step 3: Rename old version
        old_app_path = os.path.join(app_dir, f'old_v{current_version}.app')
        if os.path.exists(old_app_path):
            os.remove(old_app_path)  # Clean up any previous old version
        os.rename(app_path, old_app_path)

        print("Update downloaded and applied successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the release: {e}")
        raise e
