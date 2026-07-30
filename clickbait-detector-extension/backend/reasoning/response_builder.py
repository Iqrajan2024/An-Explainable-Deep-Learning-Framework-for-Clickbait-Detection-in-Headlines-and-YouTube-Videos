"""
===========================================================
ClickDetect AI
Response Builder

Constructs standardized API responses for the
Chrome Extension.

===========================================================
"""

from __future__ import annotations

from datetime import datetime

from backend.reasoning.exceptions import (
    ResponseBuilderException,
)


class ResponseBuilder:

    # --------------------------------------------------
    # Headline Response
    # --------------------------------------------------

    @staticmethod
    def build_headline_response(
        confidence: dict,
        explanation: dict
    ) -> dict:

        try:

            return {

                "success": True,

                "type": "headline",

                "prediction": confidence,

                "explanation": explanation,

                "timestamp":
                    datetime.utcnow().isoformat()

            }

        except Exception as e:

            raise ResponseBuilderException(str(e))

    # --------------------------------------------------
    # YouTube Response
    # --------------------------------------------------

    @staticmethod
    def build_youtube_response(
        confidence: dict,
        explanation: dict
    ) -> dict:

        try:

            return {

                "success": True,

                "type": "youtube",

                "prediction": confidence,

                "explanation": explanation,

                "timestamp":
                    datetime.utcnow().isoformat()

            }

        except Exception as e:

            raise ResponseBuilderException(str(e))

    # --------------------------------------------------
    # Error Response
    # --------------------------------------------------

    @staticmethod
    def build_error_response(
        message: str
    ) -> dict:

        return {

            "success": False,

            "error": message,

            "timestamp":
                datetime.utcnow().isoformat()

        }