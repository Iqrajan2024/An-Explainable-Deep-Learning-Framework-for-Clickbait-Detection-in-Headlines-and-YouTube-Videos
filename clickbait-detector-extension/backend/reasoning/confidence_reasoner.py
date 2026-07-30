"""
===========================================================
ClickDetect AI
Confidence Reasoner

Converts raw model probability into a standardized
confidence assessment used throughout the application.

Used by:
    • Headline Predictions
    • YouTube Predictions

===========================================================
"""

from __future__ import annotations

from backend.reasoning.exceptions import (
    ConfidenceReasonerException,
)


class ConfidenceReasoner:
    """
    Converts a raw prediction probability into
    human-readable confidence information.
    """

    def __init__(self):

        self.threshold = 0.50


    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def evaluate(self, probability: float) -> dict:
        """
        Evaluate model prediction confidence.

        Parameters
        ----------
        probability : float
            Clickbait probability returned by model.

        Returns
        -------
        dict
            Standardized prediction and confidence information.
        """

        try:

            probability = float(probability)

            if probability < 0.0 or probability > 1.0:
                raise ValueError(
                    "Probability must be between 0 and 1."
                )


            # Determine predicted class
            prediction = (
                "Clickbait"
                if probability >= self.threshold
                else "Not Clickbait"
            )


            # Confidence of predicted class
            if prediction == "Clickbait":

                confidence_score = probability

            else:

                confidence_score = 1.0 - probability


            confidence = self._calculate_confidence(
                confidence_score
            )


            # Prediction based color
            if prediction == "Clickbait":

                color = "#D32F2F"     # Red warning

            else:

                color = "#388E3C"     # Green safe


            return {

                "prediction": prediction,

                # Raw clickbait probability
                "probability":
                    round(probability, 4),


                # Confidence in predicted class
                "confidence_percentage":
                    round(confidence_score * 100, 2),


                "confidence_level":
                    confidence["level"],


                "badge":
                    confidence["badge"],


                "color":
                    color
            }


        except Exception as e:

            raise ConfidenceReasonerException(str(e))


    # --------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------

    def _calculate_confidence(
        self,
        confidence_score: float
    ) -> dict:
        """
        Map predicted-class confidence
        to a confidence level.

        Parameters
        ----------
        confidence_score : float
            Confidence of predicted class
            (0-1 range).

        Returns
        -------
        dict
            Confidence label and badge.
        """


        if confidence_score >= 0.90:

            return {

                "level": "Very High",

                "badge":
                    "Very High Confidence"
            }


        elif confidence_score >= 0.75:

            return {

                "level": "High",

                "badge":
                    "High Confidence"
            }


        elif confidence_score >= 0.60:

            return {

                "level": "Moderate",

                "badge":
                    "Moderate Confidence"
            }


        else:

            return {

                "level": "Low",

                "badge":
                    "Low Confidence"
            }