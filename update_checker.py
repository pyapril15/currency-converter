import requests
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from threading import Thread
import tempfile
import shutil
import subprocess
import sys


def get_latest_release(user, repo):
    """Fetches the latest release information from GitHub API"""
    url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_file(url, path):
    """Downloads a file from the given URL to the specified path"""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)


def install_update(download_path):
    """Runs the installer or the new executable"""
    if sys.platform == "win32":
        # On Windows, use the os.startfile to run the installer
        os.startfile(download_path)
    else:
        # On other platforms, use subprocess to run the installer
        subprocess.Popen(['open', download_path])


def check_for_updates(user, repo, current_version):
    """Checks for updates and notifies the user if an update is available"""
    try:
        latest_release = get_latest_release(user, repo)
        latest_version = latest_release['tag_name']

        if current_version != latest_version:
            release_notes = latest_release['body']
            download_url = latest_release['assets'][0]['browser_download_url']

            root = tk.Tk()
            root.withdraw()  # Hide the root window

            message = f"A new version ({latest_version}) is available!\n\nRelease Notes:\n{release_notes}\n\nWould you like to download and install it now?"
            if messagebox.askyesno("Update Available", message):
                download_path = simpledialog.askstring("Download Path", "Enter the download path:",
                                                       initialvalue=tempfile.gettempdir())
                if download_path:
                    download_file_path = os.path.join(download_path, os.path.basename(download_url))
                    Thread(target=download_and_install, args=(download_url, download_file_path)).start()

            root.destroy()
    except requests.exceptions.RequestException as e:
        print(f"Error checking for updates: {e}")


def download_and_install(download_url, download_path):
    try:
        download_file(download_url, download_path)
        install_update(download_path)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading update: {e}")
