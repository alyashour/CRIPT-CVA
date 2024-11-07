import requests
from packaging import version
from src import __version__
current_version = __version__

def check_for_update():
    """
    Check if there is a newer version available on GitHub.
    This compares the current version with the latest release.
    """
    # GitHub API URL for fetching the latest release info
    url = "https://api.github.com/repos/alyashour/CRIPT-CVA/releases/latest"

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Get the latest version info from the release
        latest_release = response.json()
        latest_version = latest_release['tag_name']  # Example: v0.2.0
        release_url = latest_release['assets'][0]['browser_download_url']  # URL for the download

        # Compare versions
        if version.parse(latest_version) > version.parse(current_version):
            return latest_version, release_url
        else:
            return None, None  # No update needed
    except requests.exceptions.RequestException as e:
        print(f"Error checking for update: {e}")
        return None, None
