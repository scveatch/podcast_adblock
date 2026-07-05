"""
File: main.py

Description: A test module to simulate running the program.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 03/30/2026
"""

from pathlib import Path

from app.core.episode import Episode, EpisodeRepository
from app.infrastructure import rss
from app.infrastructure.downloader import download
from app.infrastructure.storage import Storage
from app.ml.features.transcription import transcribe
from app.ml.training.corpus import json_writer, load_training_data

URL: str = "https://audioboom.com/channels/5094626.rss"

DOWNLOAD_PATH: Path = Path.cwd()


def test_download() -> Path:
    """
    A test function downloading a single episode
    and returning its path.

    Returns:
        (Path): The path to the downloaded episode.
    """
    storage: Storage = Storage(DOWNLOAD_PATH)
    episodes: list[Episode] = rss.fetch_feed(URL)
    repo: EpisodeRepository = EpisodeRepository(episodes)
    ep: list[Episode] = repo.search("372: Greek Myths: Things as they Are")
    audio_path: Path = download(ep[0], storage)
    return audio_path


def test_transcription() -> None:
    """
    Tests whisper transcription.
    """
    path = test_download()
    json_writer(transcribe(path), DOWNLOAD_PATH / "data" / "372.jsonl")


def test_data_load() -> None:
    """
    Loads and prints values from the training repository.
    """
    for i, val in enumerate(load_training_data(DOWNLOAD_PATH / "data")):
        print(val)
        if i > 5:
            break


def main() -> None:
    """
    A test function used to simulate running the program.
    """
    test_transcription()


if __name__ == "__main__":
    main()
