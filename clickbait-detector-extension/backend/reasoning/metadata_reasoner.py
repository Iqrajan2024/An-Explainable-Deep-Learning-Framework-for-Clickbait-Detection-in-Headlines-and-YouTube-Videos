"""
===========================================================
ClickDetect AI
Metadata Reasoner

Converts metadata SHAP explanations into
human-readable explanations.

===========================================================
"""

from __future__ import annotations

from backend.reasoning.exceptions import (
    MetadataReasonerException,
)


class MetadataReasoner:
    """
    Generates explanations for metadata
    features used by the multimodal model.
    """

    def __init__(self):

        self.max_features = 5

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

            Output from metadata_shap.py

        prediction

            Clickbait / Not Clickbait

        Returns
        -------
        dict
        """

        try:

            metrics = shap_result.get(
                "metrics",
                []
            )

            if not metrics:

                return {
                    "summary":
                        "No significant metadata features influenced the prediction.",
                    "important_features": [],
                    "positive_features": [],
                    "negative_features": []
                }

            positive = [
                m for m in metrics
                if m["impact"] > 0
            ]

            negative = [
                m for m in metrics
                if m["impact"] < 0
            ]

            summary = self._generate_summary(
                prediction,
                positive,
                negative
            )

            return {

                "summary": summary,

                "important_features":
                    metrics[:self.max_features],

                "positive_features":
                    positive[:self.max_features],

                "negative_features":
                    negative[:self.max_features],

                "dominant_feature":
                    self._dominant_feature(metrics)

            }

        except Exception as e:

            raise MetadataReasonerException(str(e))

    # --------------------------------------------------
    # Generate Summary
    # --------------------------------------------------

    def _generate_summary(
        self,
        prediction,
        positive,
        negative
    ):

        if prediction == "Clickbait":

            if positive:

                names = ", ".join(
                    [
                        f["feature"]
                        for f in positive[:3]
                    ]
                )

                return (
                    "Metadata features such as "
                    f"{names} increased the "
                    "predicted clickbait score."
                )

            return (
                "Metadata contributed only "
                "slightly to the clickbait prediction."
            )

        else:

            if negative:

                names = ", ".join(
                    [
                        f["feature"]
                        for f in negative[:3]
                    ]
                )

                return (
                    "Metadata features such as "
                    f"{names} reduced the "
                    "predicted clickbait score."
                )

            return (
                "Metadata had little influence "
                "on the final prediction."
            )

    # --------------------------------------------------
    # Dominant Feature
    # --------------------------------------------------

    def _dominant_feature(
        self,
        metrics
    ):

        if not metrics:
            return None

        return max(
            metrics,
            key=lambda x: abs(x["impact"])
        )