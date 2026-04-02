"""
File: app/ml/features/base.py

Description: Build the base feature extractor to be used for extracting data
from raw audio.

Author: Spencer Veatch (sveatch@willamette.edu)

Last Modified: 04/01/2026
"""

from abc import ABC, abstractmethod

import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]


class FeatureExtractor(ABC):
    """
    Base interface for feature extraction from raw audio.
    """

    @abstractmethod
    def extract(self, audio: FloatArray, sr: int) -> FloatArray:
        """
        Extract features from a single audio chunk.

        Args:
            audio (FloatArray): 1D waveform array.
            sr (int): Sample rate.

        Returns:
            (FloatArray): Feature vector of shape (`n_features`,)
        """

    @abstractmethod
    def batch_extract(self, audio_chunks: list[FloatArray], sr: int) -> FloatArray:
        """
        Extract features for multiple chunks.

        Args:
            audio_chunks (list[FloatArray]): A list of 1D waveforms.
            sr (int): Sample rate.

        Returns:
            (FloatArray): Feature vector of shape (`n_chunks`, `n_features`)
        """
        return np.vstack([self.extract(chunk, sr) for chunk in audio_chunks])
