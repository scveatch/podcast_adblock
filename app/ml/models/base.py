"""
File: app/ml/models/base.py

Description: Define clean ABC models.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 04/01/2026
"""

from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np
import numpy.typing as npt

# Common Aliases
FloatArray = npt.NDArray[np.float64]
IntArray = npt.NDArray[np.int_]


class BaseModel(ABC):
    """
    The abstract base for all models in the application.
    """

    @abstractmethod
    def fit(self, features: FloatArray, target: IntArray) -> None:
        """
        Train the model.

        Args:
            features (FloatArray): Feature matrix of shape (`n_samples`, `n_features`)
            target (IntArray): Target labels of shape (`n_samples`,)
        """

    @abstractmethod
    def predict(self, features: FloatArray) -> FloatArray:
        """
        Return the output labels for the given features.

        Args:
            features (FloatArray): Feature matrix of shape (`n_samples`, `n_features`)

        Returns:
            (FloatArray): Array of predicted labels of the shape (`n_samples`,)
        """

    def predict_probabilities(self, features: FloatArray) -> FloatArray:
        """
        Optionally return the probabilities associated with the given
        output labels. Not implemented by default.

        Args:
            features (FloatArray): Feature matrix of shape (`n_samples`, `n_features`)

        Returns:
            (FloatArray): Array of probabilities of the shape (`n_samples`, `n_classes`)

        Raises:
            NotImplementedError: By default, ensuring that the method is
            not called by models which do not support it.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not support `predict_probabilities()`")

    @abstractmethod
    def save(self, path: Path) -> None:
        """
        Save a model to the disk.

        Args:
            path (Path): The destination path of the model.
        """

    @classmethod
    @abstractmethod
    def load(cls, path: Path) -> "BaseModel":
        """
        Load a model from disk.

        Args:
            path (Path): The origination path of the model.

        Returns:
            (BaseModel): The model, loaded from disk.
        """
