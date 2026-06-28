"""
File: app/ml/features/corpus.py

Description: Generates a corpus of training data to help
classify ad material.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 06/25/2026
"""

import json
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

from .transcription import Sentence


def json_writer(sentences: Iterable[Sentence], output_path: Path, default_label: str = "content") -> None:
    """
    Writes a stream of transcribed sentences to a json file for manual classification,
    recording the start, end, and content of the sentence.

    Args:
        sentences (Iterable[Sentence]): A generator of sentences.
        output_path (Path): The file to which to write the transcribed sentences.
        default_label (str): The text to fill the `label` field with in the
        generated json. Defaults to `content`.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for s in sentences:
            record = {"start": s.start, "end": s.end, "text": s.text, "label": default_label}
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


@dataclass(frozen=True)
class LabeledSentence:
    """
    An interpretable object representing a manually classified sentence.

    Attributes:
        episode (str): Episode title.
        start (float): Start time of the sentence in seconds.
        end (float): End time of the sentence in seconds.
        text (str): Sentence contents.
        label (str): Human-created label denoting "ad" or "content"
    """

    episode: str
    start: float
    end: float
    text: str
    label: str


def load_file(path: Path) -> Iterator[LabeledSentence]:
    """
    Loads a single 'jsonl' file via the given `path`,
    rendering each sentence present in the `jsonl` as a
    LabeledSentence object.

    Args:
        path (Path): The path to the jsonl file.

    Yields:
        (LabeledSentence): A LabeledSentence object for each
        sentence in the jsonl.

    Raises:
        ValueError: If json label or file is malformed.
    """
    valid_labels = ["ad", "content"]
    with path.open() as f:
        for line in f:
            clean_line = line.strip()
            if clean_line:
                try:
                    data = json.loads(clean_line)
                    if data["label"] not in valid_labels:
                        raise ValueError(f"Found malformed label name: {data}")
                except json.JSONDecodeError as e:
                    raise ValueError(f"Encountered malformed json: {path}") from e
                yield LabeledSentence(path.stem, **data)


def load_training_data(training_dir: Path, extension: str = "jsonl") -> Iterator[LabeledSentence]:
    """
    Loads all files of type `extension` from the given directory.

    Args:
        training_dir (Path): The directory containing transcribed files.
        extension (str): The extension of the files containing training data.

    Yields:
        (LabeledSentence): A LabeledSentence for each sentence in the training data.
    """
    for file in training_dir.glob(f"*.{extension}"):
        yield from load_file(file)
