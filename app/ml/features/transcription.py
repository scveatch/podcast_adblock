"""
File: app/ml/features/transcription.py

Description: Convert an audio file to a transcription for easier parsing.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 06/24/2026
"""

import os
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from faster_whisper import BatchedInferencePipeline, WhisperModel

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


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


def transcribe(
    audio_file_path: Path,
    compute_type: str = "int8",
    model_size: str = "tiny.en",
    batch_size: int = 16,
    show_progress: bool = True,
) -> Iterator[Sentence]:
    """
    Performs ASR to transcribe the audio file, extracts word-level timestamps,
    and streams sentence segmentation.

    Outputs a generator to support streaming pipelines; sentences are produced incrementally
    as the podcast is processed.

    Args:
        audio_file_path (Path): The path to the audio file to be transcribed.
        compute_type (str): The quantization level of the used model.
        model_size (str): Size of the model to be used (tiny, tiny.en, base, base.en, etc.)
        batch_size (int): The minimum number of parallel requests to model for decoding.
        show_progress (bool): When `True`, display a progress bar as segments are processed.
    """
    model: WhisperModel = WhisperModel(model_size, device="cpu", compute_type=compute_type, use_auth_token=HF_TOKEN)
    batched_model: BatchedInferencePipeline = BatchedInferencePipeline(model=model)
    segments, _ = batched_model.transcribe(
        audio_file_path, batch_size=batch_size, log_progress=show_progress, word_timestamps=True
    )

    return iter_sentences(iter_words(segments))


def iter_words(segments: Iterator[Any]) -> Iterator[Any]:
    """
    Flattens Whisper segments into a continuous stream of timestamped words.

    Args:
        segments (Iterator[Word]): A series of segments.

    Yields:
        (Iterator[Word]): A generator of words.
    """
    for segment in segments:
        yield from segment.words


def iter_sentences(words: Iterator[Any]) -> Iterator[Sentence]:
    """
    Streams word-level ASR into sentence segments using simple punctuation-based
    heuristics. Tracks a running buffer of words, sentence start time, and emits
    a sentence when punctuation is encountered.

    Args:
        words (Iterator[Word]): A generator of words.

    Yields:
        (Iterator[Sentence]): A generator returning sentences.

    Raises:
        ValueError: If internal state invarients are violated (should be impossible).
    """
    current_words: list[str] = []
    sentence_start: float | None = None
    for word in words:
        if sentence_start is None:
            sentence_start = word.start
        current_words.append(word.word)

        if word.word.strip().endswith(("!", ".", "?")):
            if sentence_start is None:
                raise ValueError("Sentence start is None -- this should never happen.")
            yield Sentence(start=sentence_start, end=word.end, text="".join(w for w in current_words))
            current_words = []
            sentence_start = None
