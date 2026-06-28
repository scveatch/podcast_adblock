"""
File: app/core/episode.py

Description: Stores a representation of the fetched episodes and an
indexer that can be used to search / load episodes.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 06/27/2026
"""

from collections.abc import Iterator
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Episode:
    """
    Containerizes the attributes of a fetched episode.

    Attributes:
        id (str): A unique identifier associated with the episode.
        title (str): The episode's title.
        image_url (str | None): The URL to the episode's associated title image.
        `None` if the URL cannot be found.
        page_url (str): The URL to the episode's associated page.
        audio_url (str | None): The URL to the episode's audo. `None` if the URL
        cannot be found. Note that this URL may contain redirects.
        duration (int | None): The duration (in seconds) of the audio. `None` if
        duration could not be established.
        published (str): The date the episode was published.

    Private Attributes:
        _resolved_audio_url (str | None): The URL to download the audio. `None` if the
        URL cannot be found. Used to cache resolved URL fetched by the `resolved_url`
        property -- should not be directly accessed.
    """

    id: str
    title: str
    image_url: str | None
    page_url: str
    audio_url: str | None
    duration: int | None
    published: str

    def __str__(self) -> str:
        """
        A magic method printing the Episode class more cleanly.

        Returns:
            (str): The Episode object, represented as a string.
        """
        return "\n".join(f"{attribute}: {value}" for attribute, value in asdict(self).items())


class EpisodeRepository:
    """
    In-memory repository of episodes with search and lookup.
    """

    def __init__(self, episodes: list[Episode]) -> None:
        """
        Initializes the indexed repository.

        Args:
            episodes (list[Episode]): A list of episodes constructed
            from the RSS feed.
        """
        self._episodes = episodes
        self._by_id: dict[str, Episode] = {ep.id: ep for ep in self._episodes}

    def __iter__(self) -> Iterator[Episode]:
        """
        Iterator magic method.

        Returns:
            (Iterator[Episode]): An iterator over the Episodes contained within.
        """
        return iter(self._episodes)

    def all(self) -> list[Episode]:
        """
        Return all episodes.

        Returns:
            (list[Episode]): All episodes scraped from the RSS feed.
        """
        return self._episodes

    def get(self, episode_id: str) -> Episode | None:
        """
        A system-facing function that returns an episode
        given an ID. Returns `None` if the episode cannot
        be found.

        Args:
            episode_id (str): The unique ID associated with
            any Episode object.

        Returns:
            (Episode | None): The associated Episode object if
            it exists, `None` otherwise.
        """
        return self._by_id.get(episode_id)

    def search(self, query: str) -> list[Episode]:
        """
        Search titles of episodes for some query. Return all
        episodes which have some match for the query.

        Args:
            query (str): The search parameter to be matched.

        Returns:
            (list[Episode]): A list of episodes whose titles contain
            the query parameter.
        """
        q: str = query.lower()
        return [ep for ep in self._episodes if q in ep.title.lower()]
