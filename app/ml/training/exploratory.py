"""
File: app/ml/training/exploratory.py

Description: Serves as a playground for model experimentation / feature exploration.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 06/28/2026
"""

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import StandardScaler

from .corpus import LabeledSentence, load_training_data

TRAINING_DATA = Path("/home/sveatch/projects/podcast_adblock/data")
SEP = " [SEP] "


@dataclass
class Episode:
    id: str
    sentences: list[LabeledSentence]


def build_train_test(data_path: Path):
    grouped_data: dict[str, list[LabeledSentence]] = defaultdict(list)
    for i in load_training_data(data_path):
        grouped_data[i.episode].append(i)
    episodes: list[Episode] = [Episode(episode_id, sentences) for episode_id, sentences in grouped_data.items()]
    train, test = train_test_split(episodes, test_size=0.2, random_state=1729)
    return train, test


def build_context(episode: Episode, index: int, radius: int) -> str:
    start = max(0, index - radius)
    end = min(len(episode.sentences), index + radius + 1)
    return SEP.join(s.text for s in episode.sentences[start:end])


def make_context(episodes: list[Episode], radius: int = 2):
    x = []
    y = []

    for episode in episodes:
        for i, sentence in enumerate(episode.sentences):
            x.append((build_context(episode, i, radius), i / max(1, len(episode.sentences) - 1)))
            y.append(sentence.label)
    return x, y


class ContextExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [context for context, _ in X]


class PositionExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):

        return np.asarray([[position] for _, position in X])


features = FeatureUnion(
    [
        (
            "word",
            Pipeline(
                [
                    ("context", ContextExtractor()),
                    ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2), min_df=2)),
                ]
            ),
        ),
        (
            "char",
            Pipeline(
                [
                    ("context", ContextExtractor()),
                    ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2)),
                ]
            ),
        ),
        (
            "position",
            Pipeline(
                [
                    ("extract", PositionExtractor()),
                    ("scale", StandardScaler()),
                ]
            ),
        ),
    ]
)

model = Pipeline(
    [
        ("features", features),
        # ("tfidf", TfidfVectorizer(ngram_range = (1, 2), min_df = 2)),
        ("clf", LogisticRegression(max_iter=2_000, class_weight="balanced")),
    ]
)


def predict_episode(model, episode, radius=2):
    n = len(episode.sentences)
    vals = [
        (
            build_context(episode, i, radius),
            i / max(1, n - 1),
        )
        for i in range(n)
    ]
    probs = model.predict_proba(vals)
    ad_index = list(model.classes_).index("ad")
    return probs[:, ad_index]


def smooth(probabilities, window=5):
    kernel = np.ones(window)
    kernel /= kernel.sum()
    return np.convolve(
        probabilities,
        kernel,
        mode="same",
    )


def evaluate(
    model,
    episodes,
    threshold=0.55,
    window=5,
):
    truth = []
    pred = []

    for episode in episodes:
        probs = predict_episode(model, episode)
        probs = smooth(probs, window)

        labels = np.where(
            probs >= threshold,
            "ad",
            "content",
        )

        truth.extend(s.label for s in episode.sentences)
        pred.extend(labels)

    print(f"Accuracy : {accuracy_score(truth, pred):.3f}")
    print(f"Precision: {precision_score(truth, pred, pos_label='ad'):.3f}")
    print(f"Recall   : {recall_score(truth, pred, pos_label='ad'):.3f}")
    print(f"F1       : {f1_score(truth, pred, pos_label='ad'):.3f}")

    print()
    print(classification_report(truth, pred))
    print()
    print(confusion_matrix(truth, pred))

    return truth, pred


if __name__ == "__main__":
    train_episodes, test_episodes = build_train_test(TRAINING_DATA)
    x_train, y_train = make_context(train_episodes)
    x_test, y_test = make_context(test_episodes)
    model.fit(x_train, y_train)
    evaluate(model, test_episodes)
