"""
===========================================================
ClickDetect AI
FastAPI Application

Initializes the backend and loads every shared
component exactly once during application startup.

===========================================================
"""

import warnings

# Suppress StandardScaler feature-name warning
warnings.filterwarnings(
    "ignore",
    message="X does not have valid feature names*"
)

# Suppress SHAP KernelExplainer warning
warnings.filterwarnings(
    "ignore",
    message="Linear regression equation is singular*"
)

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models.loader import assets

from backend.services.youtube_api_client import YoutubeAPIClient

# Validators
from backend.validators.headline_validator import (
    HeadlineValidator,
)

from backend.validators.multimodal_validator import (
    MultimodalValidator,
)

# Explainability
from backend.explainability.headline_text_shap import (
    HeadlineTextShap,
)

from backend.explainability.youtube_text_shap import (
    YouTubeTextShap,
)

from backend.explainability.metadata_shap import (
    MetadataShap,
)

# Reasoning

from backend.reasoning.reason_engine import (
    ReasonEngine,
)

# Routers

from backend.api.headline_api import router as headline_router
from backend.api.youtube_api import router as youtube_router


from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("\n===================================")
    print("Starting ClickDetect Backend...")
    print("===================================\n")

    # ---------------------------------------------
    # Load all ML assets
    # ---------------------------------------------

    assets.initialize()

    # ---------------------------------------------
    # Shared Components
    # ---------------------------------------------

    app.state.components = {

        "headline_validator":
            HeadlineValidator(),

        "multimodal_validator":
            MultimodalValidator(),

        "headline_shap":
            HeadlineTextShap(),

        "youtube_text_shap":
            YouTubeTextShap(),

        "metadata_shap":
            MetadataShap(),



        "reason_engine":
            ReasonEngine(),

        "youtube_client": YoutubeAPIClient()

    }

    print("\nBackend Ready.\n")

    yield

    print("\nStopping ClickDetect Backend...\n")

app = FastAPI(

    title="ClickDetect AI",

    version="1.0",

    lifespan=lifespan

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(

    headline_router,

    tags=["Headline"]

)

app.include_router(

    youtube_router,

    tags=["YouTube"]

)



@app.get("/")
def root():

    return {

        "application":
            "ClickDetect AI",

        "status":
            "Running"

    }


@app.get("/health")
def health():

    return {

        "status":
            "healthy"

    }