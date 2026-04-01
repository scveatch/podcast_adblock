"""
File: app/core/episode.py

Description: Stores a representation of the fetched episodes and an
indexer that can be used to search / load episodes.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 03/31/2026
"""

from dataclasses import asdict, dataclass

import requests


@dataclass
class Episode:
    """
    Containerizes the attributes of a fetched episode.

    Attributes:
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

    title: str
    image_url: str | None
    page_url: str
    audio_url: str | None
    duration: int | None
    published: str
    _resolved_audio_url: str | None = None

    @property
    def resolved_url(self) -> str | None:
        """
        Lazily resolves the final audio url, following any redirects. Returns `None`
        if the url is missing or cannot be resolved.

        Returns:
            (str | None): The resolved url or `None` if the url could not be resolved.
        """
        if self._resolved_audio_url:
            return self._resolved_audio_url
        if not self.audio_url:
            return None
        # Resolve url
        try:
            resp: requests.Response = requests.head(self.audio_url, allow_redirects=True, timeout=10)
            if resp.status_code == 200:
                return resp.url
        except requests.RequestException:
            return None
        return None

    def __str__(self) -> str:
        """
        A magic method printing the Episode class more cleanly.

        Returns:
            (str): The Episode object, represented as a string.
        """
        return "\n".join(f"{attribute}: {value}" for attribute, value in asdict(self).items())


class EpisodeIndex:
    """
    Indexes the returned episodes to make them searchable.
    """

    def __init__(self, episodes: list[Episode]) -> None:
        """
        Initializes the indexed repository.

        Args:
            episodes (list[Episode]): A list of episodes constructed
            from the RSS feed.
        """
        self._episodes = episodes
        self._by_title: dict[str, Episode] = {ep.title.lower(): ep for ep in self._episodes}

    def all(self) -> list[Episode]:
        """
        Return all episodes.

        Returns:
            (list[Episode]): All episodes scraped from the RSS feed.
        """
        return self._episodes

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

    def get_by_title(self, title: str) -> Episode | None:
        """
        Fetches a given Episode by its title.

        Args:
            title (str): The title to search for.

        Returns:
            (Episode | None): The Episode whose title matches the search
            parameter(s). `None` if the Episode cannot be found.
        """
        return self._by_title.get(title.lower())
