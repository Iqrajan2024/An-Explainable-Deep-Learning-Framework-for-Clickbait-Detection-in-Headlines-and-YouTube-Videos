"""
===========================================================
ClickDetect AI
Headline Prediction API

Handles article headline predictions.

Pipeline

Request
    ↓
Validator
    ↓
Headline Model
    ↓
SHAP Generator
    ↓
Reason Engine
    ↓
JSON Response

===========================================================
"""

from __future__ import annotations

import traceback

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)

from pydantic import BaseModel

from backend.models.loader import assets


router = APIRouter()

# ==========================================================
# Request Schema
# ==========================================================

class HeadlineRequest(BaseModel):

    headline: str

# ==========================================================
# Prediction Endpoint
# ==========================================================

@router.post("/predict/headline")

async def predict_headline(

    payload: HeadlineRequest,

    request: Request

):

    try:

        components = request.app.state.components

        validator = components["headline_validator"]

        shap_generator = components["headline_shap"]

        engine = components["reason_engine"]


        validated = validator.validate(

            payload.headline

        )

        print("=" * 60)
        print("HEADLINE DATA")
        print("=" * 60)
        print(f"Headline: {payload.headline}")
        print("=" * 60)



        sequence = validated["text"]
        raw_score = float(

            assets.headline_model.predict(

                sequence,

                verbose=0

            )[0][0]

        )
        shap_result = shap_generator.generate_explanation(

            validated

        )


        response = engine.process_headline(

            raw_score=raw_score,

            headline_shap=shap_result

        )

        return response

    except Exception as e:

        print()

        print("=" * 60)

        print("Headline Prediction Error")

        traceback.print_exc()

        print("=" * 60)

        print()

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )