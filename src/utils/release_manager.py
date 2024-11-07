import os
import requests
import zipfile
import shutil
from io import BytesIO


def download_release(release_url):
    """
    Download the latest release from the provided URL and apply it.
    """
    try:
        response = requests.get(release_url)
        response.raise_for_status()

        # For a .zip file, for example
        zip_file = BytesIO(response.content)
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # Extract the contents of the zip to the current directory (or a specific folder)
            extract_path = os.path.join(os.getcwd(), 'new_version')
            zip_ref.extractall(extract_path)

        # Optional: Replace old version with new version
        old_version_folder = os.path.join(os.getcwd(), 'old_version')
        if os.path.exists(old_version_folder):
            shutil.rmtree(old_version_folder)
        os.rename(extract_path, old_version_folder)

        # You can also implement logic to move or update specific files (like replacing the app binary, etc.)

        print("Update downloaded and applied successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the release: {e}")
        raise e
