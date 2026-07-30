"""
===========================================================
ClickDetect AI

Headline SHAP Explanation Generator

Generates word-level SHAP explanations for the
Headline BiLSTM model.

Uses:

• Original Headline BiLSTM
• SHAP KernelExplainer
• Cached resources from ModelLoader

===========================================================
"""

from __future__ import annotations

import numpy as np
import shap

from backend.models.loader import assets


class HeadlineTextShap:
    """
    Generates SHAP explanations for article headlines.

    Input
    -----
    validator_output

    Uses
    ----
    assets.headline_model

    Returns
    -------
    JSON-ready explanation.
    """

    def __init__(self):

        self.model = assets.headline_model

        self.background = np.asarray(
            assets.bg_headline
        )

        self.reverse_index = (
            assets.headline_reverse_word_index
        )

        self.stopwords = set(
            assets.headline_stopwords
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
        Prediction callback used by SHAP.
        """

        predictions = self.model.predict(
            sequences,
            verbose=0
        )

        return predictions

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
        Remove stopwords while keeping SHAP values aligned.
        """

        filtered_words = []

        filtered_scores = []

        for word, score in zip(words, shap_values):


            if word in self.stopwords:
                continue

            if len(word) <= 1:
                continue

            filtered_words.append(word)

            filtered_scores.append(float(score))

        return filtered_words, filtered_scores

    # --------------------------------------------------
    # Build Word Importance
    # --------------------------------------------------

    def build_importance(
        self,
        words,
        scores,
    ):
        """
        Convert words and SHAP scores into
        JSON-ready dictionaries.
        """

        importance = []

        for word, score in zip(words, scores):

            direction = (
                "positive"
                if score >= 0
                else "negative"
            )

            importance.append({

                "word": word,

                "importance": round(
                    float(score),
                    6,
                ),

                "direction": direction

            })

        importance.sort(

            key=lambda x: abs(
                x["importance"]
            ),

            reverse=True

        )

        return importance

    # --------------------------------------------------
    # Positive Contributors
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
    # Negative Contributors
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

    # --------------------------------------------------
    # Generate SHAP Explanation
    # --------------------------------------------------

    def generate_explanation(
        self,
        validator_output: dict,
        top_k: int = 10,
    ) -> dict:
        """
        Generate SHAP explanation for a validated headline.

        Parameters
        ----------
        validator_output : dict
            Output returned by HeadlineValidator.validate()

        top_k : int
            Number of important words to return.

        Returns
        -------
        dict
            JSON-ready explanation.
        """

        # ------------------------------------------
        # Input sequence
        # ------------------------------------------

        sequence = validator_output["text"]

        # ------------------------------------------
        # Prediction
        # ------------------------------------------

        prediction = float(
            self.model.predict(
                sequence,
                verbose=0
            )[0][0]
        )

        # ------------------------------------------
        # SHAP values
        # ------------------------------------------

        shap_values = self.explainer.shap_values(
            sequence,
            nsamples=100
        )


        # KernelExplainer may return a list
        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        shap_values = np.asarray(shap_values)

        # Remove batch dimension (13,1)
        if shap_values.ndim == 3:
            shap_values = shap_values[0]

        #Remove output dimension (13,)
        if shap_values.ndim == 2 and shap_values.shape[-1] == 1:
            shap_values = shap_values[:,0]


        # ------------------------------------------
        # Convert sequence to words
        # ------------------------------------------

        words = self.sequence_to_words(
            sequence[0]
        )

        # Only keep SHAP values for non-padding tokens
        token_count = len(words)

        scores = shap_values[:token_count]

        # ------------------------------------------
        # Remove stopwords
        # ------------------------------------------


        words, scores = self.filter_words(
            words,
            scores
        )


        # ------------------------------------------
        # Build importance table
        # ------------------------------------------

        importance = self.build_importance(
            words,
            scores
        )

        positive = self.top_positive(
            importance,
            top_k
        )

        negative = self.top_negative(
            importance,
            top_k
        )

        # ------------------------------------------
        # Base value
        # ------------------------------------------

        try:

            base_value = float(
                np.asarray(
                    self.explainer.expected_value
                ).flatten()[0]
            )

        except Exception:

            base_value = None

        # ------------------------------------------
        # Return
        # ------------------------------------------

        return {

            "prediction": prediction,

            "label": (
                "Clickbait"
                if prediction >= 0.5
                else "Not Clickbait"
            ),

            "base_value": base_value,

            "important_words": importance[:top_k],

            "positive_words": positive,

            "negative_words": negative,

            "shap_values": scores,

            "words": words
        }