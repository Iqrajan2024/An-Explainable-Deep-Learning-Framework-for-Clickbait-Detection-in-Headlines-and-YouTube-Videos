"""
===========================================================
ClickDetect AI

YouTube Text SHAP Generator

Generates SHAP explanations for the textual branch
of the multimodal clickbait detector.

Uses

• Text Surrogate Model
• Kernel SHAP

===========================================================
"""

from __future__ import annotations

import numpy as np
import shap

from backend.models.loader import assets


class YouTubeTextShap:
    """
    Generates SHAP explanations for the textual
    component of the multimodal model.

    Uses

    assets.text_surrogate

    """

    def __init__(self):

        self.model = assets.text_surrogate

        self.background = np.asarray(
            assets.bg_youtube_text
        )

        self.reverse_index = (
            assets.youtube_reverse_word_index
        )

        self.stopwords = set(
            assets.youtube_stopwords
        )

        self.explainer = shap.KernelExplainer(
            self.predict_fn,
            self.background
        )

    # --------------------------------------------------
    # Prediction Function
    # --------------------------------------------------

    def predict_fn(
        self,
        sequences: np.ndarray
    ) -> np.ndarray:
        """
        Prediction callback for Kernel SHAP.
        """

        return self.model.predict(
            sequences,
            verbose=0
        )

    # --------------------------------------------------
    # Sequence → Words
    # --------------------------------------------------

    def sequence_to_words(
        self,
        sequence: np.ndarray,
    ) -> list[str]:
        """
        Convert an integer token sequence back into words.
        """

        words = []

        for token in sequence:

            token = int(token)

            if token == 0:
                continue

            word = self.reverse_index.get(token)

            if word is None:
                continue

            words.append(word)

        return words


    # --------------------------------------------------
    # Remove Stopwords
    # --------------------------------------------------

    def filter_words(
        self,
        words: list[str],
        shap_values: np.ndarray,
    ):
        """
        Remove stopwords while preserving SHAP alignment.
        """

        filtered_words = []

        filtered_scores = []

        for word, score in zip(words, shap_values):

            if word in self.stopwords:
                continue

            if len(word) <= 1:
                continue

            filtered_words.append(word)

            filtered_scores.append(float(np.ravel(score)[0]))

        return filtered_words, filtered_scores


    # --------------------------------------------------
    # Build Importance
    # --------------------------------------------------

    def build_importance(
        self,
        words,
        scores,
    ):
        """
        Convert words and SHAP values into JSON-ready objects.
        """

        importance = []

        for word, score in zip(words, scores):

            importance.append({

                "word": word,

                "importance": round(
                    float(score),
                    6,
                ),

                "direction":
                    "positive"
                    if score >= 0
                    else "negative"

            })

        importance.sort(

            key=lambda x: abs(
                x["importance"]
            ),

            reverse=True

        )

        return importance

    # --------------------------------------------------
    # Top Positive
    # --------------------------------------------------

    def top_positive(
        self,
        importance,
        top_k=10,
    ):
        return [
            item
            for item in importance
            if item["importance"] > 0
        ][:top_k]


    # --------------------------------------------------
    # Top Negative
    # --------------------------------------------------

    def top_negative(
        self,
        importance,
        top_k=10,
    ):
        return [
            item
            for item in importance
            if item["importance"] < 0
        ][:top_k]


    def generate(self, text_input):
        shap_values = self.explainer.shap_values(text_input, nsamples=50)

        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        shap_values = np.asarray(shap_values)

        words = self.sequence_to_words(text_input[0])

        scores = shap_values[0][:len(words)]

        words, scores = self.filter_words(words, scores)

        importance = self.build_importance(words, scores)

        # ---------------------------------------
        # Remove insignificant words
        # ---------------------------------------

        MIN_IMPORTANCE = 0.01

        importance = [
            item
            for item in importance
            if abs(item["importance"]) >= MIN_IMPORTANCE
        ]

        positive = self.top_positive(importance)

        negative = self.top_negative(importance)

        return {

            # Detailed SHAP information
            "importance": importance,
            "positive": positive,
            "negative": negative,

            # Simple word lists for the reasoner
            "important_words": [
                item["word"]
                for item in importance
            ],

            "positive_words": [
                item["word"]
                for item in positive
            ],

            "negative_words": [
                item["word"]
                for item in negative
            ]

        }

