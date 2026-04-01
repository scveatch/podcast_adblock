"""
File: app/infrastructure/storage.py

Description: Defines logic for a storage boundary.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 03/31/2026
"""

import re
from pathlib import Path

from app.core.episode import Episode


class Storage:
    """
    Handles filesystem layout for downloaded audio.
    """

    def __init__(self, base_dir: Path) -> None:
        """
        Constructs the storage boundary layer.

        Args:
            base_dir (Path): The root directory from which to create child
            download directories.
        """
        self._base_dir = base_dir
        self.audio = base_dir / "audio"

        self.ensure_exists()

    def ensure_exists(self) -> None:
        """
        Construct required directories if they don't exist.
        """
        self.audio.mkdir(parents=True, exist_ok=True)

    def get_audio_path(self, filename: str) -> Path:
        """
        Return full audio path for a given filename.

        Returns:
            (Path): The full path to the audio file.
        """
        return self.audio / filename

    def build_audio_path(self, ep: Episode) -> Path:
        """
        Constructs the final path for an audio file from an episode object.

        Args:
            ep (Episode): A container with resolved audio url and metadata for
            a given episode.

        Returns:
            (Path): The destination path of the downloaded audio.

        Raises:
            ValueError: If the episode identifier (i.e., `12`, `23A`, etc.)
            could not be identified in the title.
        """
        file: str | None = self._extract_id(ep)
        if not file:
            raise ValueError("Could not parse episode identifier from title")
        return self.audio / f"{file}.mp3"

    def _extract_id(self, ep: Episode) -> str | None:
        """
        Extract out the episode identifier from the title string
        (i.e., '22A' from `22A Irish Legends`).

        Args:
            ep (Episode): The episode object whose audio we want to download.

        Returns:
            (str | None): The extracted identifier string, or `None` if the
            identifier could not be found.
        """
        match = re.match(r"^\s*(\d+[A-Za-z]?)\b", ep.title)
        return match.group(1) if match else None
