import requests
import os
import sys
import tkinter as tk
from tkinter import messagebox

VERSION = "1.0.0"  # Current version of your application


def check_for_updates():
    try:
        response = requests.get("https://api.github.com/repos/yourusername/currency-converter/releases/latest")
        response.raise_for_status()
        latest_release = response.json()
        latest_version = latest_release['tag_name']

        if latest_version != VERSION:
            answer = messagebox.askyesno("Update Available",
                                         f"A new version {latest_version} is available. Do you want to update?")
            if answer:
                download_and_install_update(latest_release['assets'][0]['browser_download_url'])

    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")


def download_and_install_update(download_url):
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        with open("currency_converter_update.exe", "wb") as f:
            f.write(response.content)

        messagebox.showinfo("Update Downloaded",
                            "The update has been downloaded. The application will now restart to apply the update.")
        os.startfile("currency_converter_update.exe")
        sys.exit()

    except requests.RequestException as e:
        messagebox.showerror("Update Error", f"Failed to download the update: {e}")
