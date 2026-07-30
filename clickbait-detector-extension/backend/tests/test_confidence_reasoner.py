import pytest

from backend.reasoning.confidence_reasoner import ConfidenceReasoner
from backend.reasoning.exceptions import ConfidenceReasonerException

def test_clickbait_prediction():

    reasoner = ConfidenceReasoner()

    result = reasoner.evaluate(0.95)

    assert result["prediction"] == "Clickbait"

def test_not_clickbait_prediction():

    reasoner = ConfidenceReasoner()

    result = reasoner.evaluate(0.20)

    assert result["prediction"] == "Not Clickbait"


def test_threshold_prediction():

    reasoner = ConfidenceReasoner()

    result = reasoner.evaluate(0.50)

    assert result["prediction"] == "Clickbait"

def test_very_high_confidence():

    reasoner = ConfidenceReasoner()

    result = reasoner.evaluate(0.95)

    assert result["confidence_level"] == "Very High"


def test_high_confidence():

    reasoner = ConfidenceReasoner()

    result = reasoner.evaluate(0.80)

    assert result["confidence_level"] == "High"

def test_moderate_confidence():

    reasoner = ConfidenceReasoner()

    result = reasoner.evaluate(0.65)

    assert result["confidence_level"] == "Moderate"


def test_low_confidence():

    reasoner = ConfidenceReasoner()

    result = reasoner.evaluate(0.55)

    assert result["confidence_level"] == "Low"

def test_probability_greater_than_one():

    reasoner = ConfidenceReasoner()

    with pytest.raises(ConfidenceReasonerException):

        reasoner.evaluate(1.5)

def test_probability_less_than_zero():

    reasoner = ConfidenceReasoner()

    with pytest.raises(ConfidenceReasonerException):

        reasoner.evaluate(-0.25)