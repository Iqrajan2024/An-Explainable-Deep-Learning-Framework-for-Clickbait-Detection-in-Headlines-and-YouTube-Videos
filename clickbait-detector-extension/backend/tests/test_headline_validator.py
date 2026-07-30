# backend/tests/test_headline_validator.py
import pytest

from backend.validators.headline_validator import HeadlineValidator


def test_clean_text():

    text = "Scientists Discover!!! New Planet 2025"

    cleaned = HeadlineValidator.clean_text(text)

    assert cleaned == "scientists discover new planet"


def test_validate_input_valid():

    HeadlineValidator._validate_input(

        "Scientists discover new planet"

    )

def test_validate_input_empty():

    with pytest.raises(ValueError):

        HeadlineValidator._validate_input("")


def test_validate_input_none():

    with pytest.raises(ValueError):

        HeadlineValidator._validate_input(None)



def test_validate_input_integer():

    with pytest.raises(TypeError):

        HeadlineValidator._validate_input(123)
