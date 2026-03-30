"""
File: app/ingest/rss.py

Description: Used to watch the RSS feed of the podcast and query / fetch episodes.

NOTE: The RSS parser `feedparser` does not ship with stubs. As far as I have been
able to tell, there are no community provided stubs either. As the usage of this
library is largely limited to this module and our class returns a consistent and
normalized container of relevant information, I have disabled the `no-any-unimported`
error from `mypy` on lines using `feedparser` types. Beyond that, the module is
regularly typed.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 03/29/2026
"""

from dataclasses import dataclass

import feedparser as fp

URL: str = "https://audioboom.com/channels/5094626.rss"


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
        resolved_audio_url (str | None): The URL to download the audio. `None` if the
        URL cannot be found.
    """

    title: str
    image_url: str | None
    page_url: str
    audio_url: str | None
    duration: int | None
    published: str
    resolved_audio_url: str | None = None


class ParseRSS:
    """
    Parses the RSS feed and returns a normalized container of the fetched data.

    Attributes:
        rss (fp.FeedParserDict): The full RSS feed, returned as a dictionary by the
        RSS package.
    """

    def __init__(self, url: str = URL) -> None:
        self.rss: fp.FeedParserDict = fp.parse(url)  # type: ignore[no-any-unimported]
        # print(json.dumps(x, indent = 4))
        # print(self.normalize_episode(x))

    def normalize_episode(self, episode: "fp.FeedParserDict") -> Episode:  # type: ignore[no-any-unimported]
        """
        Normalizes the rendered XML entry for any particular episode
        into an `Episode` container for future processing.

        Args:
            episode (fp.FeedParserDict): A single episode, rendered by the
            RSS parser into a dictionary for simpler parsing.

        Returns:
            (Episode): A distillation of the most useful elements of the rendered
            XML in a type-safe and easy to access format.
        """
        return Episode(
            title=self._get_title(episode),
            image_url=self._get_img_url(episode),
            page_url=self._get_page_url(episode),
            audio_url=self._get_audio_url(episode),
            duration=self._get_duration(episode),
            published=self._get_published(episode),
        )

    def get_episode_by_title(self, title: str) -> Episode | None:
        """
        Allows a user to search the RSS feed by episode title. Returns
        a normalized `Episode` object.

        Args:
            title (str): The title of the episode the user wishes to pull
            from the RSS feed.

        Returns:
            (Episode): A distillation of the most useful elements of the rendered
            XML in a type-safe and easy to access format.
        """
        for entry in self.rss.entries:
            if title.lower() in str(entry.get("title", "")).lower():
                return self.normalize_episode(entry)
        return None

    def _get_title(self, ep: "fp.FeedParserDict") -> str:  # type: ignore[no-any-unimported]
        """
        Fetches the title from an episode's rendered XML entry.

        Args:
            ep (fp.FeedParserDict): An episode, rendered by the
            RSS parser.

        Returns:
            (str): A string representation of the column.
        """
        return str(ep.get("title"))

    def _get_img_url(self, ep: "fp.FeedParserDict") -> str | None:  # type: ignore[no-any-unimported]
        """
        Fetches the image URL from an episode's rendered XML entry.
        Returns `None` if the image URL cannot be found.

        Args:
            ep (fp.FeedParserDict): An episode rendered by the RSS parser.

        Returns:
            (str | None): A string representation of the URL, if it is found,
            `None` otherwise.
        """
        image = ep.get("image")

        if isinstance(image, fp.FeedParserDict):
            return str(image.get("href"))

        return None

    def _get_page_url(self, ep: "fp.FeedParserDict") -> str:  # type: ignore[no-any-unimported]
        """
        Fetches the page URL from an episode's rendered XML entry.


        Args:
            ep (fp.FeedParserDict): An episode rendered by the RSS parser.

        Returns:
            (str): A string representation of the episode's page URL.
        """
        return str(ep.get("link"))

    def _get_audio_url(self, ep: "fp.FeedParserDict") -> str | None:  # type: ignore[no-any-unimported]
        """
        Fetches the audio URL from an episode's rendered XML entry.
        Returns `None` if the audio URL cannot be found.


        Args:
            ep (fp.FeedParserDict): An episode rendered by the RSS parser.

        Returns:
            (str | None): A string representation of the episode's audio URL,
            or `None` if the URL could not be found.
        """
        links = ep.get("links")
        if not links:
            return None
        for link in links:
            if link.get("rel") == "enclosure":
                return str(link.get("href"))
        return None

    def _get_duration(self, ep: "fp.FeedParserDict") -> int | None:  # type: ignore[no-any-unimported]
        """
        Fetches the duration from an episode's rendered XML entry.
        Returns `None` if the duration could not be resolved.

        Args:
            ep (fp.FeedParserDict): The rendered episode object.

        Returns:
            (int | None): The duration of the episode (measured in seconds)
            or `None` if the duration could not be found.
        """
        val = ep.get("itunes_duration")
        if isinstance(val, (int, str)):
            try:
                return int(val)
            except ValueError:
                return None
        return None

    def _get_published(self, ep: "fp.FeedParserDict") -> str:  # type: ignore[no-any-unimported]
        """
        Fetches the published date from an episode's rendered XML entry.

        Args:
            ep (fp.FeedParserDict): An episode, rendered by the
            RSS parser.

        Returns:
            (str): A string representation of the date.
        """
        return str(ep.get("published"))
