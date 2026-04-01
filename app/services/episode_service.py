"""
File: app/services/episode_service.py

Description: An interface that allows us to load, search, and return
episodes from the RSS.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 03/30/2026
"""

from pathlib import Path

from app.core.episode import Episode, EpisodeIndex
from app.infrastructure.downloader import download_audio
from app.infrastructure.rss import fetch_feed
from app.infrastructure.storage import Storage


class EpisodeService:
    """
    Service layer for querying and downloading podcast episodes.

    Coordinates fetching episode data from an RSS feed, indexing
    episodes for searching and retrieval, and managing downloads
    via the storage layer.
    """

    def __init__(self, rss_url: str, download_path: Path) -> None:
        """
        Initializes the EpisodeService. Fetches episodes from the provided
        RSS feed, builds an index for efficient lookup, and initializes storage
        for the downloaded audio.

        Args:
            rss_url (str): The URL of the RSS feed to fetch episodes from.
            download_path (Path): Base directory where audio files will be stored.
        """
        self._episodes: list[Episode] = fetch_feed(rss_url)
        self._index: EpisodeIndex = EpisodeIndex(self._episodes)
        self._storage: Storage = Storage(download_path)

    def search(self, query: str) -> list[Episode]:
        """
        Searches for episodes whose titles match a query string.

        Args:
            query (str): Search string used to match episode titles.

        Returns:
            (list[Episode]): A list of episodes matching the query.
        """
        return self._index.search(query)

    def get(self, title: str) -> Episode | None:
        """
        Retrieves a single episode by its title.

        Args:
            title (str): The title of the episode to retrieve.

        Returns:
            (Episode | None): The matching episode if found, `None` otherwise.
        """
        return self._index.get_by_title(title)

    def download(self, title: str, show_progress: bool = True) -> Path:
        """
        Downloads the audio for a given episode. Resolves the episode by
        its title, determines the storage path, and downloads the audio
        file if it does not already exist.

        Args:
            title (str): The title of the episode to download.
            show_progress (bool): Whether or not to display a download bar. Defaults
            to `True`.

        Returns:
            (Path): Filesystem path to the downloaded (or existing) audio file.

        Raises:
            ValueError:
                - If the episode cannot be found or the audio file cannot be resolved.
                - If the download request fails.
                - If the file cannot be written to disk.
        """
        ep: Episode | None = self._index.get_by_title(title)
        if ep is None:
            raise ValueError(f"Could not find episode `{title}`")

        if not ep.resolved_url:
            raise ValueError(f"Episode {title} audio url cannot be resolved")

        path: Path = self._storage.build_audio_path(ep)
        if path.exists():
            return path
        download_audio(ep.resolved_url, path, show_progress)
        return path
