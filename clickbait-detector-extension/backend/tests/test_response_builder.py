import re

from backend.reasoning.response_builder import ResponseBuilder


def test_build_headline_response():

    confidence = {

        "prediction": "Clickbait",

        "confidence_level": "High"

    }

    explanation = {

        "summary": "Headline contains sensational wording."

    }

    result = ResponseBuilder.build_headline_response(

        confidence,

        explanation

    )

    assert result["success"] is True

    assert result["type"] == "headline"

    assert result["prediction"] == confidence

    assert result["explanation"] == explanation

    assert "timestamp" in result


def test_build_youtube_response():

    confidence = {

        "prediction": "Not Clickbait"

    }

    explanation = {

        "summary": "Video title appears informative."

    }

    result = ResponseBuilder.build_youtube_response(

        confidence,

        explanation

    )

    assert result["success"] is True

    assert result["type"] == "youtube"

    assert result["prediction"] == confidence

    assert result["explanation"] == explanation

    assert "timestamp" in result

def test_build_error_response():

    result = ResponseBuilder.build_error_response(

        "Invalid request"

    )

    assert result["success"] is False

    assert result["error"] == "Invalid request"

    assert "timestamp" in result

from datetime import datetime


def test_timestamp_is_valid():

    confidence = {}

    explanation = {}

    result = ResponseBuilder.build_headline_response(

        confidence,

        explanation

    )

    datetime.fromisoformat(result["timestamp"])