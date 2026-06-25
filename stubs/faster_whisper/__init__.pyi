"""
File: /stubs/faster-whisper/__init__.pyi

Description: Contains stubs for the faster-whisper library.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 06/24/2026
"""

from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any

class Segment:
    """
    Transcription segment returned by faster-whisper.

    Attributes:
        start (float): Start time of the segment in seconds.
        end (float): End time of the segment in seconds.
        text (str): Transcribed text of the segment.
        words (Sequence[str]): Word-level timestamps.
    """

    start: float
    end: float
    text: str
    words: Sequence[str]

class WhisperModel:
    """
    Transcription model returned by the faster-whisper library.
    """
    def __init__(
        self,
        model_size_or_path: str,
        device: str = ...,
        compute_type: str = ...,
        use_auth_token: str | None = ...,
        **kwargs: Any,
    ) -> None:
        """
        Initialize a WhisperModel.

        Args:
            model_size_or_path (str): Name of pretrained model.
            device (str): Device on which the model will run (i.e., "cpu" or "cuda")
            compute_type (str): Level of precision to be used for inference.
            use_auth_token (str | None): Hugging Face authentication token.
        """
        pass

class BatchedInferencePipeline:
    """
    Performs batched transcription using a WhisperModel.
    """
    def __init__(self, model: WhisperModel) -> None:
        """
        Create a batched inference pipeline from a model.

        Args:
            model (WhisperModel): WhisperModel used for transcription.
        """
        ...

    def transcribe(
        self,
        audio: str | Path,
        batch_size: int = ...,
        log_progress: bool = ...,
        word_timestamps: bool = ...,
        **kwargs: Any,
    ) -> tuple[Iterator[Segment], Any]:
        """
        Processes a batch of audio in chunks and return language information.

        Args:
            audio (str | Path): Path to the input file.
            batch_size (int): Maximum number of parallel requests.
            log_progress (bool): Displays progress bar when `True`.

            word_timestamps (bool): Whether to extract word-level timestamps.

        Returns:
            (tuple[Iterator[Segment], Any]): Returns a tuple with a generator
            over the transcribed segments and some metadata about the transcription.
        """
        ...
