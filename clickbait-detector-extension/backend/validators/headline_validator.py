"""
===========================================================
ClickDetect AI
Headline Input Validator

This module validates and preprocesses article headlines
before inference by the Headline BiLSTM model.
===========================================================
"""

from __future__ import annotations

import re
import string
from typing import Dict

import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

from backend.models.loader import assets


class HeadlineValidator:
    """
    Validates and preprocesses article headlines.

    Responsibilities
    ----------------
    - Validate input
    - Clean headline text
    - Tokenize
    - Pad sequence
    - Return prepared tensor
    """

    MAX_SEQUENCE_LENGTH = 13

    def __init__(self):

        self.tokenizer = assets.headline_tokenizer

    # ======================================================
    # Text Cleaning
    # ======================================================

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean headline text exactly as performed
        during model training.
        """

        text = str(text).lower()

        text = re.sub(r"http\S+\s*", " ", text)

        text = re.sub(r"<.*?>", " ", text)

        text = text.translate(
            str.maketrans("", "", string.punctuation)
        )

        text = re.sub(r"\d+", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # ======================================================
    # Input Validation
    # ======================================================

    @staticmethod
    def _validate_input(headline: str):

        if headline is None:
            raise ValueError("Headline cannot be None.")

        if not isinstance(headline, str):
            raise TypeError("Headline must be a string.")

        if headline.strip() == "":
            raise ValueError("Headline cannot be empty.")

    # ======================================================
    # Tokenization
    # ======================================================

    def tokenize(self, cleaned_text: str) -> np.ndarray:
        """
        Convert cleaned headline into
        padded integer sequence.
        """

        sequence = self.tokenizer.texts_to_sequences(
            [cleaned_text]
        )

        padded = pad_sequences(
            sequence,
            maxlen=self.MAX_SEQUENCE_LENGTH,
            padding="post",
            truncating="post"
        )

        return padded.astype(np.int32)

    # ======================================================
    # Public Interface
    # ======================================================

    def validate(self, headline: str) -> Dict:
        """
        Complete preprocessing pipeline.
        """

        self._validate_input(headline)

        cleaned = self.clean_text(headline)

        tensor = self.tokenize(cleaned)

        return {

            "original_text": headline,

            "clean_text": cleaned,

            "text": tensor

        }