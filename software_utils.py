import subprocess
import os


def launch_resolve():
    print("Launching DaVinci Resolve...")
    try:
        subprocess.Popen([r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"])
    except FileNotFoundError:
        QMessageBox.warning(self, "Error", "Software not found. Please check the path.")
    except Exception as e:
        QMessageBox.warning(self, "Error", f"Failed to launch software: {str(e)}")

def launch_krita():
    print("Launching Krita...")
    try:
        subprocess.Popen([r"C:\Program Files\Krita (x64)\bin\krita.exe"])
    except FileNotFoundError:
        QMessageBox.warning(self, "Error", "Software not found. Please check the path.")
    except Exception as e:
        QMessageBox.warning(self, "Error", f"Failed to launch software: {str(e)}")