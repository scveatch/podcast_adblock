"""
File: main.py

Description: A test module to simulate running the program.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 03/30/2026
"""

from pathlib import Path

from app.services.episode_service import EpisodeService

URL: str = "https://audioboom.com/channels/5094626.rss"

DOWNLOAD_PATH: Path = Path.cwd()


def main() -> None:
    """
    A test function used to simulate running the program.
    """
    s = EpisodeService(URL, DOWNLOAD_PATH)
    monkeys = s.get("6A-King Arthur Prologue: The Once and Really Only that One Time King")
    path = s.download("6A-King Arthur Prologue: The Once and Really Only that One Time King")
    print(path)
    print(monkeys)


if __name__ == "__main__":
    main()
