"""
===========================================================
ClickDetect AI
YouTube Reasoner

Fuses explanations from the text, metadata,
and image branches into one final explanation.

===========================================================
"""

from __future__ import annotations

from backend.reasoning.exceptions import (
    YoutubeReasonerException,
)


class YoutubeReasoner:
    """
    Combines explanations from all modalities
    into a single multimodal explanation.
    """

    def __init__(self):

        self.max_modalities = 3

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def compile(
        self,
        prediction: str,
        confidence: dict,
        text_reason: dict,
        metadata_reason: dict
    ) -> dict:


        """
        Create the final multimodal explanation.
        """

        try:

            summary = self._generate_summary(
                prediction,
                text_reason,
                metadata_reason
            )

            evidence = self._collect_evidence(
                text_reason,
                metadata_reason
            )

            return {

                "summary": summary,

                "text": text_reason,

                "metadata": metadata_reason,

                "confidence": confidence,

                "modalities_used": [
                    "Text (SHAP)",
                    "Metadata (SHAP)"

                ],

                "evidence":
                    evidence

            }

        except Exception as e:

            raise YoutubeReasonerException(str(e))


    # --------------------------------------------------
    # Generate Overall Summary
    # --------------------------------------------------

    def _generate_summary(
        self,
        prediction,
        text_reason,
        metadata_reason
    ):

        if prediction == "Clickbait":

            return (

                "The video was classified as "
                "clickbait because the textual "
                "content, metadata characteristics, "
                "and thumbnail jointly exhibited "
                "patterns commonly associated with "
                "clickbait."

            )

        return (

            "The video was classified as "
            "not clickbait because the textual "
            "content, metadata, and thumbnail "
            "collectively showed few indicators "
            "of misleading or sensational content."

        )

    # --------------------------------------------------
    # Collect Key Evidence
    # --------------------------------------------------

    def _collect_evidence(
        self,
        text_reason,
        metadata_reason
    ):

        evidence = []

        dominant_word = text_reason.get(
            "dominant_word"
        )

        if dominant_word:

            evidence.append(
                f"Dominant text indicator: {dominant_word}"
            )

        dominant_feature = metadata_reason.get(
            "dominant_feature"
        )

        if dominant_feature:

            evidence.append(

                "Dominant metadata feature: "

                f"{dominant_feature['feature']}"

            )


        return evidence