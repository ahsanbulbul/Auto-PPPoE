import psutil
import platform
import subprocess

def get_wifi_name():
    # For Windows
    if platform.system() == "Windows":
        try:
            result = subprocess.run(["netsh", "wlan", "show", "interfaces"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode()
            if result.returncode != 0:
                print("Error running netsh command:", result.stderr.decode())
                return None
            for line in output.splitlines():
                if "SSID" in line:
                    return line.split(":")[1].strip()
            print("SSID not found in the output.")
        except Exception as e:
            print("Error running subprocess for Windows:", e)

    # For macOS
    elif platform.system() == "Darwin":
        try:
            result = subprocess.run(["networksetup", "-getairportnetwork", "en0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode()
            if result.returncode != 0:
                print("Error running networksetup command:", result.stderr.decode())
                return None
            return output.strip().split(":")[-1].strip()
        except Exception as e:
            print("Error running subprocess for macOS:", e)

    # For Linux (using nmcli or iwconfig)
    elif platform.system() == "Linux":
        try:
            # Try using nmcli
            result = subprocess.run(["nmcli", "-t", "-f", "active,ssid", "device", "wifi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode()
            if result.returncode != 0:
                print("Error running nmcli command:", result.stderr.decode())
                return None
            for line in output.splitlines():
                if line.startswith("yes"):
                    return line.split(":")[1].strip()
        except FileNotFoundError:
            print("nmcli command not found, trying iwconfig...")

        try:
            # Fall back to iwconfig if nmcli is not available
            result = subprocess.run(["iwconfig"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode()
            if result.returncode != 0:
                print("Error running iwconfig command:", result.stderr.decode())
                return None
            for line in output.splitlines():
                if "ESSID" in line:
                    return line.split(":")[1].replace('"', '').strip()
        except FileNotFoundError:
            print("iwconfig command not found.")

    return None
