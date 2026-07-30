"""
===========================================================
ClickDetect AI
Headline Reasoner

Converts SHAP explanations into a human-readable
explanation for article headlines.

===========================================================
"""

from __future__ import annotations

from backend.reasoning.exceptions import (
    HeadlineReasonerException,
)


class HeadlineReasoner:
    """
    Converts SHAP outputs into explanations suitable
    for the API response.
    """

    def __init__(self):

        self.max_keywords = 5

    # ==================================================
    # Public API
    # ==================================================

    def explain(
        self,
        shap_result: dict,
        prediction: str,
    ) -> dict:

        try:

            important = shap_result.get(
                "important_words",
                []
            )

            positive = shap_result.get(
                "positive_words",
                []
            )

            negative = shap_result.get(
                "negative_words",
                []
            )

            summary = self._generate_summary(
                prediction,
                positive,
                negative,
            )

            return {

                "summary": summary,

                "important_words":
                    important[:self.max_keywords],

                "positive_words":
                    positive[:self.max_keywords],

                "negative_words":
                    negative[:self.max_keywords],

                "most_influential_word":
                    self._most_influential_word(
                        positive,
                        negative,
                        prediction,
                    )

            }

        except Exception as e:

            raise HeadlineReasonerException(str(e))

    # ==================================================
    # Summary
    # ==================================================

    def _generate_summary(
        self,
        prediction,
        positive,
        negative,
    ):

        if prediction == "Clickbait":

            if positive:

                words = ", ".join(
                    item["word"]
                    for item in positive[:3]
                )

                return (
                    "The headline was classified as clickbait "
                    "because words such as "
                    f"{words} "
                    "strongly increased the predicted clickbait probability."
                )

            return (
                "The headline contains language patterns "
                "commonly associated with clickbait."
            )

        # ---------------------------------------------

        if negative:

            words = ", ".join(
                item["word"]
                for item in negative[:3]
            )

            return (
                "The headline was classified as not clickbait "
                "because words such as "
                f"{words} "
                "reduced the predicted clickbait probability."
            )

        return (
            "The headline contains mostly neutral wording "
            "with few strong clickbait indicators."
        )

    # ==================================================
    # Most Influential Word
    # ==================================================

    def _most_influential_word(
        self,
        positive,
        negative,
        prediction,
    ):

        if prediction == "Clickbait":

            if positive:
                return positive[0]["word"]

            if negative:
                return negative[0]["word"]

        else:

            if negative:
                return negative[0]["word"]

            if positive:
                return positive[0]["word"]

        return None