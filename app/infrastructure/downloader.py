"""
File: app/infrastructure/downloader.py

Description: Holds logic related to fetching audio associated episode(s).

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 03/31/2026
"""

from pathlib import Path

import requests
from tqdm import tqdm


def download_audio(url: str, download_path: Path, show_progress: bool = False) -> None:
    """
    Downloads an audio file from a URL to a specified path. The file is
    streamed in chunks to avoid loading the whole file into memory.

    Args:
        url (str): The direct URL to the audio file.
        download_path (Path): The destination path for the audio file.
        show_progress (bool): Whether or not to display a progress bar.
        Defaults to `False`.
    """
    with requests.get(url, stream=True, timeout=20) as resp:
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        with (
            open(download_path, "wb") as f,
            tqdm(total=total, unit="B", unit_scale=True, disable=not show_progress) as progress,
        ):
            for chunk in resp.iter_content(chunk_size=1024 * 1024):  # One megabyte chunks
                if chunk:
                    f.write(chunk)
                    progress.update(len(chunk))
