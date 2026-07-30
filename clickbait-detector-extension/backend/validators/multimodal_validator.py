"""
===========================================================
ClickDetect AI
Multimodal Input Validator

Validates and preprocesses YouTube video data before
prediction using the multimodal clickbait model.

This module is responsible ONLY for preprocessing.
No prediction or explainability is performed here.
===========================================================
"""

from __future__ import annotations

import re
import string
import pandas as pd
from typing import Any, Dict, List

import cv2
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

from backend.models.loader import assets


class MultimodalValidator:
    """
    Validates and preprocesses YouTube inputs.

    Responsibilities
    ----------------
    • Validate incoming data
    • Clean textual information
    • Build combined text
    • Tokenize text
    • Scale metadata
    • Prepare thumbnail
    • Return tensors ready for inference

    This validator is shared by:

    • Prediction API
    • Text SHAP
    • Metadata SHAP
    • Image SHAP
    • GradCAM
    • Reason Engine
    """

    MAX_SEQUENCE_LENGTH = 599

    IMAGE_WIDTH = 224
    IMAGE_HEIGHT = 224

    def __init__(self):

        self.tokenizer = assets.youtube_text_tokenizer

        self.scaler = assets.metadata_scaler

        self.feature_names = assets.metadata_feature_names

    # ======================================================
    # SAFE TEXT
    # ======================================================

    @staticmethod
    def safe_text(value: Any) -> str:
        """
        Convert None values into empty strings.

        Prevents the tokenizer from seeing
        the literal string 'None'.
        """

        if value is None:
            return ""

        return str(value).strip()

    # ======================================================
    # TEXT CLEANING
    # ======================================================

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text exactly as performed during
        multimodal model training.
        """

        text = str(text).lower()

        # Remove URLs
        text = re.sub(r"http\S+", "", text)

        # Remove HTML tags
        text = re.sub(r"<.*?>", "", text)

        # Remove punctuation
        text = text.translate(
            str.maketrans("", "", string.punctuation)
        )

        # Remove numbers
        text = re.sub(r"\d+", "", text)

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # ======================================================
    # INPUT VALIDATION
    # ======================================================

    def _validate_inputs(
        self,
        title,
        description,
        tags,
        top_comments,
        category,
        channel,
        metadata,
        image,
    ):
        """
        Validate incoming request data.

        Rather than raising an exception immediately,
        collect warnings whenever possible so the API
        can still decide whether prediction can continue.
        """

        warnings = []

        # -----------------------------
        # Text Fields
        # -----------------------------

        title = self.safe_text(title)
        description = self.safe_text(description)
        tags = self.safe_text(tags)
        top_comments = self.safe_text(top_comments)
        category = self.safe_text(category)
        channel = self.safe_text(channel)

        if title == "":
            raise ValueError(
                "Video title cannot be empty."
            )

        if description == "":
            warnings.append(
                "Description missing."
            )

        if tags == "":
            warnings.append(
                "Tags missing."
            )

        if top_comments == "":
            warnings.append(
                "Top comments missing."
            )

        if category == "":
            warnings.append(
                "Category missing."
            )

        if channel == "":
            warnings.append(
                "Channel name missing."
            )

        # -----------------------------
        # Metadata
        # -----------------------------

        expected = len(self.feature_names)

        if metadata is None:

            warnings.append(
                "Metadata missing."
            )

            metadata = np.zeros(
                expected,
                dtype=np.float32
            )

        else:

            metadata = list(metadata)

            cleaned = []

            for value in metadata:

                if value is None:

                    cleaned.append(0.0)

                else:

                    try:
                        cleaned.append(float(value))

                    except Exception:

                        cleaned.append(0.0)

            metadata = cleaned

            if len(metadata) < expected:

                warnings.append(
                    "Metadata incomplete."
                )

                metadata.extend(
                    [0.0] * (expected - len(metadata))
                )

            elif len(metadata) > expected:

                warnings.append(
                    "Extra metadata ignored."
                )

                metadata = metadata[:expected]

        # -----------------------------
        # Image
        # -----------------------------

        if image is None:

            warnings.append(
                "Thumbnail unavailable."
            )

        return {
            "title": title,
            "description": description,
            "tags": tags,
            "top_comments": top_comments,
            "category": category,
            "channel": channel,
            "metadata": metadata,
            "image": image,
            "warnings": warnings,
        }

    # ======================================================
    # BUILD COMBINED TEXT
    # ======================================================

    def build_text(
        self,
        title,
        description,
        tags,
        top_comments,
        category,
        channel,
    ):
        """
        Construct the combined textual representation
        used during multimodal training.
        """
        combined = f"""
        TITLE {title}
        DESCRIPTION {description}
        TAGS {tags}
        COMMENTS {top_comments}
        CATEGORY {category}
        CHANNEL {channel}
        """

        return self.clean_text(combined)


    # ======================================================
    # TOKENIZATION
    # ======================================================

    def tokenize(self, text: str) -> np.ndarray:
        """
        Convert cleaned text into the padded integer sequence
        expected by the multimodal text branch.
        """

        sequence = self.tokenizer.texts_to_sequences([text])

        padded = pad_sequences(
            sequence,
            maxlen=self.MAX_SEQUENCE_LENGTH,
            padding="post",
            truncating="post",
        )

        return padded.astype(np.int32)

    # ======================================================
    # METADATA PREPARATION
    # ======================================================

    def prepare_metadata(
        self,
        metadata: list | np.ndarray
    ) -> np.ndarray:
        """
        Prepare metadata for the multimodal model.

        Handles:
            • None values
            • Invalid numbers
            • Wrong feature count
            • Scaling
            • Data type conversion
        """

        expected_features = len(self.feature_names)

        # ----------------------------
        # No metadata supplied
        # ----------------------------

        if metadata is None:

            metadata = np.zeros(
                expected_features,
                dtype=np.float32
            )

        # Convert to list

        metadata = list(metadata)

        cleaned = []

        # ----------------------------
        # Clean values
        # ----------------------------

        for value in metadata:

            if value is None:

                cleaned.append(0.0)

                continue

            try:

                value = float(value)

                if np.isnan(value):

                    value = 0.0

                if np.isinf(value):

                    value = 0.0

                cleaned.append(value)

            except Exception:

                cleaned.append(0.0)

        metadata = cleaned

        # ----------------------------
        # Feature length check
        # ----------------------------

        if len(metadata) < expected_features:

            metadata.extend(
                [0.0] *
                (expected_features - len(metadata))
            )

        elif len(metadata) > expected_features:

            metadata = metadata[:expected_features]

        # ----------------------------
        # Convert to NumPy
        # ----------------------------

        metadata = pd.DataFrame(
            [metadata],
            columns=self.feature_names
        )

        metadata = self.scaler.transform(metadata)

        # ----------------------------
        # Feature Scaling
        # ----------------------------

        metadata = self.scaler.transform(
            metadata
        )

        return metadata.astype(np.float32)

    # ======================================================
    # IMAGE PREPARATION
    # ======================================================

    def prepare_image(
        self,
        image: np.ndarray | None
    ) -> np.ndarray | None:
        """
        Prepare thumbnail for the multimodal CNN.

        Handles:
        • None images
        • Grayscale images
        • RGBA images
        • RGB/BGR conversion
        • Resizing
        • Normalization

        Returns
        -------
        np.ndarray | None
        """

        if image is None:
            return np.zeros(
                (1,224,224,3),
                dtype=np.float32
            )

        image = np.asarray(image)

        # -------------------------
        # Grayscale
        # -------------------------

        if len(image.shape) == 2:

            image = cv2.cvtColor(
                image,
                cv2.COLOR_GRAY2RGB
            )

        # -------------------------
        # RGBA
        # -------------------------

        elif image.shape[-1] == 4:

            image = cv2.cvtColor(
                image,
                cv2.COLOR_RGBA2RGB
            )

        # -------------------------
        # Resize
        # -------------------------

        image = cv2.resize(
            image,
            (
                self.IMAGE_WIDTH,
                self.IMAGE_HEIGHT
            )
        )

        # -------------------------
        # Normalize
        # -------------------------

        image = image.astype(np.float32)

        image /= 255.0

        # -------------------------
        # Batch Dimension
        # -------------------------

        image = np.expand_dims(
            image,
            axis=0
        )

        return image



    # ======================================================
    # COMPLETE VALIDATION PIPELINE
    # ======================================================

    def validate(
        self,
        title,
        description,
        tags,
        top_comments,
        category,
        channel,
        metadata,
        image,
    ) -> Dict:
        """
        Complete preprocessing pipeline.

        Returns all validated inputs required by:

        - Multimodal prediction
        - SHAP explainability
        - GradCAM
        - Reason Engine
        """

        validated = self._validate_inputs(
            title,
            description,
            tags,
            top_comments,
            category,
            channel,
            metadata,
            image,
        )


        # ==================================================
        # TEXT PROCESSING
        # ==================================================

        cleaned_text = self.build_text(
            validated["title"],
            validated["description"],
            validated["tags"],
            validated["top_comments"],
            validated["category"],
            validated["channel"],
        )

        # ==================================================
        # TEXT TOKENIZATION
        # ==================================================

        text_tensor = self.tokenize(
            cleaned_text
        )

        raw_text = f"""
        TITLE {validated['title']}
        DESCRIPTION {validated['description']}
        TAGS {validated['tags']}
        COMMENTS {validated['top_comments']}
        CATEGORY {validated['category']}
        CHANNEL {validated['channel']}
        """


        # ==================================================
        # METADATA PROCESSING
        # ==================================================

        metadata_tensor = self.prepare_metadata(
            validated["metadata"]
        )


        # ==================================================
        # IMAGE PROCESSING
        # ==================================================

        image_tensor = self.prepare_image(
            validated["image"]
        )


        # ==================================================
        # FINAL OUTPUT
        # ==================================================

        return {


            # -----------------------------
            # Original Information
            # -----------------------------

            "title":
                validated["title"],


            "description":
                validated["description"],


            "tags":
                validated["tags"],

            "top_comments":
                validated["top_comments"],


            "category":
                validated["category"],


            "channel":
                validated["channel"],



            # -----------------------------
            # Text Inputs
            # -----------------------------

            "original_text":
                raw_text,


            "clean_text":
                cleaned_text,


            "text":
                text_tensor,



            # -----------------------------
            # Metadata Inputs
            # -----------------------------

            "metadata":
                metadata_tensor,


            "metadata_feature_names":
                self.feature_names,



            # -----------------------------
            # Image Inputs
            # -----------------------------

            "image":
                image_tensor,


            "image_available":
                image_tensor is not None,



            # -----------------------------
            # Validation Status
            # -----------------------------

            "warnings":
                validated["warnings"]
        }