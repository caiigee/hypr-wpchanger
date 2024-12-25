import json
import subprocess
import time
import random
from pathlib import Path


def get_monitors():
    """Get list of connected monitors using hyprctl."""
    result = subprocess.run(
        ["hyprctl", "-j", "monitors"], capture_output=True, text=True
    )
    monitors = json.loads(result.stdout)
    return [monitor["name"] for monitor in monitors]


def get_random_wallpapers(count):
    """Get random wallpapers from the wallpapers directory."""
    wallpaper_dir = Path.home() / "Pictures/Wallpapers"
    wallpapers = list(wallpaper_dir.glob("*"))
    return random.sample(wallpapers, min(count, len(wallpapers)))


def set_wallpapers():
    """Set random wallpapers for all connected monitors."""
    monitors = get_monitors()
    wallpapers = get_random_wallpapers(len(monitors))

    # # Preloading wallpapers:
    # for wallpaper in wallpapers:
    #     subprocess.run(["hyprctl", "hyprpaper", "preload", str(wallpaper)])

    # Setting the wallpapers for each monitor:
    for monitor, wallpaper in zip(monitors, wallpapers):
        subprocess.run(
            ["hyprctl", "hyprpaper", "reload", f"{monitor},{str(wallpaper)}"]
        )


def main():
    while True:
        try:
            set_wallpapers()
        except Exception as e:
            print(f"Error setting wallpapers: {e}")
        time.sleep(600)


if __name__ == "__main__":
    main()
