"""
===========================================================
ClickDetect AI
YouTube Text Reasoner

Converts SHAP explanations from the YouTube text
branch into human-readable explanations.

===========================================================
"""

from __future__ import annotations

from backend.reasoning.exceptions import (
    YoutubeTextReasonerException,
)


class YoutubeTextReasoner:
    """
    Generates explanations for the textual
    component of the multimodal model.
    """

    def __init__(self):

        self.max_words = 5

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def explain(
        self,
        shap_result: dict,
        prediction: str
    ) -> dict:

        """
        Parameters
        ----------
        shap_result

            Output from youtube_text_shap.py

        prediction

            Clickbait / Not Clickbait

        Returns
        -------
        dict
        """

        try:

            positive = shap_result.get(
                "positive_words",
                []
            )

            negative = shap_result.get(
                "negative_words",
                []
            )

            important = shap_result.get(
                "important_words",
                []
            )

            summary = self._generate_summary(
                prediction,
                positive,
                negative,
                important
            )

            return {

                "summary": summary,

                "important_words":
                    shap_result.get("importance", [])[:self.max_words],

                "positive_words":
                    shap_result.get("positive", [])[:self.max_words],

                "negative_words":
                    shap_result.get("negative", [])[:self.max_words],

                "dominant_word":
                    self._dominant_word(
                        important
                    )

            }

        except Exception as e:

            raise YoutubeTextReasonerException(str(e))

    # --------------------------------------------------
    # Generate Summary
    # --------------------------------------------------

    def _generate_summary(
        self,
        prediction,
        positive,
        negative,
        important
    ):

        if prediction == "Clickbait":

            if positive:

                words = ", ".join(
                    positive[:3]
                )

                return (

                    "The video's text contains "
                    "attention-grabbing language "
                    f"such as {words}, which "
                    "strongly increased the "
                    "clickbait probability."

                )

            return (

                "The textual content contains "
                "patterns commonly associated "
                "with clickbait."

            )

        else:

            if negative:

                words = ", ".join(
                    negative[:3]
                )

                return (

                    "The video's text appears "
                    "more informative because "
                    f"words such as {words} "
                    "reduced the clickbait score."

                )

            return (

                "The textual content appears "
                "mostly neutral with few "
                "clickbait indicators."

            )

    # --------------------------------------------------
    # Dominant Word
    # --------------------------------------------------

    def _dominant_word(
        self,
        important_words
    ):

        if not important_words:

            return None

        return important_words[0]