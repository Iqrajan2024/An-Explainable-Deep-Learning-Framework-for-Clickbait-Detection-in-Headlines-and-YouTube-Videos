import pytest
from backend.validators.multimodal_validator  import MultimodalValidator

def test_safe_text_none():
    assert MultimodalValidator.safe_text(None) == ""

def test_safe_text_string():
    assert MultimodalValidator.safe_text(" Hello ") == "Hello"


def test_clean_text():
    text = "WATCH THIS!!! 2025 https://youtube.com"

    cleaned = MultimodalValidator.clean_text(text)

    assert cleaned == "watch this"
def test_validate_inputs_empty_title():
    validator = MultimodalValidator()

    with pytest.raises(ValueError):
        validator._validate_inputs(
            "",
            "",
            "",
            "",
            "",
            "",
            None,
            None
        )

def test_build_text():
    validator = MultimodalValidator()

    text = validator.build_text(
        "AI News",
        "Latest update",
        "AI",
        "Amazing",
        "Tech",
        "OpenAI"
    )

    assert "ai news" in text