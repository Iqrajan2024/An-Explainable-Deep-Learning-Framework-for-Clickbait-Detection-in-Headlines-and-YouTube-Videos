import pytest

from backend.reasoning.headline_reasoner import HeadlineReasoner

def test_clickbait_summary():

    reasoner = HeadlineReasoner()

    shap = {

        "important_words": [],

        "positive_words": [

            {"word":"shocking"},

            {"word":"secret"}

        ],

        "negative_words":[]
    }

    result = reasoner.explain(

        shap,

        "Clickbait"

    )

    assert "clickbait" in result["summary"].lower()

    assert result["most_influential_word"] == "shocking"


def test_not_clickbait_summary():

    reasoner = HeadlineReasoner()

    shap = {

        "important_words":[],

        "positive_words":[],

        "negative_words":[

            {"word":"official"},

            {"word":"government"}

        ]
    }

    result = reasoner.explain(

        shap,

        "Not Clickbait"

    )

    assert "not clickbait" in result["summary"].lower()

    assert result["most_influential_word"] == "official"

def test_clickbait_without_positive_words():

    reasoner = HeadlineReasoner()

    shap = {

        "important_words":[],

        "positive_words":[],

        "negative_words":[]
    }

    result = reasoner.explain(

        shap,

        "Clickbait"

    )

    assert "language patterns" in result["summary"].lower()


def test_not_clickbait_without_negative_words():

    reasoner = HeadlineReasoner()

    shap = {

        "important_words":[],

        "positive_words":[],

        "negative_words":[]
    }

    result = reasoner.explain(

        shap,

        "Not Clickbait"

    )

    assert "neutral wording" in result["summary"].lower()

def test_max_keywords():

    reasoner = HeadlineReasoner()

    positive = [

        {"word":"w1"},
        {"word":"w2"},
        {"word":"w3"},
        {"word":"w4"},
        {"word":"w5"},
        {"word":"w6"},
        {"word":"w7"}

    ]

    shap = {

        "important_words":positive,

        "positive_words":positive,

        "negative_words":[]
    }

    result = reasoner.explain(

        shap,

        "Clickbait"

    )

    assert len(result["positive_words"]) == 5

def test_no_influential_word():

    reasoner = HeadlineReasoner()

    shap = {

        "important_words":[],

        "positive_words":[],

        "negative_words":[]
    }

    result = reasoner.explain(

        shap,

        "Clickbait"

    )

    assert result["most_influential_word"] is None