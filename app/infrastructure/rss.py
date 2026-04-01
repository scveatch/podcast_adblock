"""
File: app/infrastructure/rss.py

Description: Used to watch the RSS feed of the podcast and query / fetch episodes.

NOTE: The RSS parser `feedparser` does not ship with stubs. As far as I have been
able to tell, there are no community provided stubs either. As the usage of this
library is largely limited to this module and we return a consistent and
normalized container of relevant information, I have disabled the
`no-any-unimported` error from `mypy` on lines using `feedparser` types. Beyond
that, the module is regularly typed.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 03/30/2026
"""

import feedparser as fp

from app.core.episode import Episode


def fetch_feed(url: str) -> list[Episode]:
    """
    Gets the whole RSS feed and returns it as a list of
    normalized `Episode` objects.

    Args:
        url (str): The RSS URL string.

    Returns:
        (list[Episode]): All episode XML objects, converted
        to the `Episode` dataclass.
    """
    rss = fp.parse(url)
    return [normalize_episode(ep) for ep in rss.entries]


def normalize_episode(episode: "fp.FeedParserDict") -> Episode:  # type: ignore[no-any-unimported]
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
        title=_get_title(episode),
        image_url=_get_img_url(episode),
        page_url=_get_page_url(episode),
        audio_url=_get_audio_url(episode),
        duration=_get_duration(episode),
        published=_get_published(episode),
    )


def _get_title(ep: "fp.FeedParserDict") -> str:  # type: ignore[no-any-unimported]
    """
    Fetches the title from an episode's rendered XML entry.

    Args:
        ep (fp.FeedParserDict): An episode, rendered by the
        RSS parser.

    Returns:
        (str): A string representation of the column.
    """
    return str(ep.get("title"))


def _get_img_url(ep: "fp.FeedParserDict") -> str | None:  # type: ignore[no-any-unimported]
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


def _get_page_url(ep: "fp.FeedParserDict") -> str:  # type: ignore[no-any-unimported]
    """
    Fetches the page URL from an episode's rendered XML entry.

    Args:
        ep (fp.FeedParserDict): An episode rendered by the RSS parser.

    Returns:
        (str): A string representation of the episode's page URL.
    """
    return str(ep.get("link"))


def _get_audio_url(ep: "fp.FeedParserDict") -> str | None:  # type: ignore[no-any-unimported]
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


def _get_duration(ep: "fp.FeedParserDict") -> int | None:  # type: ignore[no-any-unimported]
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


def _get_published(ep: "fp.FeedParserDict") -> str:  # type: ignore[no-any-unimported]
    """
    Fetches the published date from an episode's rendered XML entry.

    Args:
        ep (fp.FeedParserDict): An episode, rendered by the
        RSS parser.

    Returns:
        (str): A string representation of the date.
    """
    return str(ep.get("published"))
