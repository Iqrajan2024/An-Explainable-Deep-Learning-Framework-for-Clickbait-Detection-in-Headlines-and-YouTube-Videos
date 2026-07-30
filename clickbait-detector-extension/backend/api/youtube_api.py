"""
===========================================================
ClickDetect AI
YouTube Prediction API

Handles multimodal YouTube clickbait prediction.

Pipeline

Request
    ↓
Multimodal Validator
    ↓
Multimodal Model
    ↓
Text SHAP
Metadata SHAP
GradCAM
    ↓
Reason Engine
    ↓
JSON Response

===========================================================
"""

from __future__ import annotations
from backend.models.loader import assets

import traceback
import time

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)

from pydantic import BaseModel

router = APIRouter()

# ==========================================================
# Request Schema
# ==========================================================

class YoutubeRequest(BaseModel):

    videoId: str



# ==========================================================
# Prediction Endpoint
# ==========================================================

@router.post("/predict/youtube")

async def predict_youtube(

    payload: YoutubeRequest,

    request: Request

):

    try:

        components = request.app.state.components

        validator = components["multimodal_validator"]

        text_shap = components["youtube_text_shap"]

        metadata_shap = components["metadata_shap"]

        engine = components["reason_engine"]

        youtube = components["youtube_client"]

        start = time.time()

        video = youtube.get_video(
            payload.videoId
        )

        print("\n" + "=" * 60)
        print("VIDEO DATA")
        print("=" * 60)
        print("Title:", video["title"])
        print("Video ID:", payload.videoId)
        print("=" * 60 + "\n")

        print(
            "YouTube API:",
            time.time() - start
        )

        t = time.time()

        validated = validator.validate(

            title=video["title"],

            description=video["description"],

            tags=video["tags"],

            category=video["category"],

            channel=video["channel_title"],

            top_comments=video["top_comments"],

            metadata= video["metadata"],

            image=video["thumbnail"]

        )

        print("Validation:", time.time()-t)

        text_input = validated["text"]

        metadata_input = validated["metadata"]

        image_input = validated["image"]



        t = time.time()

        raw_score = float(

            assets.multimodal_model.predict(

                [

                    image_input,

                    text_input,

                    metadata_input

                ],

                verbose=0

            )[0][0]

        )

        print("Prediction:", time.time()-t)

        t = time.time()

        text_result = text_shap.generate(

            text_input

        )




        print("Text SHAP:", time.time()-t)

        t = time.time()

        metadata_result = metadata_shap.generate_explanation(

            validated

        )

        print("Metadata SHAP:", time.time()-t)

        

        response = engine.process_youtube(

            raw_score=raw_score,

            text_shap=text_result,

            metadata_shap=metadata_result,
            
            )

        response["title"] = video["title"]

        response["channel_title"] = video["channel_title"]


        return response

    except Exception as e:

        print()

        print("=" * 60)

        print("YouTube Prediction Error")

        traceback.print_exc()

        print("=" * 60)

        print()

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
