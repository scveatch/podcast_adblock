"""
File: app/ml/features/types.py

Description: Contains commonly used feature types.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 07/05/2026
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Sentence:
    """
    A time-aligned transcription unit representing the span
    of a sentence.

    This is a lossy linguistic grouping, but will hopefully
    be sufficient for the immediate term.

    Attributes:
        start (float): The time at the beginning of the sentence.
        end (float): The time at the end of the sentence.
        text (str): The transcribed sentence.
    """

    start: float
    end: float
    text: str


@dataclass(frozen=True)
class ContextSentence:
    """
    Expands the Sentence class to include
    previous and subsequent sentences as
    contextual information.

    Attributes:
        sentence (Sentence): The sentence of interest.
        previous (tuple[Sentence, ...]): `n` previous sentences.
        next (tuple[Sentence, ...]): `n` subsequent sentences.
    """

    sentence: Sentence
    previous: tuple[Sentence, ...]
    next: tuple[Sentence, ...]
