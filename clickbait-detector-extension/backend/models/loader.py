"""
===========================================================
ClickDetect AI
Model & Resource Asset Manager

This module is responsible for loading and caching every
AI model and supporting resource required by the backend.

All assets are loaded exactly once during FastAPI startup
and shared across the entire application.

===========================================================
"""

from __future__ import annotations

import json
import pickle
import time
from pathlib import Path

import numpy as np
import tensorflow as tf


class ModelLoader:
    """
    Singleton asset manager responsible for loading and caching
    every machine learning model and resource used by ClickDetect.

    
    """

    _instance = None

    # --------------------------------------------------------
    # Singleton
    # --------------------------------------------------------

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    # --------------------------------------------------------
    # Constructor
    # --------------------------------------------------------

    def __init__(self):

        if self.initialized:
            return

        self.initialized = False

        self.start_time = None
        self.loading_time = 0.0

        # ----------------------------------------------------
        # Project Directories
        # ----------------------------------------------------

        self.backend_dir = Path(__file__).resolve().parents[1]

        self.models_dir = self.backend_dir / "models"

        self.resources_dir = self.backend_dir / "resources"

        # ----------------------------------------------------
        # Prediction Models
        # ----------------------------------------------------

        self.headline_model = None

        self.multimodal_model = None

        # ----------------------------------------------------
        # Surrogate Models
        # ----------------------------------------------------

        self.text_surrogate = None

        self.metadata_surrogate = None


        # ----------------------------------------------------
        # NLP Resources
        # ----------------------------------------------------

        self.headline_tokenizer = None

        self.youtube_text_tokenizer = None

        self.headline_reverse_word_index = None

        self.youtube_reverse_word_index = None

        self.headline_stopwords = None

        self.youtube_stopwords = None

        # ----------------------------------------------------
        # Metadata Resources
        # ----------------------------------------------------

        self.metadata_scaler = None

        self.metadata_feature_names = None

        # ----------------------------------------------------
        # SHAP Background Arrays
        # ----------------------------------------------------

        self.bg_headline = None

        self.bg_youtube_text = None

        self.bg_metadata = None


        # ----------------------------------------------------
        # File Registry
        # ----------------------------------------------------

        self.MODEL_FILES = {
            "headline_model": "headline_bilstm.keras",
            "multimodal_model": "best_multimodal_model.keras",
            "text_surrogate": "text_surrogate.keras",
            "metadata_surrogate": "metadata_surrogate.keras",
        }

        self.RESOURCE_FILES = {
            "headline_tokenizer": "headline_tokenizer.pkl",
            "youtube_text_tokenizer": "youtube_text_tokenizer.pkl",

            "headline_reverse_word_index":
                "headline_reverse_word_index.pkl",

            "youtube_reverse_word_index":
                "youtube_reverse_word_index.pkl",

            "headline_stopwords":
                "headline_stopwords.pkl",

            "youtube_stopwords":
                "youtube_stopwords.pkl",

            "metadata_scaler":
                "youtube_metadata_scaler.pkl",

            "metadata_feature_names":
                "metadata_feature_names.json",

            "bg_headline":
                "headline_background.npy",

            "bg_youtube_text":
                "youtube_text_background.npy",

            "bg_metadata":
                "metadata_background.npy",

            }

    # ==========================================================
    # Logging Utilities
    # ==========================================================

    def _log(self, message: str) -> None:
        """Print formatted loader messages."""
        print(f"[ClickDetect] {message}")

    # ==========================================================
    # File Validation
    # ==========================================================

    def _validate_file(self, file_path: Path) -> None:
        """
        Ensure a required resource exists before attempting
        to load it.
        """

        if not file_path.exists():
            raise FileNotFoundError(
                f"\nRequired file not found:\n{file_path}\n"
            )

    # ==========================================================
    # Generic Resource Loaders
    # ==========================================================

    def _load_pickle(self, filename: str):
        """
        Load a pickle resource from backend/resources.
        """

        file_path = self.resources_dir / filename

        self._validate_file(file_path)

        with open(file_path, "rb") as f:
            return pickle.load(f)

    def _load_json(self, filename: str):
        """
        Load a JSON resource from backend/resources.
        """

        file_path = self.resources_dir / filename

        self._validate_file(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_numpy(self, filename: str):
        """
        Load large NumPy arrays using memory mapping.

        This avoids copying the entire array into RAM.
        """

        file_path = self.resources_dir / filename

        self._validate_file(file_path)

        return np.load(file_path, mmap_mode="r")

    # ==========================================================
    # TensorFlow Model Loader
    # ==========================================================

    def _load_model(self, filename: str):
        """
        Load a TensorFlow / Keras model.
        """

        file_path = self.models_dir / filename

        self._validate_file(file_path)

        self._log(f"Loading {filename}")

        return tf.keras.models.load_model(file_path)

    # ==========================================================
    # Startup Banner
    # ==========================================================

    def _print_banner(self):

        print("\n" + "=" * 60)
        print(" ClickDetect AI v1.0")
        print(" Loading Backend Assets")
        print("=" * 60)



    # ==========================================================
    # Initialize Asset Manager
    # ==========================================================

    def initialize(self):
        """
        Load and cache every model and resource required by
        ClickDetect AI.

        This method is called once during FastAPI startup.
        """

        # Prevent loading twice
        if self.initialized:
            self._log("Assets already initialized.")
            return

        self.start_time = time.time()

        self._print_banner()

        # ------------------------------------------------------
        # Prediction Models
        # ------------------------------------------------------

        self._log("Loading prediction models...")

        self.headline_model = self._load_model(
            self.MODEL_FILES["headline_model"]
        )

        self.multimodal_model = self._load_model(
            self.MODEL_FILES["multimodal_model"]
        )

        # ------------------------------------------------------
        # Surrogate Models
        # ------------------------------------------------------

        self._log("Loading surrogate models...")

        self.text_surrogate = self._load_model(
            self.MODEL_FILES["text_surrogate"]
        )

        self.metadata_surrogate = self._load_model(
            self.MODEL_FILES["metadata_surrogate"]
        )

        # ------------------------------------------------------
        # Tokenizers
        # ------------------------------------------------------

        self._log("Loading tokenizers...")

        self.headline_tokenizer = self._load_pickle(
            self.RESOURCE_FILES["headline_tokenizer"]
        )

        self.youtube_text_tokenizer = self._load_pickle(
            self.RESOURCE_FILES["youtube_text_tokenizer"]
        )

        # ------------------------------------------------------
        # Reverse Word Indices
        # ------------------------------------------------------

        self._log("Loading reverse dictionaries...")

        self.headline_reverse_word_index = self._load_pickle(
            self.RESOURCE_FILES["headline_reverse_word_index"]
        )

        self.youtube_reverse_word_index = self._load_pickle(
            self.RESOURCE_FILES["youtube_reverse_word_index"]
        )

        # ------------------------------------------------------
        # Stopwords
        # ------------------------------------------------------

        self._log("Loading stopword lists...")

        self.headline_stopwords = self._load_pickle(
            self.RESOURCE_FILES["headline_stopwords"]
        )

        self.youtube_stopwords = self._load_pickle(
            self.RESOURCE_FILES["youtube_stopwords"]
        )

        # ------------------------------------------------------
        # Metadata Resources
        # ------------------------------------------------------

        self._log("Loading metadata resources...")

        self.metadata_scaler = self._load_pickle(
            self.RESOURCE_FILES["metadata_scaler"]
        )

        self.metadata_feature_names = self._load_json(
            self.RESOURCE_FILES["metadata_feature_names"]
        )

        # ------------------------------------------------------
        # SHAP Background Arrays
        # ------------------------------------------------------

        self._log("Loading SHAP background arrays...")

        self.bg_headline = self._load_numpy(
            self.RESOURCE_FILES["bg_headline"]
        )

        self.bg_youtube_text = self._load_numpy(
            self.RESOURCE_FILES["bg_youtube_text"]
        )

        self.bg_metadata = self._load_numpy(
            self.RESOURCE_FILES["bg_metadata"]
        )



        # ------------------------------------------------------
        # Finish
        # ------------------------------------------------------

        self.loading_time = round(
            time.time() - self.start_time,
            2
        )

        self.initialized = True

        print()
        self._log("All assets successfully loaded.")
        self._log(f"Initialization time : {self.loading_time} sec")
        print("=" * 60)


# ==========================================================
# Global Asset Manager
# ==========================================================

assets = ModelLoader()