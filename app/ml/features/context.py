"""
File: app/ml/features/context.py

Description: Contains a context interface enriching sentence-level information.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 07/05/2026
"""

import contextlib
from collections import deque
from collections.abc import Iterator

from .types import ContextSentence, Sentence


def construct_context(sentences: Iterator[Sentence], radius: int = 2) -> Iterator[ContextSentence]:
    """
    Stream sentences into overlapping context windows. Uses a sliding window and yield
    each sentence together with `radius` preceding and subsequent sentences. Where insufficient
    context exists, the returned windows are truncated accordingly.

    Args:
        sentences (Iterator[Sentence]): A stream of transcribed sentences.
        radius (int): Maximum number of neighboring sentences to include on either
        side of the current sentence.

    Yields:
        (Iterator[ContextSentence]): A stream of context-enriched sentences, containing
        the current sentence and `radius` surrounding ones.
    """
    window: deque[Sentence] = deque(maxlen=2 * radius + 1)

    # Prime window by loading `n` values
    for _ in range(2 * radius + 1):
        try:
            window.append(next(sentences))
        except StopIteration:
            break

    while window:
        center: int = min(radius, len(window) // 2)
        items: tuple[Sentence, ...] = tuple(window)
        yield ContextSentence(
            sentence=items[center],
            previous=items[:center],
            next=items[center + 1 :],
        )

        window.popleft()

        with contextlib.suppress(StopIteration):
            window.append(next(sentences))
