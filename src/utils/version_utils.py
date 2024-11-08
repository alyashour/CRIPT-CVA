import requests
from packaging import version
from src import __version__ as current_version

def check_for_update():
    """
    Checks GitHub for the latest version and compares it to the current version.
    """
    url = "https://api.github.com/repos/alyashour/CRIPT-CVA/releases/latest"
    try:
        response = requests.get(url)
        response.raise_for_status()
        latest_release = response.json()
        latest_version = latest_release['tag_name']
        release_url = latest_release['assets'][0]['browser_download_url']

        if version.parse(latest_version) > version.parse(current_version):
            return latest_version, release_url
        return None, None  # No update needed

    except requests.exceptions.RequestException as e:
        print(f"Error checking for update: {e}")
        return None, None
