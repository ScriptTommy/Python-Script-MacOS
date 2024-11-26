import os
import sys
import requests
from time import sleep
import subprocess

# URLs for version checking and executable download
VERSION_CHECK_URL = "https://raw.githubusercontent.com/ScriptTommy/Python-Script-Windows/main/version.txt"
EXE_DOWNLOAD_URL = "https://raw.githubusercontent.com/ScriptTommy/Python-Script-Windows/main/main.exe"
EXE_NAME = "main.exe"  # Current executable name

# Current version embedded in the script
CURRENT_VERSION = "1.0.0"  # Update this manually in the script for new versions

# ASCII logo for the app
logo = """
     _______. __    _______ .__   __.  __   ___________    ____
    /       ||  |  /  _____||  \ |  | |  | |   ____\   \  /   /
   |   (----`|  | |  |  __  |   \|  | |  | |  |__   \   \/   /
    \   \    |  | |  | |_ | |  . `  | |  | |   __|   \_    _/
.----)   |   |  | |  |__| | |  |\   | |  | |  |        |  |
|_______/    |__|  \______| |__| \__| |__| |__|        |__|
"""
logo_color = "\033[95m"  # Purple color for the logo
reset_color = "\033[0m"  # Reset to default terminal color


def check_for_updates():
    """Check online for updates and prompt the user to update."""
    print("Checking for updates...")
    sleep(1)

    try:
        # Fetch the latest version number from the server
        response = requests.get(VERSION_CHECK_URL)
        response.raise_for_status()
        latest_version = response.text.strip()

        # Compare versions
        if latest_version != CURRENT_VERSION:
            print(f"A new version is available: {latest_version} (current: {CURRENT_VERSION})")
            choice = input(f"Do you want to update to version {latest_version}? (y/n): ").strip().lower()
            if choice == "y":
                download_and_replace_exe(latest_version)
            else:
                print("Update skipped. You will be prompted again next time.")
                sleep(2)
        else:
            print("You are using the latest version.")
            sleep(2)
    except Exception as e:
        print(f"Error checking for updates: {e}")
        sleep(2)


def download_and_replace_exe(new_version):
    """Download and replace the current executable with the latest version."""
    print("Downloading the latest version...")
    try:
        response = requests.get(EXE_DOWNLOAD_URL, stream=True)
        response.raise_for_status()

        with open(EXE_NAME, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Update to version {new_version} was successful. Restarting application...")
        sleep(2)

        # Restart the application with the updated executable
        if os.path.exists(EXE_NAME) and os.access(EXE_NAME, os.X_OK):
            subprocess.Popen([EXE_NAME], shell=True)
            sys.exit()
        else:
            print("Failed to restart the application. Please run the new .exe manually.")
    except Exception as e:
        print(f"Failed to update: {e}")
        sleep(2)


def main_menu():
    """Displays the main menu."""
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # Clear the screen for a clean display
        print(logo_color + logo + reset_color)
        print(f"--- MAIN MENU ---")
        print("1. Check for Updates")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            check_for_updates()
        elif choice == "0":
            sys.exit("Goodbye!")
        else:
            print("Invalid choice. Please try again.")
            sleep(1)


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")  # Clear the screen at the start
    print(logo_color + logo + reset_color)  # Display the logo at the beginning
    print("Welcome to Signify!")
    sleep(1)
    check_for_updates()  # Always check for updates at startup
    main_menu()