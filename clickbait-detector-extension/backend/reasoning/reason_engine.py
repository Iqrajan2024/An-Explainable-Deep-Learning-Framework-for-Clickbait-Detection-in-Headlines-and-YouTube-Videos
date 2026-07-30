"""
===========================================================
ClickDetect AI
Reason Engine

Main orchestration layer for explanation generation.

Responsible for:

• Confidence evaluation
• Headline reasoning
• Multimodal reasoning
• Response construction

===========================================================
"""

from __future__ import annotations

from backend.reasoning.confidence_reasoner import ConfidenceReasoner
from backend.reasoning.headline_reasoner import HeadlineReasoner
from backend.reasoning.text_reasoner import YoutubeTextReasoner
from backend.reasoning.metadata_reasoner import MetadataReasoner
from backend.reasoning.youtube_reasoner import YoutubeReasoner
from backend.reasoning.response_builder import ResponseBuilder
from backend.reasoning.exceptions import (
    ReasonEngineException,
)


class ReasonEngine:

    def __init__(self):

        self.confidence_reasoner = ConfidenceReasoner()

        self.headline_reasoner = HeadlineReasoner()

        self.youtube_text_reasoner = YoutubeTextReasoner()

        self.metadata_reasoner = MetadataReasoner()

        self.youtube_reasoner = YoutubeReasoner()

        self.response_builder = ResponseBuilder()

    # --------------------------------------------------
    # Headline Pipeline
    # --------------------------------------------------

    def process_headline(
        self,
        raw_score: float,
        headline_shap: dict
    ) -> dict:

        try:

            confidence = self.confidence_reasoner.evaluate(
                raw_score
            )

            explanation = self.headline_reasoner.explain(

                shap_result=headline_shap,

                prediction=confidence["prediction"]

            )

            return self.response_builder.build_headline_response(

                confidence=confidence,

                explanation=explanation

            )

        except Exception as e:

            raise ReasonEngineException(str(e))

    # --------------------------------------------------
    # YouTube Pipeline
    # --------------------------------------------------

    def process_youtube(
        self,
        raw_score: float,
        text_shap: dict,
        metadata_shap: dict,
        gradcam: dict | None = None
    ) -> dict:

        try:

            confidence = self.confidence_reasoner.evaluate(
                raw_score
            )

            prediction = confidence["prediction"]

            text_reason = self.youtube_text_reasoner.explain(

                shap_result=text_shap,

                prediction=prediction

            )

            metadata_reason = self.metadata_reasoner.explain(

                shap_result=metadata_shap,

                prediction=prediction

            )


            explanation = self.youtube_reasoner.compile(

                prediction=prediction,

                confidence=confidence,

                text_reason=text_reason,

                metadata_reason=metadata_reason

            )

            return self.response_builder.build_youtube_response(

                confidence=confidence,

                explanation=explanation,


            )

        except Exception as e:

            raise ReasonEngineException(str(e))